from packet import Packet
from bot import Bot
# Attacker class that inherits from the Game class
class Attacker:
    def __init__(self, currency):
        self.currency = currency
        self.bot_list = []
        self.bot_dict = {}
        self.bot_transmission_rate = 0

    
    def __str__(self):
        return "Attacker "+str(self.currency)
        
    def add_bot(self):
        new_bot = Bot(self.bot_transmission_rate)
        self.bot_list.append(new_bot)
        self.bot_dict[new_bot.uid] = 0

    def clear_dict(self):
        for value in self.bot_dict.values():
            del value[:]

    def remove_bot(self, uid):
        self.bot_list.remove(uid)

