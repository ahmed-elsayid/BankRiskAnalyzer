import os
from DataManager import DataManager
from TransactionCleaner import TransactionCleaner
from FeatureBuilder import FeatureBuilder
from RiskScorer import RiskScorer
from TransactionFlagger import TransactionFlagger
from ReportGenerator import ReportGenerator

class ConsoleApp:
    def __init__(self):
        self.data_manager = None
        self.raw_data = None
        self.clean_data = None
        self.features = None
        self.flagged_data = None

        self.data_path = "../data/PS_20174392719_1491204439457_log.csv"

    def load_dataset(self):
        print("\n--- Loading Dataset ---")
        path_input = input(f"Enter dataset path (default: {self.data_path}): ").strip()
        path = path_input if path_input else self.data_path
        n_rows = int(input(f"Enter dataset number of rows (default: 100000): "))

        if not os.path.exists(path):
            print(f"Error: File not found at {path}")
            return

        try:
            self.data_manager = DataManager(path,num_rows=n_rows)
            self.raw_data = self.data_manager.get_data()
            print(f"Dataset loaded successfully. Rows: {len(self.raw_data)}")
            print("Initial Data Summary:")
            print(self.data_manager.get_summary_statistics())
        except Exception as e:
            print(f"Error loading data: {e}")

    def clean_data_process(self):
        if self.raw_data is None:
            print("Please load a dataset first.")
            return

        print("\n--- Validate and Clean the Data ---")
        cleaner = TransactionCleaner(self.raw_data)
        # Validation output
        self.data_manager.handle_invalid_datatypes()
        self.data_manager.validate_categorical_columns()
        self.data_manager.validate_numeric_columns()

        # cleaning
        self.clean_data = cleaner.clean()

    def build_features_process(self):
        if self.clean_data is None:
            print("Please clean the data first.")
            return

        print("\n--- Building Features ---")
        builder = FeatureBuilder()
        self.features = builder.build_features(self.clean_data)
        print("Features built successfully.")
        print(self.features.head())

    def score_customers(self):
        if self.features is None:
            print("Please build features first.")
            return

        print("\n--- Scoring Customers ---")
        scorer = RiskScorer(self.features)
        self.features = scorer.calculate_risk_scores()
        print("Risk scoring complete.")
        print(self.features[['nameOrig', 'risk_rank', 'mixed_zscore']].head())

    def flag_suspicious(self):
        if self.clean_data is None or self.features is None:
            print("Data cleaning and feature building must be done first.")
            return

        print("\n--- Flagging Suspicious Transactions ---")
        flagger = TransactionFlagger()
        self.flagged_data = flagger.flag_anomalies(self.clean_data, self.features)

        suspicious_count = self.flagged_data['is_suspicious'].sum()
        print(f"Flagging complete. Found {suspicious_count} suspicious transactions.")

    def export_reports(self):
        if self.flagged_data is None or self.features is None:
            print("Analysis not complete. Cannot export.")
            return

        print("\n--- Exporting Reports ---")
        reporter = ReportGenerator()
        reporter.export_flagged_transactions(self.flagged_data)
        reporter.export_customer_summary(self.features)
        reporter.generate_text_report(self.features)

    def display_summary(self):
        if self.features is None:
            print("No analysis data available.")
            return

        print("\n--- Analysis Summary ---")
        print(self.features['risk_rank'].value_counts())
        print("\nTop 5 Riskiest Customers:")
        print(self.features.sort_values(by='mixed_zscore', ascending=False).head(5))

    def run(self):
        while True:
            print("\n=== Bank Risk Analyzer Menu ===")
            print("1. Load Dataset")
            print("2. Clean and Validate Data")
            print("3. Build Features")
            print("4. Score Customers")
            print("5. Flag Suspicious Transactions")
            print("6. Export Reports")
            print("7. Display Summary")
            print("8. Exit")

            choice = input("Select an option: ")

            if choice == '1':
                self.load_dataset()
            elif choice == '2':
                self.clean_data_process()
            elif choice == '3':
                self.build_features_process()
            elif choice == '4':
                self.score_customers()
            elif choice == '5':
                self.flag_suspicious()
            elif choice == '6':
                self.export_reports()
            elif choice == '7':
                self.display_summary()
            elif choice == '8':
                print("Exiting...")
                break
            else:
                print("Invalid option. Please try again.")