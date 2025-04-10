from packet import Packet
from bot import Bot
# Attacker class that inherits from the Game class
class Attacker:
    def __init__(self, currency, num_bots=0):
        self.currency = currency
        self.bot_list = []
        self.bot_dict = {}
        self.total_bot_band = 0
        num_bots = int(num_bots)
        for i in range(num_bots):
            new_bot = Bot()
            self.bot_list.append(new_bot)
            self.bot_dict[new_bot.uid] = 0

    
    def __str__(self):
        return "Attacker "+str(self.currency)+ " "+str(len(self.bot_list))+" "+str(self.total_bot_band)
        
    def add_bot(self):
        new_bot = Bot()
        self.bot_list.append(new_bot)
        self.bot_dict[new_bot.uid] = 0

    def clear_dict(self):
        for value in self.bot_dict.values():
            del value[:]

    def remove_bot(self, uid):
        self.bot_list.remove(uid)

