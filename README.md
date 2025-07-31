# Performance Testing Scripts - SM vs ST Comparison

This repository contains performance analysis scripts and data for comparing **SharedMatrix (SM)** vs **SharedTree (ST)** implementations in the Fluid Framework.

## 📊 Key Performance Charts

### **Primary Time Performance Analysis**
- **`time_period_with_error_bar_chart`** - 🏆 **Main time performance diagram**
  - Measures **Period (ns/op)** - the core metric for operation speed
  - Includes error bars for statistical reliability
  - Uses logarithmic scale to handle 10x-1000x performance differences
  - **Shows SM is 10-100x faster than ST across all operations**

### **Primary Memory Performance Analysis**
- **`memory_bar_chart`** - 🏆 **Main memory performance diagram**
  - Measures **Heap Used Average (bytes)** - actual memory consumption
  - Includes error bars for measurement reliability
  - Shows both allocation and deallocation patterns (positive/negative values)
  - **Shows SM uses more predictable, smaller memory footprints**

## 📈 Additional Analysis Scripts

### Time Analysis
- `time_elapsed_time_bar_chart` - Total elapsed time comparison
- `time_relative_margin_error_chart` - Measurement uncertainty analysis

### Memory Analysis
- `memory_elapsed_time_chart` - Memory operation timing
- `memory_heap_stddev_chart` - Memory usage variability
- `memory_relative_margin_error_chart` - Memory measurement uncertainty
- `memory_split_charts` - Separate small/large scale memory operations

## 📁 Data Files
- **`time.csv`** - Time performance data (Period, Elapsed Time, Margin of Error)
- **`memory.csv`** - Memory performance data (Heap Usage, Standard Deviation, Margin of Error)


## 🚀 Usage

### Prerequisites
```bash
pip install pandas plotly kaleido
```

### Running the Scripts
```bash
# Primary time analysis
python time_period_with_error_bar_chart

# Primary memory analysis
python memory_bar_chart

# Additional analyses
python [script_name]
```

### Output Files
Each script generates:
- `.png` - High-resolution charts
- `.html` - Interactive visualizations
- `.json` - Raw chart data
