from nanoid import generate
from packet import Packet

class Server:
    def __init__(self, server_yield, firewall_type):
        self.server_yield = server_yield
        self.firewall_type = firewall_type
        self.num_total_packets = 0
        self.num_malicious_packets = 0
        self.update_quality()  # Set initial quality based on firewall type

    def update_quality(self):
        """Update server quality based on firewall type"""
        if self.firewall_type <= 0.01:  # Premium
            self.quality = "Premium"
            self.yield_multiplier = 2.0
            self.security_bonus = 0.1
        elif self.firewall_type <= 0.1:  # Enterprise
            self.quality = "Enterprise"
            self.yield_multiplier = 1.5
            self.security_bonus = 0.05
        elif self.firewall_type <= 0.33:  # Business
            self.quality = "Business"
            self.yield_multiplier = 1.2
            self.security_bonus = 0.02
        elif self.firewall_type <= 0.5:  # Standard
            self.quality = "Standard"
            self.yield_multiplier = 1.0
            self.security_bonus = 0.0
        else:  # Basic
            self.quality = "Basic"
            self.yield_multiplier = 0.8
            self.security_bonus = -0.05

    def load_packet(self, packet):
        self.num_total_packets += 1
        if packet.is_malicious:
            self.num_malicious_packets += 1

    def process_packets(self):
        # Process packets and apply firewall effectiveness
        # Lower firewall_type means better security
        malicious_filtered = self.num_malicious_packets * (1 - self.firewall_type)
        self.num_malicious_packets = 0
        self.num_total_packets = 0
        return malicious_filtered

    def get_defender_yield(self):
        # Apply quality multiplier to base yield
        return self.server_yield * self.yield_multiplier

    def __str__(self):
        return f"{self.quality} Server (Yield: {self.server_yield}, Security: {self.firewall_type})"
