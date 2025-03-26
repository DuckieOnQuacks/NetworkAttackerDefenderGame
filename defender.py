

class Defender:
    def __init__(self, currency, servers):
        self.currency = currency
        self.servers = servers
        self.black_listed_bots = []

    def add_black_listed_bot(self, bot):
        self.black_listed_bots.append(bot)

    def remove_black_listed_bot(self, bot):
        self.black_listed_bots.remove(bot)


