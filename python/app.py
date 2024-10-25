import plotly.express as px
from shiny import reactive
from shiny.express import render, input, ui
from shinywidgets import render_plotly
import duckdb
import pandas as pd
from pipe import ELTPipeline


ui.page_opts(title = "Countries Olympic Medals vs their Population and GDP", fillable=True)

@reactive.calc
def getdata():
    pipeline = ELTPipeline()
    df = pipeline.extract()
    return df
    

with ui.layout_columns():
    
    @render_plotly
    def total_medals_plot():
        df = getdata()
        top_5 = df.groupby('country_code')['total'].sum().nlargest(5).reset_index()
        return px.bar(top_5, x = 'country_code', y = 'total')


    @render.data_frame
    def showtable():
        return getdata()