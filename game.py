
from attacker import Attacker
from defender import Defender

class Game(Attacker, Defender): 
    def __init__(self, attacker_currency, defender_currency, rounds, defender_servers):
        self.attacker = Attacker(attacker_currency)
        self.defender = Defender(defender_currency, defender_servers)
        self.rounds = rounds
