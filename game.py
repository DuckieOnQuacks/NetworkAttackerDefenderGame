
from attacker import Attacker
from defender import Defender
from packet import Packet
import random

# Main game class
class Game(Attacker, Defender): 
    def __init__(self, attacker_currency, defender_currency, rounds, defender_servers):
        self.attacker = Attacker(attacker_currency)
        self.defender = Defender(defender_currency, defender_servers)
        self.rounds = rounds
        self.packetLoad = []

    def run_game(self):
        for i in range(self.rounds):
            self.generate_packet_load(self.attacker.bot_transmission_rate)

    def generate_packet_load(self, transmission_rate):
        packet = Packet(transmission_rate)
        print("Packet generated with transmission rate: ", packet.transmission_rate)
        num_packets = random.randint(1, 1000)  # Generate a random number of packets
        for _ in range(num_packets):
            packet = Packet(transmission_rate)
            self.packetLoad.append(packet)
        print(f"{num_packets} packets added to the packetLoad list.")