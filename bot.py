from nanoid import generate

class Bot:
    def __init__(self, transmission_rate):
        self.uid = generate(size=16)
        self.bot_transmission_rate = transmission_rate
        self.packet_load = self.generate_packet_load()
    
    def __str__(self):
        return "Bot "+ str(self.uid)

    def generate_packet_load(self):
        Packet = Packet(True, self.bot_transmission_rate)
        return Packet
    
