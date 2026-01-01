from scipy.stats import zscore


class RiskScorer:
    def __init__(self,features):
        self.features = features

    def calculate_risk_scores(self):
        self.features['max_amount_zscore'] = zscore(self.features['max_amount'])
        self.features['transaction_count_zscore'] = zscore(self.features['transaction_count'])

        mixed_zscore = 0.6 * self.features['max_amount_zscore'] + 0.4 * self.features['transaction_count_zscore']
        self.features['mixed_zscore'] = mixed_zscore

        def determine_risk_rank(row):
            if row['mixed_zscore'] >= 2:
                return 'High'
            elif 1 <= row['mixed_zscore'] < 2:
                return 'Medium'
            else:
                return 'Low'

        self.features['risk_rank'] = self.features.apply(determine_risk_rank, axis=1)

        self.features.drop(columns=['max_amount_zscore', 'transaction_count_zscore'], inplace=True)

        return self.features
