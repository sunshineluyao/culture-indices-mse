import dash
from dash import dcc, html, dash_table, Input, Output
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Define cultural regions
cultural_regions = {
    'African-Islamic': ['Algeria', 'Egypt', 'Jordan', 'Libya', 'Morocco', 'Tunisia', 'Yemen', 'Iraq',
                        'Nigeria', 'Uganda', 'Lebanon', 'Pakistan', 'Bangladesh', 'Turkey', 'Palestine',
                        'Ethiopia', 'Kenya', 'Ghana', 'Mali', 'Maldives', 'Trinidad and Tobago', 'Rwanda',
                        'Tanzania', 'Zimbabwe', 'Burkina Faso'],
    'Confucian': ['China', 'Hong Kong SAR', 'Japan', 'South Korea', 'Taiwan ROC', 'Singapore', 'Vietnam', 'Macau SAR', 'Mongolia'],
    'Latin America': ['Argentina', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Mexico', 'Peru', 'Uruguay', 'Venezuela',
                      'Bolivia', 'Guatemala', 'Honduras', 'Nicaragua', 'Paraguay', 'Dominican Republic', 'Haiti',
                      'Philippines', 'Puerto Rico', 'El Salvador'],
    'Catholic Europe': ['France', 'Italy', 'Spain', 'Portugal', 'Poland', 'Austria', 'Belgium', 'Luxembourg', 'Ireland', 'Malta', 'Andorra', 'Cyprus'],
    'English-Speaking': ['United States', 'Canada', 'Australia', 'New Zealand', 'United Kingdom', 'Ireland', 'Great Britain', 'Northern Ireland'],
    'Orthodox Europe': ['Russia', 'Ukraine', 'Belarus', 'Serbia', 'Armenia', 'Georgia', 'Moldova', 'Romania',
                        'Bosnia and Herzegovina', 'Montenegro', 'Bulgaria', 'North Macedonia', 'Greece', 'Albania', 'Kosovo'],
    'Protestant Europe': ['Germany', 'Germany West', 'Denmark', 'Sweden', 'Norway', 'Netherlands', 'Switzerland', 'Finland', 'Iceland',
                          'Lithuania', 'Latvia', 'Estonia', 'Czechia', 'Hungary', 'Slovakia', 'Slovenia', 'Croatia'],
    'West & South Asia': ['India', 'Indonesia', 'Malaysia', 'Bangladesh', 'Thailand', 'Philippines', 'Sri Lanka', 'Iran', 'Saudi Arabia',
                          'Kazakhstan', 'Kyrgyzstan', 'Uzbekistan', 'Turkey', 'Myanmar', 'Zambia', 'South Africa', 'Tajikistan', 'Qatar', 'Israel', 'Azerbaijan']
}

# Convert cultural regions into a DataFrame for the table
cultural_regions_df = pd.DataFrame([
    {"Region": region, "Countries": ', '.join(countries)}
    for region, countries in cultural_regions.items()
])

# Load the MSE dataset
region_summary_df = pd.read_json("region_summary.json")  # Ensure this file exists in the same directory

# Create Dash app
app = dash.Dash(__name__)
server = app.server  # Expose the Flask server instance for Render

# Calculate benchmarks
sorted_data_mse_traditional = region_summary_df.sort_values(by='MSE_Traditional_vs_Secular', ascending=True)
sorted_data_mse_survival = region_summary_df.sort_values(by='MSE_Survival_vs_SelfExpression', ascending=True)

benchmark_mse_traditional = (
    sorted_data_mse_traditional['MSE_Traditional_vs_Secular'].iloc[3] +
    sorted_data_mse_traditional['MSE_Traditional_vs_Secular'].iloc[4]
) / 2

benchmark_mse_survival = (
    sorted_data_mse_survival['MSE_Survival_vs_SelfExpression'].iloc[3] +
    sorted_data_mse_survival['MSE_Survival_vs_SelfExpression'].iloc[4]
) / 2

# Helper function for colors
def get_colors(data, col, benchmark):
    return ['red' if x > benchmark else 'blue' for x in data[col]]

# Create the figure
def create_figure():
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=[
            "MSE Traditional vs Secular Values",
            "MSE Survival vs Self-Expression Values"
        ],
        vertical_spacing=0.5,  # Increased spacing between subplots
        row_heights=[0.4, 0.4],
        specs=[[{"type": "xy"}], [{"type": "xy"}]]
    )

    # Plot for MSE Traditional vs Secular
    colors_traditional = get_colors(sorted_data_mse_traditional, 'MSE_Traditional_vs_Secular', benchmark_mse_traditional)
    fig.add_trace(go.Scatter(
        x=sorted_data_mse_traditional['MSE_Traditional_vs_Secular'],
        y=sorted_data_mse_traditional['Cultural_Region'],
        mode='markers+lines',
        marker=dict(size=8, color=colors_traditional),
        line=dict(color='grey', width=1),
        name="MSE Traditional vs Secular"
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=[benchmark_mse_traditional] * len(sorted_data_mse_traditional),
        y=sorted_data_mse_traditional['Cultural_Region'],
        mode='lines',
        line=dict(color='black', width=2, dash='dash'),
        name="Benchmark (Traditional vs Secular)"
    ), row=1, col=1)

    # Plot for MSE Survival vs Self-Expression
    colors_survival = get_colors(sorted_data_mse_survival, 'MSE_Survival_vs_SelfExpression', benchmark_mse_survival)
    fig.add_trace(go.Scatter(
        x=sorted_data_mse_survival['MSE_Survival_vs_SelfExpression'],
        y=sorted_data_mse_survival['Cultural_Region'],
        mode='markers+lines',
        marker=dict(size=8, color=colors_survival),
        line=dict(color='grey', width=1),
        name="MSE Survival vs Self-Expression"
    ), row=2, col=1)

    fig.add_trace(go.Scatter(
        x=[benchmark_mse_survival] * len(sorted_data_mse_survival),
        y=sorted_data_mse_survival['Cultural_Region'],
        mode='lines',
        line=dict(color='black', width=2, dash='dash'),
        name="Benchmark (Survival vs Self-Expression)"
    ), row=2, col=1)

    # Add description as annotation between plots
    fig.add_annotation(
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        text=(
            "<b>Summary and Insights:</b><br>"
            "1. The Confucian region shows the <b>highest discrepancy</b> in both indices.<br>"
            "2. Regions with <b>higher MSE (red)</b> indicate larger deviations between ChatGPT and survey data.<br>"
            "3. Benchmarks:<br>"
            "   - Traditional vs Secular: ~0.4<br>"
            "   - Survival vs Self-Expression: ~0.6<br>"
            "4. Protestant Europe and Latin America also exceed benchmarks."
        ),
        align="center",
        font=dict(size=16, color="black"),
        bgcolor="#f8f8f8",
        bordercolor="black",
        borderwidth=1,
        borderpad=20
    )

    # Update layout
    fig.update_layout(
        title="Mean Square Error (MSE) Comparison by Cultural Region",
        xaxis_title="Mean Square Error",
        yaxis_title="Cultural Region",
        template="plotly_white",
        height=950,
        width=1400,
        showlegend=False
    )

    return fig

