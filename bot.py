from nanoid import generate
from packet import Packet
class Bot:
    def __init__(self):
        self.uid = generate(size=16)
        self.bot_transmission_rate = 0
        self.packet_load = None
    
    def __str__(self):
        return "Bot "+ str(self.uid)

    def generate_packet_load(self):
        packet = Packet(True, self.bot_transmission_rate)
        return packet
    
