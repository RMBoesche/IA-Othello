import time
from typing import Tuple

from ..othello.gamestate import GameState
from ..othello.board import Board

MAX_COST_VALUE = 10000
MIN_COST_VALUE = -10000
MIN = 0
MAX = 1

_start_time = 0
_my_player = 0
_enemy_player = 0
_alfa_beta_cut = 0
max_depth = 5


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
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/c)
    """
    move = 0, 0

    if not state.board.has_legal_move(state.player):
        move = -1, -1
        return move
    
    free_tiles = state.board.piece_count['.']
    if free_tiles < 10:
        max_depth = 10
    elif free_tiles < 20:
        max_depth = 8
    elif free_tiles < 30:
        max_depth = 6

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
    if stop(depth):
        move_value = calculate_move_value(state), None
        return move_value

    if not state.board.has_legal_move(current_player):
        return MIN(state, Board.opponent(current_player), alpha, beta, depth + 1)

    move_value = MIN_COST_VALUE, None

    for legal_move in state.legal_moves():
        legal_move_value = MIN(state.next_state(legal_move), Board.opponent(current_player), alpha, beta, depth + 1)[0]
        legal_move_tuple = (legal_move_value, legal_move)

        move_value = best_value(MAX,
                            move_value,
                            legal_move_tuple)

        alpha = best_value(MAX,
                       alpha,
                       move_value)

        if (alpha[0] >= beta[0]):
            global _alfa_beta_cut
            _alfa_beta_cut += 1
            break

    return alpha


def MIN(state: GameState, current_player, alpha, beta, depth=0):
    if stop(depth):
        move_value = calculate_move_value(state), None
        return move_value
    
    if not state.board.has_legal_move(current_player):
       return MAX(state, Board.opponent(current_player), alpha, beta, depth + 1)

    move_value = MAX_COST_VALUE, None

    for legal_move in state.legal_moves():
        legal_move_value = MAX(state.next_state(legal_move), Board.opponent(current_player), alpha, beta, depth + 1)[0]
        legal_move_tuple = (legal_move_value, legal_move)

        move_value = best_value(MIN,
                            move_value,
                            legal_move_tuple)

        beta = best_value(MIN,
                      beta,
                      move_value)
        
        if (beta[0] <= alpha[0]):
            global _alfa_beta_cut
            _alfa_beta_cut += 1
            break

    return beta


def calculate_move_value(state: GameState):
    free_tiles = state.board.piece_count['.']

    if free_tiles >= 15:
        cost = static_cost(state)

    elif free_tiles >= 0:
        cost = static_cost(state) + 25*pieces_cost(state)

    return cost


def static_cost(state: GameState):
    cost = 0
    tiles = state.board.tiles

    static_board_tile_cost = [
        [1000 , -200, 100,  50,  50, 100, -200,  1000],
        [-200, -500, -50, -50, -50, -50, -500, -200],
        [100 ,  -50, 100,   0,   0, 100,  -50,  100],
        [50  ,  -50,   0,   0,   0,   0,  -50,   50],
        [50  ,  -50,   0,   0,   0,   0,  -50,   50],
        [100 ,  -50, 100,   0,   0, 100,  -50,  100],
        [-200, -500, -50, -50, -50, -50, -500, -200],
        [1000 , -200, 100,  50,  50, 100, -200,  1000]
    ]
    for l in range(8):
        for c in range(8):
            static = static_board_tile_cost[c][l]

            if tiles[c][l] == _my_player:
                cost += static

            if tiles[c][l] == _enemy_player:
                cost -= static
    return cost


def pieces_cost(state: GameState):
    my_pieces = state.board.num_pieces(_my_player)
    enemy_pieces = state.board.num_pieces(_enemy_player)

    pieces_cost = 50 * ((my_pieces - enemy_pieces) / (my_pieces + enemy_pieces))
    return int(pieces_cost)


def stop(depth):
    stop_time = time.time()
    total_time = stop_time - _start_time

    if total_time > 4.8:
        return True

    if depth >= max_depth:
        return True
    else:
        return False


def best_value(type: int, value1: tuple, value2: tuple) -> tuple:
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
