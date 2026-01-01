import pandas as pd

class DataManager:
    def __init__(self, data_path,num_rows=None):
        self.data = pd.read_csv(data_path, nrows=num_rows)

    def get_data(self):
        return self.data

    def get_summary_statistics(self):
        return self.data.describe()

    def get_missing_values_summary(self):
        missing_values = self.data.isnull().sum()
        missing_percentage = (missing_values / len(self.data)) * 100
        return pd.DataFrame({'Missing Values': missing_values, 'Percentage': missing_percentage})

    def get_duplicates_summary(self):
        total_duplicates = self.data.duplicated().sum()
        return total_duplicates

    def handle_invalid_datatypes(self):
        expected_types = {
            'step': 'int64',
            'type': 'object',
            'amount': 'float64',
            'nameOrig': 'object',
            'oldbalanceOrg': 'float64',
            'newbalanceOrig': 'float64',
            'nameDest': 'object',
            'oldbalanceDest': 'float64',
            'newbalanceDest': 'float64',
            'isFraud': 'int64',
            'isFlaggedFraud': 'int64'
        }
        for c, type_ in expected_types.items():
            if self.data[c].dtype != type_:
                print(f"Converting column {c} from {self.data[c].dtype} to {type_}")
                self.data[c] = self.data[c].astype(type_)

        return self.data

    def validate_numeric_columns(self):
        numeric_columns = ['amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest']
        for col in numeric_columns:
            negative_values = self.data[self.data[col] < 0]
            if not negative_values.empty:
                print(f"Negative values found in column {col}:")
                print(negative_values[[col]])
            else:
                print(f"No negative values in column {col}.")


    def validate_categorical_columns(self):
        expected_types = {'PAYMENT', 'TRANSFER', 'CASH_OUT', 'DEBIT', 'CASH_IN'}
        invalid_types = self.data[~self.data['type'].isin(expected_types)]
        if not invalid_types.empty:
            print("Invalid transaction types found:")
            print(invalid_types['type'].unique())
        else:
            print("All transaction types are valid.")
