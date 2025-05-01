import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')
import os
from scenario_loader import load_scenario

class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Attacker-Defender Game")
        self.root.geometry("1920x1080")  # Full HD resolution
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Create main frame with padding
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure main frame grid weights
        self.main_frame.grid_rowconfigure(2, weight=1)  # Plots and messages frame
        self.main_frame.grid_columnconfigure(1, weight=1)  # Plots frame
        
        # Create control frame with more padding
        self.control_frame = ttk.LabelFrame(self.main_frame, text="Controls", padding="15")
        self.control_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Configure control frame grid
        self.control_frame.grid_columnconfigure(4, weight=1)
        
        # Create a frame for buttons to ensure proper spacing
        self.button_frame = ttk.Frame(self.control_frame)
        self.button_frame.grid(row=0, column=0, columnspan=5, sticky=(tk.W, tk.E), pady=5)
        
        # Add Scenario Selection with more padding
        self.scenario_label = ttk.Label(self.button_frame, text="Scenario:", padding=5)
        self.scenario_label.grid(row=0, column=0, padx=(0, 10), sticky=tk.W)
        
        # Get available scenarios from templates directory
        self.scenarios = self.get_available_scenarios()
        self.scenario_var = tk.StringVar()
        self.scenario_dropdown = ttk.Combobox(self.button_frame, textvariable=self.scenario_var, 
                                            values=list(self.scenarios.keys()), width=40)
        self.scenario_dropdown.grid(row=0, column=1, padx=(0, 20), sticky=tk.W)
        self.scenario_dropdown.bind('<<ComboboxSelected>>', self.on_scenario_select)
        
        # Add Run Game button with more padding and larger size
        self.run_button = ttk.Button(self.button_frame, text="Run Game", command=self.start_game, 
                                   width=20, padding=5)
        self.run_button.grid(row=0, column=2, padx=(0, 20), sticky=tk.W)
        
        # Add Skip to End button
        self.skip_button = ttk.Button(self.button_frame, text="Skip to End", command=self.skip_to_end,
                                    width=20, padding=5)
        self.skip_button.grid(row=0, column=3, padx=(0, 20), sticky=tk.W)
        
        # Add Auto Mode checkbox with more padding
        self.auto_mode = tk.BooleanVar()
        self.auto_check = ttk.Checkbutton(self.button_frame, text="Auto Mode", 
                                        variable=self.auto_mode, padding=5)
        self.auto_check.grid(row=0, column=4, padx=(0, 20), sticky=tk.W)
        
        # Add Continue button (initially hidden) with more padding
        self.continue_button = ttk.Button(self.button_frame, text="Continue", 
                                        command=self.continue_game, width=20, padding=5)
        self.continue_button.grid(row=0, column=5, padx=(0, 20), sticky=tk.W)
        self.continue_button.grid_remove()
        
        # Add malicious packet percentage control
        self.malicious_frame = ttk.LabelFrame(self.control_frame, text="Attack Intensity", padding="10")
        self.malicious_frame.grid(row=1, column=0, columnspan=5, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.malicious_label = ttk.Label(self.malicious_frame, text="Malicious Packets: 50%")
        self.malicious_label.grid(row=0, column=0, padx=(0, 10), sticky=tk.W)
        
        self.malicious_slider = ttk.Scale(self.malicious_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                        command=self.update_malicious_percentage)
        self.malicious_slider.set(50)  # Default to 50%
        self.malicious_slider.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Store the current malicious percentage
        self.malicious_percentage = 0.5
        
        # Create status frame with more padding
        self.status_frame = ttk.LabelFrame(self.main_frame, text="Game Status", padding="15")
        self.status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Create stats frame with more padding
        self.stats_frame = ttk.LabelFrame(self.main_frame, text="Game Statistics", padding="15")
        self.stats_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Configure stats frame grid
        self.stats_frame.grid_columnconfigure(1, weight=1)
        
        # Create plots frame with more padding
        self.plots_frame = ttk.LabelFrame(self.main_frame, text="Game Progress", padding="15")
        self.plots_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        
        # Create message frame with more padding
        self.message_frame = ttk.LabelFrame(self.main_frame, text="Messages", padding="15")
        self.message_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure message frame grid
        self.message_frame.grid_columnconfigure(0, weight=1)
        self.message_frame.grid_rowconfigure(0, weight=1)
        
        # Initialize status labels with more padding
        self.status_label = ttk.Label(self.status_frame, text="Game Ready", padding=5)
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        # Initialize stats labels with more padding
        self.round_label = ttk.Label(self.stats_frame, text="Round: 0", padding=5)
        self.round_label.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.attacker_currency_label = ttk.Label(self.stats_frame, text="Attacker Currency: 0", padding=5)
        self.attacker_currency_label.grid(row=1, column=0, sticky=tk.W, pady=2)
        
        self.defender_currency_label = ttk.Label(self.stats_frame, text="Defender Currency: 0", padding=5)
        self.defender_currency_label.grid(row=2, column=0, sticky=tk.W, pady=2)
        
        self.bot_count_label = ttk.Label(self.stats_frame, text="Bot Count: 0", padding=5)
        self.bot_count_label.grid(row=3, column=0, sticky=tk.W, pady=2)
        
        self.bot_bandwidth_label = ttk.Label(self.stats_frame, text="Bot Bandwidth: 0", padding=5)
        self.bot_bandwidth_label.grid(row=4, column=0, sticky=tk.W, pady=2)

        # Add packet statistics frame
        self.packet_frame = ttk.LabelFrame(self.stats_frame, text="Packet Statistics", padding="10")
        self.packet_frame.grid(row=0, column=1, rowspan=5, sticky=(tk.W, tk.E), padx=(20, 0))
        
        # Packet statistics labels
        self.total_packets_label = ttk.Label(self.packet_frame, text="Total Packets: 0", padding=5)
        self.total_packets_label.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.good_packets_label = ttk.Label(self.packet_frame, text="Good Packets: 0", padding=5)
        self.good_packets_label.grid(row=1, column=0, sticky=tk.W, pady=2)
        
        self.malicious_packets_label = ttk.Label(self.packet_frame, text="Malicious Packets: 0", padding=5)
        self.malicious_packets_label.grid(row=2, column=0, sticky=tk.W, pady=2)
        
        self.successful_intrusions_label = ttk.Label(self.packet_frame, text="Successful Intrusions: 0", padding=5)
        self.successful_intrusions_label.grid(row=3, column=0, sticky=tk.W, pady=2)
        
        self.blocked_intrusions_label = ttk.Label(self.packet_frame, text="Blocked Intrusions: 0", padding=5)
        self.blocked_intrusions_label.grid(row=4, column=0, sticky=tk.W, pady=2)

        # Add firewall statistics frame
        self.firewall_frame = ttk.LabelFrame(self.stats_frame, text="Firewall Statistics", padding="10")
        self.firewall_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Firewall statistics labels
        self.firewall_type_label = ttk.Label(self.firewall_frame, text="Current Firewall Type: 0.0", padding=5)
        self.firewall_type_label.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.firewall_quality_label = ttk.Label(self.firewall_frame, text="Firewall Quality: Basic", padding=5)
        self.firewall_quality_label.grid(row=0, column=1, sticky=tk.W, pady=2, padx=(20, 0))
        
        self.firewall_cost_label = ttk.Label(self.firewall_frame, text="Firewall Cost: 0", padding=5)
        self.firewall_cost_label.grid(row=1, column=0, sticky=tk.W, pady=2)
        
        # Initialize packet statistics
        self.total_packets = 0
        self.good_packets = 0
        self.malicious_packets = 0
        self.successful_intrusions = 0
        self.blocked_intrusions = 0
        
        # Initialize message text with scrollbar and more padding
        self.message_text = tk.Text(self.message_frame, height=8, width=100, padx=10, pady=10)
        self.message_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.message_text.config(state=tk.DISABLED)
        
        # Add scrollbar to message text
        scrollbar = ttk.Scrollbar(self.message_frame, orient="vertical", command=self.message_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.message_text.configure(yscrollcommand=scrollbar.set)
        
        # Add a separator for game end messages
        self.separator = ttk.Separator(self.message_frame, orient='horizontal')
        self.separator.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        self.separator.grid_remove()
        
        # Add a special message label for game end
        self.game_end_label = ttk.Label(self.message_frame, text="", font=('Helvetica', 12, 'bold'), padding=10)
        self.game_end_label.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        self.game_end_label.grid_remove()
        
        # Initialize plots with larger size
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(15, 10))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plots_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure plots frame grid
        self.plots_frame.grid_rowconfigure(0, weight=1)
        self.plots_frame.grid_columnconfigure(0, weight=1)
        
        # Initialize data storage
        self.attacker_currency_data = []
        self.defender_currency_data = []
        self.bot_count_data = []
        self.rounds = 0
        
        # Game state
        self.game = None
        self.is_running = False
        
    def get_available_scenarios(self):
        scenarios = {}
        templates_dir = "templates"
        if os.path.exists(templates_dir):
            for file in os.listdir(templates_dir):
                if file.endswith(".txt"):
                    name = file.replace(".txt", "").replace("_", " ").title()
                    scenarios[name] = os.path.join(templates_dir, file)
        return scenarios
        
    def on_scenario_select(self, event):
        selected_scenario = self.scenario_var.get()
        if selected_scenario in self.scenarios:
            self.add_message(f"Selected scenario: {selected_scenario}")
            # Here you would load the scenario settings
            # For now, we'll just update the status
            self.update_status(f"Scenario '{selected_scenario}' selected")
            
    def start_game(self):
        if not self.is_running:
            selected_scenario = self.scenario_var.get()
            if not selected_scenario:
                self.add_message("Please select a scenario first")
                return
                
            try:
                # Load the selected scenario
                scenario_path = self.scenarios[selected_scenario]
                self.game = load_scenario(scenario_path)
                
                # Set initial malicious percentage
                self.game.good_traffic = 1 - self.malicious_percentage
                
                self.is_running = True
                self.run_button.config(text="Stop Game")
                self.update_status("Game Running")
                self.add_message(f"Starting game with scenario: {selected_scenario}")
                
                # Reset data for new game
                self.attacker_currency_data = []
                self.defender_currency_data = []
                self.bot_count_data = []
                self.rounds = 0
                
                # Start the game loop
                self.run_game_loop()
            except Exception as e:
                self.add_message(f"Error loading scenario: {str(e)}")
                self.is_running = False
                self.run_button.config(text="Run Game")
        else:
            self.is_running = False
            self.run_button.config(text="Run Game")
            self.update_status("Game Stopped")
            self.add_message("Game stopped")
            
    def run_game_loop(self):
        if not self.is_running:
            return
            
        if self.game.attacker.currency > 0 and self.game.defender.currency > 0:
            # Check if defender should pull out (firewall is 1)
            if self.game.defender.firewall_type == 1:
                self.add_message("\nDefender has pulled out of the market due to maximum firewall effectiveness!")
                self.show_game_end(self.game.attacker.currency, self.game.defender.currency, 
                                self.game.attacker.num_bots, self.game.attacker.profit_memory)
                self.is_running = False
                self.run_button.config(text="Run Game")
                return
                
            self.game.run_game(auto_mode=self.auto_mode.get())
            
            # Calculate packet statistics
            total_traffic = self.game.attacker.total_bot_band * self.game.attacker.num_bots
            good_traffic = total_traffic * self.game.good_traffic
            malicious_traffic = total_traffic * (1 - self.game.good_traffic)
            successful_intrusions = malicious_traffic * self.game.defender.firewall_type
            blocked_intrusions = malicious_traffic * (1 - self.game.defender.firewall_type)
            
            # Update packet statistics
            self.update_packet_stats(
                int(total_traffic),
                int(good_traffic),
                int(malicious_traffic),
                int(successful_intrusions),
                int(blocked_intrusions)
            )
            
            # Update GUI with current stats
            self.update_stats(self.game.rounds, self.game.attacker.currency, 
                            self.game.defender.currency, self.game.attacker.num_bots, 
                            self.game.attacker.total_bot_band)
            self.update_plots(self.game.attacker.currency, self.game.defender.currency, 
                            self.game.attacker.num_bots)
            
            # Check if attacker wants to leave the market
            if self.game.attacker.decision(self.game.shop):
                self.add_message("\nAttacker is considering leaving the market...")
                self.show_game_end(self.game.attacker.currency, self.game.defender.currency, 
                                self.game.attacker.num_bots, self.game.attacker.profit_memory)
                self.is_running = False
                self.run_button.config(text="Run Game")
                return
                
            if not self.auto_mode.get():
                self.continue_button.grid()
                self.root.wait_variable(self.continue_var)
                self.root.after(100, self.run_game_loop)
            else:
                self.root.after(1000, self.run_game_loop)
        else:
            self.add_message("Game completed")
            self.show_game_end(self.game.attacker.currency, self.game.defender.currency, 
                            self.game.attacker.num_bots, self.game.attacker.profit_memory)
            self.is_running = False
            self.run_button.config(text="Run Game")
            
    def continue_game(self):
        self.continue_button.grid_remove()
        self.continue_var.set(1)
        if self.is_running:
            self.root.after(1000, self.run_game_loop)
            
    def update_status(self, text):
        self.status_label.config(text=text)
        self.root.update()
        
    def update_stats(self, round_num, attacker_currency, defender_currency, bot_count, bot_bandwidth):
        self.round_label.config(text=f"Round: {round_num}")
        self.attacker_currency_label.config(text=f"Attacker Currency: {attacker_currency:,}")
        self.defender_currency_label.config(text=f"Defender Currency: {defender_currency:,}")
        self.bot_count_label.config(text=f"Bot Count: {bot_count}")
        self.bot_bandwidth_label.config(text=f"Bot Bandwidth: {bot_bandwidth}")
        
        # Update firewall statistics
        if hasattr(self, 'game') and self.game is not None:
            current_firewall = self.game.defender.firewall_type
            self.firewall_type_label.config(text=f"Current Firewall Type: {current_firewall:.3f}")
            
            # Determine firewall quality
            if current_firewall <= 0.01:
                quality = "Premium"
            elif current_firewall <= 0.1:
                quality = "Enterprise"
            elif current_firewall <= 0.33:
                quality = "Business"
            elif current_firewall <= 0.5:
                quality = "Standard"
            else:
                quality = "Basic"
            self.firewall_quality_label.config(text=f"Firewall Quality: {quality}")
            
            # Update firewall cost
            cost = self.game.defender.get_firewall_cost(current_firewall)
            self.firewall_cost_label.config(text=f"Firewall Cost: {cost:,}")
        
        self.root.update()
        
    def add_message(self, text):
        self.message_text.config(state=tk.NORMAL)
        self.message_text.insert(tk.END, text + "\n")
        self.message_text.see(tk.END)
        self.message_text.config(state=tk.DISABLED)
        self.root.update()
        
    def update_plots(self, attacker_currency, defender_currency, bot_count):
        self.attacker_currency_data.append(attacker_currency)
        self.defender_currency_data.append(defender_currency)
        self.bot_count_data.append(bot_count)
        
        # Clear previous plots
        self.ax1.clear()
        self.ax2.clear()
        
        # Plot currency
        self.ax1.plot(self.attacker_currency_data, 'r-', label='Attacker')
        self.ax1.plot(self.defender_currency_data, 'b-', label='Defender')
        self.ax1.set_title('Currency Over Time')
        self.ax1.set_xlabel('Rounds')
        self.ax1.set_ylabel('Currency')
        self.ax1.legend()
        self.ax1.grid(True)
        
        # Plot bot count
        self.ax2.plot(self.bot_count_data, 'g-', label='Bot Count')
        self.ax2.set_title('Bot Count Over Time')
        self.ax2.set_xlabel('Rounds')
        self.ax2.set_ylabel('Number of Bots')
        self.ax2.legend()
        self.ax2.grid(True)
        
        # Adjust layout and draw
        self.fig.tight_layout()
        self.canvas.draw()
        self.root.update()
        
    def show_attacker_leaving(self):
        self.separator.grid()
        self.game_end_label.config(text="ATTACKER HAS DECIDED TO LEAVE THE MARKET", foreground='red')
        self.game_end_label.grid()
        self.add_message("\n=== GAME END ===")
        self.add_message("The attacker has decided to leave the market due to having no bots or negative profits.")
        self.add_message("This marks the end of the game.")
        
    def show_game_end(self, attacker_currency, defender_currency, bot_count, profit):
        self.update_status("Game Ended")
        
        # Check if game ended due to defender pulling out
        if self.game.defender.firewall_type == 1:
            self.separator.grid()
            self.game_end_label.config(text="DEFENDER HAS PULLED OUT OF THE MARKET", foreground='red')
            self.game_end_label.grid()
            self.add_message("\n=== GAME END ===")
            self.add_message("The defender has pulled out of the market due to maximum firewall effectiveness.")
            self.add_message("This marks the end of the game.")
        else:
            self.show_attacker_leaving()
        
        self.add_message(f"\nFinal Statistics:")
        self.add_message(f"Final Attacker Currency: {attacker_currency:,}")
        self.add_message(f"Final Defender Currency: {defender_currency:,}")
        self.add_message(f"Final Bot Count: {bot_count}")
        self.add_message(f"Final Profit: {profit:,}")
        
        # Determine winner based on currency
        if attacker_currency > defender_currency:
            self.add_message("\nAttacker Wins!")
            self.game_end_label.config(text="ATTACKER WINS!", foreground='green')
        elif defender_currency > attacker_currency:
            self.add_message("\nDefender Wins!")
            self.game_end_label.config(text="DEFENDER WINS!", foreground='blue')
        else:
            self.add_message("\nGame Ended in Stalemate")
            self.game_end_label.config(text="GAME ENDED IN STALEMATE", foreground='orange')
            
        self.root.update()
        
    def wait_for_continue(self):
        self.continue_button.grid()
        self.continue_var = tk.IntVar()
        self.root.wait_variable(self.continue_var)
        self.continue_button.grid_remove()

    def update_packet_stats(self, total, good, malicious, successful, blocked):
        """Update packet statistics display"""
        self.total_packets = total
        self.good_packets = good
        self.malicious_packets = malicious
        self.successful_intrusions = successful
        self.blocked_intrusions = blocked
        
        self.total_packets_label.config(text=f"Total Packets: {total:,}")
        self.good_packets_label.config(text=f"Good Packets: {good:,}")
        self.malicious_packets_label.config(text=f"Malicious Packets: {malicious:,}")
        self.successful_intrusions_label.config(text=f"Successful Intrusions: {successful:,}")
        self.blocked_intrusions_label.config(text=f"Blocked Intrusions: {blocked:,}")
        
        # Update colors based on success rate
        if total > 0:
            success_rate = successful / total
            if success_rate > 0.5:
                self.successful_intrusions_label.config(foreground='green')
            else:
                self.successful_intrusions_label.config(foreground='red')
        
        self.root.update()

    def skip_to_end(self):
        """Run the simulation at maximum speed until completion"""
        if not self.is_running:
            return
            
        self.update_status("Running at maximum speed...")
        self.auto_mode.set(True)  # Enable auto mode
        self.continue_button.grid_remove()  # Hide continue button
        
        # Run the game loop without delays
        while self.is_running and self.game.attacker.currency > 0 and self.game.defender.currency > 0:
            self.run_game_loop()
            self.root.update()  # Update GUI to prevent freezing
            
        self.update_status("Simulation Complete")
        self.auto_mode.set(False)  # Disable auto mode 

    def update_malicious_percentage(self, value):
        """Update the malicious packet percentage when slider is moved"""
        percentage = int(float(value))
        self.malicious_label.config(text=f"Malicious Packets: {percentage}%")
        self.malicious_percentage = percentage / 100.0
        # Only update game if it exists
        if hasattr(self, 'game') and self.game is not None:
            self.game.good_traffic = 1 - self.malicious_percentage 