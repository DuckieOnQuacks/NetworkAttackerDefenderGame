from game import Game
from packet import Packet


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
    print("How much service should the defender have?")
    defender_servers = input()
    return defender_servers

if __name__ == "__main__":
    attacker_currency, defender_currency = ask_user_for_currency_amount()
    rounds = ask_user_for_rounds_to_attack()
    defender_servers = ask_user_for_defender_servers_amount()
    game = Game(attacker_currency, defender_currency, rounds, defender_servers)
    game.run_game()

