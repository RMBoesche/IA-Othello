import time
from typing import Tuple

from ..othello.gamestate import GameState
from ..othello.board import Board

MAX_COST_VALUE = 100000
MIN_COST_VALUE = -100000

_depth = 5
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
    """
    Returns an Othello move
    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """
    move = 0, 0

    if not state.board.has_legal_move(state.player):
        move = -1, -1
        return move
    
    # Control the time
    global _start_time
    _start_time = time.time()
    move = play_othello(state)
    stop_time = time.time()
    total_time = stop_time - _start_time

    # Back Depth to normal if something strange happens
    global _depth
    if _depth <= 0:
        _depth = 4

    # Normal Throttle
    if total_time < 0.5:
        _depth += 1
    if total_time > 4.85:
        _depth -= 1

    # Final Burst
    free_tiles = state.board.piece_count['.']
    if free_tiles < 40:
        if total_time < 0.3:
            _depth += 1
    if free_tiles < 20:
        if total_time < 0.3:
            _depth += 2
    elif free_tiles < 10:
        if total_time < 0.3:
            _depth += 4
    
    return move

def play_othello(state: GameState):
    global _my_player
    global _enemy_player

    _my_player = state.player
    _enemy_player = oposite_player(state.player)

    value, move = MAX(state, state.player, (MIN_COST_VALUE,None), (MAX_COST_VALUE,None))
    return move


def MAX(state: GameState, current_player, alpha, beta, depth=0):
    if stop_search(depth):
        value_move = evaluate_board(state), None
        return value_move

    if not state.board.has_legal_move(current_player):
        return MIN(state, oposite_player(current_player), alpha, beta, depth + 1)

    value_move = MIN_COST_VALUE, None

    for legal_move in state.board.legal_moves(current_player):
        value_move = choose('max',
                            value_move,
                            (MIN(state.next_state(legal_move), oposite_player(current_player), alpha, beta, depth + 1)[0], legal_move))

        alpha = choose('max', alpha, value_move)

        if (alpha[0] >= beta[0]):
            global _alfa_beta_cut
            _alfa_beta_cut += 1
            break

    return alpha


def MIN(state: GameState, current_player, alpha, beta, depth=0):
    if stop_search(depth):
        value_move = evaluate_board(state), None
        return value_move
    
    if not state.board.has_legal_move(_my_player):
        return MAX(state, _enemy_player, alpha, beta, depth + 1)

    value_move = MAX_COST_VALUE, None

    for legal_move in state.board.legal_moves(current_player):
        value_move = choose('min',
                            value_move,
                            (MAX(state.next_state(legal_move), oposite_player(current_player), alpha, beta, depth + 1)[0],
                            legal_move))

        beta = choose('min', beta, value_move)
        
        if (beta[0] <= alpha[0]):
            global _alfa_beta_cut
            _alfa_beta_cut += 1
            break

    return beta


def evaluate_board(state: GameState):
    free_tiles = state.board.piece_count['.']
    if free_tiles >= 20:
        cost = static_cost(state)
    elif free_tiles >= 10:
        cost = 2*static_cost(state) + mobility(state)
    elif free_tiles >= 0:
        cost = mobility(state) + pieces_cost(state)
    else:
        cost = static_cost(state)
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


def mobility(state: GameState):
    my_mobility = len(state.board.legal_moves(_my_player))
    enemy_mobility = len(state.board.legal_moves(_enemy_player))

    if(my_mobility + enemy_mobility != 0):
        actual_mobility = 10*((my_mobility - enemy_mobility)/(my_mobility+enemy_mobility))
        return int(actual_mobility)
    else:
        return 0


def pieces_cost(state: GameState):
    my_pieces = state.board.num_pieces(_my_player)
    enemy_pieces = state.board.num_pieces(_enemy_player)

    pieces_cost = 100 * ((my_pieces - enemy_pieces) / (my_pieces + enemy_pieces))
    return int(pieces_cost)


def stop_search(depth):
    stop_time = time.time()
    total_time = stop_time - _start_time
    if total_time > 4.85:
        return True

    if depth >= _depth:
        return True
    else:
        return False


def oposite_player(player):
    if player == Board.WHITE:
        return Board.BLACK
    else:
        return Board.WHITE


def choose(type: str, value1: tuple, value2: tuple) -> tuple:
    if type == 'max':
        if value1[0] >= value2[0]:
            return value1
        else:
            return value2
    if type == 'min':
        if value1[0] <= value2[0]:
            return value1
        else:
            return value2
    return None
