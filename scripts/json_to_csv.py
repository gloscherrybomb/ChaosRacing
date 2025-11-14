#!/usr/bin/env python3
"""
Convert JSON race results to CSV format
Handles JSON POST data from race results API
"""

import json
import csv
import sys
from datetime import datetime
from pathlib import Path


def json_to_csv(json_file_path, output_folder):
    """
    Convert JSON race result to CSV format matching TrainingPeaks Virtual format.
    
    Args:
        json_file_path: Path to JSON file with race results
        output_folder: Folder where CSV should be saved
    """
    # Read JSON data
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    # Extract results array - adjust this based on your actual JSON structure
    # This assumes the JSON has a structure like:
    # {
    #   "event_key": 88022,
    #   "pen": 3,
    #   "results": [ { "position": 1, "name": "...", ... }, ... ]
    # }
    
    # Handle different possible JSON structures
    if 'results' in data:
        results = data['results']
        event_key = data.get('event_key', data.get('EventKey', '88000'))
        pen = data.get('pen', data.get('Pen', '1'))
    elif isinstance(data, list):
        # If the entire payload is just the results array
        results = data
        event_key = '88000'
        pen = '1'
    else:
        # Single result object wrapped in metadata
        event_key = data.get('event_key', data.get('EventKey', '88000'))
        pen = data.get('pen', data.get('Pen', '1'))
        results = [data]  # Single result
    
    if not results:
        print("No results found in JSON data")
        return
    
    # Ensure output folder exists
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = Path(output_folder) / f"TPVirtual-Results-Event{event_key}-Pen{pen}-{timestamp}.csv"
    
    # Write CSV in TrainingPeaks Virtual format
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
        # Write title row
        f.write('OVERALL INDIVIDUAL RESULTS:\n')
        # Write blank row
        f.write('\n')
        
        # Define fieldnames (standard TPV format)
        fieldnames = [
            'EventKey', 'Pen', 'Position', 'Name', 'Team', 'Country', 'Time',
            'DeltaTime', 'Distance', 'DeltaDistance', 'Points', 'Gender', 'UID',
            'ARR', 'ARRBand', 'EventRating', 'EventRatingBand', 'AgeBand',
            'NGB', 'NGB ID', 'UCI ID'
        ]
        
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        
        # Process each result
        for result in results:
            # Map JSON fields to CSV fields (handle different naming conventions)
            row = {
                'EventKey': result.get('EventKey', result.get('event_key', event_key)),
                'Pen': result.get('Pen', result.get('pen', pen)),
                'Position': result.get('Position', result.get('position', '')),
                'Name': result.get('Name', result.get('name', '')),
                'Team': result.get('Team', result.get('team', '')),
                'Country': result.get('Country', result.get('country', '')),
                'Time': result.get('Time', result.get('time', 0)),
                'DeltaTime': result.get('DeltaTime', result.get('delta_time', 0)),
                'Distance': result.get('Distance', result.get('distance', 32417.966)),
                'DeltaDistance': result.get('DeltaDistance', result.get('delta_distance', 0)),
                'Points': result.get('Points', result.get('points', 0)),
                'Gender': result.get('Gender', result.get('gender', '')),
                'UID': result.get('UID', result.get('uid', result.get('user_id', ''))),
                'ARR': result.get('ARR', result.get('arr', '')),
                'ARRBand': result.get('ARRBand', result.get('arr_band', '')),
                'EventRating': result.get('EventRating', result.get('event_rating', '')),
                'EventRatingBand': result.get('EventRatingBand', result.get('event_rating_band', '')),
                'AgeBand': result.get('AgeBand', result.get('age_band', '')),
                'NGB': result.get('NGB', result.get('ngb', '')),
                'NGB ID': result.get('NGB ID', result.get('ngb_id', '')),
                'UCI ID': result.get('UCI ID', result.get('uci_id', ''))
            }
            
            writer.writerow(row)
    
    print(f"✓ Converted JSON to CSV: {output_file}")
    print(f"  - {len(results)} results processed")
    return output_file


def main():
    """Main function."""
    if len(sys.argv) < 3:
        print("Usage: python json_to_csv.py <json_file> <output_folder>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    output_folder = sys.argv[2]
    
    if not Path(json_file).exists():
        print(f"Error: JSON file not found: {json_file}")
        sys.exit(1)
    
    json_to_csv(json_file, output_folder)


if __name__ == "__main__":
    main()
