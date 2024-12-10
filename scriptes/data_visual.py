import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

class DataVisualizer:
    def __init__(self, file_path):
        print("Loading dataset...")
        self.df = pd.read_csv(file_path, delimiter='\t', low_memory=False)
        print(f"Dataset loaded. Shape: {self.df.shape}")

    def create_visualizations(self):
        """Create comprehensive data visualizations"""
        print("\nGenerating Data Visualizations...")
        
        try:
            # 1. Missing Values Heatmap
            print("Creating missing values heatmap...")
            self.plot_missing_values()

            # 2. Numerical Distributions
            print("Creating numerical distributions...")
            self.plot_numerical_distributions()

            # 3. Categorical Data Visualization
            print("Creating categorical data plots...")
            self.plot_categorical_data()

            # 4. IUCN Category Distribution
            print("Creating IUCN category distribution...")
            self.plot_iucn_distribution()

            print("\nAll visualizations completed and saved!")

        except Exception as e:
            print(f"Error in visualization: {str(e)}")

    def plot_missing_values(self):
        """Create missing values heatmap"""
        plt.figure(figsize=(12, 6))
        plt.style.use('default')
        
        # Create missing data matrix
        missing_data = self.df.isnull()
        
        # Plot heatmap
        plt.imshow(missing_data, cmap='Blues', aspect='auto')
        plt.title('Missing Values Heatmap')
        plt.xlabel('Columns')
        plt.ylabel('Rows')
        
        # Add colorbar
        plt.colorbar(label='Missing (True/False)')
        
        # Adjust layout and save
        plt.tight_layout()
        plt.savefig('missing_values_heatmap.png')
        plt.close()

    def plot_numerical_distributions(self):
        """Plot distributions of numerical columns"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns[:5]
        
        plt.style.use('default')
        fig, axes = plt.subplots(len(numeric_cols), 1, figsize=(10, 4*len(numeric_cols)))
        
        for i, col in enumerate(numeric_cols):
            # Create histogram
            if len(numeric_cols) > 1:
                ax = axes[i]
            else:
                ax = axes
                
            ax.hist(self.df[col].dropna(), bins=30, edgecolor='black')
            ax.set_title(f'Distribution of {col}')
            ax.set_xlabel(col)
            ax.set_ylabel('Frequency')
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('numerical_distributions.png')
        plt.close()

    def plot_categorical_data(self):
        """Plot distribution of key categorical variables"""
        categorical_cols = ['countryCode', 'taxonRank', 'taxonomicStatus']
        categorical_cols = [col for col in categorical_cols if col in self.df.columns]
        
        plt.style.use('default')
        fig, axes = plt.subplots(len(categorical_cols), 1, figsize=(12, 5*len(categorical_cols)))
        
        for i, col in enumerate(categorical_cols):
            # Get value counts
            value_counts = self.df[col].value_counts()
            
            # Create bar plot
            if len(categorical_cols) > 1:
                ax = axes[i]
            else:
                ax = axes
                
            value_counts.plot(kind='bar', ax=ax)
            ax.set_title(f'Distribution of {col}')
            ax.set_xlabel(col)
            ax.set_ylabel('Count')
            ax.grid(True, alpha=0.3)
            
            # Rotate x-labels
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        plt.savefig('categorical_distributions.png')
        plt.close()

    def plot_iucn_distribution(self):
        """Plot IUCN Red List Category distribution"""
        if 'iucnRedListCategory' in self.df.columns:
            plt.figure(figsize=(10, 6))
            plt.style.use('default')
            
            # Get IUCN category counts
            iucn_counts = self.df['iucnRedListCategory'].value_counts()
            
            # Create color map
            colors = ['lightgray', 'green', 'yellow', 'orange', 'red']
            
            # Create bar plot
            bars = plt.bar(iucn_counts.index, iucn_counts.values)
            
            # Color the bars
            for i, bar in enumerate(bars):
                if i < len(colors):
                    bar.set_color(colors[i])
            
            plt.title('Distribution of IUCN Red List Categories')
            plt.xlabel('IUCN Category')
            plt.ylabel('Count')
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45, ha='right')
            
            plt.tight_layout()
            plt.savefig('iucn_distribution.png')
            plt.close()

if __name__ == "__main__":
    try:
        file_path = 'occurrence.txt'  # Replace with your file path
        visualizer = DataVisualizer(file_path)
        visualizer.create_visualizations()
    except Exception as e:
        print(f"Error: {str(e)}")