import random

# Constants for the game
NUM_DICE = 3
DICE_SIDES = 6

# Function to roll the dice and return the results as a list
def roll_dice():
    """Rolls NUM_DICE dice and returns the results."""
    return [random.randint(1, DICE_SIDES) for _ in range(NUM_DICE)]

# Function to check if there are exactly two identical dice (tuple out condition)
def has_tuple_out(dice_roll):
    """Checks if there are exactly two identical dice."""
    return len(set(dice_roll)) == 2  # Tuple out if exactly two unique values

# Function to categorize dice into fixed (appears twice) and non-fixed (appears once)
def categorize_dice(dice_roll):
    """Categorizes dice into fixed and non-fixed based on occurrences."""
    dice_count = {die: dice_roll.count(die) for die in set(dice_roll)}
    fixed = [die for die, count in dice_count.items() if count == 2]
    non_fixed = [die for die, count in dice_count.items() if count == 1]
    
    return fixed, non_fixed

# Function to get validated player input (y/n)
def get_player_input(prompt, valid_choices):
    """Prompts the player for input and ensures it's valid."""
    choice = input(prompt).strip().lower()
    while choice not in valid_choices:
        print("Invalid choice. Please try again.")
        choice = input(prompt).strip().lower()
    return choice

# Function to reroll non-fixed dice
def reroll_non_fixed_dice(non_fixed_dice):
    """Rerolls non-fixed dice and returns the new roll."""
    return [random.randint(1, DICE_SIDES) for _ in range(len(non_fixed_dice))]

# Function to simulate a player's turn
def player_turn(player_name):
    """Simulates a player's turn to roll the dice and decide what to do with them."""
    dice_roll = roll_dice()
    print(f"\n{player_name}'s turn: {dice_roll}")

    # Check if there is a tuple out (two identical dice)
    if has_tuple_out(dice_roll):
        print(f"{player_name}: Tuple Out! Rerolling non-fixed dice...")
    else:
        print(f"{player_name}: No Tuple Out. Deciding whether to reroll or stop.")

    # Categorize dice into fixed and non-fixed
    fixed_dice, non_fixed_dice = categorize_dice(dice_roll)
    print(f"{player_name}: Fixed dice: {fixed_dice}")
    print(f"{player_name}: Non-fixed dice: {non_fixed_dice}")

    # Allow player to decide whether to reroll non-fixed dice
    reroll_decision = get_player_input(f"{player_name}, do you want to reroll non-fixed dice? (y/n): ", ['y', 'n'])
    if reroll_decision == 'y' and non_fixed_dice:
        print(f"{player_name}: Rerolling non-fixed dice...")
        new_roll = reroll_non_fixed_dice(non_fixed_dice)
        dice_roll = fixed_dice + new_roll
    else:
        print(f"{player_name}: No dice to reroll, ending turn.")

    return dice_roll, fixed_dice

# Function for the final roll phase
def final_roll(player_name, fixed_dice):
    """Handles the final roll phase, where non-fixed dice are rerolled."""
    print(f"\n{player_name}'s final roll:")

    # If needed, reroll non-fixed dice
    if len(fixed_dice) < NUM_DICE:
        non_fixed_dice_needed = NUM_DICE - len(fixed_dice)
        non_fixed_dice = [random.randint(1, DICE_SIDES) for _ in range(non_fixed_dice_needed)]
        print(f"{player_name}: Rolling non-fixed dice: {non_fixed_dice}")
        fixed_dice += non_fixed_dice
    else:
        print(f"{player_name}: No dice to reroll, all dice are fixed.")

    # Calculate and return the final score
    final_score = sum(fixed_dice)
    print(f"{player_name}: Final score: {final_score}")
    return final_score

# Main game loop
def play_game(player_names, max_turns=5):
    """Simulates the full game with multiple players and turns."""
    scores = {player: 0 for player in player_names}
    fixed_dice = {player: [] for player in player_names}
    turn_count = 0

    while turn_count < max_turns:
        for player_name in player_names:
            print(f"\n{'='*10} {player_name}'s Turn {'='*10}")
            dice_roll, player_fixed_dice = player_turn(player_name)
            fixed_dice[player_name] += player_fixed_dice
            turn_score = sum(player_fixed_dice)
            scores[player_name] += turn_score
            print(f"{player_name}: Turn score: {turn_score}")
            print(f"{player_name}: Total score: {scores[player_name]}")

        turn_count += 1
        print(f"\nAfter {turn_count} turns: {scores}")

    # Final roll phase
    print("\nFinal roll phase:")
    final_scores = {player: final_roll(player, fixed_dice[player]) for player in player_names}

    # Add final scores to main scores
    for player_name in player_names:
        scores[player_name] += final_scores[player_name]

    # Determine and announce the winner
    winner = max(scores, key=scores.get)
    print(f"\nThe winner is {winner} with {scores[winner]} points!")

# Example of running the game with two players
player_names = ["Ewurabena", "Chaz"]
play_game(player_names, max_turns=3)
