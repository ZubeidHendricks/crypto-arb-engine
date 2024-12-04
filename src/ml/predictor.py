import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Tuple

class OpportunityPredictor:
    def __init__(self, lookback_period: int = 100):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.lookback_period = lookback_period
        self.is_trained = False

    def prepare_features(self, price_history: pd.DataFrame) -> np.ndarray:
        """Prepare features for the model"""
        features = []
        
        # Price-based features
        price_history['returns'] = price_history['price'].pct_change()
        price_history['volatility'] = price_history['returns'].rolling(window=20).std()
        price_history['ma_5'] = price_history['price'].rolling(window=5).mean()
        price_history['ma_20'] = price_history['price'].rolling(window=20).mean()
        
        # Volume-based features
        price_history['volume_ma_5'] = price_history['volume'].rolling(window=5).mean()
        price_history['volume_ma_20'] = price_history['volume'].rolling(window=20).mean()
        
        # Technical indicators
        price_history['rsi'] = self._calculate_rsi(price_history['price'])
        
        feature_columns = [
            'returns', 'volatility', 'ma_5', 'ma_20',
            'volume_ma_5', 'volume_ma_20', 'rsi'
        ]
        
        return price_history[feature_columns].values

    def train(self, historical_data: Dict[str, pd.DataFrame]):
        """Train the model on historical data"""
        X, y = self._prepare_training_data(historical_data)
        
        if len(X) > 0:
            X_scaled = self.scaler.fit_transform(X)
            self.model.fit(X_scaled, y)
            self.is_trained = True

    def predict_opportunity(self, current_data: Dict[str, float]) -> float:
        """Predict the probability of a successful arbitrage opportunity"""
        if not self.is_trained:
            return 0.5

        features = self._extract_features(current_data)
        features_scaled = self.scaler.transform(features.reshape(1, -1))
        
        probability = self.model.predict_proba(features_scaled)[0][1]
        return probability

    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def _prepare_training_data(self, historical_data: Dict[str, pd.DataFrame]) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare training data from historical arbitrage opportunities"""
        X = []
        y = []
        
        for exchange, data in historical_data.items():
            features = self.prepare_features(data)
            labels = self._generate_labels(data)
            
            X.extend(features)
            y.extend(labels)
        
        return np.array(X), np.array(y)

    def _generate_labels(self, data: pd.DataFrame) -> List[int]:
        """Generate binary labels for training"""
        # Consider an opportunity successful if profit > 0
        return (data['profit'] > 0).astype(int).tolist()