import random
import copy
import quarto
from .rule import Rule
import agents.quartolib as quartolib
import numpy as np
NUMROWS=4
NUMCOLUMNS=4
NEWLINE="\n"
MINRULES=5
MAXRULES=10

#random choosing function used in case of no good rule found or by random player
def random_choose(quarto) -> int:
    return random.randint(0, 15)
#random placing function used in case of no good rule found or by random player
def random_place(quarto) -> tuple:
    return random.randint(0, 3), random.randint(0, 3)

    
class RandomPlayer(quarto.Player):
    """Random player"""

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)

    def choose_piece(self) -> int:
        return random.randint(0, 15)

    def place_piece(self) -> tuple:
        return random.randint(0, 3), random.randint(0, 3)

class Genome(quarto.Player):
    def __init__(self,quarto: quarto.Quarto,choose_piece_rules=None,place_piece_rules=None) -> None:
        super().__init__(quarto)
        self.quarto=quarto
        #set of rules used
        self.choose_piece_rules=copy.deepcopy(choose_piece_rules) if choose_piece_rules is not None else [Rule(True,None) for _ in range(random.randint(MINRULES,MAXRULES))]
        self.place_piece_rules=copy.deepcopy(place_piece_rules) if place_piece_rules is not None else [Rule(False,None) for _ in range(random.randint(MINRULES,MAXRULES))]
        #rules used during evaluation of the rules
        self.evaluating_choose_piece_rules=self.choose_piece_rules
        self.evaluating_place_piece_rules=self.place_piece_rules
        self.fitness=0
        #am I during the evaluation of some rules?
        self.evaluating=False
        #am I during my own evaluation?
        self.evaluating_genome=False
        #number of times a random rule was used
        self.random_pick=0
        #print(f'\tChoose piece rules :\n {NEWLINE.join([str(rule) for rule in self.choose_piece_rules])} \n\t;Place piece rules:\n {NEWLINE.join([str(rule) for rule in self.place_piece_rules])}')
        if choose_piece_rules is None:
            #I am a completely new genome and I need to be evaluated immediately
            self.evaluate_fitness()
            print(f'Generated genome with fit {self.fitness} rnd {self.random_pick}, wins {self.fitness+0.4*self.random_pick}')
    
    def set_quarto(self,quarto):
        #set quarto for myself + all my rules
        self.quarto=quarto
        for rule in self.choose_piece_rules+self.place_piece_rules:
            rule.set_quarto(self.quarto)

    def choose_piece(self):
        #get possible actions
        board=self.quarto.get_board_status()
        placed_pieces=quartolib.get_placed_pieces(board)
        possible_pieces=[_ for _ in range(NUMROWS*NUMCOLUMNS) if _ not in placed_pieces]
        rules_to_use=self.evaluating_choose_piece_rules if self.evaluating else self.choose_piece_rules
        for rule in rules_to_use:
            #evaluate the if tree
            val=rule.evaluate()
            if val:
                #if true check the then tree
                act=rule.action()
                if act in possible_pieces:
                    #if the if tree is true and the then tree is possible update the stats of the rule and use it
                    if self.evaluating:
                        rule.evaluated(True,True)
                    return act
                else:
                    #if the if tree is true but the then tree is not possible update the stats and check next rule
                    if self.evaluating:
                        rule.evaluated(True,False)
            else:
                #if the if tree is not possible update the stats of the rule
                if self.evaluating:
                    rule.evaluated(False,False)
        #no good rule was found, update the stats of the random picks
        if self.evaluating_genome:
            self.random_pick+=1
        return random_choose(self.quarto)

    def place_piece(self):
        #get possible actions
        board=self.quarto.get_board_status()
        possible_placements=[(a[1],a[0]) for a in np.argwhere(board==-1).tolist()]
        rules_to_use=self.evaluating_place_piece_rules if self.evaluating else self.place_piece_rules
        for rule in rules_to_use:
            #evaluate the if tree
            val=rule.evaluate()
            if val:
                #if true check the then tree
                act=rule.action()
                if act in possible_placements:
                    #if the if tree is true and the then tree is possible update the stats of the rule and use it
                    if self.evaluating:
                        rule.evaluated(True,True)
                    return act
                else:
                    #if the if tree is true but the then tree is not possible update the stats and check next rule
                    if self.evaluating:
                        rule.evaluated(True,False)
            else:
                #if the if tree is not possible update the stats of the rule
                if self.evaluating:
                    rule.evaluated(False,False)
        #no good rule was found, update the stats of the random picks
        if self.evaluating_genome:
            self.random_pick+=1
        return random_place(self.quarto)
    
    def mutate(self):
        #get a random number to choose which combination of mutation to apply
        num=random.randint(0,6)
        if num%2==0:
            #mutate a random choose piece rule
            self.choose_piece_rules[random.randint(0,len(self.choose_piece_rules)-1)].mutate()
        if num==1 or num==2 or num==5 or num==6:
            #mutate a random place piece rule
            self.place_piece_rules[random.randint(0,len(self.place_piece_rules)-1)].mutate()
        if num>2:
            #do crossover between rules
            self.crossover_rules()

    def crossover_rules(self):
        #pick random rules
        chooseind1,chooseind2=random.randint(0,len(self.choose_piece_rules)-1),random.randint(0,len(self.choose_piece_rules)-1)
        placeind1,placeind2=random.randint(0,len(self.place_piece_rules)-1),random.randint(0,len(self.place_piece_rules)-1)
        #swap trees between rules
        choose_then_node,place_then_node=self.choose_piece_rules[chooseind1].then_node,self.place_piece_rules[placeind1].then_node
        self.choose_piece_rules[chooseind1].then_node=self.choose_piece_rules[chooseind2].then_node
        self.choose_piece_rules[chooseind1].then_node=choose_then_node
        self.place_piece_rules[placeind1].then_node=self.place_piece_rules[placeind2].then_node
        self.place_piece_rules[placeind2].then_node=place_then_node
        #reset evaluation stats of rules, they need to be reevealuted
        self.choose_piece_rules[chooseind1].reset_evaluation_stats()
        self.choose_piece_rules[chooseind2].reset_evaluation_stats()
        self.place_piece_rules[placeind1].reset_evaluation_stats()
        self.place_piece_rules[placeind2].reset_evaluation_stats()


    def evaluate_fitness(self):
        #evaluate choose piece rules
        self.evaluating=True
        for i in range(len(self.choose_piece_rules)):
            #put rule as first
            self.evaluating_choose_piece_rules= [self.choose_piece_rules[i]] + self.choose_piece_rules[:i] + self.choose_piece_rules[i+1:]
            make_sense=False
            # run only if the rule needs to be evaluated, so if the rule is mutated, otherwise use old data
            while not make_sense and self.choose_piece_rules[i].needs_evaluation():
                #run 3 games with that rule evaluated as the first one
                for _ in range(3):
                    self.choose_piece_rules[i].reset_game_stats()
                    game = quarto.Quarto()
                    playerindex=random.randint(0,1)
                    game.set_players((RandomPlayer(game), self) if playerindex==1 else (self, RandomPlayer(game)))
                    self.set_quarto(game)
                    winner = game.run()
                    #update game stats
                    self.choose_piece_rules[i].evaluate_game_rule(winner==playerindex)
                #does the rule make sense?
                make_sense=self.choose_piece_rules[i].rule_make_sense and self.choose_piece_rules[i].action_make_sense
                #if not mutate the rule and rerun the loop
                if not make_sense:
                    self.choose_piece_rules[i].mutate(self.choose_piece_rules[i].rule_make_sense,self.choose_piece_rules[i].action_make_sense)
        #reset order of rules
        self.evaluating_choose_piece_rules=self.choose_piece_rules
        
        for i in range(len(self.place_piece_rules)):
            #put rule as first
            self.evaluating_place_piece_rules= [self.place_piece_rules[i]] + self.place_piece_rules[:i] + self.place_piece_rules[i+1:]
            make_sense=False
            # run only if the rule needs to be evaluated, so if the rule is mutated, otherwise use old data
            while not make_sense and self.place_piece_rules[i].needs_evaluation():
                #run 3 games with that rule evaluated as the first one
                for _ in range(3):
                    self.place_piece_rules[i].reset_game_stats()
                    game = quarto.Quarto()
                    playerindex=random.randint(0,1)
                    game.set_players((RandomPlayer(game), self) if playerindex==1 else (self, RandomPlayer(game)))
                    self.set_quarto(game)
                    winner = game.run()
                    #update game stats
                    self.place_piece_rules[i].evaluate_game_rule(winner==playerindex)
                #does the rule make sense?
                make_sense=self.place_piece_rules[i].rule_make_sense and self.place_piece_rules[i].action_make_sense
                #if not mutate the rule and rerun the loop
                if not make_sense:
                    self.place_piece_rules[i].mutate(self.place_piece_rules[i].rule_make_sense,self.place_piece_rules[i].action_make_sense)
        #reset order of rules
        self.evaluating_place_piece_rules=self.place_piece_rules

        self.evaluating=False
        #updated priority of rules based on the rule quality parameter
        self.choose_piece_rules=sorted(self.choose_piece_rules,key=lambda a: a.rule_quality,reverse=True)  
        self.place_piece_rules=sorted(self.place_piece_rules,key=lambda a: a.rule_quality,reverse=True)
        #now evaluate whole genome over a 100 games span
        self.evaluating_genome=True
        wins=0
        for _ in range(100):
            game = quarto.Quarto()
            playerindex=random.randint(0,1)
            game.set_players((RandomPlayer(game), self) if playerindex==1 else (self, RandomPlayer(game)))
            self.set_quarto(game)
            winner = game.run()
            if winner==playerindex:
                wins+=1
        #fitness of genome
        self.fitness= wins - 0.4*self.random_pick


    def __str__(self):
        return f'\tChoose piece rules :\n{NEWLINE.join([str(rule) for rule in self.choose_piece_rules])} \n\t; Place piece rules :\n{NEWLINE.join([str(rule) for rule in self.place_piece_rules])}'

def generate_rules():
    #function that generated a set of rules, not used anymore .... xxxxx
    return [Rule(True,None) for _ in range(random.randint(MINRULES,MAXRULES))],[Rule(False,None) for _ in range(random.randint(MINRULES,MAXRULES))]