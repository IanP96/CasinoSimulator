"""
Casino Simulator
Version Feb19.1
Made by Ian Pinto
Requires an additional file CasinoStats.txt

UPDATES (Jan19.1 -> Feb19.1)
-

ABOUT
A casino simulator with roulette and blackjack.
"""
from random import randint


def get_bet():
    test_bet = input("How much are you betting? ")
    while not test_bet.isnumeric():
        test_bet = input("Enter a valid bet: ")
    test_bet = int(test_bet)
    return test_bet


# Initialising money
print("Casino simulator!")
currency = input("Type a symbol for your currency: ") + " "
try:
    read_file = open("CasinoStats.txt", "r+")
    money = float(read_file.readlines()[1][7:])
except FileNotFoundError:
    print(f"No progress file found - your starting balance is {currency}100.")
    money = 100.0
except (ValueError, IndexError):
    print(f"Total not found - your starting balance is {currency}100.")
    money = 100.0
else:
    money = float(round(money, 2))
    print(f"Your starting total is {currency}{int(money)}")

# Game help
if input("Is this your first time in the casino? ").lower() == "yes":
    print("\nROULETTE or R")
    print("Bet on one of the following: colour, number, colour and number, column, column and colour.")
    for print_colour in ["Red", "Black"]:
        print(print_colour)
        print("1st 2nd 3rd (columns)")
        print("1   2   3")
        print("4   5   6")
        print("7   8   9 ...")
        print("28  29  30")

    print("\nBLACKJACK or B")
    print("Choose hit to take a card or stand to keep your hand.")
    print("An Ace is worth 11 or 1. It is worth 11 by default - go over 21 and it will be worth 1. All face cards are "
          "worth 10.")
    print("The objective is to get a your total close to 21 without going over.")
    print("If you go over 21, it is called a bust. If you bust, you automatically lose.")
    print("The dealer will also take cards. If your total is higher than the dealer's after they get at least 17, you "
          "win!")
    print("An Ace and a 10 card is called a blackjack, which beats all other 21-worth hands. Win with a blackjack to "
          "receive 1.5x the original bet.")
    print("Get the same total as the dealer and it is called a push - no change to your balance is made.")

while True:
    print()
    game = input("What game do you want to play? Or type done: ").lower()

    # Roulette
    if game in ["roulette", "r"]:
        bet = get_bet()
        money -= bet
        while True:
            multiplier = 1
            colour = None
            number = 0
            column = None
            guess = input("Place your betting space: ")
            if guess[:3] == "red":
                colour = "red"
                multiplier *= 2
                if guess == "red":
                    break
                elif guess[4:].isnumeric():
                    if int(guess[4:]) >= 1 and int(guess[4:]) <= 30:
                        number = int(guess[4:])
                        multiplier *= 30
                        break
                elif guess[4:] == "1st":
                    column = "1st"
                    multiplier *= 3
                    break
                elif guess[4:] == "2nd":
                    column = "2nd"
                    multiplier *= 3
                    break
                elif guess[4:] == "3rd":
                    column = "3rd"
                    multiplier *= 3
                    break
            elif guess[:5] == "black":
                colour = "black"
                multiplier *= 2
                if guess == "black":
                    break
                elif guess[6:].isnumeric():
                    if int(guess[6:]) >= 1 and int(guess[6:]) <= 30:
                        number = int(guess[6:])
                        multiplier *= 30
                        break
                elif guess[6:] == "1st":
                    column = "1st"
                    multiplier *= 3
                    break
                elif guess[6:] == "2nd":
                    column = "2nd"
                    multiplier *= 3
                    break
                elif guess[6:] == "3rd":
                    column = "3rd"
                    multiplier *= 3
                    break
            elif guess.isnumeric():
                if int(guess) >= 1 and int(guess) <= 30:
                    number = int(guess)
                    multiplier *= 30
                    break
            elif guess == "1st":
                column = "1st"
                multiplier *= 3
                break
            elif guess == "2nd":
                column = "2nd"
                multiplier *= 3
                break
            elif guess == "3rd":
                column = "3rd"
                multiplier *= 3
                break
        result = []
        if randint(1, 2) == 1:
            result.append("red")
        else:
            result.append("black")
        result.append(randint(1, 30))
        if result[1] % 3 == 1:
            result.append("1st")
        elif result[1] % 3 == 2:
            result.append("2nd")
        else:
            result.append("3rd")
        print("The ball landed on: %s %s." % (result[0], result[1]))
        if (colour and colour != result[0]) or (number and number != result[1]) or (column and column != result[2]):
            print("You lose!")
        else:
            print("You win %s%s!" % (currency, bet * multiplier))
            money += bet * multiplier
        money = round(money, 2)
        print("Your balance: %s%s" % (currency, money))

    # Blackjack
    elif game in ["blackjack", "b"]:
        bet = get_bet()
        money -= bet
        deck = [["Ace", 11], ["2", 2], ["3", 3], ["4", 4], ["5", 5], ["6", 6], ["7", 7], ["8", 8], ["9", 9],
                ["10", 10], ["Jack", 10], ["Queen", 10], ["King", 10]]

        def blackjack(player):
            hand = []
            aces = 0
            hand_total = 0
            for card in range(2):
                card_index = randint(0, 12)
                hand.append(deck[card_index][0])
                if deck[card_index][0] == "Ace":
                    aces += 1
                hand_total += deck[card_index][1]
            while True:
                if hand_total > 21:
                    if aces > 0:
                        aces -= 1
                        hand_total -= 10
                    else:
                        print("%s%s (Bust!)" % (player, ", ".join(hand),))
                        break
                if len(hand) == 2 and hand_total == 21:
                    print("%s%s (Blackjack!)" % (player, ", ".join(hand),))
                    hand_total += 0.5
                    break
                else:
                    print("%s%s (%s)" % (player, ", ".join(hand), hand_total))
                if player == "You:    ":
                    choice = input("Hit or stand? ").lower()
                    while choice != "hit" and choice != "stand":
                        choice = input("Hit or stand? ").lower()
                    new_card = choice == "hit"
                else:
                    new_card = hand_total < 17
                if new_card:
                    card_no = randint(0, 12)
                    hand.append(deck[card_no][0])
                    if deck[card_no][0] == "Ace":
                        aces += 1
                    hand_total += deck[card_no][1]
                else:
                    break
            return hand_total

        player_total = blackjack("You:    ")
        dealer_total = blackjack("Dealer: ")
        if player_total < dealer_total and dealer_total < 22 or player_total >= 22:
            print("You lose!")
        elif player_total == dealer_total:
            print("Push!")
            money += bet
        elif player_total == 21.5:
            print("You win %s%s!" % (currency, bet * 1.5))
            money += bet * 2.5
        else:
            print("You win %s%s!" % (currency, bet))
            money += bet * 2
        money = round(money, 2)
        print("Your balance: %s%s" % (currency, money))

    # Game completion
    elif game == "done":
        write_file = open("CasinoStats.txt", "w+")
        write_file.write("DON'T TAMPER WITH THIS FILE!\nTotal: " + str(money))
        print("Your stats have successfully been saved.\nThanks for playing Casino!")
        break
