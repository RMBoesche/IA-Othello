import time
from typing import Tuple

from ..othello.gamestate import GameState
from ..othello.board import Board

MAX_COST_VALUE = 100000
MIN_COST_VALUE = -100000
MIN = 0
MAX = 1

max_depth = 2
_start_time = 0
_my_player = 0
_enemy_player = 0
_alfa_beta_cut = 0


# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.


def make_move(state: GameState) -> Tuple[int, int]:
    global max_depth
    """
    Returns an Othello move
    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """
    move = 0, 0

    if not state.board.has_legal_move(state.player):
        move = -1, -1
        return move
    
    # Final Burst
    free_tiles = state.board.piece_count['.']
    if free_tiles < 20:
        max_depth = 5
    elif free_tiles < 10:
        max_depth = 7

    global _start_time
    _start_time = time.time()

    move = next_move(state)

    stop_time = time.time()
    total_time = stop_time - _start_time

    
    return move

def next_move(state: GameState):
    global _my_player
    global _enemy_player

    _my_player = state.player
    _enemy_player = Board.opponent(state.player)

    value, move = MAX(state, state.player, (MIN_COST_VALUE,None), (MAX_COST_VALUE,None))
    return move


def MAX(state: GameState, current_player, alpha, beta, depth=0):
    if stop_search(depth):
        move_value = calculate_move_value(state), None
        return move_value

    if not state.board.has_legal_move(current_player):
        return MIN(state, Board.opponent(current_player), alpha, beta, depth + 1)

    move_value = MIN_COST_VALUE, None

    for legal_move in state.legal_moves():
        legal_move_value = MIN(state.next_state(legal_move), Board.opponent(current_player), alpha, beta, depth + 1)[0]
        legal_move_tuple = (legal_move_value, legal_move)

        move_value = choose(MAX,
                            move_value,
                            legal_move_tuple)

        alpha = choose(MAX,
                       alpha,
                       move_value)

        if (alpha[0] >= beta[0]):
            global _alfa_beta_cut
            _alfa_beta_cut += 1
            break

    return alpha


def MIN(state: GameState, current_player, alpha, beta, depth=0):
    if stop_search(depth):
        move_value = calculate_move_value(state), None
        return move_value
    
    if not state.board.has_legal_move(current_player):
        return MAX(state, Board.opponent(current_player), alpha, beta, depth + 1)

    move_value = MAX_COST_VALUE, None

    for legal_move in state.legal_moves():
        legal_move_value = MAX(state.next_state(legal_move), Board.opponent(current_player), alpha, beta, depth + 1)[0]
        legal_move_tuple = (legal_move_value, legal_move)

        move_value = choose(MIN,
                            move_value,
                            legal_move_tuple)

        beta = choose(MIN,
                      beta,
                      move_value)
        
        if (beta[0] <= alpha[0]):
            global _alfa_beta_cut
            _alfa_beta_cut += 1
            break

    return beta


def calculate_move_value(state: GameState):
    free_tiles = state.board.piece_count['.']

    if free_tiles >= 20:
        cost = static_cost(state)

    elif free_tiles >= 0:
        cost = static_cost(state) + 30*pieces_cost(state)

    return cost


def static_cost(state: GameState):
    cost = 0
    tiles = state.board.tiles

    static_board_tile_cost = [
        [800, -100, 20, 20, 20, 20, -100, 800],
        [-100, -150, -15, -1, -1, -15, -150, -100],
        [20, -15, 20, 0, 0, 20, -15, 20],
        [20, -1, 0, 10, 10, 0, -1, 20],
        [20, -1, 0, 10, 10, 0, -1, 20],
        [20, -15, 20, 0, 0, 20, -15, 20],
        [-100, -150, -15, -1, -1, -15, -150, -100],
        [800, -100, 20, 20, 20, 20, -100, 800]
    ]
    for line in range(8):
        for column in range(8):
            static = static_board_tile_cost[column][line]

            if tiles[column][line] == _my_player:
                cost += static

            if tiles[column][line] == _enemy_player:
                cost -= static
    return cost


def pieces_cost(state: GameState):
    my_pieces = state.board.num_pieces(_my_player)
    enemy_pieces = state.board.num_pieces(_enemy_player)

    pieces_cost = 100 * ((my_pieces - enemy_pieces) / (my_pieces + enemy_pieces))
    return int(pieces_cost)


def stop_search(depth):
    stop_time = time.time()
    total_time = stop_time - _start_time

    if total_time > 4.8:
        return True

    if depth >= max_depth:
        # print(max_depth)
        return True
    else:
        return False


def choose(type: int, value1: tuple, value2: tuple) -> tuple:
    if type == MIN:
        if value1[0] <= value2[0]:
            return value1
        else:
            return value2

    if type == MAX:
        if value1[0] >= value2[0]:
            return value1
        else:
            return value2

    return None
