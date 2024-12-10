import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os

class BiodiversityAnalyzer:
    def __init__(self, file_path):
        print("Loading cleaned dataset...")
        self.df = pd.read_csv(file_path)
        print(f"Dataset loaded. Shape: {self.df.shape}")
        
        # Create directory for plots
        self.plot_dir = 'cleaned_data_plots'
        if not os.path.exists(self.plot_dir):
            os.makedirs(self.plot_dir)
            print(f"Created directory: {self.plot_dir}")
        
        # Set up plotting style
        plt.style.use('default')  # Using default matplotlib style
        self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                      '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

    def save_plot(self, filename):
        """Helper function to save plots to the plots directory"""
        filepath = os.path.join(self.plot_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Saved plot: {filepath}")

    def taxonomic_analysis(self):
        """Analyze and visualize taxonomic distribution"""
        print("\n1. TAXONOMIC ANALYSIS")
        print("-" * 50)
        
        # Create taxonomic distribution plot
        plt.figure(figsize=(12, 6))
        taxonomic_levels = ['phylum', 'class', 'order', 'family', 'genus']
        counts = [self.df[level].nunique() for level in taxonomic_levels]
        
        plt.bar(taxonomic_levels, counts, color=self.colors)
        plt.title('Taxonomic Diversity', pad=20)
        plt.ylabel('Number of Unique Taxa')
        plt.xlabel('Taxonomic Level')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        self.save_plot('taxonomic_diversity.png')
        
        # Print taxonomic statistics
        print("\nTaxonomic Statistics:")
        for level in taxonomic_levels:
            print(f"\nTop 5 {level}:")
            print(self.df[level].value_counts().head())

    def conservation_status_analysis(self):
        """Analyze IUCN Red List categories"""
        print("\n2. CONSERVATION STATUS ANALYSIS")
        print("-" * 50)
        
        if 'iucnRedListCategory' in self.df.columns:
            plt.figure(figsize=(10, 6))
            iucn_counts = self.df['iucnRedListCategory'].value_counts()
            
            # Define colors for IUCN categories
            iucn_colors = {
                'LC': '#4CAF50',  # Green
                'NT': '#FFC107',  # Amber
                'VU': '#FF9800',  # Orange
                'EN': '#FF5722',  # Deep Orange
                'CR': '#F44336',  # Red
                'DD': '#9E9E9E',  # Grey
                'NE': '#BDBDBD'   # Light Grey
            }
            
            bars = plt.bar(iucn_counts.index, iucn_counts.values)
            
            # Color the bars
            for i, bar in enumerate(bars):
                bar.set_color(iucn_colors.get(iucn_counts.index[i], '#2196F3'))
            
            plt.title('Distribution of IUCN Red List Categories', pad=20)
            plt.xlabel('IUCN Category')
            plt.ylabel('Number of Species')
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            self.save_plot('iucn_distribution.png')
            
            # Print conservation statistics
            print("\nConservation Status Statistics:")
            print(iucn_counts)

    def temporal_analysis(self):
        """Analyze temporal patterns in data collection"""
        print("\n3. TEMPORAL ANALYSIS")
        print("-" * 50)
        
        if 'eventDate' in self.df.columns:
            # Convert to datetime if needed
            self.df['eventDate'] = pd.to_datetime(self.df['eventDate'])
            
            plt.figure(figsize=(12, 6))
            yearly_counts = self.df['eventDate'].dt.year.value_counts().sort_index()
            plt.plot(yearly_counts.index, yearly_counts.values, marker='o')
            plt.title('Temporal Distribution of Records', pad=20)
            plt.xlabel('Year')
            plt.ylabel('Number of Records')
            plt.grid(True, alpha=0.3)
            self.save_plot('temporal_distribution.png')
            
            # Print temporal statistics
            print("\nTemporal Coverage:")
            print(f"Earliest record: {self.df['eventDate'].min()}")
            print(f"Latest record: {self.df['eventDate'].max()}")
            print(f"Peak collection year: {yearly_counts.idxmax()} ({yearly_counts.max()} records)")

    def geographic_distribution(self):
        """Analyze geographic distribution of records"""
        print("\n4. GEOGRAPHIC DISTRIBUTION")
        print("-" * 50)
        
        if 'stateProvince' in self.df.columns:
            plt.figure(figsize=(12, 6))
            state_counts = self.df['stateProvince'].value_counts()
            plt.bar(state_counts.index, state_counts.values, color=self.colors)
            plt.title('Geographic Distribution by State/Province', pad=20)
            plt.xlabel('State/Province')
            plt.ylabel('Number of Records')
            plt.xticks(rotation=45, ha='right')
            plt.grid(True, alpha=0.3)
            self.save_plot('geographic_distribution.png')
            
            # Print geographic statistics
            print("\nGeographic Coverage:")
            print(state_counts)

    def data_completeness_analysis(self):
        """Analyze data completeness and quality"""
        print("\n5. DATA COMPLETENESS ANALYSIS")
        print("-" * 50)
        
        # Calculate completeness for each column
        completeness = (self.df.count() / len(self.df) * 100).round(2)
        
        plt.figure(figsize=(12, 6))
        top_20_completeness = completeness.sort_values().tail(20)
        plt.barh(range(len(top_20_completeness)), top_20_completeness.values)
        plt.yticks(range(len(top_20_completeness)), top_20_completeness.index)
        plt.title('Data Completeness (Top 20 Fields)', pad=20)
        plt.xlabel('Completeness (%)')
        plt.grid(True, alpha=0.3)
        self.save_plot('data_completeness.png')
        
        # Print completeness statistics
        print("\nData Completeness Statistics:")
        print(completeness.sort_values(ascending=False).head())

    def generate_summary_report(self):
        """Generate a summary report of the analysis"""
        print("\n6. SUMMARY REPORT")
        print("-" * 50)
        
        summary = {
            "Total Records": len(self.df),
            "Unique Species": self.df['species'].nunique(),
            "Unique Genera": self.df['genus'].nunique(),
            "Unique Families": self.df['family'].nunique(),
            "Geographic Coverage": self.df['stateProvince'].nunique(),
            "Data Completeness": f"{self.df.notna().mean().mean()*100:.2f}%"
        }
        
        print("\nDataset Summary:")
        for key, value in summary.items():
            print(f"{key}: {value}")

    def run_analysis(self):
        """Run all analyses"""
        self.taxonomic_analysis()
        self.conservation_status_analysis()
        self.temporal_analysis()
        self.geographic_distribution()
        self.data_completeness_analysis()
        self.generate_summary_report()

if __name__ == "__main__":
    try:
        analyzer = BiodiversityAnalyzer('cleaned_dataset.csv')
        analyzer.run_analysis()
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nDebug information:")
        print("Available matplotlib styles:", plt.style.available)