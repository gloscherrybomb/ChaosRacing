#!/usr/bin/env python3
"""
Race Results Processor (GitHub Actions version)
Processes multiple race result CSV files and creates a general classification table.
"""

import pandas as pd
import os
from pathlib import Path


def convert_seconds_to_mmss(seconds):
    """
    Convert time in seconds to MM:SS format.
    
    Args:
        seconds: Time in seconds (can be float)
    
    Returns:
        String in MM:SS format
    """
    try:
        total_seconds = int(float(seconds))
        minutes = total_seconds // 60
        secs = total_seconds % 60
        return f"{minutes}:{secs:02d}"
    except (ValueError, TypeError):
        return "DNF"


def process_race_results(race_results_folder, output_folder):
    """
    Process all race result CSV files and create general classification table.
    
    Args:
        race_results_folder: Path to folder containing race result CSV files
        output_folder: Path to folder where general classification CSV will be saved
    """
    # Create folders if they don't exist
    Path(race_results_folder).mkdir(parents=True, exist_ok=True)
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    # List to store all results
    all_results = []
    
    # Get all CSV files in the race_results folder
    csv_files = list(Path(race_results_folder).glob("*.csv"))
    
    if not csv_files:
        print(f"No CSV files found in {race_results_folder}")
        return
    
    print(f"Found {len(csv_files)} CSV file(s) to process:")
    
    # Process each CSV file
    for csv_file in csv_files:
        print(f"  - {csv_file.name}")
        
        try:
            # Read CSV, skipping the first 2 rows (title and blank line)
            df = pd.read_csv(csv_file, skiprows=2)
            
            # Filter out rows where Gender is 'Bot'
            df = df[df['Gender'] != 'Bot']
            
            # Filter out DNF entries (where Position is 'DNF')
            df = df[df['Position'] != 'DNF']
            
            # Select only the columns we need
            columns_to_keep = ['UID', 'Name', 'Team', 'Country', 'Time', 
                             'Gender', 'ARR', 'ARRBand', 'EventRating', 'AgeBand']
            df = df[columns_to_keep]
            
            # Add to our collection
            all_results.append(df)
            
        except Exception as e:
            print(f"  Error processing {csv_file.name}: {e}")
            continue
    
    if not all_results:
        print("No valid results found to process")
        return
    
    # Combine all results into a single dataframe
    combined_df = pd.concat(all_results, ignore_index=True)
    
    print(f"\nTotal entries before deduplication: {len(combined_df)}")
    
    # Convert Time to numeric (in case it's stored as string)
    combined_df['Time'] = pd.to_numeric(combined_df['Time'], errors='coerce')
    
    # Remove any rows with invalid time values
    combined_df = combined_df.dropna(subset=['Time'])
    
    # Keep only the fastest time for each UID
    # Sort by Time first, then drop duplicates keeping the first (fastest)
    combined_df = combined_df.sort_values('Time')
    combined_df = combined_df.drop_duplicates(subset=['UID'], keep='first')
    
    print(f"Total unique riders after deduplication: {len(combined_df)}")
    
    # Sort by Time (ascending - fastest first)
    combined_df = combined_df.sort_values('Time').reset_index(drop=True)
    
    # Add Position column (1-indexed)
    combined_df.insert(0, 'Position', range(1, len(combined_df) + 1))
    
    # Convert Time from seconds to MM:SS format
    combined_df['Time'] = combined_df['Time'].apply(convert_seconds_to_mmss)
    
    # Remove the UID column as it's not needed in the final output
    output_df = combined_df.drop(columns=['UID'])
    
    # Define output file path
    output_file = Path(output_folder) / "general_classification.csv"
    
    # Save to CSV
    output_df.to_csv(output_file, index=False)
    
    print(f"\nGeneral classification table created successfully!")
    print(f"Output file: {output_file}")
    print(f"Total riders in classification: {len(output_df)}")
    
    # Display top 10 results
    if len(output_df) > 0:
        print("\nTop 10 results:")
        print(output_df.head(10).to_string(index=False))


def main():
    """Main function to run the script."""
    # Define folder paths for GitHub Actions
    race_results_folder = "race_results"
    output_folder = "general_classification"
    
    print("=" * 60)
    print("Race Results Processor")
    print("=" * 60)
    print(f"Input folder: {race_results_folder}")
    print(f"Output folder: {output_folder}")
    print("=" * 60)
    print()
    
    process_race_results(race_results_folder, output_folder)


if __name__ == "__main__":
    main()
