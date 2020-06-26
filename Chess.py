from collections import deque
from tkinter import *
import math
import itertools
import heapq
import time

# Board:
# -1 --> NOT MOVEABLE
# 0 --> EMPTY
# 1 --> RED
# 2 --> BLUE
# 3 --> GOLDEN


# CONFIGURATION
INITIAL_BOARD = [2,3,1,2,-1,
                 3,2,2,-1,-1,
                 1,1,3,3,-1,
                 -1,3,-1,1,0,
                 0,3,3,3,2]
WINNING_BOARD = [0,2,1,1,-1,
                 2,2,1,-1,-1,
                 1,0,0,0,-1,
                 -1,0,-1,2,0,
                 0,0,0,2,0]

# SPEEDUP OR SPEEDUP_EXP, NOT both!
SPEEDUP = False  # May be turned on for speed, Heuristic: Out of Position
SPEEDUP_EXP = True  # Non-admissible heuristic, very fast, probably NOT optimal
#

assert len(WINNING_BOARD) == len(INITIAL_BOARD)
assert len(WINNING_BOARD) in [9, 12, 16, 20, 25]

print("Starting...")

master = Tk();
canvas_width = 1200;
canvas_height = 960;
drawing = Canvas(master, width=canvas_width, height=canvas_height);
drawing.pack();

x_position = 0;
y_position = 0;
max_x = (canvas_width/120)-1;

LEN_X = 1;
LEN_Y = 1;

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
    def __init__(self, board, parent, depth):
        self.board = board
        self.parent = parent
        self.depth = depth + 1

        if SPEEDUP:
            self.value = self.generate_value() + self.depth

        elif SPEEDUP_EXP:
            self.value = self.generate_value()

    def is_winner(self):
        return [0 if x == 3 else x for x in self.board] == WINNING_BOARD

    def generate_value(self):
        counter = 0
        for i in range(LEN):
            if WINNING_BOARD[i] == 1 or WINNING_BOARD[i] == 2:
                if WINNING_BOARD[i] != self.board[i]:
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

    return ChessBoard(new_board, board, board.depth)


def list_to_string(l):
    return "".join(str(l))


def bfs(node):
    heap = []
    queue = []
    counter = itertools.count()

    if SPEEDUP or SPEEDUP_EXP:
        heapq.heappush(heap, [node.value, next(counter), node])
    else:
        queue = deque([node])

    visited = set()
    k = 0
    while True:    # Since solvability is guaranteed this is equivalent: while queue:
        if k % 100000 == 0:
            if SPEEDUP or SPEEDUP_EXP:
                print(len(heap))
            else:
                print(len(queue))

        if SPEEDUP or SPEEDUP_EXP:
            pop = heapq.heappop(heap)[2]
        else:
            pop = queue.popleft()

        if pop.is_winner():
            return pop

        for x in get_valid_moves(pop):
            node_ = get_board(pop, x)

            if list_to_string(node_.board) not in visited:
                visited.add(list_to_string(node_.board))
                if SPEEDUP or SPEEDUP_EXP:
                    heapq.heappush(heap, [node_.value, next(counter), node_])
                else:
                    queue.append(node_)

        k += 1


def board_print(board,parent):
    print("\n")
    cell_size = 100/LEN_X;
    origin_x = (x_position * 120)+10;
    origin_y = (y_position * 120)+10;
    global line_x;
    global line_y;
    line_x = [0,0];
    line_y = [0,0];
    drawing.create_rectangle(origin_x,origin_y,origin_x+100,origin_y+100);
    for i in range(len(board)):
        position_x = (i%LEN_X)*cell_size;
        position_y = math.floor(i/LEN_Y)*cell_size;
        drawing.create_rectangle(origin_x+position_x,origin_y+position_y,origin_x+position_x+cell_size,origin_y+position_y+cell_size);
        if (board[i] == -1):
            drawing.create_rectangle(origin_x+position_x,origin_y+position_y,origin_x+position_x+cell_size,origin_y+position_y+cell_size,fill="#333333");
        elif (board[i] == 1):
            drawing.create_oval(origin_x+position_x,origin_y+position_y,origin_x+position_x+cell_size,origin_y+position_y+cell_size,fill="#ff5555")
        elif (board[i] == 2):
            drawing.create_oval(origin_x+position_x,origin_y+position_y,origin_x+position_x+cell_size,origin_y+position_y+cell_size,fill="#5555ff")
        elif (board[i] == 3):
            drawing.create_oval(origin_x+position_x,origin_y+position_y,origin_x+position_x+cell_size,origin_y+position_y+cell_size,fill="#aaaa55")
        if (parent) and (board[i] != parent.board[i]):
            if (line_x == [0,0]):
                line_x = [origin_x+position_x+(cell_size/2),origin_y+position_y+(cell_size/2)];
            else:
                line_y = [origin_x+position_x+(cell_size/2),origin_y+position_y+(cell_size/2)];
    drawing.create_line(line_x[0],line_x[1],line_y[0],line_y[1],width=2);
    for i in range(LEN_Y):
        print(board[i * LEN_X:(i + 1) * LEN_X]);

start_time = time.time();

root = ChessBoard(INITIAL_BOARD, None, 0);
winner = bfs(root);
a = 0;

while winner is not None:
    a += 1;
    board_print(winner.board,winner.parent);
    winner = winner.parent;
    if (x_position < max_x):
        x_position += 1;
    else:
        x_position = 0;
        y_position += 1;

print("--- %s seconds ---" % (time.time() - start_time))
print("Win in {} Moves. If SPEEDUP_EXP == True, this may NOT be optimal.".format(a - 1))

mainloop();
