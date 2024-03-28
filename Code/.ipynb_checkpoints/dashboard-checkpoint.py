import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np


# Neighborhood Census data
file_path = Path("Data/sfo_neighborhoods_census_data.csv")
sfo_data = pd.read_csv(file_path, index_col="year")

# Neighborhood Coordinates data
loc_path = Path("Data/neighborhoods_coordinates.csv")
sfo_coords = pd.read_csv(loc_path, index_col="Neighborhood")

# List of unique neighborhoods
neighborhoods = sfo_data['neighborhood'].drop_duplicates().tolist()
neighborhoods.sort()

# Clean data
sfo_clean = sfo_data.dropna()

# Define Visualization Functions
def housing_units_per_year():
    """Housing Units Per Year."""
    # Calculate the mean number of housing units per year 
    avg_housing_unit = sfo_clean[["housing_units"]].groupby("year").mean("housing_units")
    
    #Create bar chart to show increase in housing units per year
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
    return rent_fig

def average_sales_price():
    """Average Sales Price Per Year."""
    avg_price_rent = sfo_clean[["sale_price_sqr_foot","gross_rent"]].groupby("year").mean("sale_price_sqr_foot","gross_rent")

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
    return price_fig

def average_price_by_neighborhood(neighborhood):
    """Average Prices by Neighborhood."""
    df_prices = sfo_data[sfo_data['neighborhood'] == neighborhood]
    #Convert 'sale_price_sqr_foot' to a numeric type, ignore errors to avoid conversion issues
    df_prices['sale_price_sqr_foot'] = pd.to_numeric(df_prices['sale_price_sqr_foot'], errors='coerce')
    # Drop rows with NaN values in 'sale_price_sqr_foot' after conversion
    df_prices.dropna(inplace=True)
    # Group by 'year' and calculate mean, ensuring 'sale_price_sqr_foot' is now numeric
    avg_price_sqft = df_prices[["sale_price_sqr_foot"]].groupby("year").mean("sale_price_sqr_foot")

    # Create and return the plot
    fig = px.line(avg_price_sqft, x=avg_price_sqft.index, y="sale_price_sqr_foot", title=f"Avg. Price per Square Foot in {neighborhood}")
    fig.update_traces(line_color='green')
    fig.update_layout(
    autosize=False,
    width=800,
    height=500
)
    fig.update_xaxes(title='Year')
    fig.update_yaxes(title='Sales Price per Square Foot')
    return fig

def average_rent_by_neighborhood(neighborhood):
    df_rent = sfo_data[sfo_data['neighborhood'] == neighborhood]
    # Convert 'gross_rent' to a numeric type, ignore errors to avoid conversion issues
    df_rent['gross_rent'] = pd.to_numeric(df_rent['gross_rent'], errors='coerce')
    # Drop rows with NaN values in 'gross_rent' after conversion
    df_rent.dropna(inplace=True)
    # Group by 'year' and calculate mean, ensuring 'gross_rent' is now numeric
    avg_rent_df = df_rent[["gross_rent"]].groupby("year").mean("gross_rent")
    # Create and return the plot
    fig = px.line(avg_rent_df, x=avg_rent_df.index, y="gross_rent", title=f"Avg. Rent in {neighborhood}")
    fig.update_traces(line_color='purple')
    fig.update_layout(
    autosize=False,
    width=800,
    height=500
)
    fig.update_xaxes(title='Year')
    fig.update_yaxes(title='Rent Price')
    return fig


def top_most_expensive_neighborhoods():
    """Top 10 Most Expensive Neighborhoods."""

    # Getting the data from the top 10 expensive neighborhoods to own
    df_expensive_neighborhoods = sfo_clean[['neighborhood','sale_price_sqr_foot']].groupby(by="neighborhood").mean('sale_price_sqr_foot')
    df_expensive_neighborhoods.reset_index(inplace=True)
    top_10_neighbor_df = df_expensive_neighborhoods.sort_values('sale_price_sqr_foot', ascending=False).head(10)

    # Plotting the data from the top 10 expensive neighborhoods
    exp_fig = px.bar(top_10_neighbor_df, x='neighborhood', y='sale_price_sqr_foot', title='Top 10 Most Expensive Neighborhoods in San Francisco (2010 - 2016)')
    exp_fig.update_xaxes(title="Neighborhood")
    exp_fig.update_yaxes(title="Price per Square Foot")
    exp_fig.update_layout(
        autosize=False,
        width=900,
        height=500
    )
    exp_fig.update_traces(marker_color='green')
    return exp_fig
    
