import sys
import random
import argparse
from math import factorial, comb
from fractions import Fraction


choice = None
runs = None


parser = argparse.ArgumentParser(description="Optional bool and int args")

# Optional Boolean arg
parser.add_argument(
    "--choice",
    "-c",
    type=lambda x: x.lower() == "true",
    help="Boolean choice (True/False)",
    default=None,
)

# Optional integer arg
parser.add_argument("--runs", "-r", type=int, help="Number of runs (int)", default=None)

# Optional arg to make the user randomly choose each time
parser.add_argument(
    "--random",
    "-rdm",
    action="store_true",
    help="Set switch to a random bool if this flag is present",
    default=None,
)

args = parser.parse_args()

choice = args.choice
runs = args.runs
rdm = args.random


def main():
    """
    Entry point for the script.
    If command-line arguments are given, it runs the game simulation.
    Otherwise, prompts the user to choose between playing or running simulations.
    """

    if len(sys.argv) > 1:
        play_game(choice, runs, rdm)
    else:

        while True:

            option = input(
                "Enter 1 if you would like to run a sim, or 2 if you'd like to play the game yourself: "
            )

            if option == "1":
                play_game(choice, runs, rdm)
            elif option == "2":
                user_play()
            elif option == "exit" or option == "stop":
                break
            else:
                print(
                    "Invalid input. Please try again. To exit, enter 'exit' or 'stop'."
                )
                continue


def game(switch: bool = False, runs: int = 1):
    """
    Runs the Monty Hall simulation.

    Args:
        switch (bool): Whether the guest switches doors.
        runs (int): Number of simulation runs.

    Displays:
        Win/loss outcome for each game and overall stats.
    """

    GREEN = "\033[32m"
    RED = "\033[31m"
    RESET = "\033[0m"
    CYAN = "\033[36m"
    YELLOW = "\033[33m"

    wins = 0
    losses = 0

    y_switch = 0
    n_switch = 0

    for i in range(runs):
        doors = [1, 2, 3]
        car = random.choice(doors)
        guest = random.choice(doors)

        remaining_doors = [d for d in doors if d != guest and d != car]
        host = random.choice(remaining_doors)

        remaining_doors = [d for d in doors if d != host]

        if rdm:
            switch = random.choice([True, False])
            if switch == True:
                y_switch += 1
            else:
                n_switch += 1
        else:
            switch = switch

        if switch:
            guest = [d for d in remaining_doors if d != guest][0]
            switch_str = "Guest switched."
        else:
            switch_str = "Guest did not switch."

        if guest == car:
            wins += 1
            print(f"{GREEN}Guest wins!{RESET}")
        else:
            losses += 1
            print(f"{RED}Host wins!{RESET}")

        if switch == True:
            print(f"{i+1}. {switch_str}. Switch: {CYAN}{switch}{RESET}")
        else:
            print(f"{i+1}. {switch_str}. Switch: {YELLOW}{switch}{RESET}")
        print(f"Wins: {GREEN}{wins}{RESET}, Losses: {RED}{losses}{RESET}")

        win_rate = round(wins / runs * 100, 2)
        if win_rate < 50.00:
            new_win_rate = f"{RED}{win_rate}%{RESET}"
        else:
            new_win_rate = f"{GREEN}{win_rate}%{RESET}"

        if rdm:
            print(
                f"{new_win_rate} win rate out of {runs} runs.\
                   User switched doors {y_switch} times and did not switch doors {n_switch} times"
            )
        else:
            print(f"{new_win_rate} win rate out of {runs} runs.")

    if not rdm:
        prob = post_prob(wins, runs, switch)
        simplified = prob.limit_denominator(1000)
        if runs <= 500000:
            perc_prob = f"{float(prob) * 100:.2f}%"
        else:
            perc_prob = f"{float(prob) * 100:.4f}%"
        print(
            f"{YELLOW}The probability of this win rate is {CYAN}{simplified}{YELLOW}, or {GREEN}{perc_prob}{RESET}"
        )

        range_probs = []
        delta = 10 if runs <= 100 else 30 if runs <= 1000 else 50
        lower = max(0, wins - delta)
        upper = min(runs, wins + delta)

        for k in range(lower, upper + 1):
            range_prob = post_prob(k, runs, switch)
            simple = range_prob.limit_denominator(1000)
            range_probs.append(simple)
            # calc_wins += 1
        final_r_prob = sum(range_probs)
        print(
            f"{YELLOW}The probability of the win rate being in a range of ∆ = {delta} is {GREEN}{float(final_r_prob) * 100:.2f}%{RESET}"
        )


