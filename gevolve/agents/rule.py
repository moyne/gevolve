import random
import agents.quartolib as quartolib
#characteristic that are true
TRUE_PROPS=['high','solid','square','coloured']
#is the object a number (float, bool, int) or a string?
def isnumber(a):
    return (isinstance(a,int) or isinstance(a,float) or isinstance(a,bool))
#transform to a numeric representation
def tonum(a):
    if isnumber(a):
        return a
    else:
        return 0
#dict of if operations, each operation is characterized by the name and an associated lambda that takes two parameters(even the ones that
# use only one like not) and return a value
IF_OPERATIONS={
    'mul': (lambda a,b: a*b if isnumber(a) and isnumber(b) else float(a) if isnumber(a) else float(b) if isnumber(b) else 0),
    'add': (lambda a,b: a+b if isnumber(a) and isnumber(b) else float(a) if isnumber(a) else float(b) if isnumber(b) else 0),
    'sub': (lambda a,b: a-b if isnumber(a) and isnumber(b) else float(a) if isnumber(a) else float(b) if isnumber(b) else 0),
    'not': (lambda a,b: not a),
    'or': (lambda a,b: a or b),
    'truechar':(lambda a,b: a in TRUE_PROPS),
    'falsechar':(lambda a,b: a not in TRUE_PROPS),
    'gt':(lambda a,b:tonum(a)>tonum(b)),
    'lt':(lambda a,b:tonum(a)<tonum(b)),
    'gte':(lambda a,b:tonum(a)>=tonum(b)),
    'lte':(lambda a,b:tonum(a)<=tonum(b)),
    'and': (lambda a,b: a and b),
    'eq': (lambda a,b: a==b),
    'ne': (lambda a,b: a!=b)
}
#then operations in case of place rules, these operations returns either the left node, or the right node always!
THEN_PLACE_OPERATIONS={
    'colmore': (lambda quarto,a,b: a if quartolib.compare_elements_in_columns(quarto,a[0],b[0]) else b),
    'colless': (lambda quarto,a,b: b if quartolib.compare_elements_in_columns(quarto,a[0],b[0]) else a),
    'rowmore': (lambda quarto,a,b: a if quartolib.compare_elements_in_rows(quarto,a[1],b[1]) else b),
    'rowless': (lambda quarto,a,b: b if quartolib.compare_elements_in_rows(quarto,a[1],b[1]) else a),
    'diagmore': (lambda quarto,a,b: a if quartolib.compare_elements_in_diag(quarto,a,b) else b),
    'diagless': (lambda quarto,a,b: b if quartolib.compare_elements_in_diag(quarto,a,b) else a),
    'antidiagmore': (lambda quarto,a,b: a if quartolib.compare_elements_in_antidiag(quarto,a,b) else b),
    'antidiagless': (lambda quarto,a,b: b if quartolib.compare_elements_in_antidiag(quarto,a,b) else a),
    'possible': (lambda quarto,a,b: a if quartolib.place_possible(quarto,a,b) else b)
}
#then operations in case of choose piece, these operations returns either the left node, or the right node always!
THEN_CHOOSE_OPERATIONS={
    'moreunique': (lambda quarto,a,b: a if quartolib.compare_uniqueness(quarto,a,b) else b),
    'lessunique': (lambda quarto,a,b: b if quartolib.compare_uniqueness(quarto,a,b) else a),
    'trues': (lambda quarto,a,b: a if quartolib.compare_trues(quarto,a,b) else b),
    'falses': (lambda quarto,a,b: b if quartolib.compare_trues(quarto,a,b) else a),
    'diffinmostusedrownotcomplete': (lambda quarto,a,b: a if quartolib.more_different_in_most_used_row_not_complete(quarto,a,b) else b),
    'similarinmostusedrownotcomplete': (lambda quarto,a,b: b if quartolib.more_different_in_most_used_row_not_complete(quarto,a,b) else a),
    'diffinmostusedcolnotcomplete': (lambda quarto,a,b: a if quartolib.more_different_in_most_used_column_not_complete(quarto,a,b) else b),
    'similarinmostusedcolumnnotcomplete': (lambda quarto,a,b: b if quartolib.more_different_in_most_used_column_not_complete(quarto,a,b) else a),
    'diffinlessusedrownotcomplete': (lambda quarto,a,b: a if quartolib.more_different_in_less_used_row(quarto,a,b) else b),
    'similarinlessusedrownotcomplete': (lambda quarto,a,b: b if quartolib.more_different_in_less_used_row(quarto,a,b) else a),
    'diffinlessusedcolnotcomplete': (lambda quarto,a,b: a if quartolib.more_different_in_less_used_column(quarto,a,b) else b),
    'similarinlessusedcolumnnotcomplete': (lambda quarto,a,b: b if quartolib.more_different_in_less_used_column(quarto,a,b) else a),
    'differentdiag': (lambda quarto,a,b: a if quartolib.more_different_in_diagonal(quarto,a,b) else b),
    'similardiag': (lambda quarto,a,b: b if quartolib.more_different_in_diagonal(quarto,a,b) else a),
    'differentantidiag': (lambda quarto,a,b: a if quartolib.more_different_in_antidiagonal(quarto,a,b) else b),
    'similardiag': (lambda quarto,a,b: b if quartolib.more_different_in_antidiagonal(quarto,a,b) else a),
    'possible': (lambda quarto,a,b: a if quartolib.choose_possible(quarto,a,b) else b)
}
#then leaf place functions, these functions are the ones in the leafs of the then trees, they return a placing action
THEN_LEAF_PLACE_FUNCTIONS=quartolib.get_then_place_functions()
#then leaf choose functions, these functions are the ones used in the leafs of the then trees, they return a choosing action
THEN_LEAF_CHOOSE_FUNCTIONS=quartolib.get_then_choose_functions()

