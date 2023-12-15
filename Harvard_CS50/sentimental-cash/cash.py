from cs50 import get_float

# Function to calculate the minimum number of coins
def calculate_coins(change):
    coins = 0
    cents = round(change * 100)  # Convert dollars to cents

    # Calculate the number of quarters
    coins += cents // 25
    cents %= 25

    # Calculate the number of dimes
    coins += cents // 10
    cents %= 10

    # Calculate the number of nickels
    coins += cents // 5
    cents %= 5

    # Calculate the number of pennies
    coins += cents

    return coins

def main():
    while True:
        change_owed = get_float("Change owed: ")

        if change_owed >= 0:
            break

    coins_needed = calculate_coins(change_owed)
    print(coins_needed)

if __name__ == "__main__":
    main()