def most_expensive_neighborhoods_rent_sales(selected_neighborhood):
    """Comparison of Rent and Sales Prices of Most Expensive Neighborhoods."""   
    
    df_costs = sfo_data[sfo_data['neighborhood'] == selected_neighborhood]
    fig = px.bar(df_costs, x=df_costs.index, y=["gross_rent","sale_price_sqr_foot"], 
                 title=f"Rent and Sales Price in {selected_neighborhood} (2010-2016)",
                barmode='group')
    fig.update_layout(
    xaxis_title='Year',
    yaxis_title='USD',
    legend_title_text='Type',
    autosize=False,
    width=800,
    height=500
)
    return fig

def neighborhood_map():
    """Neighborhood Map."""
    # Calculate the mean values for each neighborhood
    mean_values = np.round(sfo_data[["gross_rent"]].groupby(sfo_data["neighborhood"]).mean("gross_rent"), decimals=2)
    # Join the average values with the neighborhood locations
    combined_data = pd.concat([sfo_coords, mean_values], axis="columns", join="inner")
    
    #Create mapbox visualization
    df = combined_data
    fig = px.scatter_mapbox(df, lat="Lat", lon="Lon", color="gross_rent", size="gross_rent", hover_name=df.index,
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=11, mapbox_style='carto-positron')
    fig.update_layout(height = 800)
    return fig

# Streamlit App Data
st.set_page_config(page_title="San Francisco Rent Analysis (2010-2016)", layout="wide")

tab1, tab2, tab3, tab4 = st.tabs(["Intro", "Supply and Demand", "Neighborhood Breakdown", "Map of Average Rental Prices"])

# Intro Tab
with tab1:
    st.header("San Francisco Rent Analysis (2010-2016)")
    col1, col2 = st.columns(2)
    with col1:
        st.image("../Images/san-francisco.jpg")
    with col2:
        st.markdown(
    """
    <div style="display: flex; justify-content: center; align-items: center; height: 50vh;">
        <h4 style="text-align: center;">An analysis of San Francisco rental prices since 2010-2016.  This analysis includes overall trends, as well as a neighborhood  breakdown to determine which were the most expensive neighborhoods over that time.  In general, rent and sales prices steadily increased from 2010-2016, though there were certain neighborhoods within the city that didn't experience as rapid an increase as others which can be explored by the user.</h3>
    </div>
    """,
    unsafe_allow_html=True
)


# Supply and Demand
with tab2:
       st.header("Supply and Demand")
       st.write("The number of housing units in San Francisco increased between the 2010 - 2016, which created additional supply.  However, as we can see in the trend charts below, demand appears to have increased at a higher rate as rent prices also increased over time during this same period.")
       st.plotly_chart(housing_units_per_year(),use_container_width=True)
       col1, col2 = st.columns(2, gap="medium")
       with col1:
           st.plotly_chart(average_gross_rent())
       with col2: 
           st.plotly_chart(average_sales_price())
           
# Neighborhood Breakdown
with tab3:
    st.header("Neighborhood Breakdown")
    input = st.selectbox("Select a neighborhood",neighborhoods)
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.plotly_chart(top_most_expensive_neighborhoods())
        st.plotly_chart(average_rent_by_neighborhood(input))
    with col2:
        st.plotly_chart(most_expensive_neighborhoods_rent_sales(input))
        st.plotly_chart(average_price_by_neighborhood(input))

# Neighborhood Interactive Map
with tab4:
    st.header("Map of Average Rental Prices")
    st.write("This is an interactive map.  You may hover over each neighborhood to see its location as well as the average rent for that area of the city.")
    st.plotly_chart(neighborhood_map(), use_container_width=True)

#def parallel_coordinates():
#    """Parallel Coordinates Plot."""

    # YOUR CODE HERE!



#def parallel_categories():
#    """Parallel Categories Plot."""
    
    # YOUR CODE HERE!



#def sunburst():
#    """Sunburst Plot."""
    
    # YOUR CODE HERE!

# Start Streamlit App
# YOUR CODE HERE!
