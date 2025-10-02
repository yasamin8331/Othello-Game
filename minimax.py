from board import Board
from utils import raiseNotDefined

def minimax(board, depth, maximizing_player, player_color,use_pruning=False,alpha = -float('inf'),beta = float('inf')):
    """
    Implements the Minimax algorithm to determine the best move for a player in an Othello game.

    Args:
        board (Board): The current game board.
        depth (int): The remaining depth to search in the game tree.
        maximizing_player (bool): A boolean indicating whether the current player is the maximizing player.
        player_color (str): The color of the current player ('B' for black, 'W' for white).

    Returns:
        tuple: A tuple containing the best move (row, col) and its evaluation score (int). 
               If no valid moves are available, returns (None, evaluation score).
    """
    if depth == 0 :
        return None, evaluate_board(board, player_color)
    
    if (not board.get_valid_moves('B') and not board.get_valid_moves('W')):
        return None, evaluate_board(board, player_color)
    
    valid_moves = board.get_valid_moves(player_color)
    if not valid_moves:
        return None, evaluate_board(board, player_color)
    
    best_move = None
    if maximizing_player:

        maxScore = -float('inf')

        for move in valid_moves:

            new_board = copy_board(board)
            new_board.place_disc(move[0], move[1], player_color)
            _, score = minimax(new_board, depth-1, False, player_color, use_pruning, alpha, beta)
            
            if score > maxScore:
                maxScore = score
                best_move = move

            if use_pruning:

                alpha = max(alpha, score)

                if beta <= alpha:

                    break

        return best_move, maxScore
    
    else:

        min_eval = float('inf')
        opponent_color = 'W' if player_color == 'B' else 'B'
        
        for move in valid_moves:

            new_board = copy_board(board)
            new_board.place_disc(move[0], move[1], opponent_color)
            _, score = minimax(new_board, depth-1, True, player_color, use_pruning, alpha, beta)
            
            if score < min_eval:

                min_eval = score
                best_move = move
            
            if use_pruning:

                beta = min(beta, score)

                if beta <= alpha:

                    break
                
        return best_move, min_eval


    
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
    """
    Creates a deep copy of the current board to simulate future moves without altering the original.

    Args:
        board (Board): The current game board to be copied.

    Returns:
        Board: A new Board object with the same state as the original.
    """
    new_board = Board(board.size)
    new_board.board = [row[:] for row in board.board]
    return new_board