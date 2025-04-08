import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np

# Initialize the Dash app with Bootstrap styling
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Cross-Modal Plasticity Visualization", className="text-center my-4"),
            html.P("Interactive visualization of neural pathways between auditory and visual cortices", 
                   className="text-center mb-4"),
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("3D Brain Visualization"),
                dbc.CardBody([
                    dcc.Graph(id='brain-3d-model', style={'height': '600px'})
                ])
            ])
        ], width=8),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Controls"),
                dbc.CardBody([
                    html.H5("Brain Region Selection"),
                    dbc.Checklist(
                        id="region-checklist",
                        options=[
                            {"label": "Visual Cortex (V1)", "value": "v1"},
                            {"label": "Secondary Visual Areas", "value": "v2-v5"},
                            {"label": "Auditory Cortex (A1)", "value": "a1"},
                            {"label": "Secondary Auditory Areas", "value": "a2"},
                            {"label": "Association Areas", "value": "association"},
                            {"label": "Thalamus", "value": "thalamus"},
                        ],
                        value=["v1", "a1"],
                        inline=False,
                    ),
                    html.Hr(),
                    html.H5("Neural Pathway Visualization"),
                    dbc.RadioItems(
                        id="pathway-radio",
                        options=[
                            {"label": "Normal State", "value": "normal"},
                            {"label": "Early Adaptation", "value": "early"},
                            {"label": "Established Connections", "value": "established"},
                            {"label": "Advanced Rewiring", "value": "advanced"},
                        ],
                        value="normal",
                        inline=False,
                    ),
                    html.Hr(),
                    html.H5("Activation Simulation"),
                    dbc.Button("Simulate Activation", id="simulate-btn", color="primary", className="mr-2"),
                    dbc.Button("Reset", id="reset-btn", color="secondary"),
                ])
            ]),
            dbc.Card([
                dbc.CardHeader("Information"),
                dbc.CardBody([
                    html.Div(id="info-panel", children=[
                        html.H5("Cross-Modal Plasticity"),
                        html.P("Select brain regions and neural pathways to visualize how auditory stimuli can activate the visual cortex in blind individuals.")
                    ])
                ])
            ], className="mt-3")
        ], width=4)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Auditory-Visual Mapping"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H5("Auditory Parameters"),
                            dbc.Label("Base Frequency (f0)"),
                            dcc.Slider(
                                id="f0-slider",
                                min=220,
                                max=880,
                                step=20,
                                value=440,
                                marks={220: '220Hz', 440: '440Hz', 880: '880Hz'},
                            ),
                            dbc.Label("Depth Factor (α)"),
                            dcc.Slider(
                                id="alpha-slider",
                                min=0.1,
                                max=2.0,
                                step=0.1,
                                value=1.0,
                                marks={0.1: '0.1', 1.0: '1.0', 2.0: '2.0'},
                            ),
                            dbc.Label("Angular Factor (β)"),
                            dcc.Slider(
                                id="beta-slider",
                                min=0.1,
                                max=2.0,
                                step=0.1,
                                value=1.0,
                                marks={0.1: '0.1', 1.0: '1.0', 2.0: '2.0'},
                            ),
                        ], width=6),
                        dbc.Col([
                            html.H5("Encoding Strategy"),
                            dbc.RadioItems(
                                id="encoding-radio",
                                options=[
                                    {"label": "Spatial-Frequency", "value": "spatial-freq"},
                                    {"label": "Frequency-Amplitude", "value": "freq-amp"},
                                    {"label": "Temporal Pattern", "value": "temporal"},
                                    {"label": "Spectral Contour", "value": "spectral"},
                                    {"label": "Hybrid", "value": "hybrid"},
                                ],
                                value="spatial-freq",
                                inline=False,
                            ),
                        ], width=6)
                    ])
                ])
            ])
        ], width=12, className="mt-3")
    ])
], fluid=True)

