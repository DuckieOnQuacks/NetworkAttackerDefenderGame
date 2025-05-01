from packet import Packet
from bot import Bot
import random
# Attacker class that inherits from the Game class
class Attacker:

    def get_firewall_cost(self, firewall_type):
        if firewall_type == 0.01:
            return 1000000
        elif firewall_type == 0.1:
            return 100000
        elif firewall_type == 0.33:
            return 1000
        elif firewall_type == 0.5:
            return 100
        else:
            return 0
        
    def __init__(self, currency, num_bots, energy, bot_band):
        self.currency = currency

        self.num_bots = num_bots
        self.total_bot_band = bot_band
        self.energy = energy
        num_bots = int(num_bots)

        self.server_memory = []
        self.profit_memory = 0

    
    def __str__(self):
        return "Attacker "+str(self.currency)+ " "+str(len(self.bot_list))+" "+str(self.total_bot_band)
        
    # def add_bot(self):
    #     new_bot = Bot()
    #     self.bot_list.append(new_bot)
    #     self.bot_dict[new_bot.uid] = 0

    def clear_dict(self):
        for value in self.bot_dict.values():
            del value[:]

    def remove_bot(self, uid):
        self.bot_list.remove(uid)


    def add_server_memory(self, servers):
        self.server_memory.append(servers)

    def add_profit_memory(self, profit):
        self.profit_memory.append(profit)

    def predict_defender_server_count(self):
        return sum(self.server_memory) / len(self.server_memory)

    def predict_revenue(self, firewall_type):
        return self.total_bot_band * self.num_bots * self.energy * firewall_type

    def predict_firewall_type(self):
        return 

    def predict_expenses(self, shop):
        if self.num_bots == 0:
            return 0
        return shop.bot_cost * self.num_bots + shop.bot_energy_cost * self.total_bot_band
    
    def predict_profit(self, shop, firewall_type):
        return self.predict_revenue(firewall_type) - self.predict_expenses(shop)
    
    def clear_bots(self):
        self.num_bots = 0

    def update_currency(self, amount):
        self.currency += amount

    def calculate_change_cost(self, shop, bot_change, band_change):
        return shop.bot_cost * bot_change + shop.bot_energy_cost * band_change


    def update_attacker(self, shop, bot_change, band_change):
        print("Want to change bot count by", bot_change)
        print("Want to change bot band by", band_change)
        if self.num_bots + bot_change < 0:
            print("Not enough bots to remove")
            return
        if self.total_bot_band + band_change < 0:
            print("Not enough bot band to remove")
            return
            
        # Calculate costs only for positive changes (we don't get refunds for reductions)
        costs = self.calculate_change_cost(shop, max(0, bot_change), max(0, band_change))
        print("Attacker Costs for Change", costs)
        
        if costs > self.currency:
            print("Not enough currency to change")
            return
            
        # Apply the changes
        self.num_bots += bot_change
        self.total_bot_band += band_change
        self.currency -= costs

    def decision(self, shop, intrusion_rate):
        # High intrusion rate means our attacks are getting through
        # Low intrusion rate means the firewall is blocking most attacks
        
        # Calculate loss percentage relative to current currency
        loss_percentage = abs(self.profit_memory) / self.currency if self.currency > 0 else float('inf')
        
        # If losses are severe (more than 20% of current currency), withdraw completely
        if loss_percentage > 0.20 and self.num_bots > 0:
            print(f"Withdrawing all bots due to severe losses ({self.profit_memory}, {loss_percentage*100:.1f}% of currency)")
            self.update_attacker(shop, -self.num_bots, -self.total_bot_band)
            return True  # Signal to end the game
            
        # If intrusion rate is good (>50%), add more bots
        if intrusion_rate > 0.50:
            # Scale increase with intrusion rate success
            increase = min(max(1, int(intrusion_rate * 10)), 10)
            print(f"Increasing bots by {increase} due to high intrusion success rate ({intrusion_rate*100:.1f}%)")
            self.update_attacker(shop, increase, increase)
        # If intrusion rate is poor (<30%) and we have more than minimum bots, reduce
        elif intrusion_rate < 0.30 and self.num_bots > 5:
            decrease = min(max(1, int((0.30 - intrusion_rate) * 10)), 5)
            print(f"Decreasing bots by {decrease} due to low intrusion success rate ({intrusion_rate*100:.1f}%)")
            self.update_attacker(shop, -decrease, -decrease)
        # If we're in between but losing money, make small adjustments
        elif self.profit_memory < -1000 and self.num_bots > 5:
            decrease = min(max(1, int(abs(self.profit_memory) / 2000)), 3)
            print(f"Minor reduction of {decrease} bots due to losses while having moderate success")
            self.update_attacker(shop, -decrease, -decrease)
            
        return False  # Continue playing
    