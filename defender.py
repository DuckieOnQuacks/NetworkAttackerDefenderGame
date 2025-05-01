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
        self.server_list = []
        self.intrusion_history = []  # Track recent intrusions
        
        # Initialize servers with different qualities
        for _ in range(servers):
            server = Server(server_yield, firewall_type)
            self.server_list.append(server)

    def get_firewall_cost(self, firewall_type):
        """Calculate the cost of a firewall type"""
        if firewall_type <= 0.01:  # Premium
            return 1000000
        elif firewall_type <= 0.1:  # Enterprise
            return 100000
        elif firewall_type <= 0.33:  # Business
            return 1000
        elif firewall_type <= 0.5:  # Standard
            return 100
        else:  # Basic
            return 0

    def __str__(self):
        return f"Defender {self.currency} with {self.servers} {self.server_list[0].quality} servers"

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
        # Calculate total revenue from all servers
        total_revenue = 0
        for server in self.server_list:
            total_revenue += server.get_defender_yield()
        return total_revenue

    def predict_expenses(self, shop):
        # Calculate total expenses including server maintenance and firewall costs
        total_expenses = 0
        for server in self.server_list:
            # Higher quality servers have higher maintenance costs
            maintenance_cost = shop.server_cost * (1 + server.security_bonus)
            total_expenses += maintenance_cost + shop.server_energy_cost
        
        # Add firewall cost
        total_expenses += shop.get_firewall_cost(self.firewall_type)
        return total_expenses
    
    def predict_profit(self, shop):
        return self.predict_revenue() - self.predict_expenses(shop=shop)

    def update_currency(self, amount):
        self.currency += amount
        
    def get_server_quality_summary(self):
        """Returns a summary of server qualities and their counts"""
        quality_counts = {}
        for server in self.server_list:
            quality = server.quality
            if quality in quality_counts:
                quality_counts[quality] += 1
            else:
                quality_counts[quality] = 1
        return quality_counts

    def update_firewall_based_on_intrusions(self, intrusion_rate):
        """Dynamically adjust firewall type based on intrusion rate"""
        # Add current intrusion rate to history
        self.intrusion_history.append(intrusion_rate)
        if len(self.intrusion_history) > 5:  # Keep last 5 rounds
            self.intrusion_history.pop(0)
            
        # Calculate average intrusion rate over last 5 rounds
        avg_rate = sum(self.intrusion_history) / len(self.intrusion_history)
        
        # Try to get the best firewall we can afford
        firewall_options = [
            (0.01, "Premium"),    # Best security
            (0.1, "Enterprise"),  # Very good security
            (0.33, "Business"),   # Good security
            (0.5, "Standard"),    # Basic security
            (1.0, "Basic")        # No security
        ]
        
        # Only upgrade if we have high intrusion rate (5% or more)
        should_upgrade = avg_rate > 0.05
        
        if should_upgrade:
            # Try each firewall option from best to worst
            for firewall_type, quality in firewall_options:
                cost_change = self.get_firewall_cost(firewall_type) - self.get_firewall_cost(self.firewall_type)
                # If we can afford it and it's better than current
                if cost_change <= self.currency and firewall_type < self.firewall_type:
                    print(f"Upgrading firewall to {quality} ({firewall_type}) for {cost_change:,} currency")
                    self.firewall_type = firewall_type
                    self.currency -= cost_change
                    # Update all servers with new firewall type
                    for server in self.server_list:
                        server.firewall_type = firewall_type
                        server.update_quality()
                    break  # Stop after finding best affordable option
        elif avg_rate < 0.02 and self.firewall_type < 0.5:  # Also adjusted the downgrade threshold to 2%
            # If intrusion rate is very low and we have strong security,
            # consider slightly relaxing to save costs
            new_firewall = min(0.5, self.firewall_type * 1.1)
            cost_change = self.get_firewall_cost(new_firewall) - self.get_firewall_cost(self.firewall_type)
            if abs(new_firewall - self.firewall_type) > 0.01:
                print(f"Relaxing firewall from {self.firewall_type} to {new_firewall} to save costs")
                self.firewall_type = new_firewall
                # Update all servers with new firewall type
                for server in self.server_list:
                    server.firewall_type = new_firewall
                    server.update_quality()

    def process_round(self, intrusion_rate):
        """Process end of round statistics and adjust firewall"""
        self.update_firewall_based_on_intrusions(intrusion_rate)