# Create a simple 3D brain model for initial setup
def generate_brain_model():
    # Create a simple ellipsoid for the brain
    u = np.linspace(0, 2*np.pi, 20)
    v = np.linspace(0, np.pi, 20)
    x = 50 * np.outer(np.cos(u), np.sin(v))
    y = 65 * np.outer(np.sin(u), np.sin(v))
    z = 50 * np.outer(np.ones(np.size(u)), np.cos(v))
    
    # Create the brain surface
    brain = go.Surface(
        x=x, y=y, z=z,
        colorscale='Greys',
        opacity=0.7,
        showscale=False
    )
    
    # Create a simple visual cortex region (back of brain)
    vc_x = []
    vc_y = []
    vc_z = []
    for i in range(10):
        for j in range(10):
            vc_x.append(-40 + i*2)
            vc_y.append(-30 + j*2)
            vc_z.append(-20)
    
    visual_cortex = go.Scatter3d(
        x=vc_x, y=vc_y, z=vc_z,
        mode='markers',
        marker=dict(
            size=5,
            color='red',
            opacity=0.8
        ),
        name='Visual Cortex'
    )
    
    # Create a simple auditory cortex region (sides of brain)
    ac_x = []
    ac_y = []
    ac_z = []
    for i in range(10):
        for j in range(10):
            ac_x.append(0 + i*2)
            ac_y.append(50)
            ac_z.append(-10 + j*2)
    
    auditory_cortex = go.Scatter3d(
        x=ac_x, y=ac_y, z=ac_z,
        mode='markers',
        marker=dict(
            size=5,
            color='blue',
            opacity=0.8
        ),
        name='Auditory Cortex'
    )
    
    # Create a simple neural pathway between regions
    path_x = []
    path_y = []
    path_z = []
    
    # Create a curved path between auditory and visual cortex
    for t in np.linspace(0, 1, 20):
        path_x.append(10 + t*(-40 - 10))
        path_y.append(50 - t*(50 + 30))
        path_z.append(-10 + 20*np.sin(t*np.pi))
    
    neural_pathway = go.Scatter3d(
        x=path_x, y=path_y, z=path_z,
        mode='lines',
        line=dict(
            color='green',
            width=5
        ),
        name='Neural Pathway'
    )
    
    # Combine all elements
    data = [brain, visual_cortex, auditory_cortex, neural_pathway]
    
    # Set up the layout
    layout = go.Layout(
        scene=dict(
            xaxis=dict(title='', showticklabels=False),
            yaxis=dict(title='', showticklabels=False),
            zaxis=dict(title='', showticklabels=False),
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        margin=dict(l=0, r=0, b=0, t=0)
    )
    
    return {'data': data, 'layout': layout}

# Callback to update the 3D brain model
@app.callback(
    dash.dependencies.Output('brain-3d-model', 'figure'),
    [dash.dependencies.Input('region-checklist', 'value'),
     dash.dependencies.Input('pathway-radio', 'value'),
     dash.dependencies.Input('simulate-btn', 'n_clicks')]
)
def update_brain_model(selected_regions, pathway_state, n_clicks):
    # For now, just return the basic brain model
    # This will be expanded in the implementation phase
    return generate_brain_model()

# Callback to update the information panel
@app.callback(
    dash.dependencies.Output('info-panel', 'children'),
    [dash.dependencies.Input('region-checklist', 'value'),
     dash.dependencies.Input('pathway-radio', 'value')]
)
def update_info_panel(selected_regions, pathway_state):
    # This will be expanded in the implementation phase
    if 'v1' in selected_regions and 'a1' in selected_regions:
        return [
            html.H5("Visual and Auditory Cortices"),
            html.P("The visual cortex processes visual information, while the auditory cortex processes sound. In blind individuals, cross-modal plasticity allows auditory information to activate the visual cortex.")
        ]
    elif 'v1' in selected_regions:
        return [
            html.H5("Visual Cortex"),
            html.P("The visual cortex is located in the occipital lobe at the back of the brain. It processes visual information received from the eyes.")
        ]
    elif 'a1' in selected_regions:
        return [
            html.H5("Auditory Cortex"),
            html.P("The auditory cortex is located in the temporal lobe. It processes sound information received from the ears.")
        ]
    else:
        return [
            html.H5("Cross-Modal Plasticity"),
            html.P("Select brain regions to learn more about how auditory stimuli can activate the visual cortex in blind individuals.")
        ]

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
