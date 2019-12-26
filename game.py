"""
Ex2: Create a class Deck that uses a class Card . Each card has a suit (Hearts, Diamonds, Clubs,
Spades) and a value (A,2,3,4,5,6,7,8,9,10,J,Q,K). The deck should have a list of all possible cards (you
should use list comprehension to set this attribute). The Deck class has a method deal to deal a single
card from the deck (i.e. to remove the last card from the deck) and a method shuffle which raises a
ValueError if the deck does not have all the cards, otherwise returns the cards in a random order.
"""

import random
from player import Player

class Deck:

    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    values = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]

    def __init__(self):

        self.deck = [Card(suite, value) for suite in self.suits for value in self.values]

    def deal(self):
        return self.deck.pop()

    def shuffle(self):

        if len(self.deck) != 52:
            return ValueError

        random.shuffle(self.deck)

    def disp_deck(self):
        print([str(card) for card in self.deck])


class Card:


    def __init__(self, suite, value):

        self.suite = suite
        self.value = value

    def numeric_value(self):

        if self.value == "A":
            return 11
        elif self.value == "J" or self.value == "Q" or self.value == "K":
            return 10
        else:
            return int(self.value)



    def __str__(self):

        return "({}, {})".format(self.suite, self.value)



class Game:

    def  __init__(self, min_bet):
        self.deck = Deck()
        self.dealer = Player("Dealer", 1e10)
        self.tot_players = 0
        self.player_lst = [self.dealer]
        self.min_bet = min_bet


    def add_player(self, player):
        self.tot_players += 1
        self.player_lst.append(player)


    def remove_player(self, player):

        try:
            indx_player = self.player_lst.index(player)
            del self.player_lst[indx_player]
            self.tot_players -= 1

        except:
            print("The player named is not playing")


    def disp_players(self):
        print(" ".join(self.player_lst))

    def is_winner(self, player):

        value_of_player = player.tot_hand()
        value_of_dealer = self.dealer.tot_hand()

        #  dealer wins
        if value_of_player > 21:
            print("You lost")
            return -1

        if value_of_dealer > 21:
            player.tot_money += 2*player.curr_bet_size
            print("You win")
            return 1

        if value_of_player < value_of_dealer:
            print("You lost")
            return -1

        # player wins
        if value_of_player > value_of_dealer:
            player.tot_money += 2*player.curr_bet_size
            print("You win")
            return 1
        # tie
        if value_of_dealer == value_of_player:
            player.tot_money += player.curr_bet_size
            print("Tie")
            return 0

    def bet_and_deal(self):

        # shuffle deck
        self.deck.shuffle()

        # ask players for bets
        for player in self.player_lst:
            if player.player_name == "Dealer":
                continue
            while True:
                print("{}:".format(player.player_name), end=" ")
                bet_amount = float(input("How much would you like to bet? "))

                bet_made = player._make_bet(bet_amount, self.min_bet)
                if bet_made:
                    break
        print("\nThe cards are being dealt\n")

        # deal to all players
        for i in range(2):
            for player in self.player_lst:
                player.add_card(self.deck.deal())

                if player.player_name != "Dealer":
                    player.disp_hand()
                else:
                    if i == 0:
                        player.disp_hand()




    def one_round(self, debug=False):

        # init round
        self.bet_and_deal()

        # ask each player what to do
        for player in self.player_lst:
            if player.player_name == "Dealer":

                if debug == True:
                    print("Dealer:", end = " ")
                    player.disp_hand()
                else:
                    # show one card
                    print("\nDealer shows: {}\n".format(player.hand[0]))

            else:
                player.disp_hand()

                finished = False

                while not finished:
                    # ask each player for a move between stand of hit
                    move = input("Would you like to stand or hit (type 'hit' or 'stand'): ")
                    # if hit
                    if move == "hit":
                        # add card and repeat
                        player.add_card(self.deck.deal())
                        player.disp_hand()

                        if player.tot_hand() > 21:
                            print("Over 21, you have lost")
                            finished = True

                    #  if stand
                    elif move == "stand":
                        # move to next player
                        finished = True

                    else:
                        print("Not a valid move.")
                        print("Please type either 'hit' or 'stand'")


        # now act for the dealer
        while self.dealer.tot_hand() < 17: # if tot under 17 hit
            self.dealer.add_card(self.deck.deal())
            self.dealer.disp_hand()

        i = 0
        # check winner for each player
        while i <= self.tot_players:

            player = self.player_lst[i]

            if player.player_name == "Dealer":
                i += 1
                continue
            player.disp_hand()
            self.dealer.disp_hand()

            # see who wins
            self.is_winner(player)

            print("Your chip total is: {}".format(player.tot_money))



            # check if the player can play again
            if player.tot_money < self.min_bet:
                print("\nYou do not have enough money to play again")
                self.remove_player(player)

            else:
                # ask if they would like to play again
                play_again = input("\nWould you like to play again? (type 'yes' or 'no') ")

                if play_again != "yes":
                    print("Thanks for playing")
                    self.remove_player(player)
                else:
                    player._reset_hand()
                    i += 1

        # reset the dealer
        self.dealer._reset_hand()

    def play(self):

        while self.tot_players > 0:
            print("\n-------- New Round -----------\n")
            self.one_round()


        print("Game Finished")







if __name__ == "__main__":

    bj = Game(10)


    bj.add_player(Player("Francesco", 100))
    # bj.add_player(Player("Lapo", 100))

    bj.play()
