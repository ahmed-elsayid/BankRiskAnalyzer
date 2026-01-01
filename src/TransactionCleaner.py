import pandas as pd


class TransactionCleaner:
    def __init__(self, data):
        self.data = data

    def remove_duplicates(self):
        print("Removing duplicates...")
        self.data.drop_duplicates(inplace=True)
        self.data.reset_index(drop=True, inplace=True)

    def handle_missing_values(self):
        print("Handling missing values...")
        numeric_cols = self.data.select_dtypes(include=['number']).columns
        self.data[numeric_cols] = self.data[numeric_cols].fillna(0)

        object_cols = self.data.select_dtypes(include=['object']).columns
        self.data[object_cols] = self.data[object_cols].fillna('Unknown')

    def convert_time_step(self):
        print("Converting timestamps...")
        base_time = pd.to_datetime('2002-03-10')
        temp_time = base_time + pd.to_timedelta(self.data['step'], unit='h')
        self.data['day'] = temp_time.dt.day

    def filter(self):
        print("Filtering for CASH_OUT and TRANSFER...")
        return self.data[self.data['type'].isin(['CASH_OUT', 'TRANSFER'])].copy()

    def clean(self):
        self.remove_duplicates()
        self.handle_missing_values()
        self.convert_time_step()
        self.data = self.filter()
        print(f"Data cleaning complete. Rows remaining: {len(self.data)}")
        return self.data
