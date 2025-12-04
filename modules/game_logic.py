import random
from modules.data_loader import load_situations, load_cards

ALL_SITUATIONS = load_situations()
ALL_CARDS = load_cards()


CARDS_POOL = [
    "Карта мемного момента 1",
    "Карта мемного момента 2",
    "Карта мемного момента 3",
    "Карта мемного момента 4",
    "Карта мемного момента 5",
    "Карта мемного момента 6",
    "Карта мемного момента 7",
]

class Player:
    def __init__(self, name, avatar):
        self.name = name
        self.avatar = avatar
        self.hand = []

    def draw_cards(self, amount=5):
        self.hand = random.sample(ALL_CARDS, amount)

class Game:
    def __init__(self, players):
        self.players = players          # список объектов Player
        self.deck = CARDS_POOL.copy()   # колода карт
        self.discarded = []             # уже сыгранные карты
        self.current_situation = "Фраза-ситуация на раунд"
        self.state = "waiting"          # "waiting", "playing", "voting"

    def deal_hands(self):
        for player in self.players:
            while len(player.hand) < 5 and len(self.deck) > 0:
                card = random.choice(self.deck)
                self.deck.remove(card)
                player.hand.append(card)
                self.discarded.append(card)

    def all_played(self):
        return all(p.current_card is not None for p in self.players)

    def reset_round(self):
        for p in self.players:
            p.current_card = None
        if len(self.deck) > 0:
            self.deal_hands()

    def play_card(self, player, card):
        if card not in player.hand:
            raise ValueError("Такой карты нет в руке")
        player.hand.remove(card)
        player.current_card = card
        self.discarded.append(card)

    def vote(self, votes):
        """
        votes: словарь {voter_name: voted_player_name}
        начисляем очки
        """
        points = {}
        for voter, vote_for in votes.items():
            points[vote_for] = points.get(vote_for, 0) + 1
        for p in self.players:
            if p.name in points:
                p.points += points[p.name]
        self.reset_round()

    def is_game_over(self):
        # игра заканчивается, когда карты закончились и все руки пусты
        return all(len(p.hand) == 0 for p in self.players) and len(self.deck) == 0
