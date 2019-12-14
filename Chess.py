from collections import deque
import heapq
import time

# Board:
# -1 --> NOT MOVEABLE
# 0 --> EMPTY
# 1 --> RED
# 2 --> BLUE
# 3 --> GOLDEN


# CONFIGURATION
INITIAL_BOARD = [2, 0, 0, 1, 0, -1, 0, 2, 0, 0, 0, -1, 1, 2, -1, 0]
WINNING_BOARD = [1, 0, 2, 0, 0, -1, 0, 0, 0, 0, 0, -1, 1, 2, -1, 2]

SPEEDUP = False  # May be turned on for speed, may NOT be optimal
#

assert len(WINNING_BOARD) == len(INITIAL_BOARD)
assert len(WINNING_BOARD) in [9, 12, 16, 20, 25]

print("Starting.. Speedup: {}".format(SPEEDUP))


LEN_X = 1
LEN_Y = 1

if len(WINNING_BOARD) == 9:
    LEN_X = 3
    LEN_Y = 3

elif len(WINNING_BOARD) == 12:
    LEN_X = 3
    LEN_Y = 4

elif len(WINNING_BOARD) == 16:
    LEN_X = 4
    LEN_Y = 4

elif len(WINNING_BOARD) == 20:
    LEN_X = 4
    LEN_Y = 5

elif len(WINNING_BOARD) == 25:
    LEN_X = 5
    LEN_Y = 5


LEN = LEN_X * LEN_Y


class ChessBoard:
    def __init__(self, board, parent):
        self.board = board
        self.parent = parent

        if SPEEDUP:
            self.value = self.generate_value()

    def is_winner(self):
        return [0 if x == 3 else x for x in self.board] == WINNING_BOARD

    def generate_value(self):
        counter = 0
        for i in range(len(WINNING_BOARD)):
            if WINNING_BOARD[i] == self.board[i] and self.board[i] != 0 and self.board[i] != -1:
                counter += 1

        return counter


def get_valid_moves(board):
    moves = []

    for i, x in enumerate(board.board):
        if x != 0 and x != -1:
            if i + 2 * LEN_X - 1 < LEN and i % LEN_X - 1 >= 0 and board.board[i + 2 * LEN_X - 1] == 0:
                moves.append((i, i + 2 * LEN_X - 1))

            if i + 2 * LEN_X + 1 < LEN and i % LEN_X + 1 < LEN_X and board.board[i + 2 * LEN_X + 1] == 0:
                moves.append((i, i + 2 * LEN_X + 1))

            if i - 2 * LEN_X + 1 >= 0 and i % LEN_X + 1 < LEN_X and board.board[i - 2 * LEN_X + 1] == 0:
                moves.append((i, i - 2 * LEN_X + 1))

            if i - 2 * LEN_X - 1 >= 0 and i % LEN_X - 1 >= 0 and board.board[i - 2 * LEN_X - 1] == 0:
                moves.append((i, i - 2 * LEN_X - 1))

            if i % LEN_X - 2 >= 0 and i - LEN_X - 2 >= 0 and board.board[i - LEN_X - 2] == 0:
                moves.append((i, i - LEN_X - 2))

            if i % LEN_X - 2 >= 0 and i + LEN_X - 2 < LEN and board.board[i + LEN_X - 2] == 0:
                moves.append((i, i + LEN_X - 2))

            if i % LEN_X + 2 < LEN_X and i - LEN_X + 2 >= 0 and board.board[i - LEN_X + 2] == 0:
                moves.append((i, i - LEN_X + 2))

            if i % LEN_X + 2 < LEN_X and i + LEN_X + 2 < LEN and board.board[i + LEN_X + 2] == 0:
                moves.append((i, i + LEN_X + 2))

    return moves


def get_board(board, move):  # move -> tuple (index_before, index_after)
    new_board = board.board[:]

    new_board[move[1]] = new_board[move[0]]
    new_board[move[0]] = 0

    return ChessBoard(new_board, board)


def list_to_string(l):
    return "".join(str(l))


def bfs(node):
    heap = []
    queue = []

    if SPEEDUP:
        heapq.heappush(heap, (-node.value, node))
    else:
        queue = deque([node])

    visited = set()

    k = 0
    while True:    # Since solvability is guaranteed this is equivalent: while queue:
        if k % 100000 == 0:
            if SPEEDUP:
                print(len(heap))
            else:
                print(len(queue))

        if SPEEDUP:
            pop = heapq.heappop(heap)[1]
        else:
            pop = queue.popleft()

        if pop.is_winner():
            return pop

        for x in get_valid_moves(pop):
            node_ = get_board(pop, x)

            if list_to_string(node_.board) not in visited:
                visited.add(list_to_string(node_.board))
                if SPEEDUP:
                    heapq.heappush(heap, (-node_.value, node_))
                else:
                    queue.append(node_)

        k += 1


def board_print(board):
    print("\n")
    for i in range(LEN_Y):
        print(board[i * LEN_X:(i + 1) * LEN_X])


start_time = time.time()

root = ChessBoard(INITIAL_BOARD, None)
winner = bfs(root)

a = 0
while winner is not None:
    a += 1
    board_print(winner.board)

    winner = winner.parent


print("--- %s seconds ---" % (time.time() - start_time))
print("Win in {} Moves. If SPEEDUP == True, this may NOT be optimal.".format(a - 1))

