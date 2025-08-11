# Quick Reference: Test Results to Charts

## 🚀 Three-Step Process

### 1️⃣ Extract Data (JSON → CSV)
```bash
python generate_memory_csv_enhanced.py
```
**Input:** `shared_matrix_memory/` + `shared_tree_memory/` directories  
**Output:** `enhanced_memory.csv` (averaged values from all test runs)

### 2️⃣ Generate Charts (CSV → HTML)
```bash
python memory_chart_generator.py
```
**Input:** CSV from step 1  
**Output:** 5 individual metric charts (elapsed time, heap usage, etc.)

### 3️⃣ Specialized Analysis
```bash
python heap_usage_with_error_bars.py
```
**Input:** CSV from step 1  
**Output:** Heap usage chart with error bars

## 📊 Generated Files

| File | Description |
|------|-------------|
| `enhanced_memory.csv` | Aggregated performance data |
| `memory_elapsed_time_s_chart.html` | Time comparison chart |
| `memory_heap_used_avg_chart.html` | Heap usage comparison |
| `memory_heap_used_stddev_chart.html` | Heap variation chart |
| `memory_margin_of_error_chart.html` | Error analysis chart |
| `memory_relative_margin_of_error_chart.html` | Relative error chart |
| `memory_heap_usage_with_error_bars.html` | ⭐ Heap usage with uncertainty |

## 🔄 Data Flow
```
*.json files → CSV table → Interactive charts
(raw tests) → (averaged) → (visual comparison)
```

## 📋 Key Features

- ✅ **Automatic averaging**: Multiple test runs → single averaged value
- ✅ **Missing data handling**: Skips invalid/missing values
- ✅ **Side-by-side comparison**: SharedMatrix vs SharedTree
- ✅ **Interactive charts**: Zoom, hover, export capabilities
- ✅ **Error visualization**: Shows measurement uncertainty

## 🛠️ Prerequisites

```bash
pip install pandas plotly
```

## 📂 Required Directory Structure
```
workspace/
├── shared_matrix_memory/
│   └── .memoryTestsOutput_*/
│       └── *_perfresult.json
├── shared_tree_memory/
│   └── .memoryTestsOutput_*/
│       └── *_perfresult.json
└── (scripts)
```