# App Layout
app.layout = html.Div(
    style={'background-color': '#2d00f7', 'color': '#ffffff', 'padding': '30px', 'min-height': '100vh'},
    children=[
        # Title Section
        html.H1(
            "Mean Square Error (MSE) Analysis by Cultural Region",
            style={
                'text-align': 'center',
                'font-family': 'Arial, sans-serif',
                'margin-bottom': '20px',
                'padding': '10px',
                'border-radius': '10px',
                'background-color': '#2d00f7',
                'color': '#ffffff',
            }
        ),

        # Description Section
        html.Div(
            children=[
                html.P(
                    "This dashboard compares Mean Square Errors (MSE) of two cultural indices between ChatGPT's simulated responses "
                    "and original survey data for cultural regions. The interactive table below lists countries "
                    "for each cultural region.",
                    style={'font-size': '16px', 'font-weight': 'bold'}
                ),
                   html.Ul([
                    html.Li("Data covers 107 countries/territories that belong to 8 regions as in Inglehart R. (2005)."),
                    html.Li("Original survey data by Haerpfer et al.(2022).")
                ]),
                    html.P(
                    "The plots below provide insights into discrepancies in cultural indices. Benchmarks help identify "
                    "regions with significant deviations.",
                    style={'font-size': '14px', 'font-style': 'italic'}
                )
            ],
            style={
                'margin': '20px auto',
                'max-width': '900px',
                'background-color': '#ffffff',
                'padding': '20px',
                'border-radius': '10px',
                'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)',
                'font-family': 'Arial, sans-serif',
                'color': '#2d00f7',
            }
        ),

        # Graph Section
        html.Div(
            dcc.Graph(id='mse-graph', figure=create_figure()),
            style={
                'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.5)',
                'border-radius': '10px',
            }
        ),

        # Interactive Table Section
        html.Div(
            children=[
                html.H3("Explore Countries by Cultural Region", style={'text-align': 'left', 'font-weight': 'bold'}),
                html.P(
                    "Use the table below to view countries grouped by their cultural regions. ",
                    style={'font-size': '16px'}
                ),
                dash_table.DataTable(
                    id='region-table',
                    columns=[
                        {"name": "Region", "id": "Region"},
                        {"name": "Countries", "id": "Countries"}
                    ],
                    data=cultural_regions_df.to_dict('records'),
                    style_table={'overflowX': 'auto'},
                    style_cell={
                        'textAlign': 'left',
                        'padding': '10px',
                        'font-family': 'Arial, sans-serif',
                        'font-size': '14px'
                    },
                    style_header={
                        'backgroundColor': '#2d00f7',
                        'fontWeight': 'bold',
                        'color': 'white',
                        'textAlign': 'center'
                    },
                    style_data={'backgroundColor': '#2d00f7', 'color': '#ffffff'},
                    page_size=8  # Number of rows per page
                )
            ],
            style={
                'margin-top': '30px',
                'padding': '20px',
                'background-color': '#2d00f7',
                'border-radius': '10px',
                'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)',
                'font-family': 'Arial, sans-serif',
                'color': '#ffffff',
            }
        ),

        # References Section
        html.Div(
            children=[
                html.H3("References", style={'text-align': 'left', 'font-weight': 'bold'}),
                html.Ul([
                    html.Li(
                        "Haerpfer, C., Inglehart, R., Moreno, A., Welzel, C., Kizilova, K., Diez-Medrano J., "
                        "M. Lagos, P. Norris, E. Ponarin & B. Puranen (eds.). 2022. World Values Survey: Round Seven - "
                        "Country-Pooled Datafile Version 5.0. Madrid, Spain & Vienna, Austria: JD Systems Institute & WVSA "
                        "Secretariat. DOI: 10.14281/18241.24"
                    ),
                    html.Li(
                        "Inglehart R., Welzel C. (2005). Modernization, cultural change, and democracy: the human development "
                        "sequence. Vol. 333. Cambridge University Press."
                    )
                ])
            ],
            style={
                'margin-top': '20px',
                'padding': '10px',
                'background-color': '#2d00f7',
                'border-radius': '10px',
                'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)',
                'font-family': 'Arial, sans-serif',
                'color': '#ffffff',
            }
        )
    ]
)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8050)
