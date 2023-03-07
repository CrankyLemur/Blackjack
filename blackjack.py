from card import Card
import random
import os

initial_bank = 1000
upside_down_card = Card(0, '?')
face_cards = ['J', 'Q', 'K', 'A']
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "leaderboard.txt")


#
class Blackjack:

  def __init__(self):
    self.deck = self.get_deck()
    self.player_cards = []
    self.dealer_cards = []
    self.player_points = 0
    self.dealer_points = 0
    self.player_name = ""
    self.bet = 0
    self.money = initial_bank
    self.score = 0
    self.dealer_card_2 = None

  def get_name(self):
    return input("Enter your name: ")

  def get_bet(self):
    print(f"\nYou have ${self.money}!")
    while True:
      try:
        self.bet = int(input("\nPlace your bet: "))
        while self.bet > self.money:
          print("\nYeah you wish.")
          self.bet = int(input("\nPlace your bet: "))
        break
      except ValueError:
        print("You need to enter a number.")
        continue
    self.money -= self.bet

  def run(self):
    while True:
      choice = input("\nSelect one of the following:\n"
                     "p - Play\n"
                     "e - Explain\n"
                     "l - View leaderboard\n"
                     "q - Quit\n"
                     ":").lower()
      if choice == 'p':
        self.player_name = self.get_name()
        self.initialize_game()
        self.play()
      elif choice == 'e':
        self.explain()
      elif choice == 'l':
        self.show_leaderboard()
      elif choice == 'q':
        print("\nThanks for playing!")
        break
      else:
        print("Invalid choice")

  def play(self):
    if len(self.deck) < random.randint(14, 40):
      print("\nReshuffling...")
      self.deck = self.get_deck()
    self.get_bet()
    self.deal_cards()
    self.player_turn()
    if self.player_points > 21:
      self.dealer_turn(0)
    else:
      self.dealer_turn()
    self.win_conditions()

  def initialize_game(self):
    self.money = initial_bank
    self.deck = self.get_deck()

  def get_deck(self):
    ranks = [str(i) for i in range(2, 11)] + face_cards
    suits = ['clubs', 'diamonds', 'hearts', 'spades']
    deck = [Card(rank, suit) for rank in ranks for suit in suits]
    random.shuffle(deck)
    return deck

  def deal_cards(self):
    self.player_cards = []
    self.dealer_cards = []
    self.player_points = 0
    self.dealer_points = 0
    self.player_points = self.draw_card(self.player_cards, self.player_points)
    self.dealer_points = self.draw_card(self.dealer_cards, self.dealer_points)
    self.player_points = self.draw_card(self.player_cards, self.player_points)
    self.dealer_card_2 = self.deck[0]
    self.deck.pop(0)
    self.dealer_cards.append(upside_down_card)
    self.show_table()

  def draw_card(self, cards, points):
    cards.append(self.deck[0])
    self.deck.pop(0)
    points = self.get_points(cards, points)
    return points

  def get_points(self, cards, points):
    points = 0
    aces = 0
    for card in cards:
      if card.rank == 'A':
        points += 11
        aces += 1
      elif card.rank in face_cards:
        points += 10
      else:
        points += int(card.rank)
    while aces > 0 and points > 21:
      points -= 10
      aces -= 1
    return points

  def show_table(self):
    print("_" * 50)
    cards = ()
    for i in range(0, len(self.dealer_cards)):
      cards = cards + (repr(self.dealer_cards[i]), )
    for pieces in zip(*(card.splitlines() for card in cards)):
      print(' '.join(pieces))
    print(f"Dealer points: {self.dealer_points}")
    cards = ()
    for i in range(0, len(self.player_cards)):
      cards = cards + (repr(self.player_cards[i]), )
    for pieces in zip(*(card.splitlines() for card in cards)):
      print(' '.join(pieces))
    print(f"Your points: {self.player_points}")
    print("_" * 50)

  def player_turn(self, first_round=True):
    while self.player_points < 21:
      options = ("Select one of the following:\n"
                 "h - Hit\n"
                 "s - Stand\n")
      options_list = ['h', 's']
      if first_round and self.money >= self.bet:
        options += "d - Double bet\n"
        options_list.append('d')
      if self.player_cards[0] == self.player_cards[1]:
        options += "t - Split\n"
        options_list.append('t')
      choice = input(options + ":").lower()
      while choice not in options_list:
        print("Invalid choice")
        choice = input(options + ":").lower()
      if choice == 'h':
        self.player_points = self.draw_card(self.player_cards,
                                            self.player_points)
        if self.player_points < 21:
          self.show_table()
      elif choice == 's':
        break
      elif choice == 'd':
        self.money -= self.bet
        self.bet *= 2
        self.player_points = self.draw_card(self.player_cards,
                                            self.player_points)
        if self.player_points < 21:
          self.show_table()
        break
      elif choice == 't':
        pass
      elif choice == 'i':
        pass
      first_round = False

  def dealer_turn(self, dealer_hit_threshold=17):
    self.dealer_cards.pop(1)
    self.dealer_cards.append(self.dealer_card_2)
    self.dealer_points = self.get_points(self.dealer_cards, self.dealer_points)
    while self.dealer_points < dealer_hit_threshold:
      self.dealer_points = self.draw_card(self.dealer_cards,
                                          self.dealer_points)
    self.show_table()

  def win_conditions(self):
    if self.player_points == 21 and len(self.player_cards) == 2\
        and not (self.dealer_points == 21 and len(self.dealer_cards) == 2):
      print("\nBLACKJACK\n")
      self.money += int(round((self.bet * 2.5), 0))
    elif self.player_points > 21:
      print("\nBust\n")
    else:
      if self.dealer_points > 21:
        print("\nDealer bust!\n")
        self.money += self.bet * 2
      elif self.dealer_points == 21 and len(self.dealer_cards) == 2 and\
          not (self.player_points == 21 and len(self.player_cards) == 2):
        print("\nDealer Blackjack\n")
      else:
        if self.player_points > self.dealer_points:
          print("\nYou win!\n")
          self.money += self.bet * 2
        elif self.player_points == self.dealer_points:
          print("\nPush\n")
          self.money += self.bet
        else:
          print("\nYou lose\n")
    if self.money <= 0:
      print("End of the line, pal. You need money to play.")
      return
    while True:
      choice = input(("Select one of the following:\n"
                      "d - Deal again\n"
                      "c - Cash out\n"
                      ":")).lower()
      if choice == 'd':
        self.play()
        break
      elif choice == 'c':
        self.score = str(max(self.money - initial_bank, 0))
        print(f"\nYou finished the game with ${self.money}!\n"
              f"Your final score is {self.score}.")
        self.write_leaderboard()
        break
      else:
        print("Invalid choice")

  def explain(self):
    print("""
In Blackjack, you must aim to beat the dealer's hand without going over 21.
Aces can be worth 1 or 11, face cards are worth 10, and other cards are \
worth their face value.
The player and the dealer receive two cards, with the dealer showing one card.
Players can hit to improve their hand value, or stand allow the dealer \
their turn.
If a player goes over 21, they bust and lose their bet.
The dealer must hit until their hand value is 17 or higher.
The side with the highest hand value that doesn't exceed 21 wins.""")

  def read_leaderboard(self):
    content_dict = {}
    with open(file_path, 'r') as leaderboard:
      for line in leaderboard:
        name, score = line.strip().split(': ')
        content_dict[name] = int(score)
    return content_dict

  def write_leaderboard(self):
    content_dict = self.read_leaderboard()
    if self.player_name in content_dict:
      print(("\nYou already have a registered score of "\
            f"{content_dict[self.player_name]}. Overwrite?"))
      while True:
        choice = input(("Select one of the following:\n"
                        "y - Yes\n"
                        "n - No\n"
                        ":")).lower()
        if choice == 'y':
          content_dict[self.player_name] = int(self.score)
          print("New score added!")
          break
        elif choice == 'n':
          break
        else:
          print("Invalid choice")
    else:
      content_dict[self.player_name] = int(self.score)
    sorted_dict = dict(
      sorted(content_dict.items(), key=lambda item: item[1], reverse=True))
    with open(file_path, 'w+') as leaderboard:
      for i, (name, score) in enumerate(sorted_dict.items()):
        if i == 10:
          break
        leaderboard.write(f"{name}: {score}\n")
        

  def show_leaderboard(self):
    content_dict = self.read_leaderboard()
    print("These are the current highscores:\n")
    for name, score in content_dict.items():
      print(name, score)