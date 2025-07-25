from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ipv4
import time
import csv
import sqlite3
import os
from datetime import datetime
from threading import Timer
from utils.ml_model_loader import TrafficClassifier
classifier = TrafficClassifier(
    model_path='/home/aayush/sdn-traffic-classifier/model_evaluation/refined_model_random_forest.joblib',
    scaler_path='/home/aayush/sdn-traffic-classifier/model_evaluation/refined_scaler.joblib',
    feature_list_path='model_evaluation/feature_list_refined.csv'
)

class MLTrafficController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(MLTrafficController, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.flow_stats = {}
        self.db_path = '/home/aayush/sdn-traffic-classifier/database/flow_logs.db'
        self._init_db()

    def _init_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS flow_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            src_ip TEXT,
            dst_ip TEXT,
            protocol INTEGER,
            src_port INTEGER,
            dst_port INTEGER,
            fwd_pkts INTEGER,
            fwd_bytes INTEGER,
            fwd_pps REAL,
            fwd_bps REAL,
            rev_pkts INTEGER,
            rev_bytes INTEGER,
            rev_pps REAL,
            rev_bps REAL,
            duration REAL,
            prediction TEXT
            )
        ''')
        conn.commit()
        conn.close()
        self.logger.info("[DB] Initialized flow_logs.db successfully")


    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(
            datapath=datapath, buffer_id=buffer_id if buffer_id else 0xffffffff,
            priority=priority, match=match, instructions=inst
        )
        datapath.send_msg(mod)

    def log_flow_later(self, flow_key, rev_flow_key, features, src_ip, dst_ip, proto, traffic_type):
        Timer(2.0, self._delayed_log, args=(flow_key, rev_flow_key, features, src_ip, dst_ip, proto, traffic_type)).start()

    def _delayed_log(self, flow_key, rev_flow_key, features, src_ip, dst_ip, proto, traffic_type):
        now = time.time()
        rev_stats = self.flow_stats.get(rev_flow_key, {})
        if rev_flow_key in self.flow_stats:
            print(f"[DEBUG] Reverse stats found: {self.flow_stats[rev_flow_key]}")
        else:
            print(f"[DEBUG] No reverse stats for {rev_flow_key}")

        dt_r = now - rev_stats.get('last_seen', now)
        avg_dt_r = now - rev_stats.get('first_seen', now)
        delta_byte_r = rev_stats.get('byte_count', 0) - rev_stats.get('last_byte_count', 0)

        features.update({
            'Reverse Packets': rev_stats.get('pkt_count', 0),
            'Reverse Bytes': rev_stats.get('byte_count', 0),
            'Reverse Average Packets per second': rev_stats.get('pkt_count', 0) / avg_dt_r if avg_dt_r > 0 else 0,
            'Reverse Instantaneous Bytes per Second': delta_byte_r / dt_r if dt_r > 0 else 0,
        })
        features['Duration'] = features.get('Duration', 0)

        try:
            traffic_type = classifier.predict(features)
            traffic_type = traffic_type.lower()
            print(f"[ML] Delayed Traffic type: {traffic_type}")
            print(f"[ML] Features: {features}")
            if traffic_type in ['malware', 'botnet']:
                print(f"[SECURITY] Dropped delayed malicious traffic: {traffic_type} from {src_ip} to {dst_ip}")
                return
        except Exception as e:
            self.logger.error(f"[ERROR] Delayed prediction failed: {e}")
            return

        if rev_stats:
            rev_stats['last_pkt_count'] = rev_stats['pkt_count']
            rev_stats['last_byte_count'] = rev_stats['byte_count']

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO flow_logs (
                timestamp, src_ip, dst_ip, protocol,
                fwd_pkts, fwd_bytes, fwd_pps, fwd_bps,
                rev_pkts, rev_bytes, rev_pps, rev_bps,
                duration, prediction
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
            timestamp, src_ip, dst_ip, proto,
            features['Forward Packets'], features['Forward Bytes'],
            features['Forward Instantaneous Packets per Second'],
            features['Forward Average Bytes per second'],
            features['Reverse Packets'], features['Reverse Bytes'],
            features['Reverse Average Packets per second'],
            features['Reverse Instantaneous Bytes per Second'],
            features['Duration'], traffic_type
            ))
        conn.commit()
        print(f"[DB] Logged flow from {src_ip} to {dst_ip} as {traffic_type}")
        conn.close()

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto
        in_port = msg.match['in_port']
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)

        if eth.ethertype != 0x0800:
            actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
            self.send_packet_out(datapath, msg, in_port, actions)
            return

        ip_pkt = pkt.get_protocol(ipv4.ipv4)
        src_ip, dst_ip = ip_pkt.src, ip_pkt.dst
        proto = ip_pkt.proto
        ip_proto = ip_pkt.proto
        src_port = dst_port = 0

        for p in pkt.protocols:
            if hasattr(p, 'src_port') and hasattr(p, 'dst_port'):
                src_port = p.src_port
                dst_port = p.dst_port
                break

        flow_key = (src_ip, dst_ip, src_port, dst_port, ip_proto)
        reverse_flow_key = (dst_ip, src_ip, dst_port, src_port, ip_proto)

        now = time.time()
        size = len(msg.data)

        stats = self.flow_stats.setdefault(flow_key, {
            'first_seen': now, 'last_seen': now,
            'pkt_count': 0, 'byte_count': 0,
            'last_pkt_count': 0, 'last_byte_count': 0
        })

        stats['pkt_count'] += 1
        stats['byte_count'] += size
        delta_pkt_f = stats['pkt_count'] - stats['last_pkt_count']
        delta_byte_f = stats['byte_count'] - stats['last_byte_count']
        dt_f = now - stats['last_seen']
        avg_dt_f = now - stats['first_seen']
        stats['last_seen'] = now
        stats['last_pkt_count'] = stats['pkt_count']
        stats['last_byte_count'] = stats['byte_count']

        if reverse_flow_key in self.flow_stats:
            reverse_stats = self.flow_stats[reverse_flow_key]
            dt_r = now - reverse_stats['last_seen']
            delta_pkt_r = reverse_stats['pkt_count'] - reverse_stats['last_pkt_count']
            delta_byte_r = reverse_stats['byte_count'] - reverse_stats['last_byte_count']
            avg_dt_r = now - reverse_stats['first_seen']
        else:
            reverse_stats = None
            dt_r = 0
            delta_pkt_r = 0
            delta_byte_r = 0
            avg_dt_r = 0

        duration = avg_dt_f if avg_dt_f > 0 else 0
        features = {
            'Forward Packets': stats['pkt_count'],
            'Forward Bytes': stats['byte_count'],
            'Forward Instantaneous Packets per Second': delta_pkt_f / dt_f if dt_f > 0 else 0,
            'Forward Average Bytes per second': stats['byte_count'] / avg_dt_f if avg_dt_f > 0 else 0,
            'Reverse Packets': reverse_stats['pkt_count'] if reverse_stats else 0,
            'Reverse Bytes': reverse_stats['byte_count'] if reverse_stats else 0,
            'Reverse Average Bytes per second': reverse_stats['byte_count'] / avg_dt_r if reverse_stats and avg_dt_r > 0 else 0,
            'Reverse Instantaneous Packets per Second': delta_pkt_r / dt_r if reverse_stats and dt_r > 0 else 0,
            'Duration': duration,
            'Protocol': proto
        }

        try:
            self.log_flow_later(flow_key, reverse_flow_key, features, src_ip, dst_ip, proto, 'unknown')
        except Exception as e:
            self.logger.error(f"[ERROR] Logging setup failed: {e}")


        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})
        src_mac = eth.src
        dst_mac = eth.dst
        self.mac_to_port[dpid][src_mac] = in_port
        out_port = self.mac_to_port[dpid].get(dst_mac, ofproto.OFPP_FLOOD)

        actions = [parser.OFPActionOutput(out_port)]
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst_mac)
            self.add_flow(datapath, 1, match, actions)

        self.send_packet_out(datapath, msg, in_port, actions)

    def send_packet_out(self, datapath, msg, in_port, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        out = parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=msg.data if msg.buffer_id == ofproto.OFP_NO_BUFFER else None
        )
        datapath.send_msg(out)

# Test examples:
# h2 iperf -u -s &
# h1 iperf -u -c 10.0.0.2 -b 128k -l 160 -t 20     # for voice
# h1 iperf -u -c 10.0.0.2 -b 1M -l 128 -t 20       # for game