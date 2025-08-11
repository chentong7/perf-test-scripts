#!/usr/bin/env python3
"""
Debug script to show how the aggregation is working.
This will help verify that we're correctly averaging individual values.
"""

import json
from pathlib import Path
from collections import defaultdict


def debug_aggregation():
    """Show how values are being aggregated."""
    script_dir = Path(__file__).parent
    sm_dir = script_dir / "shared_matrix_memory"
    
    # Let's look at one specific operation to see the individual values
    operation_data = defaultdict(list)
    
    # Check a few files for "Insert row" operations
    for json_file in list(sm_dir.rglob('*Row_Insertion_perfresult.json'))[:3]:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            print(f"\nFile: {json_file.name}")
            
            if 'benchmarks' in json_data and json_data['benchmarks']:
                for benchmark in json_data['benchmarks']:
                    if "Insert a row" in benchmark['benchmarkName']:
                        custom_data = benchmark.get('customData', {})
                        
                        elapsed_time = benchmark.get('elapsedSeconds')
                        heap_avg = custom_data.get('Heap Used Avg')
                        heap_stddev = custom_data.get('Heap Used StdDev')
                        
                        print(f"  Benchmark: {benchmark['benchmarkName']}")
                        print(f"    Elapsed Time: {elapsed_time}")
                        print(f"    Heap Used Avg: {heap_avg}")
                        print(f"    Heap Used StdDev: {heap_stddev}")
                        
                        # Collect for averaging
                        if elapsed_time is not None:
                            operation_data['elapsed_time'].append(elapsed_time)
                        if heap_avg is not None:
                            operation_data['heap_used_avg'].append(heap_avg)
                        if heap_stddev is not None:
                            operation_data['heap_used_stddev'].append(heap_stddev)
                            
        except Exception as e:
            print(f"Error reading {json_file}: {e}")
    
    # Show the aggregation
    print(f"\n{'='*50}")
    print("AGGREGATION RESULTS:")
    print(f"{'='*50}")
    
    for metric, values in operation_data.items():
        if values:
            avg_value = sum(values) / len(values)
            print(f"\n{metric.upper()}:")
            print(f"  Individual values: {values}")
            print(f"  Average: {avg_value}")
            print(f"  Number of values: {len(values)}")


if __name__ == "__main__":
    debug_aggregation()
