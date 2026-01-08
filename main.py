import math

# -----------------------------
# Game State
# -----------------------------
board = [" " for _ in range(9)]
HUMAN = "X"
AI = "O"

stats = {"wins": 0, "losses": 0, "draws": 0}


# -----------------------------
# UI Helpers
# -----------------------------
def print_board():
    print("\n")
    for i in range(0, 9, 3):
        print(f" {board[i]} | {board[i+1]} | {board[i+2]} ")
        if i < 6:
            print("---+---+---")
    print("\n")


def print_stats():
    print(f"Wins: {stats['wins']} | Losses: {stats['losses']} | Draws: {stats['draws']}")


# -----------------------------
# Game Logic
# -----------------------------
def available_moves():
    return [i for i, spot in enumerate(board) if spot == " "]


def check_winner(player):
    win_conditions = [
        [0,1,2],[3,4,5],[6,7,8],  # rows
        [0,3,6],[1,4,7],[2,5,8],  # columns
        [0,4,8],[2,4,6]           # diagonals
    ]
    return any(all(board[i] == player for i in combo) for combo in win_conditions)


def is_draw():
    return " " not in board


# -----------------------------
# Minimax Algorithm
# -----------------------------
def minimax(is_maximizing):
    if check_winner(AI):
        return 1
    if check_winner(HUMAN):
        return -1
    if is_draw():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for move in available_moves():
            board[move] = AI
            score = minimax(False)
            board[move] = " "
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for move in available_moves():
            board[move] = HUMAN
            score = minimax(True)
            board[move] = " "
            best_score = min(score, best_score)
        return best_score


def ai_move():
    best_score = -math.inf
    move = None
    for i in available_moves():
        board[i] = AI
        score = minimax(False)
        board[i] = " "
        if score > best_score:
            best_score = score
            move = i
    board[move] = AI


# -----------------------------
# Game Loop
# -----------------------------
def play_game():
    board[:] = [" " for _ in range(9)]
    print_board()

    while True:
        # Human Turn
        move = int(input("Choose position (0-8): "))
        if board[move] != " ":
            print("Invalid move.")
            continue
        board[move] = HUMAN
        print_board()

        if check_winner(HUMAN):
            print("You Win!")
            stats["wins"] += 1
            break
        if is_draw():
            print("Draw!")
            stats["draws"] += 1
            break

        # AI Turn
        ai_move()
        print("AI Move:")
        print_board()

        if check_winner(AI):
            print("You Lose!")
            stats["losses"] += 1
            break
        if is_draw():
            print("Draw!")
            stats["draws"] += 1
            break

    print_stats()


# -----------------------------
# Main Menu
# -----------------------------
while True:
    play_game()
    again = input("Play again? (y/n): ").lower()
    if again != "y":
        break