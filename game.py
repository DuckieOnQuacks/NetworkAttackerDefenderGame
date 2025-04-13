
from attacker import Attacker
from defender import Defender
from shop import Shop
from packet import Packet
import random

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

    def run_game(self):
        self.data_num_bots.append(self.attacker.num_bots)
        self.data_bot_bandwidth.append(self.attacker.total_bot_band)
        self.data_num_servers.append(self.defender.servers)
        self.data_server_income.append(self.defender.server_yield)
        self.data_defender_profit.append(self.defender.predict_profit(shop=self.shop))
        self.data_attacker_profit.append(self.attacker.predict_profit(shop=self.shop, firewall_type=self.defender.firewall_type))
        self.data_defender_currency.append(self.defender.currency)
        self.data_attacker_currency.append(self.attacker.currency)
        self.data_firewall_type.append(self.defender.firewall_type)

        print("Round Start Attacker Currency", self.attacker.currency)
        print("Round Start Defender Currency", self.defender.currency)
        print("-----------------------")
        attacker_profit = min(self.defender.predict_revenue(), self.attacker.predict_revenue(self.defender.firewall_type)) - self.attacker.predict_expenses(self.shop)
        defender_profit = max(self.defender.predict_revenue() - self.attacker.predict_revenue(self.defender.firewall_type), 0) - self.defender.predict_expenses(self.shop)
        print("Actual Attacker Profit", attacker_profit)
        print("Actual Defender Profit", defender_profit)
        print("-----------------------")
        self.attacker.update_currency(attacker_profit)
        self.defender.update_currency(defender_profit)
        self.attacker.profit_memory=attacker_profit
        self.defender.profit_memory=defender_profit
        print("Attack Memory", self.attacker.profit_memory)
        print("Defender Memory", self.defender.profit_memory)
        self.attacker.update_attacker(self.shop, 100,100)
        print("-----------------------")
        print("Round End Attacker Currency", self.attacker.currency)
        print("Round End Defender Currency", self.defender.currency)
        self.rounds += 1

    def get_attacker(self):
        return self.attacker
    
# Firewall Type (0.5,0.33,0.1,0.01), Server Quality (MB/s), Server Amount (#)

# Revenue = Server_Quality * Server_Amount * Energy - Total_Intrusion_Traffic

# Botnet Size (#), Botnet Bandwidth (MB/s), Energy (s)

# Total_Intrusion_Traffic = Botnet_Band * Botnet_Size * Energy * Firewall_Type
