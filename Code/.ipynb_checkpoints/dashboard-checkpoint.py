import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# Neighborhood Census data
file_path = Path("Data/sfo_neighborhoods_census_data.csv")
sfo_data = pd.read_csv(file_path, index_col="year")

# Neighborhood Coordinates data
loc_path = Path("Data/neighborhoods_coordinates.csv")
sfo_coords = pd.read_csv(loc_path, index_col="Neighborhood")
'''
## Streamlit Visualizations

In this section, you will copy the code for each plot type from your analysis notebook and place it into separate functions that Streamlit can use to visualize the different visualizations.

These functions will return the plot or figure for each visualization.

Be sure to include any DataFrame transformation/manipulation code required along with the plotting code.

Return a figure object from each function that can be used to build the dashboard.

Note: Remove any `.show()` lines from the code. We want to return the plots instead of showing them. The Streamlit dashboard will then display the plots.
'''
# Clean data
sfo_clean = sfo_data.dropna()

# Define Visualization Functions
def housing_units_per_year():
    """Housing Units Per Year."""
    # Calculate the mean number of housing units per year 
    avg_housing_unit = sfo_clean[["housing_units"]].groupby("year").mean("housing_units")
    bar_fig = px.bar(avg_housing_unit, x=avg_housing_unit.index, y="housing_units", title="Housing Units in San Francisco from 2010-2016")

    # Use the min, max, and std to scale the y limits of the chart
    min = avg_housing_unit['housing_units'].min()
    max = avg_housing_unit['housing_units'].max()
    std = avg_housing_unit['housing_units'].std()

    # Set plot size for better readability
    bar_fig.update_layout(
        autosize=False,
        width=700,
        height=500
    )

    # Adjust y limits based on min, max, and std
    bar_fig.update_yaxes(range=(min-std,max+std), title='Average Housing Units')
    bar_fig.update_xaxes(title='Year')
    return bar_fig

def average_gross_rent():
    """Average Gross Rent in San Francisco Per Year."""
    # Calculate the average sale price per square foot and average gross rent
    avg_price_rent = sfo_clean[["sale_price_sqr_foot","gross_rent"]].groupby("year").mean("sale_price_sqr_foot","gross_rent")
    # Create two line charts, one to plot the average sale price per square foot and another for average montly rent

    # Line chart for average sale price per square foot
    price_fig = px.line(avg_price_rent,x=avg_price_rent.index,y="sale_price_sqr_foot", title="Avg. Sales Price per Sq. Foot in San Francisco over Time")
    price_fig.update_traces(line_color='blue')
    price_fig.update_layout(
        autosize=False,
        width=800,
        height=500
    )
    price_fig.update_xaxes(title='Year')
    price_fig.update_yaxes(title='Avg. Sale Price per Square Foot')
    price_fig.show()
    
    # Line chart for average montly rent
    rent_fig = px.line(avg_price_rent,x=avg_price_rent.index,y="gross_rent", title="Avg. San Francisco Rent over Time")
    rent_fig.update_traces(line_color='red')
    rent_fig.update_layout(
        autosize=False,
        width=800,
        height=500
    )
    rent_fig.update_xaxes(title='Year')
    rent_fig.update_yaxes(title='Avg. Rent')
    return price_fig, rent_fig

def average_sales_price():
    """Average Sales Price Per Year."""
    
    # YOUR CODE HERE!



def average_price_by_neighborhood():
    """Average Prices by Neighborhood."""
    
    # YOUR CODE HERE!



def top_most_expensive_neighborhoods():
    """Top 10 Most Expensive Neighborhoods."""

    # YOUR CODE HERE!


def most_expensive_neighborhoods_rent_sales():
    """Comparison of Rent and Sales Prices of Most Expensive Neighborhoods."""   
    
    # YOUR CODE HERE!

    
    
def parallel_coordinates():
    """Parallel Coordinates Plot."""

    # YOUR CODE HERE!



def parallel_categories():
    """Parallel Categories Plot."""
    
    # YOUR CODE HERE!



def neighborhood_map():
    """Neighborhood Map."""

    # YOUR CODE HERE!


def sunburst():
    """Sunburst Plot."""
    
    # YOUR CODE HERE!

# Start Streamlit App
# YOUR CODE HERE!
