import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re
import os

def parse_multi_value_cell(cell_value):
    """Parse a cell that contains SM: and ST: values."""
    if pd.isna(cell_value) or cell_value == '':
        return None, None
    
    # Extract SM and ST values
    sm_match = re.search(r'SM:\s*([-\d.]+)', str(cell_value))
    st_match = re.search(r'ST:\s*([-\d.]+)', str(cell_value))
    
    sm_val = float(sm_match.group(1)) if sm_match else None
    st_val = float(st_match.group(1)) if st_match else None
    
    return sm_val, st_val

def main():
    # Load the CSV file
    file_path = 'enhanced_memory.csv'
    
    print(f"Reading CSV file: {file_path}")
    
    # Read the CSV
    df = pd.read_csv(file_path)
    print(f"CSV loaded successfully. Shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
    # Create a list to store parsed data
    plot_data = []
    
    for _, row in df.iterrows():
        operation = row['Operation']
        
        # Parse each metric column
        metrics = ['Elapsed Time (s)', 'Heap Used Avg', 'Heap Used StdDev', 
                  'Margin of Error', 'Relative Margin of Error']
        
        for metric in metrics:
            if metric in row:
                sm_val, st_val = parse_multi_value_cell(row[metric])
                
                if sm_val is not None:
                    plot_data.append({
                        'Operation': operation,
                        'Metric': metric,
                        'Value': sm_val,
                        'Type': 'SharedMatrix'
                    })
                
                if st_val is not None:
                    plot_data.append({
                        'Operation': operation,
                        'Metric': metric,
                        'Value': st_val,
                        'Type': 'SharedTree'
                    })
    
    plot_df = pd.DataFrame(plot_data)
    print(f"Parsed data shape: {plot_df.shape}")
    
    if plot_df.empty:
        print("No data to plot!")
        return
    
    # Create separate plots for each metric
    metrics = plot_df['Metric'].unique()
    
    for metric in metrics:
        metric_data = plot_df[plot_df['Metric'] == metric]
        
        if metric_data.empty:
            continue
            
        print(f"\nCreating chart for {metric}")
        
        # Create bar chart
        fig = px.bar(
            metric_data, 
            x='Operation', 
            y='Value', 
            color='Type',
            barmode='group',
            title=f'{metric} - SharedMatrix vs SharedTree',
            labels={'Value': metric}
        )
        
        # Customize layout
        fig.update_layout(
            xaxis_title="Operation",
            yaxis_title=metric,
            legend_title="Implementation",
            height=600,
            xaxis_tickangle=-45
        )
        
        # Save the plot
        filename = f"memory_{metric.lower().replace(' ', '_').replace('(', '').replace(')', '')}_chart.html"
        fig.write_html(filename)
        print(f"Saved chart: {filename}")
        
        # Show the plot
        fig.show()

if __name__ == "__main__":
    main()
