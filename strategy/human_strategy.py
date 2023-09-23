# This defines the general layout your strategy method will inherit. Do not edit this.

from game.character.action.ability_action import AbilityAction
from game.character.action.attack_action import AttackAction
from game.character.action.move_action import MoveAction
from game.character.character_class_type import CharacterClassType
from game.game_state import GameState
from game.util.position import Position
import random

class human_strategy:
    def decide_character_classes(
        self,
        possible_classes: list[CharacterClassType],
        num_to_pick: int,
        max_per_same_class: int,
    ) -> dict[CharacterClassType, int]:
        """
        Decide the character classes your humans will use (only called on humans first turn)

        possible_classes: A list of the possible classes you can select from
        num_to_pick: The total number of classes you are allowed to select
        max_per_same_class: The max number of characters you can have in the same class

        You should return a dictionary of class type to the number you want to use of that class
        """
        choices = {
            CharacterClassType.MARKSMAN: random.randint(1, 5),
            CharacterClassType.MEDIC: random.randint(1, 5),
            CharacterClassType.TRACEUR: random.randint(1, 5),
            CharacterClassType.DEMOLITIONIST: random.randint(1, 5),
        }
        return choices

    def decide_moves(
        self, possible_moves: dict[str, list[MoveAction]], game_state: GameState
    ) -> list[MoveAction]:
        """
        Decide the moves for each character based on the current game state

        possible_moves: Maps character id to it's possible moves. You can use this to validate if a move is possible, or pick from this list.
        game_state: The current state of all characters and terrain on the map
        """
        choices = []
        for cid, moves in possible_moves.items():
            if not moves:
                continue
            # humanPos = game_state.characters[cid].position
            closest = float('inf')
            best = moves[0]
            for move in moves:
                for char in game_state.characters.values():
                    if char.is_zombie:
                        distance = abs(char.position.x - move.destination.x) + abs(char.position.y - move.destination.y)
                        if distance < closest:
                            closest = distance
                            best = move
            choices.append(best)
        return choices

    def decide_attacks(
        self, possible_attacks: dict[str, list[AttackAction]], game_state: GameState
    ) -> list[AttackAction]:
        """
        Decide the attacks for each character based on the current game state
        """
        choices = []
        for cid, attacks in possible_attacks.items():
            if not attacks:
                continue
            closest = float('inf')
            best = attacks[0]
            for attack in attacks:
                if attack.type == AttackAction.CHARACTER:
                    zombiePos = game_state.characters[attack.attacking_id].position
                    humanPos = game_state.characters[cid].position
                    distance = abs(zombiePos.x - humanPos.x) + abs(zombiePos.y - humanPos.y)
                    if distance <= closest:
                        closest = distance
                        best = attack
            choices.append(best)
        return choices


    def decide_abilities(
        self, possible_abilities: dict[str, list[AbilityAction]], game_state: GameState
    ) -> list[AbilityAction]:
        """
        Decide the moves for each character based on the current game state

        possible_abilities: Maps character id to it's possible abilities. You can use this to validate if a ability is possible, or pick from this list.
        game_state: The current state of all characters and terrain on the map
        """
        choices = []
        for cid, abilities in possible_abilities.items():
            if not abilities:
                continue
            if game_state.characters[cid].class_type == CharacterClassType.MEDIC:
                lowHP = float('inf')
                bestAb = abilities[0]
                for ability in abilities:
                    target_human_health = game_state.characters[ability.character_id_target].health
                    if target_human_health < lowHP:
                        lowHP = target_human_health
                        bestAb = ability
                choices.append(bestAb)
        return choices

