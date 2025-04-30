from game import Game
from packet import Packet
import sys
import string
import os
import time
from graph import plot_list, plot_currency_over_time
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

    # Check if auto mode is enabled
    auto_mode = False
    output_dir = None
    
    # Process command line arguments
    i = 1
    while i < len(sys.argv):
        if sys.argv[i].lower() == "auto":
            auto_mode = True
            i += 1
        elif sys.argv[i].lower() == "--output" or sys.argv[i].lower() == "-o":
            if i + 1 < len(sys.argv):
                output_dir = sys.argv[i + 1]
                i += 2
            else:
                print("Error: Missing output directory after --output/-o")
                sys.exit(1)
        else:
            file = sys.argv[i]
            i += 1
    
    if 'file' not in locals():
        print("Please provide a file with the game settings.")
        print("Usage: python main.py [auto] [--output DIR] <settings_file>")
        print("  - Use 'auto' to run without manual stepping")
        print("  - Use '--output DIR' or '-o DIR' to specify where to save plots in auto mode")
        sys.exit(1)
    
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
        print("  - Use 'auto' to run without manual stepping")
        sys.exit(1)

    # attacker_currency, defender_currency = ask_user_for_currency_amount()
    # rounds = ask_user_for_rounds_to_attack()
    # defender_servers, server_yield = ask_user_for_defender_servers_amount()
    # good_traffic_transmission_load = ask_user_for_good_traffic_transmission_load()
    
    # Set up the output directory and filename for saving plots
    # Extract just the filename without path and extension
    if file:
        # Get just the filename part without path
        base_filename = os.path.basename(file)
        # Remove the extension if present
        base_filename = os.path.splitext(base_filename)[0]
    
    # Use the input filename for the plot
    plot_filename = f"plots/{base_filename}_currency_plot.png"
    
    # In auto mode, always save to /plots
    if auto_mode:
            plot_save_path = plot_filename
    else:
        plot_save_path = None
    
    game = Game(attacker_currency, defender_currency, energy, defender_servers, server_yield, 
                good_traffic_transmission_load, bots_count, bot_bandwidth, firewall_type,
                server_cost, energy_cost, bot_cost, firewall_cost, server_energy_cost)
    
    print(f"Running game in {'auto' if auto_mode else 'manual'} mode")
    
    while game.attacker.currency > 0 and game.defender.currency > 0:
        game.run_game(auto_mode=auto_mode)
        if not auto_mode:
            print("----------------")
            input("Press Enter to continue...")
            os.system('cls' if os.name == 'nt' else 'clear')
        else:
            # Show progress indicator when in auto mode
            if game.rounds % 5 == 0:  # Every 5 rounds
                print(f"Round {game.rounds}: Attacker: {game.attacker.currency}, Defender: {game.defender.currency}")
    
    # Debug information
    print(f"Game completed after {game.rounds} rounds")
    print(f"Data points collected: {len(game.data_attacker_currency)} attacker, {len(game.data_defender_currency)} defender")
    
    if game.attacker.currency > 0:
        print("Rounds: ", game.rounds)
        print("Attacker Wins")
        #data, title, xlabel, ylabel
        plot_currency_over_time(game.data_attacker_currency, game.data_defender_currency, 
                                save_path=plot_save_path)
    else:
        print("Rounds: ", game.rounds)
        print("Defender Wins")
        plot_currency_over_time(game.data_attacker_currency, game.data_defender_currency,
                                save_path=plot_save_path)

        
    # print(game.attacker)
    # print(game.defender)
    # print(game.rounds)
    # print(game.server_yield)
    # print(game.good_transmission_load)

    # print((game.attacker.bot_list))
    # print(game.attacker.bot_list[0])
    #game.run_game()

