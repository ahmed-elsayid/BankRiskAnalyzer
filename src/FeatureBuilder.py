import pandas as pd


class FeatureBuilder:
    def __init__(self):
        pass

    def build_features(self, df):
        print("Building customer profile features...")

        # Aggregate basic stats
        features = df.groupby('nameOrig').agg(
            transaction_count=('amount', 'count'),
            total_amount=('amount', 'sum'),
            avg_amount=('amount', 'mean'),
            max_amount=('amount', 'max')
        ).reset_index()

        # Daily Velocity
        daily_counts = df.groupby(['nameOrig', 'day']).size().reset_index(name='daily_count')
        daily_velocity = daily_counts.groupby('nameOrig')['daily_count'].mean()
        features = features.merge(daily_velocity.rename('daily_velocity'), on='nameOrig', how='left')
        features['daily_velocity'] = features['daily_velocity'].fillna(0)

        # Rolling Statistics
        df_sorted = df.sort_values(by=['nameOrig', 'day', 'step'])

        rolling = df_sorted.groupby('nameOrig')['amount'].rolling(window=5, min_periods=1).agg(
            ['mean', 'std']).reset_index()

        # Rename columns to match logic
        rolling = rolling.rename(columns={'mean': 'rolling_mean', 'std': 'rolling_std'})

        # Get the latest rolling stats per customer
        latest_rolling = rolling.groupby('nameOrig').tail(1)[["nameOrig", 'rolling_mean', 'rolling_std']]

        features = features.merge(latest_rolling, on='nameOrig', how='left')
        features['rolling_std'] = features['rolling_std'].fillna(0)

        return features