IF_OPERATIONS_LIST=list(IF_OPERATIONS.keys())
#used choosing operations
IF_OPERATIONS_CHOOSE=['not','or','and','ne','eq','ne']#,'truechar','falsechar']
#used placing operations
IF_OPERATIONS_PLACE=['mul','add','sub','not','or','gt','lt','gte','lte','and','eq','ne']
#operations that require only one operand
IF_OPERATIONS_WITH_ONE_OPERAND=set(['not','truechar','falsechar'])
#list of functions that the if tree can use, these functions return basic data about the current state of the game
#they can be seen as a cooked status
IF_CHOOSE_FUNCTIONS=quartolib.get_choose_functions()
IF_PLACE_FUNCTIONS=quartolib.get_place_functions()
#last type of value that a leaf in the if trees can be, a list of constants
IF_PLACE_VALUES=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,True,False]
IF_CHOOSE_VALUES=['high','not_high','solid','not_solid','coloured','not_coloured','square','not_square',True,False]
#list composing everything in groups
IF_POSSIBLE_CHOOSE_VALUES=[[(op,'operation') for op in IF_OPERATIONS_CHOOSE],[(func,'function') for func in IF_CHOOSE_FUNCTIONS]+[(val,'value') for val in IF_CHOOSE_VALUES]]

IF_POSSIBLE_PLACE_VALUES=[[(op,'operation') for op in IF_OPERATIONS_PLACE],[(func,'function') for func in IF_PLACE_FUNCTIONS]+[(val,'value') for val in IF_PLACE_VALUES]]

THEN_POSSIBLE_CHOOSE_VALUES=[[(op,'operation') for op in list(THEN_CHOOSE_OPERATIONS.keys())],[(leaf,'leaf') for leaf in THEN_LEAF_CHOOSE_FUNCTIONS]]

