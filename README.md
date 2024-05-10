# ****PROPOSED SOLUTION FOR THE QUARTO GAME**** #
***s301247@studenti.polito.it Mohamed Amine Hamdi***

## Final Project:  Quarto

### Problem definition

Develop an agent for the game Quarto that can play pretty well against a totally random agent

### Proposed solution

For this project I chose to work with the Genetic Programming technique, but developed in my own way, because I wanted to try it out, I started without much hope on the results but came out of it pretty surprised.

***

My implementation is composed of a genome that has a set of rules for the choosing and some for the placing, a rule is built with two trees, one for the if content and one for the then content, generally GP is used mainly for the if node, and in fact when using a set of predefined functions on the then content, the results may be better, but for "research" purposes, I propose the solution including both trees.

The if tree has a set of nodes that can either be operations, functions or constant values, the operations can require one or two parameters, and are done through a really easy to extend lambda dictionary, the if tree can be as long as the user requires to by the MAX_RECURSION_DEPTH constant.

The if tree is evaluated trying to see if the returned value is True or False.

***

The then tree is similar but it works differently because it has only operations and functions, the functions tho returns a proposed action, so maybe the function is place_at_diagonal and it returns a value between (0,0),(1,1),(2,2),(3,3) , so these functions are the leafs in our tree, the operations instead works very differently than the if tree counterpart, in fact here we need to return a chosen action, the operation so chooses the rigth node action or the leaf node action.

These actions are taken from the quartolib functions, they are really simple and extendible as well, so the user can try to feed the genetic programming with different actions etc.

The quartolib functions tho are not intelligent ones, they just return a simple value, the functions that I proposed for the choosing then trees in fact are just choose a high piece, or a solid piece etc.

***

The quality of the results can depend quite a lot on the quality of the functions proposed in the quartolib library, I chose really basic functions for now but as I said this piece of code is pretty extendible and really simple to modify, no functions here do some intelligent work, they do exactly what their name says, and also they don't return a possible solution for sure, in fact one of the operators I chose for now in the then trees is the possible one, this operator returns the possible operation between the two nodes.

The quality of the rule is calculated then in a 3(N) game span, in these games the rule is always chosen first by the genome, so in case I have 5 choosing rules, for each of the rules that needs to be evaluated we play 3 games against the random player and every time the choosing action is required I evaluate the rule to be evaluated as first then the rest, the rule is evaluated in the basis of the times the if tree was true and the times the then tree returned a possible action, after these 3 games I check the results and if the rule is not plausible (the if tree was never true or it was too much true(I want the rules to be correct like 33% of times, to not be overshadowing the rest of the rules, and also to have more specific rules), or the then tree has a possible action a really low amount of times) I try to mutate it until I have a good rule in that sense.

***

Then after evaluating all the rules that needs to be evaluated I sort them in the basis of a rule quality parameter(that favors rules that win and are true a small amount of time) or sort the rules by the amount of times the if tree was true(favoring less probable rules), and finally playing 100 games against the random player and calculating all the wins and all the times no rule was found(no if tree was true or no then tree returned a possible action), with this data I calculate the fitness of a player.

The mutations of a rule are done randomly through the tree, picking randomly new operations and functions etc, I tried also to work with mutating two rules giving one the then node of the other and vice versa.

The genetic programming then generates initially a population, then through mutations or crossovers(the crossover is done by shuffling the rules of the parents and picking a good amount of them for the child) we generate the offspring, one time every 6(N) generation, a new population arrives and takes by force at least 2(N) places in the population, forcing diversity a little bit and making the algorithm less stagnant.

***

The best player is pickled(thanks to the dill dependency) in a file and can be used to play against everytime.

I tried also as an approach taking singularly rules as genomes, but that approach didn't work as I wanted so I kept this approach.

