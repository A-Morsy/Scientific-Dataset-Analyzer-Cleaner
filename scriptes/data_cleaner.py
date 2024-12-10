import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from scipy import stats

class DataCleaner:
    def __init__(self, file_path):
        print("Loading dataset...")
        self.df = pd.read_csv(file_path, delimiter='\t', low_memory=False)
        self.original_df = self.df.copy()
        print(f"Dataset loaded. Shape: {self.df.shape}")

    def impute_missing_values(self):
        """Impute missing values using appropriate methods for different column types"""
        print("\n1. IMPUTING MISSING VALUES")
        print("-" * 50)

        # Separate numeric and categorical columns
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        categorical_cols = self.df.select_dtypes(include=['object']).columns

        # Impute numeric columns with mean
        for col in numeric_cols:
            if self.df[col].isnull().any():
                mean_value = self.df[col].mean()
                self.df[col].fillna(mean_value, inplace=True)
                print(f"Imputed {col} with mean value: {mean_value:.2f}")

        # Impute categorical columns with mode
        for col in categorical_cols:
            if self.df[col].isnull().any():
                mode_value = self.df[col].mode()[0]
                self.df[col].fillna(mode_value, inplace=True)
                print(f"Imputed {col} with mode value: {mode_value}")

    def knn_imputation(self):
        """Perform KNN imputation on numeric columns"""
        print("\n2. KNN IMPUTATION")
        print("-" * 50)

        try:
            # Get numeric columns
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            
            if len(numeric_cols) > 0:
                # Create a subset of numeric data
                numeric_data = self.df[numeric_cols].copy()
                
                # Check for infinite values and replace with NaN
                numeric_data = numeric_data.replace([np.inf, -np.inf], np.nan)
                
                # Remove columns with all NaN values
                numeric_data = numeric_data.dropna(axis=1, how='all')
                
                if numeric_data.shape[1] > 0:  # If we still have columns after cleaning
                    # Initialize KNN imputer
                    imputer = KNNImputer(n_neighbors=min(5, len(numeric_data)-1))
                    
                    # Perform imputation
                    imputed_data = imputer.fit_transform(numeric_data)
                    
                    # Update dataframe with imputed values
                    for i, col in enumerate(numeric_data.columns):
                        self.df[col] = imputed_data[:, i]
                    
                    print(f"KNN imputation completed for {len(numeric_data.columns)} numeric columns")
                else:
                    print("No suitable numeric columns for KNN imputation after cleaning")
            else:
                print("No numeric columns found for KNN imputation")

        except Exception as e:
            print(f"Error during KNN imputation: {str(e)}")
            print("Proceeding with other cleaning steps...")

    def handle_outliers(self):
        """Handle outliers using IQR method"""
        print("\n3. OUTLIER HANDLING")
        print("-" * 50)

        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            try:
                # Calculate IQR
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                
                # Define bounds
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                # Count outliers
                outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)][col]
                if len(outliers) > 0:
                    print(f"\nOutliers in {col}:")
                    print(f"Number of outliers: {len(outliers)}")
                    print(f"Bounds: [{lower_bound:.2f}, {upper_bound:.2f}]")
                    
                    # Replace outliers with bounds
                    self.df.loc[self.df[col] < lower_bound, col] = lower_bound
                    self.df.loc[self.df[col] > upper_bound, col] = upper_bound
                    print(f"Outliers capped at bounds")
            except Exception as e:
                print(f"Error processing outliers for {col}: {str(e)}")

    def convert_data_types(self):
        """Convert data types to appropriate formats"""
        print("\n4. DATA TYPE CONVERSION")
        print("-" * 50)

        # Convert date columns
        date_columns = [col for col in self.df.columns if 'date' in col.lower()]
        for col in date_columns:
            try:
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
                print(f"Converted {col} to datetime")
            except Exception as e:
                print(f"Could not convert {col}: {str(e)}")

        # Convert numeric strings to numbers
        for col in self.df.columns:
            if self.df[col].dtype == 'object':
                try:
                    numeric_conversion = pd.to_numeric(self.df[col], errors='coerce')
                    if numeric_conversion.notnull().any():
                        self.df[col] = numeric_conversion
                        print(f"Converted {col} to numeric")
                except:
                    pass

    def generate_cleaning_report(self):
        """Generate report comparing original and cleaned dataset"""
        print("\n5. CLEANING REPORT")
        print("-" * 50)

        # Compare missing values
        original_missing = self.original_df.isnull().sum()
        cleaned_missing = self.df.isnull().sum()
        
        print("\nMissing Values Comparison:")
        comparison_df = pd.DataFrame({
            'Original Missing': original_missing,
            'Cleaned Missing': cleaned_missing,
            'Difference': original_missing - cleaned_missing
        })
        print(comparison_df[comparison_df['Difference'] > 0])

        # Compare data types
        print("\nData Type Changes:")
        original_types = self.original_df.dtypes
        cleaned_types = self.df.dtypes
        changed_types = original_types[original_types != cleaned_types]
        for col in changed_types.index:
            print(f"{col}: {original_types[col]} -> {cleaned_types[col]}")

    def save_cleaned_data(self, output_path):
        """Save the cleaned dataset"""
        self.df.to_csv(output_path, index=False)
        print(f"\nCleaned dataset saved to: {output_path}")

    def clean_data(self):
        """Run all cleaning steps"""
        self.impute_missing_values()
        self.knn_imputation()
        self.handle_outliers()
        self.convert_data_types()
        self.generate_cleaning_report()
        self.save_cleaned_data('cleaned_dataset.csv')

if __name__ == "__main__":
    try:
        cleaner = DataCleaner('occurrence.txt')
        cleaner.clean_data()
    except Exception as e:
        print(f"Error: {str(e)}")