THEN_POSSIBLE_PLACE_VALUES=[[(op,'operation') for op in list(THEN_PLACE_OPERATIONS.keys())],[(leaf,'leaf') for leaf in THEN_LEAF_PLACE_FUNCTIONS]]

#max depth of trees
MAX_DEPTH=6
class ThenNode:
    #the then node is the action used after checking the condition of the rule
    def __init__(self,parent,choose_piece,quarto) -> None:
        self.parent=parent
        #info about parent, choose rule etc.
        self.quarto=quarto
        self.choose_piece=choose_piece
        #childs are other ThenNode elements
        self.childs=[]
        #update depth
        self.depth=0 if self.parent is None else self.parent.depth+1
        #value is a random pick from the possible ones, if the depth is maxed out pick a leaf node, otherwise random between operation or leaf
        #value=random.choice(THEN_POSSIBLE_CHOOSE_VALUES[0 if self.parent is None else random.choice([0,1,1]) if self.depth<MAX_DEPTH else 1] if self.choose_piece else THEN_POSSIBLE_PLACE_VALUES[0 if self.parent is None else random.choice([0,1,1]) if self.depth<MAX_DEPTH else 1])
        value=random.choice(THEN_POSSIBLE_CHOOSE_VALUES[0 if self.parent is None else random.randint(0,1) if self.depth<MAX_DEPTH else 1] if self.choose_piece else THEN_POSSIBLE_PLACE_VALUES[0 if self.parent is None else random.randint(0,1) if self.depth<MAX_DEPTH else 1])
        #setup info about the node, like if the node is a leaf etc.
        if self.parent is None:
            value=('possible','operation')
        self.value=value[0]
        self.op=value[1]=='operation'
        self.leaf=value[1]=='leaf'
        self.optdict=None
        if self.op:
            #if the node is an operation generate two childs
            self.optdict=THEN_CHOOSE_OPERATIONS if self.choose_piece else THEN_PLACE_OPERATIONS
            self.childs.append(ThenNode(self,self.choose_piece,self.quarto))
            self.childs.append(ThenNode(self,self.choose_piece,self.quarto))

    def mutate(self):
        if random.random()<0.5 and self.op:
            #mutate one of the childs or both
            num=random.randint(0,2)
            if num==0 or num==2:
                self.childs[0].mutate()
            if num==1 or num==2:
                self.childs[1].mutate()
        else:
            #mutate myself
            if random.random()<0.5 and self.parent is not None:
                #go full random, don't care about what type of thing I was before
                #value=random.choice(THEN_POSSIBLE_CHOOSE_VALUES[random.choice([0,1,1]) if self.depth<MAX_DEPTH else 1] if self.choose_piece else THEN_POSSIBLE_PLACE_VALUES[random.choice([0,1,1]) if self.depth<MAX_DEPTH else 1])
                value=random.choice(THEN_POSSIBLE_CHOOSE_VALUES[0 if self.parent is None else random.randint(0,1) if self.depth<MAX_DEPTH else 1] if self.choose_piece else THEN_POSSIBLE_PLACE_VALUES[0 if self.parent is None else random.randint(0,1) if self.depth<MAX_DEPTH else 1])
                self.value=value[0]
                self.op=value[1]=='operation'
                self.leaf=value[1]=='leaf'
                if self.op:
                    self.optdict=THEN_CHOOSE_OPERATIONS if self.choose_piece else THEN_PLACE_OPERATIONS
                    #if i didn't have any old child or randomly generate new ones because Im an operation
                    if random.random()<1/3 or len(self.childs)!=2:
                        self.childs=[]
                        self.childs.append(ThenNode(self,self.choose_piece,self.quarto))
                        self.childs.append(ThenNode(self,self.choose_piece,self.quarto))
                    elif len(self.childs)==2:
                        #else If I had some childs and the random picked this option mutate some childs or none
                        num=random.randint(0,6)
                        if num==0 or num==2:
                            self.childs[0].mutate()
                        if num==1 or num==2:
                            self.childs[1].mutate()
                else:
                    #If im not an operation setup childs as nothing again
                    self.childs=[]
            else:
                #keep my old type(leaf or operation)
                value=random.choice(THEN_POSSIBLE_CHOOSE_VALUES[0 if self.op else 1] if self.choose_piece else THEN_POSSIBLE_PLACE_VALUES[0 if self.op else 1])
                self.value=value[0]
                self.op=value[1]=='operation'
                self.leaf=value[1]=='leaf'
                if self.op:
                    self.optdict=THEN_CHOOSE_OPERATIONS if self.choose_piece else THEN_PLACE_OPERATIONS
                    if random.random()<1/3:
                        self.childs=[]
                        self.childs.append(ThenNode(self,self.choose_piece,self.quarto))
                        self.childs.append(ThenNode(self,self.choose_piece,self.quarto))
                    else:
                        num=random.randint(0,6)
                        if num==0 or num==2:
                            self.childs[0].mutate()
                        if num==1 or num==2:
                            self.childs[1].mutate()
                        
                else:
                    self.childs=[]

    def set_quarto(self,quarto):
        #set quarto for myself and childs
        self.quarto=quarto
        if self.op:
            for child in self.childs:
                child.set_quarto(self.quarto)

    def action(self):
        if not self.op:
            #if Im a leaf call the function that I refer to
            return self.value(self.quarto)
        else:
            #else evaluate childs and then call teh operation
            evals=[child.action() for child in self.childs]
            left_val,rigth_val=evals[0],evals[1]
            return self.optdict[self.value](self.quarto,left_val,rigth_val)

    def __str__(self):
        #string view
        if self.op:
            return f'({str(self.childs[0])}) {self.value} ({str(self.childs[1])})'
        else:
            return f'{self.value.__name__}'


