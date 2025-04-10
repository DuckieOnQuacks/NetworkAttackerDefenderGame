
from attacker import Attacker
from defender import Defender
from packet import Packet
import random

# Main game class
class Game(Attacker, Defender): 
    def __init__(self, attacker_currency, defender_currency, rounds, defender_servers, server_yield, good_traffic_transmission_load, bots_count, bot_bandwidth):
        self.attacker = Attacker(attacker_currency, bots_count)
        self.defender = Defender(defender_currency, defender_servers)
        self.rounds = rounds
        self.server_yield = server_yield
        self.good_transmission_load = good_traffic_transmission_load
        self.attacker.total_bot_band = bot_bandwidth

    def __str__(self): 
        return "Game "+str(self.attacker.currency)+" "+str(self.defender.currency)+" "+str(self.rounds)+" "+str(self.server_yield)+" "+str(self.good_transmission_load)

    # Game Loop
    def run_game(self):
        for i in range(self.rounds):
            self.attacker.generate_packet_load(self.attacker.bot_transmission_rate)

    def get_attacker(self):
        return self.attacker