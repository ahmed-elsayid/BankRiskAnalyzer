
class TransactionFlagger:
    def __init__(self):
        pass

    def flag_anomalies(self, df, customer_profiles):
        df = df.copy()
        df['is_suspicious'] = False
        condition1 = (df['amount'] > 200000) & (df['type'] == 'TRANSFER')
        df.loc[condition1, 'is_suspicious'] = True

        customer_avg_spending = customer_profiles.set_index('nameOrig')['avg_amount'].to_dict()
        df['customer_avg_spending'] = df['nameOrig'].map(customer_avg_spending)
        condition2 = df['amount'] > (df['customer_avg_spending'] * 5)
        df.loc[condition2, 'is_suspicious'] = True

        df.drop(columns=['customer_avg_spending'], inplace=True)

        return df
