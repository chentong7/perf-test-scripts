# Performance Data CSV Generator

This script reads performance test results from the `shared_matrix_memory` and `shared_tree_memory` directories and generates a CSV file similar to the existing `memory.csv`.

## Features

- Recursively scans both directories for JSON performance result files (`*_perfresult.json`)
- Extracts benchmark data including:
  - Elapsed time
  - Heap usage average
  - Heap usage standard deviation  
  - Margin of error
  - Relative margin of error
- Groups data by operation type (Insert row, Remove column, etc.)
- Aggregates multiple runs by averaging the values
- Handles missing values gracefully (skips them in calculations)
- Outputs CSV with SM (SharedMatrix) and ST (SharedTree) data side by side

## Usage

### Basic usage:
```bash
python generate_memory_csv.py
```
This creates `generated_memory.csv` in the current directory.

### Enhanced version:
```bash
python generate_memory_csv_enhanced.py [output_filename]
```

Examples:
```bash
# Use default filename (generated_memory.csv)
python generate_memory_csv_enhanced.py

# Specify custom filename
python generate_memory_csv_enhanced.py my_performance_data.csv
```

## Output Format

The generated CSV follows the same format as the original `memory.csv`:

```csv
Operation,Elapsed Time (s),Heap Used Avg,Heap Used StdDev,Margin of Error,Relative Margin of Error
Insert row,"SM: 5.08
ST: 231.27","SM: 125554.64
ST: -14300499.24","SM: 17365.67
ST: 61695.89","SM: 3038.53
ST: 17215.71","SM: 3.09
ST: 2.89"
```

Where:
- **SM**: SharedMatrix data
- **ST**: SharedTree data

## Directory Structure Expected

```
workspace/
├── shared_matrix_memory/
│   ├── .memoryTestsOutput_1/
│   │   ├── *_perfresult.json
│   │   └── ...
│   ├── .memoryTestsOutput_2/
│   └── ...
├── shared_tree_memory/
│   ├── .memoryTestsOutput_1/
│   │   ├── *_perfresult.json
│   │   └── ...
│   └── ...
└── generate_memory_csv.py
```

## Operation Mapping

The script automatically maps benchmark names to standardized operation names:

- Insert operations: "Insert row", "Insert column"
- Remove operations: "Remove row", "Remove column"  
- Undo/Redo operations: "Undo insert row", "Redo remove column", etc.
- Cell operations: "Set cell value", "Undo set cell value", etc.

## Error Handling

- Skips files that cannot be read or parsed
- Ignores missing or invalid data fields
- Continues processing even if some files fail
- Reports warnings for missing directories

## Requirements

- Python 3.6+
- Standard library only (no external dependencies required)
