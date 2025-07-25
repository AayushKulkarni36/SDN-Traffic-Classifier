import joblib
import os

class TrafficClassifier:
    def __init__(self,
                 model_path='/app/model_evaluation/refined_model_random_forest.joblib',
                 scaler_path = "/app/model_evaluation/refined_scaler.joblib",
                 feature_list_path='/app/model_evaluation/feature_list_refined.csv'):

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at: {model_path}")
        if not os.path.exists(scaler_path):
            raise FileNotFoundError(f"Scaler not found at: {scaler_path}")
        if not os.path.exists(feature_list_path):
            raise FileNotFoundError(f"Feature list not found at: {feature_list_path}")

        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        with open(feature_list_path, 'r') as f:
            self.feature_order = [line.strip() for line in f if line.strip()]

        print(f"[ML Loader] Loaded feature list ({len(self.feature_order)} features):")
        print(self.feature_order)
        print(f"[ML Loader] Model trained classes: {list(self.model.classes_)}")

    def predict(self, features: dict):
        try:
    
            feature_vector = [features[feat] for feat in self.feature_order]
            print(f"[ML] Raw Feature Vector: {feature_vector}")

        
            scaled = self.scaler.transform([feature_vector])
            print(f"[ML] Scaled Input: {scaled}")  
            prediction = self.model.predict(scaled)
            print(f"[ML] Prediction: {prediction[0]}")
            return prediction[0]

        except KeyError as e:
            raise ValueError(f"Missing feature: {e}")
        except Exception as e:
            raise RuntimeError(f"Error during prediction: {e}")
