import random

# create class to handle enemies, that appear in combat
class CombatEnemy:
    def __init__(self, name, hp, attack, element="physical", weaknesses=None, resistances=None, speed=8):
        self.name = name
        self.max_hp = hp
        self.hp = hp

        self.attack_power = attack
        self.element = element

        self.weaknesses = weaknesses if weaknesses else []
        self.resistances = resistances if resistances else []

        self.speed = speed
        self.defeated = False

# flag to check if enemy is alive/should be despawned
    def is_alive(self):
        return self.hp > 0

# dmg calc
    def take_damage(self, dmg, damage_type=None):
        base_dmg = dmg

# dmg multiplier
        if damage_type in self.weaknesses:
            dmg = int(dmg * 1.5)
            # print(f"[DEBUG] Weakness hit! {damage_type} deals {dmg} instead of {base_dmg}")
        elif damage_type in self.resistances:
            dmg = int(dmg * 0.5)
            # print(f"[DEBUG] Resistance! {damage_type} deals {dmg} instead of {base_dmg}")

        before = self.hp
        self.hp = max(0, self.hp - dmg)
        # print(f"[DEBUG] {self.name}: {before} -> {self.hp} after taking {dmg} {damage_type} damage")

# calc speed/turn order
    def effective_speed(self):
        return self.speed

# animations would be nice to have some type of feedback in the fight, but i cant do this no more
    def attack(self, player):
        dmg = random.randint(1, self.attack_power)
        # print(f"[DEBUG] {self.name} attacks for {dmg} damage")
        player.take_damage(dmg)
        return dmg

# enemy stats
# zombies have weak hp but resist physical dmg, they have ok attack and low speed
# skeletons have more hp, but are weak to physical (one of the starter elements), they deal less dmg, but are faster than zombies
# the timekeeper is the stat sheet for the first boss (no, you can not encounter him as of yet, yes, i know i suck, anyway
# he had more hp, more attack and is considerably faster, you need a strong deck to beat him and gotta make every turn count
# he is balanced around items you would get right before beating him (a puzzle before the encounter), increasing your hp, giving you a new strong card and increasing your speed
# as of now i advise to not spawn him because he will be absolutely op

ENEMY_DEFS = {
    "zombie": {
        "name": "Zombie",
        "hp": 20,
        "attack": 2,
        "element": "dark",
        "weaknesses": ["light"],
        "resistances": ["physical"],
        "speed": 5,
    },
    "skeleton": {
        "name": "Skeleton",
        "hp": 25,
        "attack": 1,
        "element": "physical",
        "weaknesses": ["physical"],
        "resistances": [],
        "speed": 7,
    },
    "time keeper": {
        "name": "Time Keeper",
        "hp": 50,
        "attack": 5,
        "element": "chaos",
        "weaknesses": ["void"],
        "resistances": ["physical"],
        "speed": 10,
    },
}

# creating combat enemy entity
def create_combat_enemy(enemy_type: str) -> CombatEnemy:
    data = ENEMY_DEFS.get(enemy_type)
    if not data:
        raise ValueError(f"Unknown enemy type: {enemy_type}")

    return CombatEnemy(
        name=data["name"],
        hp=data["hp"],
        attack=data["attack"],
        element=data.get("element", "physical"),
        weaknesses=data.get("weaknesses", []),
        resistances=data.get("resistances", []),
        speed=data.get("speed", 8)
    )