# Performance Test Analysis Workflow

This guide explains how to reproduce the complete workflow from raw performance test results to CSV tables to interactive charts.

## Overview

The workflow consists of three main steps:
1. **Data Extraction**: Convert JSON test results → CSV tables
2. **Data Visualization**: Convert CSV tables → Interactive charts
3. **Specific Analysis**: Create targeted visualizations (e.g., heap usage with error bars)

## Prerequisites

1. **Python Environment**: Ensure Python 3.6+ is installed
2. **Required Packages**: The scripts will automatically install needed packages
3. **Test Data**: Performance test results in `shared_matrix_memory/` and `shared_tree_memory/` directories

## Directory Structure

Your workspace should have this structure:
```
workspace/
├── shared_matrix_memory/           # SharedMatrix test results
│   ├── .memoryTestsOutput_1/
│   │   ├── *_perfresult.json      # Performance test JSON files
│   │   └── ...
│   ├── .memoryTestsOutput_2/
│   └── ...
├── shared_tree_memory/             # SharedTree test results
│   ├── .memoryTestsOutput_1/
│   │   ├── *_perfresult.json      # Performance test JSON files
│   │   └── ...
│   └── ...
└── (analysis scripts)
```

## Step 1: Extract Data to CSV Tables

### Script: `generate_memory_csv_enhanced.py`

This script reads all JSON performance test files and creates aggregated CSV tables.

**Command:**
```bash
python generate_memory_csv_enhanced.py [output_filename]
```

**Examples:**
```bash
# Use default filename (generated_memory.csv)
python generate_memory_csv_enhanced.py

# Specify custom filename
python generate_memory_csv_enhanced.py my_performance_data.csv
```

**What it does:**
- Scans all `*_perfresult.json` files in both directories recursively
- Extracts performance metrics:
  - Elapsed Time
  - Heap Used Average
  - Heap Used Standard Deviation
  - Margin of Error
  - Relative Margin of Error
- Groups similar operations together (e.g., "Insert row", "Remove column")
- **Averages multiple test runs**: If the same test case has values `a`, `b`, `c`, the output shows `(a+b+c)/3`
- Handles missing values gracefully (skips them in calculations)
- Outputs CSV with SM (SharedMatrix) and ST (SharedTree) data side by side

**Output Format:**
```csv
Operation,Elapsed Time (s),Heap Used Avg,Heap Used StdDev,Margin of Error,Relative Margin of Error
Insert row,"SM: 18.25
ST: 282.82","SM: 144512.31
ST: -17057723.24","SM: 28898.86
ST: 41034.86","SM: 3851.16
ST: 11175.80","SM: 33.35
ST: 2.15"
```

## Step 2: Generate General Charts

### Script: `memory_chart_generator.py`

This script creates individual charts for each performance metric.

**Command:**
```bash
python memory_chart_generator.py
```

**What it does:**
- Reads the CSV file generated in Step 1
- Parses SM/ST value pairs from each cell
- Creates separate interactive bar charts for each metric:
  - Elapsed Time comparison
  - Heap Usage Average comparison
  - Heap Usage Standard Deviation comparison
  - Margin of Error comparison
  - Relative Margin of Error comparison

**Generated Files:**
- `memory_elapsed_time_s_chart.html`
- `memory_heap_used_avg_chart.html`
- `memory_heap_used_stddev_chart.html`
- `memory_margin_of_error_chart.html`
- `memory_relative_margin_of_error_chart.html`

## Step 3: Create Specific Analysis Charts

### Script: `heap_usage_with_error_bars.py`

This script creates a specialized chart showing heap usage with error bars.

**Command:**
```bash
python heap_usage_with_error_bars.py
```

**What it does:**
- Combines "Heap Used Avg" (bar height) with "Margin of Error" (error bars)
- Creates grouped bar chart comparing SharedMatrix vs SharedTree
- Shows uncertainty/reliability of measurements through error bars

**Generated File:**
- `memory_heap_usage_with_error_bars.html`

## Complete Reproduction Steps

### 1. Setup Environment
```bash
# Navigate to your workspace
cd /path/to/your/workspace

# Configure Python environment (if needed)
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

### 2. Extract Data from Test Results
```bash
# Generate CSV table from JSON test results
python generate_memory_csv_enhanced.py performance_results.csv
```

**Expected Output:**
```
Reading performance data...
Scanning SharedMatrix directory: shared_matrix_memory
  Processed 48 files, found 5 operation types
Scanning SharedTree directory: shared_tree_memory  
  Processed 29 files, found 5 operation types

Found 5 unique operations:
  - Insert column: SM(18) ST(9)
  - Insert row: SM(54) ST(25)
  - Remove column: SM(18) ST(7)
  - Remove row: SM(36) ST(18)
  - Set cell value: SM(18) ST(11)

✅ CSV file generated successfully!
```

### 3. Generate All Charts
```bash
# Create individual metric charts
python memory_chart_generator.py
```

**Expected Output:**
```
Reading CSV file: performance_results.csv
CSV loaded successfully. Shape: (5, 6)
Parsed data shape: (50, 4)

Creating chart for Elapsed Time (s)
Saved chart: memory_elapsed_time_s_chart.html

Creating chart for Heap Used Avg
Saved chart: memory_heap_used_avg_chart.html
...
```

### 4. Create Specialized Analysis
```bash
# Create heap usage chart with error bars
python heap_usage_with_error_bars.py
```

**Expected Output:**
```
Reading CSV file: performance_results.csv
Parsed data shape: (10, 4)
Saved chart: memory_heap_usage_with_error_bars.html
```

### 5. View Results
Open any of the generated HTML files in a web browser:
- Double-click the `.html` files, or
- Use `start filename.html` (Windows) or `open filename.html` (Mac)

## Data Flow Summary

```
JSON Test Results → CSV Table → Interactive Charts
     ↓                ↓              ↓
*_perfresult.json → enhanced.csv → *.html charts
     ↓                ↓              ↓
Individual runs   → Averaged     → Visual 
Raw metrics       → values       → comparisons
```

## Troubleshooting

### Missing Dependencies
If you get import errors:
```bash
pip install pandas plotly
```

### No Data Found
- Verify directory structure matches expected format
- Check that JSON files end with `_perfresult.json`
- Ensure JSON files contain `benchmarks` array with valid data

### Empty Charts
- Check that CSV file was generated successfully
- Verify CSV contains SM/ST value pairs in expected format
- Look for parsing errors in console output

## Customization

### Modify CSV Output
Edit `generate_memory_csv_enhanced.py`:
- Change operation name mapping in `extract_operation_name()`
- Add/remove metrics in the `metrics` list
- Modify aggregation logic in `aggregate_data()`

### Customize Charts
Edit chart generator scripts:
- Change colors, titles, layout in the Plotly configuration
- Add new chart types (line charts, scatter plots, etc.)
- Filter data for specific operations or metrics

### Add New Analysis
Create new scripts following the pattern:
1. Read CSV file with `pandas`
2. Parse SM/ST values with regex
3. Create charts with `plotly`
4. Save as HTML files

## File Dependencies

- `generate_memory_csv_enhanced.py` → `enhanced_memory.csv`
- `memory_chart_generator.py` → requires CSV from step 1
- `heap_usage_with_error_bars.py` → requires CSV from step 1

Make sure to run the scripts in order: data extraction → visualization.
