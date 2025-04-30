import matplotlib.pyplot as plt
import os


def plot_list(data, title, xlabel, ylabel, save_path=None):
    if not data:
        print(f"Warning: No data to plot for {title}")
        return
    plt.figure()
    plt.plot(data, marker='o')
    
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    
    if save_path:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else '.', exist_ok=True)
        plt.savefig(save_path)
        print(f"Plot saved to {save_path}")
    else:
        plt.show()

def plot_currency_over_time(attacker_data, defender_data, title="Currency Over Time", save_path=None):
    print(f"Plotting currency data:")
    print(f"Attacker data: {attacker_data}")
    print(f"Defender data: {defender_data}")
    
    if not attacker_data and not defender_data:
        print("Error: No data available for plotting currency over time")
        return
    
    plt.figure(figsize=(10, 6))
    
    # Handle attacker data
    if attacker_data:
        # If we have just one data point, add a second one to make a line
        if len(attacker_data) == 1:
            plt.plot([0, 1], [attacker_data[0], attacker_data[0]], 'r-', marker='o', label='Attacker')
            print("Only one attacker data point found, duplicating for visualization")
        else:
            plt.plot(attacker_data, 'r-', marker='o', label='Attacker')
    
    # Handle defender data
    if defender_data:
        # If we have just one data point, add a second one to make a line
        if len(defender_data) == 1:
            plt.plot([0, 1], [defender_data[0], defender_data[0]], 'b-', marker='o', label='Defender')
            print("Only one defender data point found, duplicating for visualization")
        else:
            plt.plot(defender_data, 'b-', marker='o', label='Defender')
    
    plt.title(title)
    plt.xlabel("Rounds")
    plt.ylabel("Currency")
    plt.legend()
    plt.grid(True)
    
    # Add round numbers on x-axis
    if attacker_data or defender_data:
        max_len = max(len(attacker_data), len(defender_data))
    
    # Save and show the plot
    if save_path:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else '.', exist_ok=True)
        plt.savefig(save_path)
        print(f"Plot saved to {save_path}")
    plt.show()


