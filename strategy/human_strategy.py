# This defines the general layout your strategy method will inherit. Do not edit this.

#TODO:
'''
1. Hard code following paths:
    - maze
    - top left
    - top right entrance
    - water
    - bottom right triangle
2. Top right demolitionist breaks the wall, then him and the builder and a medic chill in there - builder keeps building randomly inside
3. Top left - traceurs avoid zombies - in a 30x30 zone - 1 healer keeps healing them
4. River - go through the entrance and split the characters randomly between left and right
'''

from game.character.action.ability_action import AbilityAction
from game.character.action.ability_action_type import AbilityActionType
from game.character.action.attack_action import AttackAction
from game.character.action.move_action import MoveAction
from game.character.character_class_type import CharacterClassType
from game.game_state import GameState
from game.util.position import Position
from strategy.population_heatmap import PopulationHeatmap
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
            CharacterClassType.MARKSMAN: 0.1*dict[num_to_pick],
            CharacterClassType.MEDIC: 0.1*dict[num_to_pick],
            CharacterClassType.TRACEUR: 0.2*dict[num_to_pick],
            CharacterClassType.DEMOLITIONIST: 0.05*dict[num_to_pick],
            CharacterClassType.BUILDER: 0.1*dict[num_to_pick],
            CharacterClassType.NORMAL: 0.45*dict[num_to_pick],
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

        for [character_id, moves] in possible_moves.items():
            if len(moves) == 0:  # No choices... Next!
                continue
            
            #TODO: Implement max distance algorithm for the tracers in the top left using the heatmap

            heatmap = PopulationHeatmap(game_state)
            heatmap.calcHeatmap()
            highest_heatmap_y, highest_heatmap_x = heatmap.hottest()

            pos = game_state.characters[character_id].position  # position of the zombie

            closest_human_pos = pos  # default position is zombie's pos
            closest_human_distance = 1984  # large number, map isn't big enough to reach this distance
            
            count_tracer, count_medic, count_builder, count_demolisher = 0, 0, 0, 0
            firstTracer, secondTracer, thirdTracer, fourthTracer, fifthTracer  = Position((3, 0)), Position((1, 1)), Position((2,0)), Position((99, 99)), Position((0, 65))
            firstMedic, secondMedic, thirdMedic, fourthMedic = Position(1, 0), Position(97, 0), Position(95, 95), Position(0, 90)
            
            # Iterate through every human to find the closest one
            for c in game_state.characters.values():
                if c.is_zombie:
                    continue  # Fellow zombies are frens :D, ignore them

                distance = abs(c.position.x - pos.x) + abs(c.position.y - pos.y) # calculate manhattan distance between human and zombie
                if distance < closest_human_distance:  # If distance is closer than current closest, replace it!
                    closest_human_pos = c.position
                    closest_human_distance = distance

            if (closest_human_distance < 10):
                    
                    move_distance = 1337  # Distance between the move action's destination and the closest human
                    move_choice = moves[0]  # The move action the zombie will be taking
                    for m in moves:
                        distance = abs(m.destination.x - closest_human_pos.x) + abs(m.destination.y - closest_human_pos.y)  # calculate manhattan distance

                        # If distance is closer, that's our new choice!
                        if distance < move_distance:  
                            move_distance = distance
                            move_choice = m

                    choices.append(move_choice)  # add the choice to the list
            else:
                # Move as close to the human as possible
                move_distance = 1337  # Distance between the move action's destination and the closest human
                move_choice = moves[0]  # The move action the zombie will be taking
                highest_heatmap_x = highest_heatmap_x * 10 + 5
                highest_heatmap_y = highest_heatmap_y * 10 + 5
                for m in moves:
                    distance = abs(m.destination.x - highest_heatmap_x) + abs(m.destination.y - highest_heatmap_y)  # calculate manhattan distance

                    # If distance is closer, that's our new choice!
                    if distance < move_distance:  
                        move_distance = distance
                        move_choice = m

                choices.append(move_choice)  # add the choice to the list

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
                
            if game_state.characters[cid].class_type == CharacterClassType.BUILDER:
                for ability in abilities:
                    # for i in game_state.characters:
                    #     if game_state.characters[cid].position == ability.positional_target: 
                    #         choices.           
                    # for i in game_state.terrains:
                    #     if game_state.terrains[cid].position == ability.positional_target:
                    if ability.positional_target == game_state.characters[cid].position:
                        choices.append(ability)
                
            if game_state.characters[cid].class_type == CharacterClassType.DEMOLITIONIST:
                for ability in abilities:
                    if ability.positional_target == game_state.characters[cid].position:
                        if ability.positional_target is None:
                            choices.append(ability)
            
            if game_state.characters[cid].class_type == CharacterClassType.NORMAL:
                lowHP = float('inf')
                bestAb = abilities[0]
                for ability in abilities:
                    target_human_health = game_state.characters[ability.character_id_target].health
                    if target_human_health < lowHP:
                        lowHP = target_human_health
                        bestAb = ability
                choices.append(bestAb)
            
            if game_state.characters[cid].class_type == CharacterClassType.TRACEUR:
                lowHP = float('inf')
                bestAb = abilities[0]
                for ability in abilities:
                    target_human_health = game_state.characters[ability.character_id_target].health
                    if target_human_health < lowHP:
                        lowHP = target_human_health
                        bestAb = ability
                choices.append(bestAb)
        return choices
    
    

