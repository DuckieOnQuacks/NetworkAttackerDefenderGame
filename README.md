# Network Attacker-Defender Game

A strategic game where an attacker and defender compete in a network security scenario. The attacker tries to compromise the defender's network while the defender tries to protect it.

## Game Mechanics

### Attacker
- Controls a botnet with configurable size and bandwidth
- Generates revenue from successful intrusions (1.2x multiplier)
- Has reduced operating costs (20% discount)
- Bot management:
  - Base growth rate: 15% per round when profitable
  - Additional growth up to 25% based on profit margin
  - Reduces bots when losses exceed 7% of currency
  - More resilient to losses with gradual reductions
  - May leave the game if losses become severe (>40% of currency)

### Defender
- Controls servers with configurable count and yield
- Uses firewalls to protect against intrusions
- Firewall types:
  - Premium (0.01): Best protection, highest cost
  - Enterprise (0.1): Good protection, high cost
  - Standard (0.33): Moderate protection, moderate cost
  - Basic (0.5): Basic protection, low cost
- Firewall upgrades/downgrades based on intrusion rate:
  - Upgrades when intrusion rate > 5%
  - Downgrades when intrusion rate < 2%

### Economy
- Both players start with configurable currency
- Attacker revenue comes from successful intrusions
- Defender revenue comes from server operations
- Both players have operating costs
- Successful intrusions cause 1.1x damage to defender revenue

## Gameplay
1. Players start with initial resources
2. Each round:
   - Attacker generates traffic (good and malicious)
   - Defender's firewall filters traffic
   - Profits/losses are calculated
   - Attacker adjusts bot count based on performance
   - Defender adjusts firewall based on intrusion rate
3. Game continues until one player leaves or resources are depleted

## Strategy
- Attacker must balance bot growth with profitability
- Defender must balance firewall cost with protection level
- Both players must manage resources carefully
- Timing of upgrades/downgrades is crucial

## Recent Balance Changes
- Attacker made more conservative with slower growth
- Defender given more resilience against attacks
- Firewall upgrade/downgrade thresholds adjusted
- Profit calculations rebalanced for fairer gameplay

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
   python main.py
   ```

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


