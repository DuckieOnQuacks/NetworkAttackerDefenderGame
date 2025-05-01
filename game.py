from attacker import Attacker
from defender import Defender
from shop import Shop
from packet import Packet

# Main game class
class Game(Attacker, Defender, Shop): 
    def __init__(self, attacker_currency, defender_currency, energy, defender_servers, 
                 server_yield, good_traffic_transmission_load, bots_count, bot_bandwidth, 
                 firewall_type, server_cost, energy_cost, bot_cost, firewall_cost, server_energy_cost):
        self.attacker = Attacker(attacker_currency, bots_count, energy, bot_bandwidth)
        self.defender = Defender(defender_currency, defender_servers, server_yield, firewall_type, 
                                 )
        self.shop = Shop(server_cost, energy_cost, bot_cost, firewall_cost, server_energy_cost)
        self.good_traffic = good_traffic_transmission_load
        self.data_num_bots = []
        self.data_bot_bandwidth = []
        self.data_num_servers= []
        self.data_server_income = []
        self.data_defender_profit = []
        self.data_attacker_profit = []
        self.data_defender_currency = []
        self.data_attacker_currency = []
        self.data_firewall_type = []
        self.rounds = 0

    def __str__(self): 
        return "Game "+str(self.attacker.currency)+" "+str(self.defender.currency)+" "+str(self.rounds)+" "+str(self.server_yield)+" "+str(self.good_transmission_load)

    # Game Loop

    # def run_game(self):
    #     is_attacking = 1
    #     if(len(self.attacker.bot_list) == 0):
    #         is_attacking = 0
    #     attacker_expenses = self.shop.bot_cost * len(self.attacker.bot_list) + self.shop.bot_energy_cost * self.attacker.total_bot_band* is_attacking
    #     defender_expenses = self.defender.servers * (self.shop.server_cost + self.shop.server_energy_cost) + self.shop.get_firewall_cost(self.defender.firewall_type)
    #     # defender_expenses = self.shop.server_cost * self.defender.servers + self.shop.server_energy_cost + self.shop.firewall_cost
    #     total_intrusion_traffic = self.attacker.total_bot_band * len(self.attacker.bot_list) * self.defender.firewall_type
    #     defender_profit = self.defender.server_yield * self.defender.servers - defender_expenses
    #     attacker_revenue = min(total_intrusion_traffic, self.defender.server_yield*self.defender.servers*self.attacker.energy) - attacker_expenses
    #     print("Actual Attacker Expenses: ", attacker_expenses)
    #     print("Predicted Attacker Expenses: ", self.attacker.predict_expenses(shop=self.shop))
    #     print("Actual Attacker Revenue: ", min(total_intrusion_traffic, self.defender.server_yield*self.defender.servers*self.attacker.energy))
    #     print("Predicted Attacker Revenue: ", self.attacker.predict_revenue(firewall_type=self.defender.firewall_type))
    #     print("Attacker Profit: ", attacker_revenue - attacker_expenses)
    #     print("Predicted Attacker Profit: ", self.attacker.predict_profit(shop=self.shop, firewall_type=self.defender.firewall_type))
        
    #     print("-------------------")
    #     print("Actual Defender Expenses: ", defender_expenses)
    #     print("Predicted Defender Expenses: ", self.defender.predict_expenses(shop=self.shop))
    #     print("Actual Defender Revenue: ", self.defender.server_yield * self.defender.servers)
    #     print("Predicted Defender Revenue: ", self.defender.predict_revenue())
    #     print("Actual Defender Profit: ", defender_profit)
    #     print("Defender Predicted Profit: ", self.defender.predict_profit(shop=self.shop))


        # data_num_bots = []
        # data_bot_bandwidth = []
        # data_num_servers= []
        # data_server_income = []
        # data_defender_profit = []
        # data_attacker_profit = []
        # data_defender_currency = []
        # data_attacker_currency = []
        # data_firewall_type = []

    def run_game(self, auto_mode=False):
        # Only record bot data if there are bots or if this is the first round
        if self.attacker.num_bots > 0 or self.rounds == 0:
            self.data_num_bots.append(self.attacker.num_bots)
            self.data_bot_bandwidth.append(self.attacker.total_bot_band)
        
        self.data_num_servers.append(self.defender.servers)
        self.data_server_income.append(self.defender.server_yield)
        self.data_defender_profit.append(self.defender.predict_profit(shop=self.shop))
        self.data_attacker_profit.append(self.attacker.predict_profit(shop=self.shop, firewall_type=self.defender.firewall_type))
        
        # Store currency before operations
        attacker_currency_start = self.attacker.currency
        defender_currency_start = self.defender.currency
        
        self.data_defender_currency.append(defender_currency_start)
        self.data_attacker_currency.append(attacker_currency_start)
        self.data_firewall_type.append(self.defender.firewall_type)

        if not auto_mode:
            print("Round Start Attacker Currency", self.attacker.currency)
            print("Round Start Defender Currency", self.defender.currency)
            print("-----------------------")
        
        # incorporate good traffic: only a fraction of bandwidth used for intrusion
        total_traffic = self.attacker.total_bot_band * self.attacker.num_bots
        good_traffic = total_traffic * self.good_traffic
        malicious_traffic = total_traffic * (1 - self.good_traffic)
        
        # Calculate successful and blocked intrusions based on firewall type
        # Lower firewall type means better security (fewer successful intrusions)
        successful_intrusions = malicious_traffic * self.defender.firewall_type
        blocked_intrusions = malicious_traffic * (1 - self.defender.firewall_type)
        
        # Calculate intrusion rate (percentage of malicious traffic that was successful)
        intrusion_rate = successful_intrusions / malicious_traffic if malicious_traffic > 0 else 0
        
        # Calculate profits based on successful intrusions
        # Attacker gets a percentage of defender's revenue based on successful intrusions
        defender_revenue = self.defender.predict_revenue()
        attacker_revenue = min(successful_intrusions, defender_revenue) * 1.2  # Reduced from 1.5 to 1.2
        attacker_expenses = self.attacker.predict_expenses(self.shop) * 0.8  # Increased from 0.7 to 0.8
        defender_loss = min(successful_intrusions * 1.1, defender_revenue)  # Reduced from 1.2 to 1.1
        
        attacker_profit = attacker_revenue - attacker_expenses
        defender_profit = max(defender_revenue - defender_loss, 0) - self.defender.predict_expenses(self.shop)
        
        if not auto_mode:
            print("Actual Attacker Profit", attacker_profit)
            print("Actual Defender Profit", defender_profit)
            print("Intrusion Rate:", intrusion_rate)
            print("-----------------------")
        
        self.attacker.update_currency(attacker_profit)
        self.defender.update_currency(defender_profit)
        self.attacker.profit_memory = attacker_profit
        self.defender.profit_memory = defender_profit
        
        if not auto_mode:
            print("Attack Memory", self.attacker.profit_memory)
            print("Defender Memory", self.defender.profit_memory)
            
        # Let the attacker's decision method handle bot management
        self.attacker.decision(self.shop, intrusion_rate)
            
        # Update defender's firewall based on intrusions
        self.defender.process_round(intrusion_rate)
        
        if not auto_mode:
            print("-----------------------")
            print("Round End Attacker Currency", self.attacker.currency)
            print("Round End Defender Currency", self.defender.currency)
            print("Current Firewall Type", self.defender.firewall_type)
            
            # Debug info to verify data collection
            print(f"Data recorded for round {self.rounds}:")
            print(f"Attacker currency data points: {len(self.data_attacker_currency)}")
            print(f"Defender currency data points: {len(self.data_defender_currency)}")
            if len(self.data_attacker_currency) > 0:
                print(f"Last attacker currency value: {self.data_attacker_currency[-1]}")
            if len(self.data_defender_currency) > 0:
                print(f"Last defender currency value: {self.data_defender_currency[-1]}")
        
        self.rounds += 1

    def get_attacker(self):
        return self.attacker
    
# Firewall Type (0.5,0.33,0.1,0.01), Server Quality (MB/s), Server Amount (#)

# Revenue = Server_Quality * Server_Amount * Energy - Total_Intrusion_Traffic

# Botnet Size (#), Botnet Bandwidth (MB/s), Energy (s)

# Total_Intrusion_Traffic = Botnet_Band * Botnet_Size * Energy * Firewall_Type
