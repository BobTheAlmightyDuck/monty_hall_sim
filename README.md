# Monty Hall Simulator


## Synopsis:

The Monty Hall Problem is a famous statistical question in which a guest on a game show has the option to pick any of three doors. Behind one of the doors is a new car, while the other two hide goats. Based on the (rather presumptuous) assumption that the guest would rather a car over a goat, he must make decisions which increase his likelihood of picking the door which hides the car. He picks a door at random, since with no prior evidence each door has a 1/3 chance of concealing the car. Now the host, who does know what each door conceals, opens one of the two remaining doors, to reveal a goat. Two doors remain closed. The host offers the guest the chance to switch doors, or to stick with his original choice. What should the guest do?

Intuition would tell many people that each door still has an equally likely chance of being the one to conceal the car. Therefore, the guest should not switch his choice, or rather it does not matter if he does or does not. However, this intuition is incorrect. 

For more information on the problem, check out [Monty Hall Problem - Wikipedia](https://en.wikipedia.org/wiki/Monty_Hall_problem)

## Statistical Analysis

There are two main camps in the statistical world: the Frequentists, and the Bayesians. Frequentists will calculate the probability of a possibility by running many iterations of a problem, or looking at existing data, and infer from the ratios of the possible real life results what the probability of something is. For a case such as ours they would run a model of the situation many times, having the guest switch between keeping his original choice or switching doors, and simply look at how many times, given each scenario, did the guest win, and how many times did the host. Counter intuitively, this simulation will show that the guest will win 2/3 times when he switches doors, and the host will win 2/3 times when he does not.

Bayesians, on the other hand, use Bayes theorem to determine the probability of a possibility.
It looks something like this: 

$$
P(H \mid E) = \frac{P(E \mid H) \cdot P(H)}{P(E)}
$$

Bayes’ Theorem describes how to update our belief in a hypothesis H after seeing evidence E.

- P(H) is the **prior** probability of the hypothesis.    
- P(E∣H) is the **likelihood**: how probable the evidence is if the hypothesis is true.    
- P(E) is the **total probability** of the evidence (over all hypotheses).   
- P(H∣E) is the **posterior**: the updated probability of the hypothesis given the evidence.

In our scenario, H is the hypothesis that the car is behind a given door, and E is the evidence: the host opened a specific other door. We use Bayes’ Theorem to compute 

$$
P(H∣E)
$$
which is the probability that the car is behind a specific door given the host's action. Applying the formula for each possible door, we find the switched-to door has a 2/3 chance of hiding the car, while the original choice retains its initial 1/3 chance.

So the two camps agree. But even with the math right in front of us, it still just doesn't seem correct. 

## Goal

Therefore, the purpose of this project is to simulate a Monty Hall scenario in Python. The expected end result is to see with our own eyes that when he does not switch his chances of winning the car decrease. 


## Functionality and Usage

This script has several functions, giving it functionality including:
- Running large batches of sims quickly, with statistical analysis optimized for larger runs.
- The ability to play the game yourself in the terminal (I'll possibly add terminal graphics at some point).
- Allowing the user great control in determining batch sizes and guest choices. The user can:
	- Make the guest switch every time,
	- Have the guest never switch,
	- or have the choice be random. Note that posterior analysis is limited in the random mode.
- The user can also enter "exit" at any point to shut down the program.

To run the program, simply begin by entering 

```
python monty_hall_sim.py
```

The program will then prompt you to enter whether you'd like to run a sim, or play the game yourself. Follow the prompts in the terminal.

Additionally, you can also make use of several `sys` args to customize your sim runs. Please note that all args are only relevant to sims, and if any of them are present the system will not prompt you to choose between playing and running a sim, but will rather go straight to the sim.

Available args include 
- `-c` to determine the guest's choice, can be either `true` or `false`
- `-r` to determine how many sims to run in a batch, must be a valid integer
- `-rdm` to make the guest's choice random. Note that this will override the `-c` arg.
Please note that if improper values are given for any arg, the program will not run.

After each individual run in the sim, the choice, current tallies of wins and losses, and the current win rate will be displayed colorfully. If the `-rdm` arg was not entered, then after the entire batch a function will calculate the total win rate, and print the prior probability of getting that exact win rate as both a fraction and a percentage. The probability of getting a win rate within a certain delta of the observed rate will also be displayed, with different deltas for different batch sizes. 

For example, when `-c` is set to `true` and `-r` is set to `1000`, terminal output might look something like:

```
999. Guest switched.. Switch: True
Wins: 671, Losses: 328
67.1% win rate out of 1000 runs.
Host wins!
1000. Guest switched.. Switch: True
Wins: 671, Losses: 329
67.1% win rate out of 1000 runs.
The probability of this win rate is 15/583, or 2.57%
The probability of the win rate being in a range of ∆ = 30 is 95.05%
```

If the `-rdm` flag was present, it might look something like:

```
999. Guest switched.. Switch: True
Wins: 501, Losses: 498
50.1% win rate out of 1000 runs.                   User switched doors 498 times and did not switch doors 501 times
Host wins!
1000. Guest switched.. Switch: True
Wins: 501, Losses: 499
50.1% win rate out of 1000 runs.                   User switched doors 499 times and did not switch doors 501 times
```

If the `-rdm` arg is present, alongside the data in the terminal displaying with each run of the sim, additional data will be displayed showing the current tally of how many times in the sim the guest did or did not switch.

I hope to come back to this project at some point and add several new features including:
- Graphing using `matplotlib` in both real time and to display results.
- Generalized monty hall, with no set value for the number of doors, and to extend this to the user play version as well.

