import random
from core.inventory import PlayerInventory
from screens.combat_screen import Card

# safe data, preserved over the course of one game (i am too lazy to add a safe and load option, im sorry) 40+ hours is enough
class PlayerData:
    def __init__(self):

        self.inventory = PlayerInventory()

        self.card_library = self.build_card_library()

        self.deck = self.build_starter_deck()

        self.max_hp = 20
        self.hp = self.max_hp

    # add an unlock flag in the far future (after hand-in)
    # also all cards, # out is locked cards, yes i know it needs an unlocked flag, no i wont do it now
    def build_card_library(self):
        library = []

        # Damage
        library.append(Card("Light Blast", 2, "damage", (5, 6), element="light"))
        library.append(Card("Dark Bolt", 2, "damage", (5, 6), element="dark"))
        # library.append(Card("Chaos Blast", 4, "damage", (7, 9), element="chaos"))
        library.append(Card("Attack", 1, "damage", (3, 5), element="physical"))

        # Buffs
        library.append(Card("Defensive", 3, "buff", ("defensive_turns", 3)))
        library.append(Card("Powerful", 3, "buff", ("powerful_turns", 3)))
        # library.append(Card("Barrier", 3, "buff", ("barrier_turns", 1)))
        # library.append(Card("Haste", 2, "buff", ("haste_turns", 3)))

        # Debuffs
        library.append(Card("Defenceless", 3, "debuff", ("defenceless_turns", 3)))
        library.append(Card("Powerless", 3, "debuff", ("powerless_turns", 3)))
        #library.append(Card("Slow", 2, "debuff", ("slow_turns", 3)))

        # Specials
        library.append(Card("Gain Charge", 0, "special", "gain_charge"))
        library.append(Card("Redraw", 0, "special", "redraw"))

        # Heal
        library.append(Card("Heal", 2, "heal", (3, 5)))

        return library

# deck when starting the game
    def build_starter_deck(self):
        deck = []

        for _ in range(4):
            deck.append(Card("Attack", 1, "damage", (3, 5), element="physical"))
        for _ in range(2):
            deck.append(Card("Heal", 2, "heal", (3, 5)))
        for _ in range(2):
            deck.append(Card("Defenceless", 3, "debuff", ("defenceless_turns", 3)))
        for _ in range(2):
            deck.append(Card("Powerless", 3, "debuff", ("powerless_turns", 3)))

        random.shuffle(deck)

        return deck

# this isnt really tied into anything, its for the future when safe/heal points are added (and hp is tracked across combats)
    def heal_full(self):
        self.hp = self.max_hp
