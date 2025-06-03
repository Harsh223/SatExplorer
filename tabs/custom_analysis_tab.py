import streamlit as st
import plotly.express as px
import pandas as pd

def render_tab(df):
    st.header("Custom Analysis & Visualization")
    st.info("""
    Build your own analysis! Select the data columns, chart type, and filters to create custom visualizations. This tool is designed for both non-technical and technical users.
    """)
    all_columns = df.columns.tolist()
    x_col = st.selectbox("X-axis column", all_columns, index=all_columns.index('LaunchYear') if 'LaunchYear' in all_columns else 0)
    y_col = st.selectbox("Y-axis column (for bar/line/scatter)", [col for col in all_columns if col != x_col], index=0)
    color_col = st.selectbox("Color/Group by (optional)", [None] + all_columns, index=0)
    chart_type = st.selectbox("Chart type", ["Bar", "Line", "Scatter", "Pie", "Histogram"])
    st.markdown("**Add Filters** (optional)")
    filter_col = st.selectbox("Filter column", [None] + all_columns, index=0)
    if filter_col:
        unique_vals = df[filter_col].dropna().unique().tolist()
        selected_vals = st.multiselect(f"Select values for {filter_col}", unique_vals, default=unique_vals)
        custom_df = df[df[filter_col].isin(selected_vals)]
    else:
        custom_df = df.copy()
    st.markdown("---")
    st.subheader("Custom Chart")
    if chart_type == "Bar":
        fig = px.bar(custom_df, x=x_col, y=y_col, color=color_col if color_col else None)
    elif chart_type == "Line":
        fig = px.line(custom_df, x=x_col, y=y_col, color=color_col if color_col else None)
    elif chart_type == "Scatter":
        fig = px.scatter(custom_df, x=x_col, y=y_col, color=color_col if color_col else None)
    elif chart_type == "Pie":
        fig = px.pie(custom_df, names=x_col, values=y_col if y_col else None, color=color_col if color_col else None)
    elif chart_type == "Histogram":
        if pd.api.types.is_numeric_dtype(custom_df[x_col]):
            bin_edges = [0, 5, 10, 20, 30, 50, 100, 200, 300, 500, 1000, 2000, 3000, 5000, 10000, 20000, 50000, 100000, 200000, 500000, 1000000]
            data = custom_df[x_col].dropna()
            bin_labels = [f"{bin_edges[i]}-{bin_edges[i+1]}" for i in range(len(bin_edges)-1)]
            binned = pd.cut(data, bins=bin_edges, labels=bin_labels, right=False)
            bin_counts = binned.value_counts().sort_index()
            nonzero_bins = bin_counts[bin_counts > 0]
            if not nonzero_bins.empty:
                hist_df = pd.DataFrame({x_col: nonzero_bins.index, 'Count': nonzero_bins.values})
                y_max = int(nonzero_bins.max())
                y_axis_max = min(5000, max(10, y_max + int(0.1*y_max)))
                fig = px.bar(hist_df, x=x_col, y='Count', title=f'{x_col} Histogram', labels={x_col: x_col, 'Count': 'Count'})
                fig.update_yaxes(range=[0, y_axis_max])
            else:
                fig = None
        else:
            fig = px.histogram(custom_df, x=x_col, color=color_col if color_col else None)
    else:
        fig = None
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Select chart options to display a chart.")