The program when called can take as an argument if it needs training through the -t (--training) flag(if set it trains otherwise no), the number of generations of training -g 41 (--generations 41) (the default number is set to 50), and the filename where to save the best player at -f best_p.p (--filename best_p.p) (the default file is best_player.p).

***

So if I want to train a player for 120 generations and save it into pp.p I will call the program like:

'python main.py --training --generations 120 --filename pp.p'

Else if I just want to play against the random one game with the player saved into pp.p I will call the program like:

'python main.py --filename pp.p'

Or if the filename is best_player.p:

'python main.py'

Example of a rule:

if (2) eq (num_pieces_left) --> then (place_at_diagonal) possible ((place_at_corner) colless (place_at_antidiagonal))

This rule check if the number of pieces left is 2 and in case tries to place a piece in a random spot in the corner and one in the antidiagonal, if the piece on the corner is in a column with less current pieces than the one in the antidiagonal it is chosen, after this pick we confront the first one in the diagonal and this last one and we choose as a placement the possible one, in case both are possible we choose the first one.

All the rules are similar to this and are maybe more deep etc., but they are all generated completely randomly.

One cool thing is about the easiness of possible 'plugins', adding functions or operators is really easy

### Results

In general after a couple of iterations the best player usually is around a range of 80% of winrate against the random player, these results are pretty promising, and could be improved significantly with parameter tuning(use of other GA to pick best params maybe) or better library functions.

The best player currently won 82% of the games against the random player, with older architectures I achieved 90, 95% as well but I didn't like the rules because they were too overshadowing of the rest of the rules, in fact is because of that that now rules are forced to have a possibility of trueness of less than 66%.

These percentages are taken from the fitness of the genome, in fact the 82% agent won 82 games but got 79.2 as fitness because during those 100 games 7 moves were random(7 in total between choosing actions and placing ones, fitness is calculated by the number of wins substracted by 0,4*number of random picks).

Here are the set of rules of the agent I got:

