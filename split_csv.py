import pandas as pd
import math
import os
from tqdm import tqdm

def split_csv(input_file, num_splits=12):
    try:
        # First try to detect the file delimiter
        print(f"Analyzing CSV file: {input_file}")
        with open(input_file, 'r', encoding='utf-8') as file:
            first_line = file.readline()
            # Check common delimiters
            delimiters = [',', '\t', ';', '|']
            counts = [first_line.count(d) for d in delimiters]
            delimiter = delimiters[counts.index(max(counts))]
        
        print(f"Detected delimiter: '{delimiter}'")
        
        # Read the CSV file with the detected delimiter and additional parameters
        df = pd.read_csv(input_file, 
                        delimiter=delimiter,
                        on_bad_lines='skip',  # Skip problematic lines
                        low_memory=False,     # Avoid dtype warnings
                        quoting=3)            # Disable quote parsing
        
        # Calculate the size of each split
        total_rows = len(df)
        rows_per_split = math.ceil(total_rows / num_splits)
        
        print(f"Total rows: {total_rows:,}")
        print(f"Rows per split: {rows_per_split:,}")
        
        # Create output directory if it doesn't exist
        output_dir = 'split_files'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Split and save the files
        print(f"Splitting file into {num_splits} parts...")
        for i in tqdm(range(num_splits)):
            start_idx = i * rows_per_split
            end_idx = min((i + 1) * rows_per_split, total_rows)
            
            # Get the slice of dataframe
            split_df = df.iloc[start_idx:end_idx]
            
            # Generate output filename
            output_file = os.path.join(output_dir, f'part_{i+1}.csv')
            
            # Save to CSV
            split_df.to_csv(output_file, index=False)
        
        print(f"\nSplit complete! Files saved in '{output_dir}' directory")
        
        # Print summary
        print("\nSummary:")
        print(f"Input file size: {os.path.getsize(input_file) / (1024*1024):.2f} MB")
        print(f"Number of splits: {num_splits}")
        print(f"Rows processed: {total_rows:,}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("\nTrying alternative approach...")
        try:
            # Alternative approach using chunk reading
            chunk_size = 10000  # Adjust this value based on your memory constraints
            total_rows = sum(1 for _ in open(input_file, 'r', encoding='utf-8')) - 1
            rows_per_split = math.ceil(total_rows / num_splits)
            
            print(f"Processing file in chunks...")
            current_split = 0
            current_row = 0
            output_df = pd.DataFrame()
            
            for chunk in tqdm(pd.read_csv(input_file, 
                                        delimiter=delimiter,
                                        chunksize=chunk_size,
                                        on_bad_lines='skip',
                                        low_memory=False,
                                        quoting=3)):
                output_df = pd.concat([output_df, chunk])
                current_row += len(chunk)
                
                while len(output_df) >= rows_per_split and current_split < num_splits - 1:
                    # Save current split
                    split_df = output_df.iloc[:rows_per_split]
                    output_file = os.path.join('split_files', f'part_{current_split + 1}.csv')
                    split_df.to_csv(output_file, index=False)
                    
                    # Prepare for next split
                    output_df = output_df.iloc[rows_per_split:]
                    current_split += 1
            
            # Save the last split
            if not output_df.empty and current_split < num_splits:
                output_file = os.path.join('split_files', f'part_{current_split + 1}.csv')
                output_df.to_csv(output_file, index=False)
            
            print(f"\nSplit complete using chunk processing! Files saved in 'split_files' directory")
            
        except Exception as e:
            print(f"Alternative approach also failed: {str(e)}")
            print("\nPlease check if the file is properly formatted or try opening it in a text editor to inspect its structure.")

if __name__ == "__main__":
    input_file = "dataset.csv"  # Replace with your file path
    split_csv(input_file)