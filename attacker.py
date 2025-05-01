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

    def decision(self, shop):
        # If attacker has sustained significant losses (more than 7% of currency), consider reducing
        if self.profit_memory < -(self.currency * 0.07):
            # If we have bots and are losing significant money, reduce bot count
            if self.num_bots > 1:  # Only reduce if we have more than 1 bot
                # Calculate reduction based on how much we're losing, but more cautious
                reduction = max(1, int(self.num_bots * (abs(self.profit_memory) / self.currency) * 0.02))
                reduction = min(reduction, self.num_bots - 1)  # Always keep at least 1 bot
                print(f"Reducing bots by {reduction} due to significant losses of {self.profit_memory:,}")
                self.update_attacker(shop, -reduction, -reduction)
                
                # If losses are very severe (more than 40% of current currency), consider leaving
                if abs(self.profit_memory) > (self.currency * 0.4):
                    if random.random() < 0.15:  # Reduced chance to leave
                        print("Attacker has decided to leave the market due to severe losses")
                        return True
            elif self.num_bots <= 1 and abs(self.profit_memory) > (self.currency * 0.45):
                # Only leave with 1 bot if losses are extremely severe
                if random.random() < 0.25:
                    print("Attacker has decided to leave the market due to severe losses with minimal bots")
                    return True
        
        # If we're profitable or losses are small, consider expanding
        elif self.profit_memory > -(self.currency * 0.02):  # More conservative with losses
            # More moderate increase when profitable
            base_increase = max(1, int(self.num_bots * 0.15))  # Base 15% increase
            if self.profit_memory > 0:
                # Additional increase based on profit margin
                profit_increase = int(self.num_bots * (self.profit_memory / self.currency) * 0.25)
                increase = max(base_increase, profit_increase)
            else:
                increase = base_increase
                
            print(f"Increasing bots by {increase} due to acceptable performance ({self.profit_memory:,})")
            self.update_attacker(shop, increase, increase)
        
        return False  # Continue playing
    