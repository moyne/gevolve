import logging
import random
import quarto
import numpy as np
from scipy.stats import binom
import dill as pickle
from .genome import Genome,generate_rules,MINRULES,MAXRULES

class GeneticProgramming:
    def __init__(self) -> None:
        #sizes
        self.__POPULATION_SIZE__=5
        self.__OFFSPRING_SIZE__=30
        print(f'Generating initial population ...')
        #generate initial population
        self.population=[Genome(None) for _ in range(self.__POPULATION_SIZE__)]
        #sort the population by fitness
        self.population=sorted(self.population,key=lambda a: a.fitness,reverse=True)[:self.__POPULATION_SIZE__]
        #weigths roulette, not used actually since the weigths are calculated differently and not though a binomial function
        self.WEIGHTS_ROULETTE=[binom.pmf(k=_,n=self.__POPULATION_SIZE__-1,p=1/self.__POPULATION_SIZE__) for _ in range(self.__POPULATION_SIZE__)]

    def select_parent(self,k=2,weigths=None):
        # Using a wheel roulette TO SELECT K PARENTS, THIS IS WITHOUT REPLACEMENT, SO THE PARENT CAN'T BE TAKEN MORE THAN ONCE
        # IN A SINGLE CALL
        return [self.population[ind] for ind in np.random.choice(range(self.__POPULATION_SIZE__),k,p=self.WEIGHTS_ROULETTE if weigths is None else weigths,replace=False )]


    def cross_oversplit(self,genome1: Genome,genome2: Genome):
        """One point split crossover"""
        #create list of rules
        c_rules=genome1.choose_piece_rules+genome2.choose_piece_rules
        p_rules=genome1.place_piece_rules+genome2.place_piece_rules
        #shuffle lists
        random.shuffle(c_rules)
        random.shuffle(p_rules)
        #take from list a good amount of rules
        return c_rules[:random.randint(MINRULES,MAXRULES)],p_rules[:random.randint(MINRULES,MAXRULES)]

    def cross_oversplit_rules(self,genome: Genome,new_c_rules,new_p_rules):
        """One point split crossover"""
        # FUNCTION NOT USED ANYMORE XXXXXXXX
        #create list of rules
        c_rules=genome.choose_piece_rules+new_c_rules
        random.shuffle(c_rules)
        #shuffle lists
        p_rules=genome.place_piece_rules+new_p_rules
        random.shuffle(p_rules)
        #take from list a good amount of rules
        return c_rules[:random.randint(MINRULES,MAXRULES)],p_rules[:random.randint(MINRULES,MAXRULES)]


    def evolve(self,iterations):
        #evolving algorithm
        offspring=[]
        print(f'Population at the beginning is {self.population_stats()}')
        for i in range(iterations):
            #get minfit and calculate weigths for parent selection probabilities
            minfit,maxfit=min([gen.fitness for gen in self.population]),max([gen.fitness for gen in self.population])
            weigths=[-minfit+self.population[_].fitness+1 for _ in range(self.__POPULATION_SIZE__)]
            weigths=[_/sum(weigths) for _ in weigths]
            for o in range(self.__OFFSPRING_SIZE__ if i%6 else int(self.__OFFSPRING_SIZE__*0.9)):
                #always mutate
                cross=True
                if random.random()<1/3:
                    #mutate tree
                    cross=False
                    parent=self.select_parent(k=1,weigths=weigths)[0]
                    #generate new genome that is the same as the parent
                    off=Genome(parent.quarto,parent.choose_piece_rules,parent.place_piece_rules)
                    off.mutate()
                else:
                    #crossover tree
                    parents= self.select_parent(k=2,weigths=weigths)
                    #get crossover rules
                    choose_rules,place_rules=self.cross_oversplit(parents[0],parents[1])
                    #generate new genome
                    off=Genome(parents[0].quarto,choose_rules,place_rules)
                #calculate fitness of new genome and add it to offspring
                off.evaluate_fitness()
                offspring.append(off)
            #get new population
            self.population=sorted(self.population+offspring,key=lambda a: a.fitness,reverse=True)[:self.__POPULATION_SIZE__]
            if not i%6:
                #once every 6 gens get new visitors to the population
                print(f'Population after {i+1} gens before visitors is {self.population_stats()}')
                print(f'Visitor from out of the town are arriving')
                #generate new genomes totally from scratch
                off_visitors=[Genome(None) for _ in range(int(0.1*self.__OFFSPRING_SIZE__))]
                print(f'Now they have meet the population they generated two kids with fitness of {[o.fitness for o in off_visitors]}')
                #force at least 2 of these visitors to the population
                self.population=sorted(self.population[:self.__POPULATION_SIZE__-2]+off_visitors,key=lambda a: a.fitness,reverse=True)[:self.__POPULATION_SIZE__]
            offspring=[]
            print(f'Population after {i+1} gens is {self.population_stats()}')

    def population_stats(self):
        #print purposes
        return [f'fit {h.fitness} rnd {h.random_pick} wins {h.fitness+0.4*h.random_pick}' for h in self.population]


    def get_best_player(self):
        #get best genome
        return self.population[0]


            

class GeneticProg(quarto.Player):
    """Genetic Programming player"""

    def __init__(self, quarto: quarto.Quarto,best_player_file,generations) -> None:
        super().__init__(quarto)
        self.quarto=quarto
        print('Training phase ...')
        #get genetic programming algorithm running and evolve it for x gens
        population=GeneticProgramming()
        population.evolve(generations)
        print(f'Population after {generations} gens is {population.population_stats()}')
        #get best player
        self.player=population.get_best_player()
        print(f'Player is\n{self.player}')
        try:
            with open(best_player_file,'wb') as file:
                #save best player into file through dill(pickle)
                pickle.dump(self.player, file,protocol=0)
        except OSError as error:
            print(f'Error while pickle saving best player {error}')
    
    def set_quarto(self,quarto):
        #set quarto to myself and best player
        self.quarto=quarto
        self.player.set_quarto(self.quarto)

    def choose_piece(self) -> int:
        #play with best player
        return self.player.choose_piece()

    def place_piece(self) -> tuple:
        #play with best player
        return self.player.place_piece()