from game import Game
from packet import Packet
import sys
import string
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
            rounds = int(lines[2].strip().translate(str.maketrans('', '', string.ascii_letters)).replace("=", "").replace("_",""))
            defender_servers = int(lines[3].strip().translate(str.maketrans('', '', string.ascii_letters)).replace("=", "").replace("_",""))
            server_yield = int(lines[4].strip().translate(str.maketrans('', '', string.ascii_letters)).replace("=", "").replace("_",""))
            good_traffic_transmission_load = float(lines[5].strip().translate(str.maketrans('', '', string.ascii_letters)).replace("=", "").replace("_",""))
            bots_count = int(lines[6].strip().translate(str.maketrans('', '', string.ascii_letters)).replace("=", "").replace("_",""))
            bot_bandwidth = float(lines[7].strip().translate(str.maketrans('', '', string.ascii_letters)).replace("=", "").replace("_",""))
    else:
        attacker_currency, defender_currency = ask_user_for_currency_amount()
        rounds = ask_user_for_rounds_to_attack()
        defender_servers, server_yield = ask_user_for_defender_servers_amount()
        good_traffic_transmission_load = ask_user_for_good_traffic_transmission_load()

    # attacker_currency, defender_currency = ask_user_for_currency_amount()
    # rounds = ask_user_for_rounds_to_attack()
    # defender_servers, server_yield = ask_user_for_defender_servers_amount()
    # good_traffic_transmission_load = ask_user_for_good_traffic_transmission_load()
    game = Game(attacker_currency, defender_currency, rounds, defender_servers, server_yield, good_traffic_transmission_load, bots_count, bot_bandwidth)
    # print(game.attacker)
    # print(game.defender)
    # print(game.rounds)
    # print(game.server_yield)
    # print(game.good_transmission_load)

    # print((game.attacker.bot_list))
    for bot in game.attacker.bot_list:
        print(bot.uid)
    # print(game.attacker.bot_list[0])
    #game.run_game()