class IfNode:
    #the ifnode node is the condition controlled for the rule, very similar to thennode
    def __init__(self,parent,choose_piece,quarto) -> None:
        self.parent=parent
        #info
        self.quarto=quarto
        self.choose_piece=choose_piece
        self.childs=[]
        self.depth=0 if self.parent is None else self.parent.depth+1
        #value=random.choice(IF_POSSIBLE_CHOOSE_VALUES[0 if self.parent is None else random.randint(0,2)] if choose_piece else IF_POSSIBLE_PLACE_VALUES[0 if self.parent is None else random.randint(0,2)])
        #get random value
        value=random.choice(IF_POSSIBLE_CHOOSE_VALUES[0 if self.parent is None else random.randint(0,1) if self.depth<MAX_DEPTH else 1] if self.choose_piece else IF_POSSIBLE_PLACE_VALUES[0 if self.parent is None else random.randint(0,1) if self.depth<MAX_DEPTH else 1])
        #setup value info
        self.value=value[0]
        self.op=value[1]=='operation'
        self.func=value[1]=='function'
        self.val=value[1]=='value'
        if self.op:
            #print(f'Need a child or two depending if the operation requires one or two')
            self.childs.append(IfNode(self,self.choose_piece,self.quarto))
            if self.value not in IF_OPERATIONS_WITH_ONE_OPERAND:
                self.childs.append(IfNode(self,self.choose_piece,self.quarto))
        else:
            pass
            #print(f'No need for childs')

    def mutate(self):
        if random.random()<0.5 and self.op:
            #mutate one of the childs or both if I have two and the random pick that option
            num=random.randint(0,2)
            if (num==0 or num==2) or (self.value in IF_OPERATIONS_WITH_ONE_OPERAND):
                self.childs[0].mutate()
            if (num==1 or num==2) and (self.value not in IF_OPERATIONS_WITH_ONE_OPERAND):
                self.childs[1].mutate()
        else:
            #mutate myself
            if random.random()<0.5 and self.parent is not None:
                #go full random, don't care about what type of thing I was before
                #value=random.choice(IF_POSSIBLE_CHOOSE_VALUES[random.randint(0,2)] if self.choose_piece else IF_POSSIBLE_PLACE_VALUES[random.randint(0,2)])
                value=random.choice(IF_POSSIBLE_CHOOSE_VALUES[0 if self.parent is None else random.randint(0,1) if self.depth<MAX_DEPTH else 1] if self.choose_piece else IF_POSSIBLE_PLACE_VALUES[0 if self.parent is None else random.randint(0,1) if self.depth<MAX_DEPTH else 1])
                self.value=value[0]
                self.op=value[1]=='operation'
                self.func=value[1]=='function'
                self.val=value[1]=='value'
                if self.op:
                    #print(f'Need a child or two')
                    if random.random()<1/3 and len(self.childs)>0:
                        #keep old childs
                        if self.value in IF_OPERATIONS_WITH_ONE_OPERAND and len(self.childs)==2:
                            #remove one of the two childs in case
                            self.childs.pop(random.randint(0,len(self.childs)-1))
                        elif (self.value not in IF_OPERATIONS_WITH_ONE_OPERAND) and (len(self.childs)==1):
                            self.childs.append(IfNode(self,self.choose_piece,self.quarto))
                        num=random.randint(0,6)
                        if num==0 or num==2 or (num==3 and (self.value in IF_OPERATIONS_WITH_ONE_OPERAND)):
                            self.childs[0].mutate()
                        if (num==1 or num==2) and (self.value not in IF_OPERATIONS_WITH_ONE_OPERAND):
                            self.childs[1].mutate()
                    else:
                        self.childs=[]
                        self.childs.append(IfNode(self,self.choose_piece,self.quarto))
                        if self.value not in IF_OPERATIONS_WITH_ONE_OPERAND:
                            self.childs.append(IfNode(self,self.choose_piece,self.quarto))
                else:
                    self.childs=[]
            else:
                #keep my old type
                value=random.choice(IF_POSSIBLE_CHOOSE_VALUES[0 if self.op else 1] if self.choose_piece else IF_POSSIBLE_PLACE_VALUES[0 if self.op else 1])
                self.value=value[0]
                self.op=value[1]=='operation'
                self.func=value[1]=='function'
                self.val=value[1]=='value'
                if self.op:
                    #print(f'Need a child or two')
                    if random.random()<1/3 and len(self.childs)>0:
                        #keep old childs
                        if self.value in IF_OPERATIONS_WITH_ONE_OPERAND and len(self.childs)==2:
                            #remove one of the two childs in case
                            self.childs.pop(random.randint(0,len(self.childs)-1))
                        elif (self.value not in IF_OPERATIONS_WITH_ONE_OPERAND) and (len(self.childs)==1):
                            self.childs.append(IfNode(self,self.choose_piece,self.quarto))
                        num=random.randint(0,6)
                        if num==0 or num==2 or (num==3 and (self.value in IF_OPERATIONS_WITH_ONE_OPERAND)):
                            self.childs[0].mutate()
                        if (num==1 or num==2) and (self.value not in IF_OPERATIONS_WITH_ONE_OPERAND):
                            self.childs[1].mutate()
                    else:
                        self.childs=[]
                        self.childs.append(IfNode(self,self.choose_piece,self.quarto))
                        if self.value not in IF_OPERATIONS_WITH_ONE_OPERAND:
                            self.childs.append(IfNode(self,self.choose_piece,self.quarto))
                else:
                    self.childs=[]      

    def set_quarto(self,quarto):
        self.quarto=quarto
        if self.op:
            for child in self.childs:
                child.set_quarto(self.quarto)

    def eval(self):
        #evaluate condition
        if not self.op:
            #if Im a leaf return my constant value or call the function Im associated with
            if self.val:
                return self.value
            else:
                return self.value(self.quarto)
        else:
            #else evaluate childs and then call operation
            evals=[child.eval() for child in self.childs] + [None,None]
            left_val,rigth_val=evals[0],evals[1]
            return IF_OPERATIONS[self.value](left_val,rigth_val)

    def __str__(self):
        #string view
        if self.op:
            if self.value not in IF_OPERATIONS_WITH_ONE_OPERAND:
                return f'({str(self.childs[0])}) {self.value} ({str(self.childs[1])})'
            else:
                return f'{self.value} ({str(self.childs[0])})'

        elif self.func:
            return f'{self.value.__name__}'
        else:
            return f'{self.value}'

