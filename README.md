# Knights-Game
#### [Steam Link](https://store.steampowered.com/app/476240/KNIGHTS/)

---

Python written BFS with heuristic for higher levels.

Works:

    In the Chess.py File change INITIAL_BORD & WINNING_BOARD accordingly.
    Set SPEEDUP False / True.
    Run.
    
    
SPEEDUP == True will usually solve the Game within max 5 second, but with probable max. ~ 1000 moves.
Around 50-150 mostly.


SPEEDUP == False will solve the Game optimal, but will take longer.

For King levels (5x5) SPEEDUP == False will mostly consume too much memory, to be solvable, SPEEDUP == False will do the job.

---

SETTINGS:

Figures:

      Empty: 0      
      Not Moveable: -1
      Red: 1
      Blue: 2
      Golden: 3


Board is numerated in this fashion:

  ![Image description](Knights1.png)

Setting BOARDS:

![Image description](Knights2.png)

---

Example:

Output with SPEEDUP == False:

![Image description](slow.png)

Output with SPEEDUP == True:

![Image description](fast.png)


False returns the optimum, True a suboptimal solution, but way faster.

Printed boards must be read from bottom to top.
