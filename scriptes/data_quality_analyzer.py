import pandas as pd
import numpy as np
from datetime import datetime
import re

class ComprehensiveDataAnalyzer:
    def __init__(self, file_path):
        print("Loading dataset...")
        self.df = pd.read_csv(file_path, delimiter='\t', low_memory=False)
        print(f"Dataset loaded. Shape: {self.df.shape}")

    def analyze_missing_data(self):
        """1. Missing Data Analysis"""
        print("\n1. MISSING DATA ANALYSIS")
        print("-" * 50)
        
        missing = self.df.isnull().sum()
        missing_percent = (missing / len(self.df) * 100).round(2)
        missing_stats = pd.DataFrame({
            'Missing Values': missing,
            'Percentage': missing_percent
        })
        print("\nColumns with missing values:")
        print(missing_stats[missing_stats['Missing Values'] > 0])

    def analyze_duplicates(self):
        """2. Duplicate Data Analysis"""
        print("\n2. DUPLICATE DATA ANALYSIS")
        print("-" * 50)
        
        # Exact duplicates
        exact_dupes = self.df.duplicated().sum()
        print(f"\nExact duplicate rows: {exact_dupes}")
        
        # Potential duplicates based on similar values
        if 'scientificName' in self.df.columns:
            similar_names = self.df['scientificName'].value_counts()
            print("\nPotential duplicate scientific names:")
            print(similar_names[similar_names > 1].head())

    def analyze_inconsistent_data(self):
        """3. Inconsistent Data Analysis"""
        print("\n3. INCONSISTENT DATA ANALYSIS")
        print("-" * 50)
        
        for column in self.df.columns:
            if self.df[column].dtype == 'object':
                unique_values = self.df[column].nunique()
                if unique_values < 10:  # Only show if small number of unique values
                    print(f"\nUnique values in {column}:")
                    print(self.df[column].value_counts().head())

    def analyze_outliers(self):
        """4. Outliers Analysis"""
        print("\n4. OUTLIERS ANALYSIS")
        print("-" * 50)
        
        numeric_columns = self.df.select_dtypes(include=[np.number]).columns
        for column in numeric_columns:
            Q1 = self.df[column].quantile(0.25)
            Q3 = self.df[column].quantile(0.75)
            IQR = Q3 - Q1
            outliers = self.df[(self.df[column] < (Q1 - 1.5 * IQR)) | 
                             (self.df[column] > (Q3 + 1.5 * IQR))]
            if len(outliers) > 0:
                print(f"\nOutliers in {column}: {len(outliers)} records")
                print(f"Range: {self.df[column].min()} to {self.df[column].max()}")

    def analyze_data_types(self):
        """5. Data Type Analysis"""
        print("\n5. DATA TYPE ANALYSIS")
        print("-" * 50)
        
        print("\nColumn Data Types:")
        print(self.df.dtypes)
        
        # Check for mixed data types
        for column in self.df.columns:
            if self.df[column].dtype == 'object':
                numeric_values = pd.to_numeric(self.df[column], errors='coerce').notna().sum()
                if 0 < numeric_values < len(self.df[column]):
                    print(f"\nMixed data types in {column}: {numeric_values} numeric values")

    def analyze_format_errors(self):
        """6. Format Error Analysis"""
        print("\n6. FORMAT ERROR ANALYSIS")
        print("-" * 50)
        
        # Date format analysis
        date_columns = [col for col in self.df.columns if 'date' in col.lower()]
        for column in date_columns:
            if self.df[column].dtype == 'object':
                unique_formats = self.df[column].dropna().unique()
                print(f"\nUnique date formats in {column}:")
                print(unique_formats[:5])  # Show first 5 unique formats

    def analyze_incorrect_values(self):
        """7. Incorrect Values Analysis"""
        print("\n7. INCORRECT VALUES ANALYSIS")
        print("-" * 50)
        
        # Check for invalid coordinates if present
        if 'decimalLatitude' in self.df.columns:
            invalid_lat = self.df[
                (self.df['decimalLatitude'] < -90) | 
                (self.df['decimalLatitude'] > 90)
            ].shape[0]
            print(f"\nInvalid latitude values: {invalid_lat}")
        
        if 'decimalLongitude' in self.df.columns:
            invalid_lon = self.df[
                (self.df['decimalLongitude'] < -180) | 
                (self.df['decimalLongitude'] > 180)
            ].shape[0]
            print(f"Invalid longitude values: {invalid_lon}")

    def analyze_structural_issues(self):
        """8. Structural Issues Analysis"""
        print("\n8. STRUCTURAL ISSUES ANALYSIS")
        print("-" * 50)
        
        print(f"\nTotal columns: {len(self.df.columns)}")
        print(f"Total rows: {len(self.df)}")
        print("\nColumn names with special characters:")
        special_chars = [col for col in self.df.columns if not col.isalnum()]
        for col in special_chars:
            print(f"- {col}")

    def run_complete_analysis(self):
        """Run all analyses"""
        self.analyze_missing_data()
        self.analyze_duplicates()
        self.analyze_inconsistent_data()
        self.analyze_outliers()
        self.analyze_data_types()
        self.analyze_format_errors()
        self.analyze_incorrect_values()
        self.analyze_structural_issues()

if __name__ == "__main__":
    try:
        file_path = 'occurrence.txt'  # Replace with your file path
        analyzer = ComprehensiveDataAnalyzer(file_path)
        analyzer.run_complete_analysis()
    except Exception as e:
        print(f"Error: {str(e)}")