def play_game(choice, runs, rdm):
    """
    Determines the appropriate mode and settings to run the game based on inputs.

    Args:
        choice (bool or None): Whether the user wants to switch.
        runs (int or None): Number of runs requested.
        rdm (bool or None): Whether switching should be randomized.
    """

    if choice != None and runs != None:
        switch = choice
        runs = runs

    else:
        if choice != None and runs == None:
            switch = choice
            runs = get_runs()
        elif runs != None and choice == None:
            runs = runs
            if rdm:
                switch = False
            else:
                switch = get_choice()
        else:
            runs = get_runs()
            if rdm:
                switch = False
            else:
                switch = get_choice()

    game(switch=switch, runs=runs)


def get_choice():
    """
    Prompts the user to decide whether to switch doors.

    Returns:
        bool: True if user wants to switch, False otherwise.
    """

    while True:
        choice = input("Switch door? Enter (yes/no): ").strip().lower()

        if choice in ("yes", "y"):
            switch = True
            break
        elif choice in ("no", "n"):
            switch = False
            break
        else:
            print("Input is not a valid choice. Please try again.")
            continue
    return switch


def get_runs():
    """
    Prompts the user to enter the number of simulation runs.

    Returns:
        int: Number of runs.
    """

    while True:
        try:
            cycles = int(
                input(
                    "How many times would you like to run the sim? Please enter a valid integer: "
                )
            )
            runs = cycles
            break
        except ValueError:
            print("Input was not a valid integer. Please try again.")
            continue
    return runs


def post_prob(wins: int, runs: int, switch: bool) -> Fraction:
    """
    Calculates the binomial probability of getting `wins` out of `runs` given switch probability.

    Args:
        wins (int): Number of wins.
        runs (int): Total number of games played.
        switch (bool): Whether switching was used.

    Returns:
        Fraction: Probability of achieving the result under the given strategy.
    """

    if switch == True:
        p = Fraction(2, 3)
    else:
        p = Fraction(1, 3)

    if runs <= 100000:
        bi_co = Fraction(factorial(runs), (factorial(wins) * factorial((runs - wins))))
    else:
        bi_co = comb(runs, wins)

    prob = bi_co * (p**wins) * ((1 - p) ** (runs - wins))

    return prob


def user_play():
    """
    Allows the user to play an interactive game of Monty Hall.

    Prompts for door choices and handles the switching logic.
    """

    print("\n")
    print(
        "Welcome to the game! There are 3 doors in front of you. One hides a car, the others hide goats."
    )
    print("\n")
    doors = [1, 2, 3]
    car = random.choice(doors)

    while True:
        s = input("Please pick a door! (1/2/3): ")
        print("\n")
        if s == "exit".strip().lower():
            exit()
        try:
            guest = int(s)
            if guest in [1, 2, 3]:
                remaining_doors = [d for d in doors if d != guest and d != car]
                print(
                    f"Great! You have chosen door {guest}. Now the host will open one of the remaining doors."
                )
                print("\n")
                break
            else:
                print("Invalid Input. Please enter an integer btween 1 and 3.")
                print("\n")
                continue
        except ValueError:
            print("Invalid Input. Please enter a number between 1 and 3 inclusive.")
            print("\n")
            continue

    host = random.choice(remaining_doors)
    print(f"The host has opened door {host}, revealing a goat.")

    remaining_doors = [d for d in doors if d != host and d != car]
    option = [d for d in doors if d != guest and d != host][0]

    while True:
        choice = input(
            f"You currently have door {guest}. Would you like to switch to door {option}? "
        )
        print("\n")

        if choice == "yes" or choice == "y":
            guest = option
            break
        elif choice == "no" or choice == "n":
            guest = guest
            break
        elif choice == "exit".strip().lower():
            exit()
        else:
            print("Invalid input. Please enter (y/n) or 'exit'. ")
            continue

    if guest == car:
        print("Congratulations! You have won the car!")
    else:
        print("Sorry, the host has won. Thank you for playing!")
    print("\n")


if __name__ == "__main__":
    main()
