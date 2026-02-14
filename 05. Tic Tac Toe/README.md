# Tic Tac Toe

* **3x3 using NiceGUI in Python.**
* Levels:
    * Easy (pc random moves)
    * Impossible
    * Medium
        1) THINK ABOUT YOUR OWN IDEA(S) & IMPLEMENT IT!
        2) Probabilistic Intelligence:
            * 60% chance: optimal move
            * 40% chance: random valid move
            * Pick Random [0-100]: easy<40/100 && 40/100>=impossible
        3) One-Step Lookahead" (Most Human-Like) --> Win or Block, Otherwise Random:
            - Check for Win: Can I win on this turn? If yes, take that spot.
            - Check for Block: If I don't move here, will the opponent win on their next turn? If yes, block that spot.
            - Else: Move randomly (or pick Center if available).
        4) Depth-Limited Minimax
            - If you are using the Minimax algorithm for your "Impossible" level, you can reuse it for Medium by limiting its brain power.
            - Impossible: Looks at the entire game tree (Depth = Infinity).
            - Medium: Looks only 2 moves ahead (Depth = 1 or 2).
            - This makes the computer play perfectly regarding the immediate future but fail to see long-term setups.
    * 2 player
* Make the any board (NxN, 3<=N<=99) version, & K win -- 1<=K<=5

* SAMPLE:
    * https://google.com/search?q=tic+tac+toe/
    * https://playtictactoe.org/

---

**===== ONLY AFTER BUILDING THE GAME YOURSELF =====**
* what are the tic tac toe algorithms
