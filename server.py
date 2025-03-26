from nanoid import generate
from packet import Packet

class Server:
    def __init__(self, currency_yield, firewall_type):
        self.id = generate(size=16)
        self.currency_yield = currency_yield
        self.firewall_type = firewall_type
        self.packet_loads = []
        self.num_malicious_packets = 0
        self.num_good_packets = 0
        self.num_total_packets = 0
    
    def __str__(self):
        return "Server "+str(self.id)

    def load_packet(self, packet_load):
        self.packet_loads.append(packet_load)

    def clear_packets(self):
        self.packet_loads = []
        self.num_malicious_packets = 0
        self.num_good_packets = 0
    
    def process_packets(self):
        for packet in self.packet_loads:
            if packet.is_malicious:
                self.num_malicious_packets += self.firewall_type*packet.packet_amt
                self.num_total_packets += self.firewall_type*packet.packet_amt
            else:
                self.num_good_packets += packet.packet_amt
                self.num_total_packets += packet.packet_amt
    
    def get_attacker_yield(self):
        return (self.num_malicious_packets/self.num_total_packets)*self.currency_yield

    def get_defender_yield(self):     
        return (self.num_good_packets/self.num_total_packets)*self.currency_yield
