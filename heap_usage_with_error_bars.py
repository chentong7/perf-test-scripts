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

def create_heap_usage_with_error_bars():
    # Load the CSV file
    file_path = 'enhanced_memory.csv'
    
    print(f"Reading CSV file: {file_path}")
    df = pd.read_csv(file_path)
    
    # Parse heap usage and margin of error data
    plot_data = []
    
    for _, row in df.iterrows():
        operation = row['Operation']
        
        # Get heap usage values
        sm_heap, st_heap = parse_multi_value_cell(row['Heap Used Avg'])
        
        # Get margin of error values
        sm_margin, st_margin = parse_multi_value_cell(row['Margin of Error'])
        
        if sm_heap is not None and sm_margin is not None:
            plot_data.append({
                'Operation': operation,
                'Heap_Usage': sm_heap,
                'Error': sm_margin,
                'Type': 'SharedMatrix'
            })
        
        if st_heap is not None and st_margin is not None:
            plot_data.append({
                'Operation': operation,
                'Heap_Usage': st_heap,
                'Error': st_margin,
                'Type': 'SharedTree'
            })
    
    plot_df = pd.DataFrame(plot_data)
    print(f"Parsed data shape: {plot_df.shape}")
    
    if plot_df.empty:
        print("No data to plot!")
        return
    
    # Create bar chart with error bars
    fig = go.Figure()
    
    # Get unique operations and types
    operations = plot_df['Operation'].unique()
    types = plot_df['Type'].unique()
    
    # Colors for different types
    colors = {'SharedMatrix': '#1f77b4', 'SharedTree': '#ff7f0e'}
    
    for i, op_type in enumerate(types):
        type_data = plot_df[plot_df['Type'] == op_type]
        
        fig.add_trace(go.Bar(
            name=op_type,
            x=type_data['Operation'],
            y=type_data['Heap_Usage'],
            error_y=dict(
                type='data',
                array=type_data['Error'],
                visible=True
            ),
            marker_color=colors.get(op_type, '#888888'),
            offsetgroup=i
        ))
    
    # Update layout
    fig.update_layout(
        title='Heap Memory Usage with Error Bars - SharedMatrix vs SharedTree',
        xaxis_title='Operation',
        yaxis_title='Heap Usage (bytes)',
        barmode='group',
        height=600,
        xaxis_tickangle=-45,
        legend_title='Implementation'
    )
    
    # Save the plot
    filename = 'memory_heap_usage_with_error_bars.html'
    fig.write_html(filename)
    print(f"Saved chart: {filename}")
    
    # Show the plot
    fig.show()
    
    return filename

if __name__ == "__main__":
    create_heap_usage_with_error_bars()
