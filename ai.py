from __future__ import absolute_import, division, print_function
import copy
import random
from game import Game

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1

# Tree node. To be used to construct a game tree.


class Node:
    # Recommended: do not modify this __init__ function
    def __init__(self, state, player_type):
        self.state = (state[0], state[1])

        # to store a list of (direction, node) tuples
        self.children = []

        self.player_type = player_type

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        # TODO: complete this
        return len(self.children) == 0

# AI agent. Determine the next move.


class AI:
    # Recommended: do not modify this __init__ function
    def __init__(self, root_state, search_depth=3):
        self.root = Node(root_state, MAX_PLAYER)
        self.search_depth = search_depth
        self.simulator = Game(*root_state)

    # (Hint) Useful functions:
    # self.simulator.current_state, self.simulator.set_state, self.simulator.move

    # TODO: build a game tree from the current node up to the given depth
    def build_tree(self, node=None, depth=0):
        if node is None:
            node = self.root

        if depth == 0:
            return

        current_state = self.simulator.current_state()
        self.simulator.set_state(init_tile_matrix=node.state[0], init_score=node.state[1])

        if node.player_type == MAX_PLAYER:
            for direction in range(4):
                state_before = self.simulator.current_state()
                if self.simulator.move(direction):
                    new_state = self.simulator.current_state()
                    child = Node(state=new_state, player_type=CHANCE_PLAYER)
                    node.children.append((direction, child))
                    self.build_tree(node=child, depth=depth - 1)
                self.simulator.set_state(init_tile_matrix=state_before[0], init_score=state_before[1])
        else:
            empty_tiles = self.simulator.get_open_tiles()
            if empty_tiles:
                state_matrix = copy.deepcopy(self.simulator.tile_matrix)
                current_score = self.simulator.score
                for pos in empty_tiles:
                    state_matrix[pos[0]][pos[1]] = 2
                    child = Node(state=(state_matrix, current_score), player_type=MAX_PLAYER)
                    node.children.append((None, child))
                    self.build_tree(node=child, depth=depth - 1)
                    state_matrix[pos[0]][pos[1]] = 0

        self.simulator.set_state(init_tile_matrix=current_state[0], init_score=current_state[1])

    def get_enhanced_score(self, state):
        matrix = state[0]
        base_score = state[1]

        empty_tiles = sum(row.count(0) for row in matrix)
        empty_bonus = empty_tiles * 10

        corners = [matrix[0][0], matrix[0][3], matrix[3][0], matrix[3][3]]
        max_tile = max(max(row) for row in matrix)
        corner_bonus = 0
        if max_tile in corners:
            corner_bonus = max_tile * 10

        merge_potential = 0
        for i in range(4):
            for j in range(3):
                if matrix[i][j] == matrix[i][j + 1] and matrix[i][j] != 0:
                    merge_potential += matrix[i][j]
                if matrix[j][i] == matrix[j + 1][i] and matrix[j][i] != 0:
                    merge_potential += matrix[j][i]

        total_score = (base_score + empty_bonus + corner_bonus + merge_potential * 10)
        return total_score

    # TODO: expectimax calculation.
    # Return a (best direction, expectimax value) tuple if node is a MAX_PLAYER
    # Return a (None, expectimax value) tuple if node is a CHANCE_PLAYER
    def expectimax(self, node=None, use_enhanced_score=True):
        # TODO: delete this random choice but make sure the return type of the function is the same
        if node is None:
            node = self.root

        if node.is_terminal():
            if not use_enhanced_score:
                return None, node.state[1]
            else:
                return None, self.get_enhanced_score(node.state)

        if node.player_type == MAX_PLAYER:
            best_value = float("-inf")
            best_move = None
            for move, child in node.children:
                _, value = self.expectimax(child)
                if value > best_value:
                    best_value = value
                    best_move = move
            return best_move, best_value
        else:
            total_value = 0
            for _, child in node.children:
                _, value = self.expectimax(child)
                total_value += value
            expected_value = total_value / len(node.children) if node.children else 0
            return None, expected_value

    # Return decision at the root
    def compute_decision(self):
        self.build_tree(self.root, self.search_depth)
        direction, _ = self.expectimax(self.root)
        return direction

    def compute_decision_ec(self):
        return random.randint(0, 3)
