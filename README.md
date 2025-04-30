# Network Attacker-Defender Game

An interactive simulation of a network security game between an attacker and a defender, visualized using Dash and Cytoscape.

## Overview

This application simulates a strategic game between two players:
- **Attacker**: Attempts to compromise network servers using bots
- **Defender**: Protects servers using firewalls and other security measures

The simulation provides a visual representation of the network, showing the interaction between attackers, defenders, and servers, along with real-time updates of currency and resources.

## Features

- **Interactive Network Visualization**
  - Real-time display of network topology
  - Visual representation of attacks and defenses
  - Dynamic updates of node states and connections

- **Game Controls**
  - Run/Pause/Reset simulation
  - Adjustable simulation speed
  - Multiple game templates to choose from
  - Manual configuration options

- **Status Tracking**
  - Real-time currency updates for both players
  - Resource tracking (bots, servers, bandwidth)
  - Round-by-round progress monitoring
  - Currency trend visualization

- **Game Templates**
  - Fair Game: Balanced starting conditions
  - High Stakes: High-risk, high-reward scenario
  - Extreme Scenario: Challenging conditions
  - Attacker Advantage: Favorable conditions for attacker
  - Defender Advantage: Favorable conditions for defender
  - Test Scenario: For testing and experimentation

## How to Use

1. **Installation**
   ```bash
   pip install -r requirements.txt
   ```

2. **Running the Application**
   ```bash
   python dash_visualization.py
   ```
   The application will start on `http://localhost:8050`

3. **Game Setup**
   - Select a game template from the dropdown menu
   - Click "Load Game" to start with the selected template
   - Alternatively, choose "Manual Configuration" to set custom parameters

4. **Playing the Game**
   - Use the "Run Simulation" button to start the game
   - Adjust simulation speed using the slider
   - Monitor the currency trends and network state
   - Use "Reset" to start over with the same configuration

## Game Parameters

### Attacker Settings
- Initial Currency
- Number of Bots
- Bot Bandwidth
- Bot Cost

### Defender Settings
- Initial Currency
- Number of Servers
- Server Income
- Firewall Strength

### Game Settings
- Energy
- Good Traffic Rate
- Server Cost
- Energy Cost
- Firewall Cost
- Server Energy Cost

## Technical Details

The application is built using:
- **Dash**: Web application framework
- **Dash Cytoscape**: Network visualization
- **Plotly**: Interactive charts
- **Dash Bootstrap Components**: UI components
- **NumPy**: Numerical computations

## Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt`

## License 

This project is open source and available under the MIT License.