```
Rule: If not ((characteristic_in_less_used_row) eq (characteristic_not_in_less_used_column)) --> Then ((not_high_piece) possible (coloured_piece)) possible (solid_piece)

Rule: If (characteristic_in_antidiagonal) and ((most_used_characteristic) ne (characteristic_in_most_used_row_not_complete)) --> Then (((high_piece) similarinmostusedcolumnnotcomplete (not_high_piece)) possible (square_piece)) possible ((not_square_piece) similarinlessusedcolumnnotcomplete (coloured_piece))

Rule: If (((characteristic_not_in_less_used_column) ne (most_used_characteristic)) ne ((((not_square) ne (characteristic_not_in_less_used_row)) and ((not (characteristic_in_antidiagonal)) ne ((characteristic_not_in_most_used_row_not_complete) and (characteristic_not_in_most_used_row_not_complete)))) eq (((square) ne ((not_solid) or (not_solid))) ne (characteristic_in_diagonal)))) eq (((characteristic_not_in_less_used_column) ne (characteristic_in_less_used_column)) ne (not_high)) --> Then (((coloured_piece) differentdiag (((not_coloured_piece) similarinmostusedrownotcomplete (coloured_piece)) diffinlessusedcolnotcomplete (not_solid_piece))) similarinmostusedrownotcomplete (not_square_piece)) diffinmostusedcolnotcomplete (square_piece)

Rule: If ((less_used_characteristic) or (not (characteristic_in_diagonal))) eq (not_coloured) --> Then ((coloured_piece) lessunique ((square_piece) similarinlessusedrownotcomplete (((coloured_piece) lessunique (coloured_piece)) lessunique ((coloured_piece) diffinmostusedrownotcomplete (coloured_piece))))) possible ((coloured_piece) differentdiag (coloured_piece))
Rule: If ((characteristic_not_in_most_used_column_not_complete) eq (characteristic_in_less_used_row)) and ((False) eq (((not (solid)) ne (False)) and (characteristic_in_diagonal))) --> Then ((((not_solid_piece) diffinlessusedrownotcomplete (((not_square_piece) differentantidiag (solid_piece)) falses (coloured_piece))) lessunique (square_piece)) similarinlessusedcolumnnotcomplete (square_piece)) possible (not_coloured_piece)

Rule: If (characteristic_not_in_most_used_column_not_complete) ne (characteristic_not_in_most_used_row_not_complete) --> Then (not_solid_piece) possible ((solid_piece) similarinmostusedcolumnnotcomplete (solid_piece))

Rule: If (most_used_characteristic) and (((((solid) ne ((not_solid) and (less_used_characteristic))) and ((characteristic_in_antidiagonal) or ((coloured) eq (most_used_characteristic)))) ne (characteristic_in_less_used_column)) eq (((characteristic_in_antidiagonal) ne (not_coloured)) and (True))) --> Then (solid_piece) possible (((solid_piece) possible ((((not_solid_piece) differentdiag (square_piece)) similarinmostusedrownotcomplete (coloured_piece)) diffinmostusedrownotcomplete (((not_high_piece) similarinlessusedrownotcomplete (square_piece)) lessunique (square_piece)))) moreunique ((((square_piece) diffinlessusedrownotcomplete ((square_piece) similarinlessusedcolumnnotcomplete (solid_piece))) differentantidiag (not_coloured_piece)) falses (not_solid_piece)))

Rule: If (((((not_coloured) eq ((False) or (characteristic_in_less_used_row))) ne (characteristic_in_most_used_column_not_complete)) eq (not (((characteristic_in_less_used_row) eq (characteristic_not_in_less_used_column)) and (characteristic_not_in_most_used_row_not_complete)))) or (characteristic_not_in_diagonal)) ne ((((not_high) eq (coloured)) or (characteristic_in_most_used_column_not_complete)) ne ((False) ne ((most_used_characteristic) and ((characteristic_in_less_used_column) ne ((characteristic_not_in_most_used_row_not_complete) ne (high)))))) --> Then ((((not_square_piece) diffinlessusedrownotcomplete (not_solid_piece)) similarinlessusedrownotcomplete (not_square_piece)) differentantidiag (high_piece)) possible (coloured_piece)

Rule: If (characteristic_not_in_less_used_row) ne (characteristic_not_in_less_used_column) --> Then ((not_solid_piece) diffinmostusedcolnotcomplete ((square_piece) diffinlessusedrownotcomplete ((solid_piece) trues (((coloured_piece) diffinlessusedrownotcomplete (not_solid_piece)) differentantidiag ((coloured_piece) diffinmostusedcolnotcomplete (not_solid_piece)))))) diffinlessusedrownotcomplete ((high_piece) diffinlessusedcolnotcomplete (not_solid_piece))

Rule: If (((characteristic_not_in_antidiagonal) ne (((characteristic_not_in_most_used_column_not_complete) ne (not (not_coloured))) and (characteristic_in_most_used_row_not_complete))) and ((solid) and (coloured))) ne ((not (((not_high) and ((True) and (not_solid))) ne (characteristic_not_in_less_used_column))) and (((((less_used_characteristic) and (not_coloured)) eq (False)) and (((characteristic_not_in_diagonal) or (coloured)) ne ((square) eq (characteristic_in_less_used_row)))) or (characteristic_in_most_used_row_not_complete))) --> Then (((solid_piece) lessunique (not_coloured_piece)) similarinmostusedcolumnnotcomplete ((not_high_piece) trues ((high_piece) similarinmostusedcolumnnotcomplete ((not_square_piece) diffinlessusedrownotcomplete ((square_piece) lessunique (not_coloured_piece)))))) possible (((not_solid_piece) diffinmostusedcolnotcomplete (square_piece)) similarinlessusedcolumnnotcomplete ((((coloured_piece) diffinlessusedrownotcomplete ((solid_piece) similarinmostusedcolumnnotcomplete (not_high_piece))) similarinlessusedrownotcomplete (not_square_piece)) similarinmostusedrownotcomplete ((high_piece) diffinlessusedrownotcomplete (not_square_piece))))

        ; Place piece rules :

Rule: If (not ((((num_pieces_chosen) or ((most_used_row) lte (9))) eq ((11) mul ((num_pieces_in_less_used_column) gt (8)))) eq ((not ((num_pieces_in_most_used_row_not_complete) gte (5))) ne (num_pieces_in_less_used_column)))) eq (((2) sub (num_elements_in_antidiagonal)) gt (num_pieces_in_most_used_row_not_complete)) --> Then (element_in_most_used_column_not_complete) possible (element_in_most_used_column_not_complete)

Rule: If not (not (num_pieces_in_less_used_row)) --> Then ((element_in_most_used_column_not_complete) colmore (element_in_diagonal)) possible (((element_in_less_used_row) antidiagmore (element_in_diagonal)) possible ((element_in_less_used_row) antidiagmore (((element_in_corner) colmore (element_in_antidiagonal)) rowmore (((element_in_less_used_column) antidiagless (element_in_most_used_column_not_complete)) rowless (element_in_corner)))))

Rule: If (1) sub (num_elements_in_antidiagonal) --> Then (element_in_most_used_row_not_complete) possible (element_in_antidiagonal)

Rule: If not (num_elements_in_diagonal) --> Then ((element_in_most_used_row_not_complete) possible (((((element_in_antidiagonal) rowmore (element_inside)) antidiagless (element_in_less_used_row)) antidiagmore (((element_in_diagonal) colmore (element_in_diagonal)) antidiagless (element_in_corner))) diagmore ((((element_in_antidiagonal) diagless (element_in_corner)) antidiagmore (element_in_corner)) colmore (element_in_diagonal)))) possible (element_in_most_used_column_not_complete)

Rule: If ((12) add (((((11) add (num_pieces_in_less_used_row)) sub ((0) add (False))) gt (16)) lte (7))) and (num_elements_in_diagonal) --> Then ((element_in_diagonal) antidiagmore (element_in_most_used_row_not_complete)) possible ((((element_in_diagonal) antidiagmore (((element_in_most_used_row_not_complete) antidiagmore (element_in_antidiagonal)) colless (element_in_most_used_column_not_complete))) possible ((element_in_less_used_row) possible ((element_in_less_used_column) colless (element_in_less_used_row)))) antidiagless (element_in_most_used_column_not_complete))

Rule: If ((((num_pieces_in_most_used_row_not_complete) gte ((14) lte (most_used_column))) mul (16)) gt (10)) gte (num_elements_in_antidiagonal) --> Then (element_in_less_used_row) possible (element_in_less_used_column)

Rule: If ((num_elements_in_diagonal) sub (most_used_row)) eq (num_pieces_in_most_used_column_not_complete) --> Then (element_in_most_used_column_not_complete) diagmore ((element_in_diagonal) diagmore ((element_in_most_used_column_not_complete) colmore (element_in_less_used_row)))

Rule: If (not ((not (((4) lte (5)) add (num_pieces_left))) or (9))) add (((most_used_column) sub (num_elements_in_antidiagonal)) sub ((num_elements_in_diagonal) gte ((num_pieces_in_less_used_row) sub (((num_elements_in_diagonal) sub (less_used_column)) mul (not (num_pieces_left)))))) --> Then (element_in_diagonal) possible (element_in_less_used_column)

Rule: If not ((False) sub (num_elements_in_diagonal)) --> Then ((element_in_diagonal) rowmore (((element_in_less_used_row) diagless (((element_in_corner) diagless (element_in_most_used_column_not_complete)) rowmore (element_inside))) diagmore (element_in_corner))) possible (element_in_most_used_column_not_complete)

with fitness: 79.2 and win% of 82.0%
```