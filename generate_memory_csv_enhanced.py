#!/usr/bin/env python3
"""
Enhanced script to read performance test results from shared_matrix_memory and shared_tree_memory
directories and generate a CSV file similar to memory.csv.

This script:
1. Recursively scans both directories for JSON performance result files
2. Extracts benchmark data including elapsed time, heap usage statistics
3. Groups data by operation type (Insert row, Remove column, etc.)
4. Aggregates multiple runs by averaging the values
5. Outputs a CSV file with SM (SharedMatrix) and ST (SharedTree) data side by side

Usage: python generate_memory_csv.py [output_filename]
"""

import json
import os
import csv
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Any


class PerformanceDataProcessor:
    """Class to handle processing of performance test data."""
    
    def __init__(self, sm_directory: str, st_directory: str):
        self.sm_directory = Path(sm_directory)
        self.st_directory = Path(st_directory)
        self.operation_patterns = {
            # Row operations
            r'insert.*row': 'Insert row',
            r'undo.*insert.*row': 'Undo insert row', 
            r'redo.*insert.*row': 'Redo insert row',
            r'remove.*row': 'Remove row',
            r'undo.*remove.*row': 'Undo remove row',
            r'redo.*remove.*row': 'Redo remove row',
            
            # Column operations
            r'insert.*column': 'Insert column',
            r'undo.*insert.*column': 'Undo insert column',
            r'redo.*insert.*column': 'Redo insert column', 
            r'remove.*column': 'Remove column',
            r'undo.*remove.*column': 'Undo remove column',
            r'redo.*remove.*column': 'Redo remove column',
            
            # Cell operations
            r'set.*cell': 'Set cell value',
            r'undo.*set.*cell': 'Undo set cell value',
            r'redo.*set.*cell': 'Redo set cell value',
        }
    
    def extract_operation_name(self, benchmark_name: str) -> str:
        """Extract standardized operation name from benchmark name."""
        import re
        
        name_lower = benchmark_name.lower()
        
        # Try to match against known patterns in order of specificity
        for pattern, operation in self.operation_patterns.items():
            if re.search(pattern, name_lower):
                return operation
        
        # If no pattern matches, try to extract a clean operation name
        # Remove common prefixes and clean up
        clean_name = re.sub(r'^\w+\s+', '', benchmark_name)  # Remove first word if it's a prefix
        clean_name = re.sub(r'\s+\d+\s+times?$', '', clean_name)  # Remove "X times" suffix
        clean_name = re.sub(r'\s+in the middle', '', clean_name)  # Remove "in the middle"
        
        return clean_name if clean_name else benchmark_name
    
    def read_json_files(self, directory: Path, data_source: str) -> Dict[str, List[Dict]]:
        """Read all JSON files from a directory and extract benchmark data."""
        data = defaultdict(list)
        files_processed = 0
        
        if not directory.exists():
            print(f"Warning: Directory {directory} does not exist")
            return data
        
        print(f"Scanning {data_source} directory: {directory}")
        
        for json_file in directory.rglob('*_perfresult.json'):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                
                if 'benchmarks' not in json_data or not json_data['benchmarks']:
                    continue
                
                files_processed += 1
                for benchmark in json_data['benchmarks']:
                    operation = self.extract_operation_name(benchmark['benchmarkName'])
                    custom_data = benchmark.get('customData', {})
                    
                    benchmark_data = {
                        'elapsed_time': benchmark.get('elapsedSeconds'),
                        'heap_used_avg': custom_data.get('Heap Used Avg'),
                        'heap_used_stddev': custom_data.get('Heap Used StdDev'),
                        'margin_of_error': custom_data.get('Margin of Error'),
                        'relative_margin_of_error': custom_data.get('Relative Margin of Error'),
                        'iterations': custom_data.get('Iterations'),
                        'source_file': json_file.name
                    }
                    
                    # Only add if we have some valid data
                    if any(v is not None and v != '' for k, v in benchmark_data.items() 
                          if k not in ['source_file']):
                        data[operation].append(benchmark_data)
                        
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error reading {json_file}: {e}")
                continue
        
        print(f"  Processed {files_processed} files, found {len(data)} operation types")
        return data
    
    def aggregate_data(self, data_list: List[Dict]) -> Optional[Dict]:
        """Aggregate data by taking the average of all runs."""
        if not data_list:
            return None
        
        metrics = ['elapsed_time', 'heap_used_avg', 'heap_used_stddev', 
                  'margin_of_error', 'relative_margin_of_error']
        
        result = {}
        total_iterations = sum(d.get('iterations', 0) for d in data_list if d.get('iterations'))
        
        for metric in metrics:
            values = [d[metric] for d in data_list if d.get(metric) is not None]
            result[metric] = sum(values) / len(values) if values else None
        
        result['total_runs'] = len(data_list)
        result['total_iterations'] = total_iterations if total_iterations > 0 else None
        
        return result
    
    def generate_csv(self, output_file: str = "generated_memory.csv") -> None:
        """Generate CSV file with aggregated performance data."""
        print("Reading performance data...")
        
        sm_data = self.read_json_files(self.sm_directory, "SharedMatrix")
        st_data = self.read_json_files(self.st_directory, "SharedTree")
        
        all_operations = set(sm_data.keys()) | set(st_data.keys())
        
        if not all_operations:
            print("No data found in either directory!")
            return
        
        print(f"\nFound {len(all_operations)} unique operations:")
        for op in sorted(all_operations):
            sm_count = len(sm_data.get(op, []))
            st_count = len(st_data.get(op, []))
            print(f"  - {op}: SM({sm_count}) ST({st_count})")
        
        output_path = Path(output_file)
        print(f"\nGenerating CSV file: {output_path.absolute()}")
        
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow([
                "Operation",
                "Elapsed Time (s)",
                "Heap Used Avg", 
                "Heap Used StdDev",
                "Margin of Error",
                "Relative Margin of Error"
            ])
            
            # Write data for each operation
            for operation in sorted(all_operations):
                sm_agg = self.aggregate_data(sm_data.get(operation, []))
                st_agg = self.aggregate_data(st_data.get(operation, []))
                
                row_data = [operation]
                
                metrics = ['elapsed_time', 'heap_used_avg', 'heap_used_stddev', 
                          'margin_of_error', 'relative_margin_of_error']
                
                for metric in metrics:
                    cell_content = []
                    
                    if sm_agg and sm_agg[metric] is not None:
                        cell_content.append(f"SM: {sm_agg[metric]}")
                    
                    if st_agg and st_agg[metric] is not None:
                        cell_content.append(f"ST: {st_agg[metric]}")
                    
                    row_data.append("\n".join(cell_content) if cell_content else "")
                
                writer.writerow(row_data)
        
        print(f"✅ CSV file generated successfully!")
        print(f"\nSummary:")
        print(f"  SharedMatrix operations: {len(sm_data)}")
        print(f"  SharedTree operations: {len(st_data)}")
        print(f"  Total unique operations: {len(all_operations)}")
        print(f"  Output file: {output_path.absolute()}")


def main():
    """Main function to run the performance data processor."""
    script_dir = Path(__file__).parent
    
    # Allow custom output filename from command line
    output_file = sys.argv[1] if len(sys.argv) > 1 else "generated_memory.csv"
    
    processor = PerformanceDataProcessor(
        sm_directory=script_dir / "shared_matrix_memory",
        st_directory=script_dir / "shared_tree_memory"
    )
    
    try:
        processor.generate_csv(output_file)
    except Exception as e:
        print(f"❌ Error generating CSV: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
