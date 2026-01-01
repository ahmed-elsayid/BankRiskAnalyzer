import pandas as pd
import os


class ReportGenerator:
    def __init__(self, output_dir='../output'):
        # Ensure output directory exists
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)


    def export_flagged_transactions(self, df):
        if 'is_suspicious' in df.columns:
            suspicious_df = df[df['is_suspicious'] == True]
            path = os.path.join(self.output_dir, 'flagged_transactions.csv')
            suspicious_df.to_csv(path, index=False)
            print(f"Exported {len(suspicious_df)} flagged transactions to {path}")
        else:
            print("No suspicious flag found in data.")

    def export_customer_summary(self, customer_profiles):
        path = os.path.join(self.output_dir, 'customer_risk_summary.csv')
        customer_profiles.to_csv(path, index=False)
        print(f"Exported customer risk summary to {path}")

    def generate_text_report(self, customer_profiles):
        path = os.path.join(self.output_dir, 'report.txt')

        total_customers = len(customer_profiles)
        high_risk = customer_profiles[customer_profiles['risk_rank'].isin(['High', 'Critical'])]
        total_high_risk = len(high_risk)
        money_at_risk = high_risk['total_amount'].sum()

        report_content = (
            "--- Bank Transaction Risk Report ---\n"
            f"Total Customers Analyzed: {total_customers}\n"
            f"High/Critical Risk Customers: {total_high_risk}\n"
            f"Total Money at Risk (High Risk Segments): ${money_at_risk:,.2f}\n\n"
            "Top 5 Riskiest Customers:\n"
        )

        top_5 = high_risk.sort_values(by='mixed_zscore', ascending=False).head(5)
        for index, row in top_5.iterrows():
            report_content += (
                f"ID: {row['nameOrig']}, Score: {row['mixed_zscore']:.2f}, "
                f"Rank: {row['risk_rank']}, Max Tx: ${row['max_amount']:,.2f}\n"
            )

        with open(path, 'w') as f:
            f.write(report_content)

        print(f"Text report generated at {path}")
