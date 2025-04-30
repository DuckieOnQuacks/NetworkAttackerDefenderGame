# Standard library imports
import os
import sys
import string

# Third-party imports
import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import plotly.graph_objects as go
import numpy as np

# Local imports
from game import Game

# Load Cytoscape preset layouts
cyto.load_extra_layouts()

class DashVisualizer:
    """
    A Dash-based visualization for the Network Attacker-Defender game.
    
    This class provides an interactive web interface for running and visualizing
    the network security game simulation.
    """
    
    def __init__(self, game=None, auto_run=False):
        """Initialize the network visualizer with a game instance.
        
        Args:
            game (Game, optional): Initial game instance. Defaults to None.
            auto_run (bool, optional): Whether to automatically run the simulation. Defaults to False.
        """
        self.game = game
        self.auto_run = auto_run
        self.game_history = []
        self.simulation_running = False
        self.simulation_complete = False
        
        # Create Dash app
        self.app = dash.Dash(
            __name__, 
            external_stylesheets=[dbc.themes.FLATLY],
            suppress_callback_exceptions=True
        )
        
        # Initialize layout and callbacks
        self.setup_layout()
        self.setup_callbacks()
        
        # If a game is provided, initialize the state
        if self.game:
            self.save_game_state()
    
    def setup_layout(self):
        """Set up the Dash app layout."""
        # Define custom styles
        cyto_stylesheet = [
            # Node styles
            {
                'selector': 'node',
                'style': {
                    'label': 'data(label)',
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'font-size': '14px',
                    'font-weight': 'bold',
                    'color': 'white',
                    'text-outline-width': 2,
                    'text-outline-opacity': 0.8,
                    'background-opacity': 0.9,
                    'border-width': 2,
                    'z-index': 10
                }
            },
            {
                'selector': '.attacker',
                'style': {
                    'background-color': '#e74c3c',
                    'text-outline-color': '#c0392b',
                    'border-color': '#c0392b',
                    'shape': 'star'
                }
            },
            {
                'selector': '.defender',
                'style': {
                    'background-color': '#27ae60',
                    'text-outline-color': '#219653',
                    'border-color': '#219653',
                    'shape': 'diamond'
                }
            },
            {
                'selector': '.server',
                'style': {
                    'background-color': '#3498db',
                    'text-outline-color': '#2980b9',
                    'border-color': '#2980b9',
                    'shape': 'ellipse'
                }
            },
            {
                'selector': '.bot',
                'style': {
                    'background-color': '#f39c12',
                    'text-outline-color': '#d35400',
                    'border-color': '#d35400',
                    'shape': 'round-rectangle'
                }
            },
            # Edge styles
            {
                'selector': 'edge',
                'style': {
                    'width': 2,
                    'curve-style': 'bezier',
                    'line-color': '#95a5a6',
                    'opacity': 0.8,
                    'z-index': 1
                }
            },
            {
                'selector': '.control-edge',
                'style': {
                    'line-color': '#7f8c8d',
                    'opacity': 0.6,
                    'line-style': 'dashed'
                }
            },
            {
                'selector': '.defense-edge',
                'style': {
                    'line-color': '#27ae60',
                    'opacity': 0.7,
                    'line-style': 'solid'
                }
            },
            {
                'selector': '.attack-edge',
                'style': {
                    'line-color': '#e74c3c',
                    'target-arrow-color': '#e74c3c',
                    'target-arrow-shape': 'triangle',
                    'arrow-scale': 1.5,
                    'line-style': 'solid'
                }
            },
            # Change label styles
            {
                'selector': '.change_label',
                'style': {
                    'label': 'data(label)',
                    'text-valign': 'bottom',
                    'text-halign': 'center',
                    'font-size': '16px',
                    'font-weight': 'bold',
                    'text-outline-width': 2,
                    'text-outline-color': 'white',
                    'text-outline-opacity': 0.8,
                    'background-opacity': 0,
                    'border-width': 0,
                    'z-index': 20
                }
            }
        ]
        
        # Initial elements
        initial_elements = self.game_history[0]['elements'] if self.game_history else []
        
        # Create layout
        self.app.layout = dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H1("Network Attacker-Defender Simulation", 
                            className="mt-4 mb-4 text-center text-primary")
                ])
            ]),
            
            # Add file selection dropdown
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Label("Select Game Template:"),
                        dcc.Dropdown(
                            id="file-dropdown",
                            options=[
                                {"label": "Fair Game", "value": "templates/fair_game.txt"},
                                {"label": "High Stakes", "value": "templates/high_stakes.txt"},
                                {"label": "Extreme Scenario", "value": "templates/extreme_scenario.txt"},
                                {"label": "Attacker Advantage", "value": "templates/attacker_advantage.txt"},
                                {"label": "Defender Advantage", "value": "templates/defender_advantage.txt"},
                                {"label": "Test Scenario", "value": "templates/test4.txt"},
                                {"label": "Manual Configuration", "value": "manual"}
                            ],
                            value="templates/fair_game.txt",
                            clearable=False,
                            className="mb-3",
                            style={'width': '400px'}
                        ),
                        html.Button(
                            "Load Game", 
                            id="load-game-button", 
                            className="btn btn-info mb-4"
                        ),
                        
                        # Manual configuration inputs
                        html.Div(id="manual-config", style={'display': 'none'}, children=[
                            html.H5("Manual Configuration", className="mt-4 mb-3"),
                            dbc.Row([
                                dbc.Col([
                                    html.H6("Attacker Settings", className="text-danger"),
                                    dbc.InputGroup([
                                        dbc.InputGroupText("Initial Currency"),
                                        dbc.Input(id="attacker-currency-input", type="number", value=100000)
                                    ], className="mb-2"),
                                    dbc.InputGroup([
                                        dbc.InputGroupText("Initial Bots"),
                                        dbc.Input(id="attacker-bots-input", type="number", value=0)
                                    ], className="mb-2"),
                                    dbc.InputGroup([
                                        dbc.InputGroupText("Bot Bandwidth"),
                                        dbc.Input(id="attacker-bandwidth-input", type="number", value=100)
                                    ], className="mb-2"),
                                    dbc.InputGroup([
                                        dbc.InputGroupText("Bot Cost"),
                                        dbc.Input(id="bot-cost-input", type="number", value=5)
                                    ], className="mb-2")
                                ], width=6),
                                dbc.Col([
                                    html.H6("Defender Settings", className="text-primary"),
                                    dbc.InputGroup([
                                        dbc.InputGroupText("Initial Currency"),
                                        dbc.Input(id="defender-currency-input", type="number", value=100000)
                                    ], className="mb-2"),
                                    dbc.InputGroup([
                                        dbc.InputGroupText("Initial Servers"),
                                        dbc.Input(id="defender-servers-input", type="number", value=2)
                                    ], className="mb-2"),
                                    dbc.InputGroup([
                                        dbc.InputGroupText("Server Income"),
                                        dbc.Input(id="server-income-input", type="number", value=100000)
                                    ], className="mb-2"),
                                    dbc.InputGroup([
                                        dbc.InputGroupText("Firewall Strength"),
                                        dbc.Input(id="firewall-input", type="number", value=0.1, step=0.1)
                                    ], className="mb-2")
                                ], width=6)
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    html.H6("Game Settings", className="text-info"),
                                    dbc.InputGroup([
                                        dbc.InputGroupText("Energy"),
                                        dbc.Input(id="energy-input", type="number", value=100)
                                    ], className="mb-2"),
                                    dbc.InputGroup([
                                        dbc.InputGroupText("Good Traffic"),
                                        dbc.Input(id="good-traffic-input", type="number", value=1.0, step=0.1)
                                    ], className="mb-2"),
                                    dbc.InputGroup([
                                        dbc.InputGroupText("Server Cost"),
                                        dbc.Input(id="server-cost-input", type="number", value=100)
                                    ], className="mb-2"),
                                    dbc.InputGroup([
                                        dbc.InputGroupText("Energy Cost"),
                                        dbc.Input(id="energy-cost-input", type="number", value=30)
                                    ], className="mb-2"),
                                    dbc.InputGroup([
                                        dbc.InputGroupText("Firewall Cost"),
                                        dbc.Input(id="firewall-cost-input", type="number", value=1000000)
                                    ], className="mb-2"),
                                    dbc.InputGroup([
                                        dbc.InputGroupText("Server Energy Cost"),
                                        dbc.Input(id="server-energy-cost-input", type="number", value=1000)
                                    ], className="mb-2")
                                ], width=12)
                            ]),
                            html.Button(
                                "Apply Manual Configuration", 
                                id="apply-manual-button", 
                                className="btn btn-success mt-3"
                            )
                        ])
                    ], className="d-flex flex-column align-items-center")
                ], width=12)
            ]),
            
            dbc.Row([
                dbc.Col([
                    # Main network visualization
                    cyto.Cytoscape(
                        id='network-graph',
                        layout={'name': 'preset'},
                        style={'width': '100%', 'height': '600px', 'background': '#f8f9fa'},
                        elements=initial_elements,
                        stylesheet=cyto_stylesheet,
                        minZoom=0.5,
                        maxZoom=2
                    )
                ], width=8),
                
                dbc.Col([
                    # Control panel and information display
                    dbc.Card([
                        dbc.CardHeader(html.H4("Game Status", className="text-center")),
                        dbc.CardBody([
                            html.Div([
                                html.H5("Round: ", className="d-inline"),
                                html.H5(id="round-display", className="d-inline text-primary")
                            ]),
                            
                            html.Hr(),
                            
                            # Currency info
                            html.Div([
                                html.H5("Attacker", className="text-danger"),
                                html.Div([
                                    html.Strong("Currency: "),
                                    html.Span(id="attacker-currency")
                                ]),
                                html.Div([
                                    html.Strong("Bots: "),
                                    html.Span(id="attacker-bots")
                                ]),
                                html.Div([
                                    html.Strong("Bandwidth: "),
                                    html.Span(id="attacker-bandwidth")
                                ])
                            ], className="mb-3"),
                            
                            html.Div([
                                html.H5("Defender", className="text-primary"),
                                html.Div([
                                    html.Strong("Currency: "),
                                    html.Span(id="defender-currency")
                                ]),
                                html.Div([
                                    html.Strong("Servers: "),
                                    html.Span(id="defender-servers")
                                ]),
                                html.Div([
                                    html.Strong("Income per server: "),
                                    html.Span(id="defender-income")
                                ]),
                                html.Div([
                                    html.Strong("Firewall strength: "),
                                    html.Span(id="defender-firewall")
                                ])
                            ], className="mb-3"),
                            
                            html.Hr(),
                            
                            # Game controls
                            html.Div([
                                html.Button("Run Simulation", 
                                           id="run-button", 
                                           className="btn btn-success me-2"),
                                html.Button("Reset", 
                                           id="reset-button", 
                                           className="btn btn-secondary me-2"),
                                html.Button("Play/Pause", 
                                           id="play-pause-button", 
                                           className="btn btn-primary")
                            ], className="d-flex justify-content-center mb-3"),
                            
                            # Simulation speed control
                            html.Div([
                                html.Label("Simulation Speed:"),
                                dcc.Slider(
                                    id="speed-slider",
                                    min=0.5,
                                    max=3,
                                    step=0.5,
                                    value=1.5,
                                    marks={
                                        0.5: 'Slow',
                                        1.5: 'Normal',
                                        3: 'Fast'
                                    },
                                    tooltip={"placement": "bottom", "always_visible": True}
                                )
                            ], className="mt-3"),
                            
                            # Simulation status message
                            html.Div([
                                html.P(id="simulation-status", className="text-center mt-3")
                            ])
                        ])
                    ], className="h-100")
                ], width=4)
            ]),
            
            dbc.Row([
                dbc.Col([
                    # Currency trend chart
                    dcc.Graph(id="currency-chart", style={'height': '300px'})
                ], width=12, className="mt-4")
            ]),
            
            # Store component to track app state
            dcc.Store(id="simulation-state", data={
                "is_running": False,
                "is_complete": False,
                "current_round": 0
            }),
            
            # Interval component for automatic simulation steps
            dcc.Interval(
                id='simulation-interval',
                interval=1500,  # 1.5 seconds default
                disabled=True
            ),
            
            # Footer
            dbc.Row([
                dbc.Col([
                    html.Hr(),
                    html.P("Network Attacker-Defender Simulation Dashboard", 
                           className="text-center text-muted")
                ], width=12, className="mt-3 mb-3")
            ])
            
        ], fluid=True, className="px-4")
    
    def setup_callbacks(self):
        """Set up Dash callbacks for interactivity."""
        
        # Callback to show/hide manual configuration
        @self.app.callback(
            Output("manual-config", "style"),
            Input("file-dropdown", "value")
        )
        def toggle_manual_config(selected_value):
            return {'display': 'block' if selected_value == 'manual' else 'none'}
        
        # Callback to load a game from a selected file or manual configuration
        @self.app.callback(
            Output("simulation-state", "data", allow_duplicate=True),
            [Input("load-game-button", "n_clicks"),
             Input("apply-manual-button", "n_clicks")],
            [State("file-dropdown", "value"),
             State("simulation-state", "data"),
             State("attacker-currency-input", "value"),
             State("attacker-bots-input", "value"),
             State("attacker-bandwidth-input", "value"),
             State("bot-cost-input", "value"),
             State("defender-currency-input", "value"),
             State("defender-servers-input", "value"),
             State("server-income-input", "value"),
             State("firewall-input", "value"),
             State("energy-input", "value"),
             State("good-traffic-input", "value"),
             State("server-cost-input", "value"),
             State("energy-cost-input", "value"),
             State("firewall-cost-input", "value"),
             State("server-energy-cost-input", "value")],
            prevent_initial_call='initial_duplicate'
        )
        def load_selected_game(load_clicks, apply_clicks, filepath, sim_state, 
                             attacker_currency, attacker_bots, attacker_bandwidth, bot_cost,
                             defender_currency, defender_servers, server_income, firewall,
                             energy, good_traffic, server_cost, energy_cost, firewall_cost, server_energy_cost):
            ctx = dash.callback_context
            trigger_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None
            
            if trigger_id == "apply-manual-button" and filepath == "manual":
                # Create game from manual configuration
                self.game = Game(
                    attacker_currency, defender_currency, energy, defender_servers, server_income,
                    good_traffic, attacker_bots, attacker_bandwidth, firewall,
                    server_cost, energy_cost, bot_cost, firewall_cost, server_energy_cost
                )
                # Reset game history
                self.game_history = []
                self.simulation_running = False
                self.simulation_complete = False
                # Save initial state
                self.save_game_state()
                return {
                    "is_running": False,
                    "is_complete": False,
                    "current_round": 0,
                    "last_loaded": "manual",
                    "last_action": "load",
                    "force_update": True  # Add this to force UI update
                }
            else:
                # Handle file loading as before
                if filepath and filepath != "manual":
                    try:
                        self.load_game(filepath)
                        return {
                            "is_running": False,
                            "is_complete": False,
                            "current_round": 0,
                            "last_loaded": filepath,
                            "last_action": "load",
                            "force_update": True  # Add this to force UI update
                        }
                    except Exception as e:
                        return {
                            "is_running": False,
                            "is_complete": False,
                            "current_round": 0,
                            "error": str(e),
                            "last_action": "error",
                            "force_update": True  # Add this to force UI update
                        }
            
            return sim_state
        
        # Callback to update simulation speed
        @self.app.callback(
            Output("simulation-interval", "interval"),
            Input("speed-slider", "value")
        )
        def update_interval(speed_value):
            # Convert speed to interval in milliseconds (inverse relationship)
            # Fast (3) = 500ms, Normal (1.5) = 1000ms, Slow (0.5) = 3000ms
            return int(3000 / speed_value)
        
        # Callback to handle simulation steps and display updates
        @self.app.callback(
            [Output("network-graph", "elements"),
             Output("round-display", "children"),
             Output("attacker-currency", "children"),
             Output("defender-currency", "children"),
             Output("attacker-bots", "children"),
             Output("attacker-bandwidth", "children"),
             Output("defender-servers", "children"),
             Output("defender-income", "children"),
             Output("defender-firewall", "children"),
             Output("currency-chart", "figure"),
             Output("simulation-status", "children"),
             Output("simulation-state", "data", allow_duplicate=True)],
            [Input("simulation-interval", "n_intervals"),
             Input("run-button", "n_clicks"),
             Input("reset-button", "n_clicks"),
             Input("play-pause-button", "n_clicks"),
             Input("load-game-button", "n_clicks"),
             Input("apply-manual-button", "n_clicks")],
            [State("simulation-state", "data"),
             State("file-dropdown", "value")],
            prevent_initial_call='initial_duplicate'
        )
        def update_simulation(interval_ticks, run_clicks, reset_clicks, play_pause_clicks, load_clicks, apply_clicks, sim_state, selected_file):
            # Determine which input triggered the callback
            ctx = dash.callback_context
            trigger_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None
            
            # Check if a game is loaded
            if self.game is None:
                # If load button was clicked but still no game, show error
                if trigger_id == "load-game-button" or trigger_id == "apply-manual-button":
                    empty_fig = go.Figure()
                    empty_fig.update_layout(
                        title="No data available - please load a game",
                        template="plotly_white"
                    )
                    status_message = "Error loading game template. Please try another."
                    if "error" in sim_state:
                        status_message = f"Error loading game: {sim_state['error']}"
                    
                    return (
                        [],  # Empty network
                        "No game loaded",  # Round display
                        "$0",  # Attacker currency
                        "$0",  # Defender currency
                        "0",  # Attacker bots
                        "0",  # Attacker bandwidth
                        "0",  # Defender servers
                        "$0",  # Defender income
                        "0",  # Defender firewall
                        empty_fig,  # Currency chart
                        status_message,  # Status message
                        sim_state  # State unchanged
                    )
                else:
                    # If no game is loaded and not trying to load one, show message
                    empty_fig = go.Figure()
                    empty_fig.update_layout(
                        title="No data available - please load a game",
                        template="plotly_white"
                    )
                    return (
                        [],  # Empty network
                        "No game loaded",  # Round display
                        "$0",  # Attacker currency
                        "$0",  # Defender currency
                        "0",  # Attacker bots
                        "0",  # Attacker bandwidth
                        "0",  # Defender servers
                        "$0",  # Defender income
                        "0",  # Defender firewall
                        empty_fig,  # Currency chart
                        "Please select a game template and click 'Load Game'",  # Status message
                        sim_state  # State unchanged
                    )
            
            # Handle reset button click
            if trigger_id == "reset-button":
                # Reset game to initial state
                if len(self.game_history) > 0:
                    self.game_history = self.game_history[:1]  # Keep only initial state
                sim_state = {
                    "is_running": False,
                    "is_complete": False,
                    "current_round": 0
                }
                status_message = "Simulation reset. Press 'Run Simulation' to start."
                
                # If we have no history at all, reload the game
                if len(self.game_history) == 0 and selected_file:
                    try:
                        self.load_game(selected_file)
                        status_message = f"Reloaded game from {selected_file}. Ready to start simulation."
                    except Exception as e:
                        status_message = f"Error reloading game: {str(e)}"
                
                if len(self.game_history) > 0:
                    current_state = self.game_history[0]
                    return (
                        current_state["elements"],
                        f"{current_state['round']}",
                        f"${current_state['attacker_currency']:,}",
                        f"${current_state['defender_currency']:,}",
                        f"{current_state['num_bots']}",
                        f"{current_state['bot_band']}",
                        f"{current_state['num_servers']}",
                        f"${current_state['server_income']:,}",
                        f"{current_state['firewall']}",
                        self.create_currency_chart(),
                        status_message,
                        sim_state
                    )
            
            # Handle run button click
            if trigger_id == "run-button":
                sim_state["is_running"] = True
                sim_state["is_complete"] = False
                status_message = "Simulation running..."
                
                # If auto_run is set or this is first click, we might want to initialize simulation
                if len(self.game_history) <= 1:
                    self.advance_simulation()  # Run first step
            
            # Handle play/pause button click
            if trigger_id == "play-pause-button":
                sim_state["is_running"] = not sim_state["is_running"]
                status_message = "Simulation running..." if sim_state["is_running"] else "Simulation paused"
            
            # Handle interval ticks (simulation steps)
            if trigger_id == "simulation-interval" and sim_state["is_running"] and not sim_state["is_complete"]:
                # Advance simulation by one step
                simulation_continues = self.advance_simulation()
                
                if not simulation_continues:
                    sim_state["is_running"] = False
                    sim_state["is_complete"] = True
                    status_message = "Simulation complete! One player has run out of currency."
                else:
                    status_message = f"Simulation running... Round {self.game.rounds}"
                
                sim_state["current_round"] = len(self.game_history) - 1
            
            # Get current state to display
            current_idx = min(sim_state["current_round"], len(self.game_history) - 1)
            if not self.game_history and not sim_state.get("force_update"):
                return dash.no_update
            
            current_state = self.game_history[current_idx] if self.game_history else None
            
            # Create currency chart
            currency_fig = self.create_currency_chart(highlight_round=current_idx)
            
            # Default status message if not set
            if 'status_message' not in locals():
                if sim_state.get("last_action") == "load":
                    status_message = f"Loaded game from {sim_state.get('last_loaded')}. Ready to start simulation."
                elif sim_state.get("last_action") == "error":
                    status_message = f"Error loading game: {sim_state.get('error')}"
                elif sim_state["is_complete"]:
                    status_message = "Simulation complete! One player has run out of currency."
                elif sim_state["is_running"]:
                    status_message = f"Simulation running... Round {current_state['round']}"
                else:
                    status_message = "Simulation paused"
            
            # If we have a current state, use it for the display
            if current_state:
                return (
                    current_state["elements"],
                    f"{current_state['round']}",
                    f"${current_state['attacker_currency']:,}",
                    f"${current_state['defender_currency']:,}",
                    f"{current_state['num_bots']}",
                    f"{current_state['bot_band']}",
                    f"{current_state['num_servers']}",
                    f"${current_state['server_income']:,}",
                    f"{current_state['firewall']}",
                    currency_fig,
                    status_message,
                    {**sim_state, "force_update": False}  # Reset force_update flag
                )
            else:
                # If no current state but force_update is true, return empty state
                return (
                    [],  # Empty network
                    "0",  # Round display
                    "$0",  # Attacker currency
                    "$0",  # Defender currency
                    "0",  # Attacker bots
                    "0",  # Attacker bandwidth
                    "0",  # Defender servers
                    "$0",  # Defender income
                    "0",  # Defender firewall
                    currency_fig,
                    status_message,
                    {**sim_state, "force_update": False}  # Reset force_update flag
                )
        
        # Callback to control the interval component
        @self.app.callback(
            Output("simulation-interval", "disabled"),
            [Input("simulation-state", "data")]
        )
        def control_interval(sim_state):
            # Enable interval when simulation is running, disable otherwise
            return not sim_state["is_running"]
    
    # Game state management methods
    def save_game_state(self):
        """Save the current game state to history."""
        elements = self.create_cytoscape_elements()
        
        # Calculate money changes if we have previous state
        attacker_change = 0
        defender_change = 0
        if self.game_history:
            prev_state = self.game_history[-1]
            attacker_change = self.game.attacker.currency - prev_state['attacker_currency']
            defender_change = self.game.defender.currency - prev_state['defender_currency']
        
        # Create a state snapshot
        state = {
            'round': self.game.rounds,
            'attacker_currency': self.game.attacker.currency,
            'defender_currency': self.game.defender.currency,
            'attacker_change': attacker_change,
            'defender_change': defender_change,
            'num_bots': self.game.attacker.num_bots,
            'bot_band': self.game.attacker.total_bot_band,
            'num_servers': self.game.defender.servers,
            'server_income': self.game.defender.server_yield,
            'firewall': self.game.defender.firewall_type,
            'elements': elements
        }
        
        self.game_history.append(state)
    
    def advance_simulation(self):
        """Run a single round of simulation and save the state.
        
        Returns:
            bool: True if simulation can continue, False if game is over
        """
        if self.game.attacker.currency <= 0 or self.game.defender.currency <= 0:
            self.simulation_running = False
            self.simulation_complete = True
            return False
            
        self.game.run_game(auto_mode=True)
        self.save_game_state()
        return True
    
    def load_game(self, filepath):
        """Load a game from a configuration file.
        
        Args:
            filepath (str): Path to the game configuration file
            
        Returns:
            Game: The loaded game instance
        """
        self.game = load_game_from_file(filepath)
        self.game_history = []
        self.simulation_running = False
        self.simulation_complete = False
        self.save_game_state()
        return self.game
    
    # Visualization methods
    def get_node_positions(self):
        """Calculate positions for nodes in the visualization.
        
        Returns:
            dict: Dictionary mapping node IDs to their x,y positions
        """
        positions = {}
        
        if not self.game:
            return positions
        
        # Place attacker on the left
        positions['attacker'] = {'x': -300, 'y': 0}
        
        # Place servers in the center, slightly to the right
        server_count = self.game.defender.servers
        server_center_x = 100
        server_radius = 150
        
        for i in range(server_count):
            angle = np.pi/2 - (i * np.pi / max(1, server_count+0.5))
            positions[f'server_{i}'] = {
                'x': server_center_x + server_radius * np.cos(angle),
                'y': server_radius * np.sin(angle)
            }
        
        # Place defender on the right side of the servers
        rightmost_x = server_center_x + server_radius * 1.1
        positions['defender'] = {'x': rightmost_x + 200, 'y': 0}
        
        # Place bots in a vertical stack to the right of the attacker
        bot_count = max(1, self.game.attacker.num_bots)
        bot_spacing = 60
        bot_x_offset = 100
        
        for i in range(bot_count):
            y_position = ((bot_count - 1) / 2 - i) * bot_spacing
            positions[f'bot_{i}'] = {
                'x': positions['attacker']['x'] + bot_x_offset,
                'y': y_position
            }
        
        return positions
    
    def create_cytoscape_elements(self):
        """Create elements for Cytoscape visualization.
        
        Returns:
            list: List of node and edge elements for the visualization
        """
        elements = []
        
        if not self.game:
            return elements
            
        positions = self.get_node_positions()
        
        # Add attacker node
        attacker_size = 50 + min(50, self.game.attacker.currency / 5000)
        elements.append({
            'data': {
                'id': 'attacker',
                'label': 'ATTACKER',
                'currency': self.game.attacker.currency,
                'nodeType': 'attacker'
            },
            'position': positions['attacker'],
            'classes': 'attacker',
            'style': {
                'width': attacker_size,
                'height': attacker_size
            }
        })
        
        # Add attacker change label
        if len(self.game_history) > 1:
            change = self.game_history[-1]['attacker_change']
            if change != 0:
                elements.append({
                    'data': {
                        'id': 'attacker_change',
                        'label': f"{'+' if change >= 0 else ''}{change:,}",
                        'nodeType': 'change_label'
                    },
                    'position': {
                        'x': positions['attacker']['x'],
                        'y': positions['attacker']['y'] - attacker_size - 20
                    },
                    'classes': 'change_label attacker_change',
                    'style': {
                        'text-valign': 'bottom',
                        'text-halign': 'center',
                        'font-size': '16px',
                        'font-weight': 'bold',
                        'color': '#e74c3c' if change >= 0 else '#c0392b'
                    }
                })
        
        # Add defender node
        defender_size = 50 + min(50, self.game.defender.currency / 5000)
        elements.append({
            'data': {
                'id': 'defender',
                'label': 'DEFENDER',
                'currency': self.game.defender.currency,
                'nodeType': 'defender'
            },
            'position': positions['defender'],
            'classes': 'defender',
            'style': {
                'width': defender_size,
                'height': defender_size
            }
        })
        
        # Add defender change label
        if len(self.game_history) > 1:
            change = self.game_history[-1]['defender_change']
            if change != 0:
                elements.append({
                    'data': {
                        'id': 'defender_change',
                        'label': f"{'+' if change >= 0 else ''}{change:,}",
                        'nodeType': 'change_label'
                    },
                    'position': {
                        'x': positions['defender']['x'],
                        'y': positions['defender']['y'] - defender_size - 20
                    },
                    'classes': 'change_label defender_change',
                    'style': {
                        'text-valign': 'bottom',
                        'text-halign': 'center',
                        'font-size': '16px',
                        'font-weight': 'bold',
                        'color': '#27ae60' if change >= 0 else '#219653'
                    }
                })
        
        # Add server nodes
        for i in range(self.game.defender.servers):
            server_id = f'server_{i}'
            server_size = 40 + min(40, self.game.defender.server_yield / 5000)
            
            elements.append({
                'data': {
                    'id': server_id,
                    'label': f'Server {i}',
                    'income': self.game.defender.server_yield,
                    'firewall': self.game.defender.firewall_type,
                    'nodeType': 'server'
                },
                'position': positions[server_id],
                'classes': 'server',
                'style': {
                    'width': server_size,
                    'height': server_size
                }
            })
            
            # Add connection between defender and server
            elements.append({
                'data': {
                    'id': f'defender-{server_id}',
                    'source': 'defender',
                    'target': server_id,
                    'edgeType': 'defense'
                },
                'classes': 'defense-edge'
            })
        
        # Add bot nodes
        for i in range(max(1, self.game.attacker.num_bots)):
            bot_id = f'bot_{i}'
            bot_size = 30 + min(30, self.game.attacker.total_bot_band / 5)
            
            elements.append({
                'data': {
                    'id': bot_id,
                    'label': f'Bot {i}',
                    'bandwidth': self.game.attacker.total_bot_band,
                    'nodeType': 'bot'
                },
                'position': positions[bot_id],
                'classes': 'bot',
                'style': {
                    'width': bot_size,
                    'height': bot_size
                }
            })
            
            # Add edge from attacker to bot
            elements.append({
                'data': {
                    'id': f'attacker-{bot_id}',
                    'source': 'attacker',
                    'target': bot_id,
                    'edgeType': 'control'
                },
                'classes': 'control-edge'
            })
            
            # Add attack edges from bots to servers
            for j in range(self.game.defender.servers):
                server_id = f'server_{j}'
                edge_width = max(1, min(8, self.game.attacker.total_bot_band / 20))
                
                elements.append({
                    'data': {
                        'id': f'{bot_id}-{server_id}',
                        'source': bot_id,
                        'target': server_id,
                        'bandwidth': self.game.attacker.total_bot_band,
                        'firewall': self.game.defender.firewall_type,
                        'edgeType': 'attack'
                    },
                    'classes': 'attack-edge',
                    'style': {
                        'width': edge_width
                    }
                })
        
        return elements
    
    def create_currency_chart(self, highlight_round=None):
        """Create a currency trend chart with optional round highlighting.
        
        Args:
            highlight_round (int, optional): Round to highlight in the chart. Defaults to None.
            
        Returns:
            go.Figure: Plotly figure object for the currency chart
        """
        if not self.game_history:
            fig = go.Figure()
            fig.update_layout(
                title="Currency Trends",
                xaxis_title="Round",
                yaxis_title="Currency",
                template="plotly_white",
                margin=dict(l=0, r=0, t=40, b=0)
            )
            return fig
            
        rounds = [state["round"] for state in self.game_history]
        attacker_currency = [state["attacker_currency"] for state in self.game_history]
        defender_currency = [state["defender_currency"] for state in self.game_history]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=rounds,
            y=attacker_currency,
            mode="lines+markers",
            name="Attacker Currency",
            line=dict(color="#e74c3c", width=3),
            marker=dict(size=8)
        ))
        
        fig.add_trace(go.Scatter(
            x=rounds,
            y=defender_currency,
            mode="lines+markers",
            name="Defender Currency",
            line=dict(color="#3498db", width=3),
            marker=dict(size=8)
        ))
        
        if highlight_round is not None and highlight_round < len(rounds):
            fig.add_vline(
                x=rounds[highlight_round],
                line_width=2,
                line_dash="dash",
                line_color="#2c3e50",
                opacity=0.7
            )
            
            fig.add_trace(go.Scatter(
                x=[rounds[highlight_round]],
                y=[attacker_currency[highlight_round]],
                mode="markers",
                marker=dict(
                    color="#e74c3c",
                    size=12,
                    line=dict(color="white", width=2)
                ),
                showlegend=False
            ))
            
            fig.add_trace(go.Scatter(
                x=[rounds[highlight_round]],
                y=[defender_currency[highlight_round]],
                mode="markers",
                marker=dict(
                    color="#3498db",
                    size=12,
                    line=dict(color="white", width=2)
                ),
                showlegend=False
            ))
        
        fig.update_layout(
            title="Currency Trends",
            xaxis_title="Round",
            yaxis_title="Currency",
            legend_title="Entity",
            hovermode="x unified",
            template="plotly_white",
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        return fig
    
    # Server methods
    def run_server(self, debug=False, port=8050):
        """Run the Dash server.
        
        Args:
            debug (bool, optional): Whether to run in debug mode. Defaults to False.
            port (int, optional): Port to run the server on. Defaults to 8050.
        """
        self.app.run(debug=debug, port=port)


def load_game_from_file(filepath):
    """Load a game from a configuration file."""
    with open(filepath, 'r') as f:
        lines = f.readlines()
        attacker_currency = int(lines[0].strip().translate(str.maketrans('', '', string.ascii_letters)).replace("=", "").replace("_",""))
        defender_currency = int(lines[1].strip().translate(str.maketrans('', '', string.ascii_letters)).replace("=", "").replace("_",""))
        energy = int(lines[2].strip().translate(str.maketrans('', '', string.ascii_letters)).replace("=", "").replace("_",""))
        defender_servers = int(lines[3].strip().translate(str.maketrans('', '', string.ascii_letters)).replace("=", "").replace("_",""))
        server_yield = int(lines[4].strip().translate(str.maketrans('', '', string.ascii_letters)).replace("=", "").replace("_",""))
        good_traffic_transmission_load = float(lines[5].strip().translate(str.maketrans('', '', string.ascii_letters)).replace("=", "").replace("_",""))
        bots_count = int(lines[6].strip().translate(str.maketrans('', '', string.ascii_letters)).replace("=", "").replace("_",""))
        bot_bandwidth = float(lines[7].strip().translate(str.maketrans('', '', string.ascii_letters)).replace("=", "").replace("_",""))
        firewall_type = float(lines[8].strip().translate(str.maketrans('', '', string.ascii_letters)).replace("=", "").replace("_",""))
        server_cost = float(lines[9].strip().translate(str.maketrans('', '', string.ascii_letters)).replace("=", "").replace("_",""))
        energy_cost = float(lines[10].strip().translate(str.maketrans('', '', string.ascii_letters)).replace("=", "").replace("_",""))
        bot_cost = float(lines[11].strip().translate(str.maketrans('', '', string.ascii_letters)).replace("=", "").replace("_",""))
        firewall_cost = float(lines[12].strip().translate(str.maketrans('', '', string.ascii_letters)).replace("=", "").replace("_",""))
        server_energy_cost = float(lines[13].strip().translate(str.maketrans('', '', string.ascii_letters)).replace("=", "").replace("_",""))
    
    # Create and return the game instance
    return Game(
        attacker_currency, defender_currency, energy, defender_servers, server_yield, 
        good_traffic_transmission_load, bots_count, bot_bandwidth, firewall_type,
        server_cost, energy_cost, bot_cost, firewall_cost, server_energy_cost
    )


if __name__ == "__main__":
    import sys
    import os
    
    # Create plots directory if it doesn't exist
    if not os.path.exists("plots"):
        os.makedirs("plots")
        print("Created plots directory")
    
    # Parse command line arguments
    auto_run = False
    port = 8050
    
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "--auto":
            auto_run = True
            i += 1
        elif sys.argv[i] == "--port" and i+1 < len(sys.argv):
            try:
                port = int(sys.argv[i+1])
                i += 2
            except ValueError:
                print(f"Invalid port number: {sys.argv[i+1]}")
                i += 2
        else:
            # Skip file argument as we're using the dropdown now
            i += 1
    
    try:
        # Create dashboard with no initial game
        dashboard = DashVisualizer(auto_run=auto_run)
        print(f"Starting dashboard on http://localhost:{port}")
        dashboard.run_server(debug=True, port=port)
        
    except Exception as e:
        print(f"Error: {e}")
        print("Examples:")
        print("  python dash_visualization.py")
        print("  python dash_visualization.py --port 8080")