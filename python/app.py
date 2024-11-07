import plotly.express as px
from shiny import reactive, App, ui
from shiny.express import render, input, ui
from shiny.ui import page_navbar
from shinywidgets import render_plotly
from functools import partial
import duckdb
import pandas as pd
from pipe import ELTPipeline


ui.page_opts(title = "Countries' Olympic Medals vs their Population and GDP",
             fillable=True,
             page_fn = partial(page_navbar, id = "page"))

with ui.nav_control():
    ui.input_dark_mode()

with ui.nav_panel("Medals"):

    with ui.card():

        ui.markdown("Olympic Total Medal Count By Country.")

        ui.input_numeric("n", "Number of items in bar plot", 5, min = 1, max = 88)

    with ui.layout_columns():
        @render_plotly
        def total_medals_plot():
            df = getdata()
            top_n = df.groupby('country_code')['total'].sum().nlargest(input.n()).reset_index()
            return px.bar(top_n, x = 'country_code', y = 'total')

    with ui.card():
    
        ui.markdown("Gold, Silver and Bronze medals.")

        ui.input_numeric("gn", "Number of items in bar plot", 5, min = 1, max = 88)

        ui.input_selectize("medalselect", "Select medal category.",
                        {"gold":"Gold Medal", "silver":"Silver Medal", "bronze":"Bronze Medal"})

    with ui.layout_columns():
        @render_plotly
        def gold_medals_plot():
            df = getdata()
            gold_n = df.groupby('country_code')[input.medalselect()].sum().nlargest(input.gn()).reset_index()
            return px.bar(gold_n, x = 'country_code' , y = input.medalselect())


with ui.nav_panel("GDP"):
    ...

with ui.nav_panel("Raw Data"):
    with ui.card():

        ui.markdown("Raw Data")

        @render.data_frame
        def showtable():
            return getdata()


@reactive.calc
def getdata():
    pipeline = ELTPipeline()
    df = pipeline.extract()
    return df