class Shop:

    def get_firewall_cost(self, firewall_type):
        if firewall_type == 0.01:
            return 1000
        elif firewall_type == 0.1:
            return 100
        elif firewall_type == 0.33:
            return 10
        elif firewall_type == 0.5:
            return 1
        else:
            return 0

    def __init__(self, server_cost, bot_energy_cost, bot_cost, firewall_type, server_energy_cost):
        self.server_cost = server_cost
        self.bot_energy_cost = bot_energy_cost
        self.bot_cost = bot_cost
        self.firewall_cost = self.get_firewall_cost(firewall_type)
        self.server_energy_cost = server_energy_cost
    
    def __str__(self):
        return "Shop "+str(self.server_cost)+ " "+str(self.bot_energy_cost)+" "+str(self.bot_cost)+" "+str(self.firewall_cost)
    