class Rule:
    def __init__(self,choose_piece,quarto):
        #my trees, the if one and the then one and my info, so if Im a choose piece rule or a place piece one, and my quarto
        self.quarto=quarto
        self.choose_piece=choose_piece
        self.if_node=IfNode(None,self.choose_piece,self.quarto)
        self.then_node=ThenNode(None,self.choose_piece,self.quarto)
        #data and evaluations
        #does the if tree make sense
        self.rule_make_sense=True
        #does the then tree make sense
        self.action_make_sense=True
        self.rule_quality=0
        self.rule_evaluations=0
        self.rule_true=0
        #game evaluations
        self.game_true=0
        self.game_evaluations=0
        #evaluations on then tree
        self.action_possible=0

    def set_quarto(self,quarto):
        #set my quarto and the ones of the if and then trees
        self.quarto=quarto
        self.if_node.set_quarto(self.quarto)
        self.then_node.set_quarto(self.quarto)

    def evaluate(self):
        #check the if node, this function is called to check if the rule is true or not
        return self.if_node.eval()

    def evaluate_game_rule(self,won):
        # update rule trueness and its evaluations
        self.rule_true+=self.game_true
        self.rule_evaluations+=self.game_evaluations
        #rule make sense check if the if tree make sense, so if it is true at least one time but not true every single time, the limit
        # is put at 2/3 now, but it can be changed making rules more strict
        self.rule_make_sense= self.rule_true>0 and self.rule_true<(2/3)*self.rule_evaluations
        #action make sense check if the then tree is plausible, so if the times that the action returned is possible is pretty high or not
        self.action_make_sense=self.rule_true>0 and self.action_possible>=(2*(self.rule_true/3))
        #rule quality is a metric that helps rules that are taken a small amount of time but in those times they perform good, this metric
        # is used to sort rules, because I want to check first rules that are more precise
        self.rule_quality+=((self.game_evaluations-self.game_true)/self.game_evaluations) * 10 if won else -((self.game_true/self.game_evaluations) * 10)

    def mutate(self,rule_make_sense=True,action_possible=True):
        if (random.random()<0.5 and rule_make_sense) or (rule_make_sense and not action_possible):
            #mutate then tree if the if tree make sense and need to update the then one, or randomly
            self.then_node.mutate()
        else:
            #mutate if tree
            self.if_node.mutate()
        #reset values
        self.reset_evaluation_stats()

    def evaluated(self,thruth,action):
        #update stats of the game at each pick or choose
        self.game_evaluations+=1
        self.game_true+=thruth
        self.action_possible+=action

    def reset_evaluation_stats(self):
        #reset all the stats, function called after mutations, crossover and stuff
        self.rule_make_sense=True
        self.action_make_sense=True
        self.rule_quality=0
        self.rule_evaluations=0
        self.rule_true=0
        self.game_true=0
        self.game_evaluations=0
        self.action_possible=0

    def reset_game_stats(self):
        #reset just stats of the game
        self.game_true=0
        self.game_evaluations=0

    def needs_evaluation(self):
        # do I need to be evaluated or Im an old rule with already some data
        return self.rule_evaluations==0

    def action(self):
        # check the action associated with the rule, so check the then node
        return self.then_node.action()

    def __str__(self):
        #string view
        return f'Rule: If {str(self.if_node)} --> Then {self.then_node}'