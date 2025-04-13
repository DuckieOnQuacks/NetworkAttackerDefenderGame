from game import Game
from packet import Packet
import sys
import string
import os
from graph import plot_list
# def ask_user_for_god_mode():
#     print("Do you want to enable god mode? (y/n)")
#     god_mode = input()
#     return god_mode == 'y'

def ask_user_for_currency_amount():
    print("How much currency should the attacker have?")
    attacker_currency = input()
    print("How much currency should the defender have?")
    defender_currency = input()
    return attacker_currency, defender_currency

def ask_user_for_rounds_to_attack():
    print("How many rounds to attack?")
    rounds = input()
    return int(rounds)

def ask_user_for_defender_servers_amount():
    print("How many servers should the defender have?")
    defender_servers = input()
    print("How much currency should each server generate per round?")
    server_yield = input()
    return defender_servers, server_yield

def ask_user_for_good_traffic_transmission_load():
    print("What is the good traffic transmission load?")
    good_traffic_transmission_load = input()
    return good_traffic_transmission_load

if __name__ == "__main__":

    file = sys.argv[1] if len(sys.argv) > 1 else None
    if file:
        with open(file, 'r') as f:
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
    else:
        print("Please provide a file with the game settings.")

    # attacker_currency, defender_currency = ask_user_for_currency_amount()
    # rounds = ask_user_for_rounds_to_attack()
    # defender_servers, server_yield = ask_user_for_defender_servers_amount()
    # good_traffic_transmission_load = ask_user_for_good_traffic_transmission_load()
    game = Game(attacker_currency, defender_currency, energy, defender_servers, server_yield, 
                good_traffic_transmission_load, bots_count, bot_bandwidth, firewall_type,
                server_cost, energy_cost, bot_cost, firewall_cost, server_energy_cost)
    while game.attacker.currency > 0 and game.defender.currency > 0:
        game.run_game()
        print("----------------")
        input("Press Enter to continue...")
        os.system('cls' if os.name == 'nt' else 'clear')
    if game.attacker.currency > 0:
        print("Rounds: ", game.rounds)
        print("Attacker Wins")
        #data, title, xlabel, ylabel
        plot_list(data=game.data_attacker_currency, title="Attacker Currency", xlabel="Rounds", ylabel="Currency")
        plot_list(data=game.data_defender_currency, title="Defender Currency", xlabel="Rounds", ylabel="Currency")
    else:
        print("Rounds: ", game.rounds)
        print("Defender Wins")
        plot_list(data=game.data_attacker_currency, title="Attacker Currency", xlabel="Rounds", ylabel="Currency")
        plot_list(data=game.data_defender_currency, title="Defender Currency", xlabel="Rounds", ylabel="Currency")
    # print(game.attacker)
    # print(game.defender)
    # print(game.rounds)
    # print(game.server_yield)
    # print(game.good_transmission_load)

    # print((game.attacker.bot_list))
    # print(game.attacker.bot_list[0])
    #game.run_game()

