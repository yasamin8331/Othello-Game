from board import Board
from utils import raiseNotDefined
import random

def expectimax(board, depth, maximizing_player, player_color):
    """
    Perform the Expectimax algorithm to evaluate and choose the optimal move in a two-player game.

    Expectimax is a variation of the minimax algorithm used in games of chance or imperfect information,
    where instead of choosing the best or worst move, it computes the expected value of a move based on
    possible outcomes.

    Parameters:
    -----------
    board : Board
        The current state of the game board. It should support methods such as `is_full`, `get_valid_moves`,
        and `place_disc`.
    depth : int
        The remaining depth to search. When the depth reaches 0, the algorithm stops searching further moves.
    maximizing_player : bool
        A flag to indicate whether the current node is for the maximizing player (True) or the opponent (False).
    player_color : str
        The color ('B' for black or 'W' for white) representing the player who is maximizing their score.

    Returns:
    --------
    best_move : tuple or None
        The best move for the maximizing player in the form (row, col). None is returned when calculating
        the expected value for the opponent's move.
    evaluation : float
        The evaluation score of the board from the perspective of the player using the `evaluate_board` function.

    Notes:
    ------
    - The function recursively explores possible moves down to the specified depth and evaluates the board using
      the `evaluate_board` function.
    - For the maximizing player, it selects the move that maximizes the evaluation score.
    - For the opponent, it calculates the expected value based on all valid moves.
    - The algorithm returns once the depth reaches 0 or if the board is full, in which case it evaluates the current
      board state.
    """

    if depth == 0 :
        return None, evaluate_board(board, player_color)
    
    if (not board.get_valid_moves('B') and not board.get_valid_moves('W')):
        return None, evaluate_board(board, player_color)
    
    valid_moves = board.get_valid_moves(player_color if maximizing_player else ('W' if player_color == 'B' else 'B'))
    if not valid_moves:
        return None, evaluate_board(board, player_color)
    
    if maximizing_player:

        maxScore = -float('inf')
        best_move = None

        for move in valid_moves:
            new_board = copy_board(board)
            new_board.place_disc(move[0], move[1], player_color)
            _, score = expectimax(new_board, depth-1, False, player_color)

            if score > maxScore:
                maxScore = score
                best_move = move

        return best_move, maxScore
    
    else:
        expected_value = 0

        for move in valid_moves:

            new_board = copy_board(board)
            opponent_color = 'W' if player_color == 'B' else 'B'
            new_board.place_disc(move[0], move[1], opponent_color)
            _, score = expectimax(new_board, depth-1, True, player_color)
            expected_value += score
            
        return None, expected_value / len(valid_moves)


    raiseNotDefined()

def evaluate_board(board, player_color):
    """
    Evaluates the current board state for a given player by considering the score, corner occupation,
    edge control, and mobility.

    Args:
        board (Board): The current game board.
        player_color (str): The color of the player to evaluate the score for ('B' for black, 'W' for white).

    Returns:
        int: An evaluation score where a positive value favors the player, and a negative value favors the opponent.
    """
    # Get the basic score
    B_score, W_score = board.get_score()
    score = W_score - B_score if player_color == 'W' else B_score - W_score

    # Define opponent color
    opponent_color = 'W' if player_color == 'B' else 'B'
    
    # Corner weights
    corners = [(0, 0), (0, board.size - 1), (board.size - 1, 0), (board.size - 1, board.size - 1)]
    corner_score = 0
    for r, c in corners:
        if board.board[r][c] == player_color:
            corner_score += 25
        elif board.board[r][c] == opponent_color:
            corner_score -= 25

    # Edge control weights
    edge_score = 0
    for i in range(1, board.size - 1):
        if board.board[0][i] == player_color:
            edge_score += 5
        elif board.board[0][i] == opponent_color:
            edge_score -= 5
        if board.board[board.size - 1][i] == player_color:
            edge_score += 5
        elif board.board[board.size - 1][i] == opponent_color:
            edge_score -= 5
        if board.board[i][0] == player_color:
            edge_score += 5
        elif board.board[i][0] == opponent_color:
            edge_score -= 5
        if board.board[i][board.size - 1] == player_color:
            edge_score += 5
        elif board.board[i][board.size - 1] == opponent_color:
            edge_score -= 5

    # Mobility: the number of valid moves
    player_moves = len(board.get_valid_moves(player_color))
    opponent_moves = len(board.get_valid_moves(opponent_color))
    mobility_score = (player_moves - opponent_moves) * 2

    # Combine all scores
    total_score = score + corner_score + edge_score + mobility_score
    return total_score


def copy_board(board):
    new_board = Board(board.size)
    new_board.board = [row[:] for row in board.board]
    return new_board
