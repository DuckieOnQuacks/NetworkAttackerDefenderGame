from server import Server
from shop import Shop

# Defender class that inherits from Game class
class Defender:
    def __init__(self, currency, servers, server_yield, firewall_type):
        self.currency = currency
        self.servers = servers
        self.server_yield = server_yield
        self.black_listed_bots = []
        self.firewall_type = firewall_type
        self.profit_memory = 0

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

    def __str__(self):
        return "Defender "+str(self.currency)

    def add_black_listed_bot(self, bot):
        self.black_listed_bots.append(bot)

    def remove_black_listed_bot(self, bot):
        self.black_listed_bots.remove(bot)

    def add_memory(self, attacker_energy):
        self.memory.append(attacker_energy)

    def predict_attack_energy(self):
        if len(self.memory) == 0:
            return 0
        else:
            return sum(self.memory) / len(self.memory)

    def predict_revenue(self):
        return self.servers * self.server_yield

    def predict_expenses(self, shop):
        return self.servers * (shop.server_cost + shop.server_energy_cost) + shop.get_firewall_cost(self.firewall_type)
    
    def predict_profit(self, shop):
        return self.predict_revenue() - self.predict_expenses(shop=shop)

    def update_currency(self, amount):
        self.currency += amount



