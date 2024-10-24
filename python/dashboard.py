from shiny import App, render, ui, reactive
import duckdb
import plotly.express as px
import pandas as pd

class AnalyticsDashboard:
    def __init__(self, db_path='analytics.ddb'):
        self.conn = duckdb.connect(db_path)
        
    def create_ui(self):
        """Create the dashboard UI"""
        return ui.page_fluid(
            ui.h1("Data Analytics Dashboard"),
            
            # Correct layout structure
            ui.layout_sidebar(
                ui.sidebar(
                    ui.input_select(
                        "chart_type",
                        "Select Chart Type",
                        choices=["line", "bar", "scatter"]
                    ),
                    ui.input_select(
                        "metric",
                        "Select Metric",
                        choices=self._get_numeric_columns()
                    ),
                    ui.input_select(
                        "group_by",
                        "Group By",
                        choices=self._get_categorical_columns()
                    ),
                    width=250
                ),
                # Main content
                ui.card(
                    ui.card_header("Visualization"),
                    ui.output_plot("main_plot")
                ),
                ui.card(
                    ui.card_header("Summary Statistics"),
                    ui.output_table("summary_stats")
                )
            )
        )
    
    def _get_numeric_columns(self):
        """Get list of numeric columns from the database"""
        try:
            query = """
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'analytics_table' 
                AND data_type IN ('INTEGER', 'DOUBLE', 'DECIMAL')
            """
            return [row[0] for row in self.conn.execute(query).fetchall()]
        except:
            return ["sample_metric"]  # Fallback if table doesn't exist yet
    
    def _get_categorical_columns(self):
        """Get list of categorical columns from the database"""
        try:
            query = """
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'analytics_table' 
                AND data_type IN ('VARCHAR', 'TEXT')
            """
            return [row[0] for row in self.conn.execute(query).fetchall()]
        except:
            return ["sample_category"]  # Fallback if table doesn't exist yet
    
    def create_server(self):
        """Create the server function"""
        def server(input, output, session):
            @output
            @render.plot
            def main_plot():
                metric = input.metric()
                group_by = input.group_by()
                chart_type = input.chart_type()
                
                try:
                    query = f"""
                        SELECT 
                            {group_by},
                            {metric}
                        FROM analytics_table
                        GROUP BY {group_by}
                        ORDER BY {group_by}
                    """
                    df = self.conn.execute(query).df()
                    
                    if chart_type == "line":
                        fig = px.line(df, x=group_by, y=metric)
                    elif chart_type == "bar":
                        fig = px.bar(df, x=group_by, y=metric)
                    else:
                        fig = px.scatter(df, x=group_by, y=metric)
                        
                    return fig
                except Exception as e:
                    # Return empty plot if data isn't ready
                    return px.scatter(pd.DataFrame({'x': [], 'y': []}))
            
            @output
            @render.table
            def summary_stats():
                metric = input.metric()
                
                try:
                    query = f"""
                        SELECT 
                            COUNT(*) as count,
                            AVG({metric}) as average,
                            MIN({metric}) as minimum,
                            MAX({metric}) as maximum,
                            STDDEV({metric}) as std_dev
                        FROM analytics_table
                    """
                    return self.conn.execute(query).df()
                except:
                    return pd.DataFrame({'Status': ['No data available yet']})
        
        return server

# Run the dashboard
if __name__ == "__main__":
    dashboard = AnalyticsDashboard()
    app = App(dashboard.create_ui(), dashboard.create_server())
    app.run()