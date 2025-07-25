import socket
import time
import os

def send_icmp_ping(target):
    print(f"[ICMP] Pinging {target}")
    os.system(f"ping -c 3 {target} > /dev/null")

def send_udp(target, port=9999):
    print(f"[UDP] Generic UDP to {target}:{port}")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        for i in range(10):
            sock.sendto(f"UDP-{i}".encode(), (target, port))
            time.sleep(0.1)

def send_voice_udp(target, port=4000):
    print(f"[VOICE] Simulating VoIP traffic to {target}:{port}")
    packet = b"\x11" * 160  # Typical G.711 payload size
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        for _ in range(50):  # 50 packets = 1 second of audio (20ms intervals)
            sock.sendto(packet, (target, port))
            time.sleep(0.02)

def send_game_udp(target, port=3000):
    print(f"[GAME] Simulating game UDP traffic to {target}:{port}")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        for _ in range(20):
            sock.sendto(b"GAME_DATA", (target, port))
            time.sleep(0.05)

def send_dns_query(target, port=53):
    print(f"[DNS] Simulating DNS query to {target}:{port}")
    # Simple fake DNS packet
    fake_dns_query = b'\xaa\xbb\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x05dummy\x03com\x00\x00\x01\x00\x01'
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(fake_dns_query, (target, port))

def send_telnet(target, port=23):
    print(f"[TELNET] Attempting Telnet to {target}:{port}")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            sock.connect((target, port))
            sock.sendall(b"telnet\r\n")
    except Exception as e:
        print(f"[TELNET] Failed: {e}")

def send_tcp_http(target, port=80):
    print(f"[HTTP] Sending basic HTTP GET to {target}:{port}")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2)
            sock.connect((target, port))
            sock.sendall(b"GET / HTTP/1.0\r\nHost: test\r\n\r\n")
    except Exception as e:
        print(f"[HTTP] Failed: {e}")

def send_tcp_variants(target):
    ports = [21, 22, 23, 80, 443]
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                sock.connect((target, port))
                sock.sendall(f"Hello port {port}\r\n".encode())
                print(f"[TCP] Sent to {target}:{port}")
        except:
            print(f"[TCP] Failed on port {port}")

def send_botnet_like_udp(target, port=6666):
    print(f"[BOTNET] Simulated UDP botnet burst to {target}:{port}")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        for _ in range(10):
            sock.sendto(b"BOTNET_COMMAND", (target, port))
            time.sleep(0.01)

def main():
    dst_ips = ["10.0.0.2", "10.0.0.3"]

    for dst in dst_ips:
        print(f"\n--- Generating traffic to {dst} ---")
        send_icmp_ping(dst)
        send_udp(dst)
        send_voice_udp(dst)
        send_game_udp(dst)
        send_dns_query(dst)
        send_telnet(dst)
        send_tcp_http(dst)
        send_tcp_variants(dst)
        send_botnet_like_udp(dst)
        print(f"--- Finished {dst} ---\n")
        time.sleep(2)

if __name__ == "__main__":
    main()


# h1 python3 /home/aayush/sdn-traffic-classifier/scripts/new/generate_mixed_traffic.py