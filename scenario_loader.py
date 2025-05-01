import string

def load_scenario(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        attacker_currency = int(lines[0].strip().translate(str.maketrans('', '', string.ascii_letters)).replace("=", "").replace("_",""))
        defender_currency = int(lines[1].strip().translate(str.maketrans('', '', string.ascii_letters)).replace("=", "").replace("_",""))
        energy = int(lines[2].strip().translate(str.maketrans('', '', string.ascii_letters)).replace("=", "").replace("_",""))
        defender_servers = int(lines[3].strip().translate(str.maketrans('', '', string.ascii_letters)).replace("=", "").replace("_",""))
        server_yield = int(lines[4].strip().translate(str.maketrans('', '', string.ascii_letters)).replace("=", "").replace("_",""))
        good_traffic_transmission_load = float(lines[5].strip().translate(str.maketrans('', '', string.ascii_letters)).replace("=", "").replace("_",""))
        bots_count = int(lines[6].strip().translate(str.maketrans('', '', string.ascii_letters)).replace("=", "").replace("_",""))
        bot_bandwidth = float(lines[7].strip().translate(str.maketrans('', '', string.ascii_letters)).replace("=", "").replace("_",""))
        firewall_type = float(lines[8].strip().translate(str.maketrans('', '', string.ascii_letters)).replace("=", "").replace("_",""))
        server_cost = float(lines[9].strip().translate(str.maketrans('', '', string.ascii_letters)).replace("=", "").replace("_",""))
        energy_cost = float(lines[10].strip().translate(str.maketrans('', '', string.ascii_letters)).replace("=", "").replace("_",""))
        bot_cost = float(lines[11].strip().translate(str.maketrans('', '', string.ascii_letters)).replace("=", "").replace("_",""))
        firewall_cost = float(lines[12].strip().translate(str.maketrans('', '', string.ascii_letters)).replace("=", "").replace("_",""))
        server_energy_cost = float(lines[13].strip().translate(str.maketrans('', '', string.ascii_letters)).replace("=", "").replace("_",""))
        
        from game import Game
        return Game(attacker_currency, defender_currency, energy, defender_servers, server_yield, 
                   good_traffic_transmission_load, bots_count, bot_bandwidth, firewall_type,
                   server_cost, energy_cost, bot_cost, firewall_cost, server_energy_cost) 