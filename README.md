FLAG WARRIOR GAME (build w/ PyGame)



Operation: 

1. Run the "Controller.py" file to initiate the game, Press "B" to start the game
2. For player1, use "WASD" to walk, "Q" to use prop
3. For player2, use "↑↓←→" to walk, "M" to use prop
4. For the loser (after the winner capture the flag), press prop key to revenge in the exact same maze



Type of terrain:

1. Water: slow down (player on the water will need to press 2 times to walk 1 unit)
2. Ice: slippery, can't stop moving (can only modify the target direction, and will auto move 1 unit forward the target direction per unit time) 

Types of props:

1. Reversal: Up and down / left and right operations are exchanged
2. Mine: Put mine behind you, after any player stepping on it, the mine will blow the player to a nearby location randomly
3. Pass wall: Ignore the maze wall in the next walk operation
4. Teleport: Long-distance teleportation
5. Teleporting mine: Mine that’s teleported (a combination of "Mine" and "Teleport")



RoadMap: https://docs.google.com/document/d/1n6_33p_GOIsmiG7ptzD9PsEPdlPgcFSJejOf-evNXww/edit?usp=sharing