

class Packet():
    def __init__(self, is_malicious, packet_amt):
        self.is_malicious = is_malicious
        self.packet_amt = packet_amt

    def __str__(self):
        return "Packet "+str(self.is_malicious)+" "+str(self.packet_amt)


# class Packet():
#     def __init__(self, transmission_rate, source_id):
#         self.transmission_rate = transmission_rate
#         self.source_id = source_id