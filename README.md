#The Multi-Agent Pac-Man
Part 1: Reflex Agent
In this part we improved the reflex agent to perform well with an average score of 1246. At first we tested the reflex agent with only food proximity changes from one state to the other.
1. But that did not take into account the ghost positions, so Pacman would often get killed.
2. Next, we incorporated ghost positions into the score. The farther, Pacman is from the ghost the better. But, this made Pacman solely focus on reacting to the ghost moments. Pacman, sometimes, would not even eat food next to him.
3. So, as a counter measure, we only consider, ghosts which are within a two distance radius and score accordingly.
4. Now, Pacman concentrates on food when the ghost is away and he tries to evade the ghost when within 2 radius .

Part 2: Minimax
To implement minimax, we have used the minimax algorithm taught in class. We observed that Minimax loses in some cases. It takes a pessimistic approach and assumes that the ghosts will always try to minimize the utility of Pacman.

Part 3: Alpha-Beta Pruning
After implementation of Alpha beta, we see a slight speed up in the runtime of the code. This speed up is due to the pruning of some nodes at various levels. Even now, there are issues of Pacman thrashing around at some places.
1. We came to a conclusion that this might be due to the evaluation function which only returns state scores. So, in future we will try to implement a better evaluation function for the same.
2. Initially, based on our understanding of the concept from class, we also pruned on equality. Then, we understood that to keep the code in accordance with auto-grader, this must not be done.

Part 4: Expectimax
We understood that not all agents are intelligent and being optimistic can get you good results most of the time. We debugged the code for the float division.
1. By taking a mean expectation, we were able to introduce chance/randomness in the replanning.
2. Through this Pacman now takes chances where he expects more utility. This is called maximizing one’s utitlity.

Results for Alpha-beta in trapped classic:
• Scores: -501.0, -501.0, -501.0, -501.0, -501.0, -501.0, -501.0, -501.0, -501.0, -501.0
• Win Rate: 0/10 (0.00)
• Record: Loss, Loss, Loss, Loss, Loss, Loss, Loss, Loss, Loss, Loss

Results for Expectimax in trapped classic:
• Scores: -502.0, -502.0, 532.0, 532.0, -502.0, -502.0, 532.0, 532.0, 532.0, 532.0
• Win Rate: 6/10 (0.60)
• Record: Loss, Loss, Win, Win, Loss, Loss, Win, Win, Win, Win

Conclusion:
1. If ghosts are not intelligent/directional Expectimax works wells compared to alpha-beta and minimax.
2. Minimax & Alpha-beta sometimes performs poorly. But, Alpha beta is slightly faster. There are some issues such as Pacman thrashing around without knowing where to go because of the evaluation function on the terminal states.
3. Reflex agent surprisingly works well with the new evaluation function. It reacts to the changes in the environment pretty well
