




class Player:


    def __init__(self, player_name, intial_bank):
        self.player_name = player_name
        self.hand = []
        self.tot_money = intial_bank

    def add_card(self, card):
        self.hand.append(card)

    def disp_hand(self):
        print("{}'s Hand:".format(self.player_name), [str(card) for card in self.hand])

    def tot_hand(self):

        tot = 0
        for card in self.hand:
            tot += card.numeric_value()

        return tot

    def _make_bet(self, bet_amount, min_bet):

        # allowed to bet
        if self.tot_money - bet_amount >= 0 and bet_amount >= min_bet:
            self.tot_money -= bet_amount
            # make a class attribute to store current bet size
            self.curr_bet_size = bet_amount
            return True
        else:
            print("Bet size to big or under the minimum")
            print("Min bet size: {}".format(min_bet))
            print("Your total chips is {}".format(self.tot_money))
            return False

    def _reset_hand(self):
        self.hand = []





class PlayerAI(Player):


    def __init__(self, player_name, initial_bank):

        super().__init__(player_name, initial_bank)
        
