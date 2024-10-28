import plotly.express as px
from shiny import reactive
from shiny.express import render, input, ui
from shinywidgets import render_plotly
import duckdb
import pandas as pd
from pipe import ELTPipeline


ui.page_opts(title = "Countries' Olympic Medals vs their Population and GDP", fillable=True)

with ui.sidebar():
    "Input Variables"
    ui.input_select(  
    "select",  
    "Select an option below:",  
    {"total": "Total Medals", "gold": "Gold Medals", "silver": "Silver Medals", "bronze": "Bronze Medals"},  
) 
"Main Content"

@reactive.calc
def getdata():
    pipeline = ELTPipeline()
    df = pipeline.extract()
    return df

with ui.card():

    ui.markdown("Olympic Medal Count By Country")

    ui.input_numeric("n", "Number of items in bar plot", 5, min = 1, max = 88)


    with ui.layout_columns():
        @render_plotly
        def total_medals_plot():
            df = getdata()
            top_n = df.groupby('country_code')['total'].sum().nlargest(input.n()).reset_index()
            return px.bar(top_n, x = 'country_code', y = 'total')

with ui.card():

    ui.markdown("Raw Data")

    @render.data_frame
    def showtable():
        return getdata()