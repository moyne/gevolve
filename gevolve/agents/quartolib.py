import numpy as np
import random
import quarto
#this library is composed of all the function used by nodes etc., a lot of them are redundant
NUMROWS=4
NUMCOLUMNS=4
POSITIONS=[(a,b) for a in range(4) for b in range(4)]
def get_placed_pieces(board) :
    #get pieces placed on the board already
    return list(board[board!=-1])

def num_pieces_chosen(quarto) -> int:
    #get num of pieces on the board
    return len(get_placed_pieces(quarto.get_board_status()))

def num_pieces_left(quarto) -> int:
    #num of pieces not on board
    return (NUMROWS*NUMCOLUMNS) - len(get_placed_pieces(quarto.get_board_status()))

def less_used_characteristic(quarto):
    #get less used characteristic, so maybe high etc.
    board=quarto.get_board_status()
    placed_pieces=get_placed_pieces(board)
    free_pieces=[_ for _ in range(NUMROWS*NUMCOLUMNS) if _ not in placed_pieces]
    placed_pieces_char={'high':0,'not_high':0,'coloured':0,'not_coloured':0,'solid':0,'not_solid':0,'square':0,'not_square':0}
    for piece in placed_pieces:
        piece_char=quarto.get_piece_charachteristics(piece)
        placed_pieces_char['high']+=piece_char.HIGH
        placed_pieces_char['coloured']+=piece_char.COLOURED
        placed_pieces_char['solid']+=piece_char.SOLID
        placed_pieces_char['square']+=piece_char.SQUARE
        placed_pieces_char['not_high']+=not piece_char.HIGH
        placed_pieces_char['not_coloured']+=not piece_char.COLOURED
        placed_pieces_char['not_solid']+=not piece_char.SOLID
        placed_pieces_char['not_square']+=not piece_char.SQUARE
    minval,minchar=None,'high'
    for k,v in placed_pieces_char.items():
        if minval is None or minval>v:
            minval=v
            minchar=k
    return minchar

def most_used_characteristic(quarto):
    #get most used characteristic, so maybe high etc.
    board=quarto.get_board_status()
    placed_pieces=get_placed_pieces(board)
    free_pieces=[_ for _ in range(NUMROWS*NUMCOLUMNS) if _ not in placed_pieces]
    placed_pieces_char={'high':0,'not_high':0,'coloured':0,'not_coloured':0,'solid':0,'not_solid':0,'square':0,'not_square':0}
    for piece in placed_pieces:
        piece_char=quarto.get_piece_charachteristics(piece)
        placed_pieces_char['high']+=piece_char.HIGH
        placed_pieces_char['coloured']+=piece_char.COLOURED
        placed_pieces_char['solid']+=piece_char.SOLID
        placed_pieces_char['square']+=piece_char.SQUARE
        placed_pieces_char['not_high']+=not piece_char.HIGH
        placed_pieces_char['not_coloured']+=not piece_char.COLOURED
        placed_pieces_char['not_solid']+=not piece_char.SOLID
        placed_pieces_char['not_square']+=not piece_char.SQUARE
    maxval,maxchar=None,'high'
    for k,v in placed_pieces_char.items():
        if maxval is None or maxval<v:
            maxval=v
            maxchar=k
    return maxchar

def most_used_row(quarto):
    #get which row is the most used one
    return np.argmax(np.count_nonzero(quarto.get_board_status()!=-1,axis=1))

def most_used_column(quarto):
    #get which column is the most used one
    return np.argmax(np.count_nonzero(quarto.get_board_status()!=-1,axis=0))

def less_used_row(quarto):
    #get which row is the least used one
    return np.argmin(np.count_nonzero(quarto.get_board_status()!=-1,axis=1))

def less_used_column(quarto):
    #get which column is the least used one
    return np.argmin(np.count_nonzero(quarto.get_board_status()!=-1,axis=0))

def most_used_column_not_complete(quarto):
    #get which column is the most used one, except for the full ones
    count=np.count_nonzero(quarto.get_board_status()!=-1,axis=0).tolist()
    maxcount=0
    maxcol=0
    for a in range(NUMCOLUMNS):
        if count[a]>=maxcount and count[a]<NUMCOLUMNS:
            maxcount=count[a]
            maxcol=a
    return maxcol

def most_used_row_not_complete(quarto):
    #get which row is the most used one, except for the full ones
    count=np.count_nonzero(quarto.get_board_status()!=-1,axis=1).tolist()
    maxcount=0
    maxrow=0
    for a in range(NUMROWS):
        if count[a]>=maxcount and count[a]<NUMROWS:
            maxcount=count[a]
            maxrow=a
    return maxrow

def num_elements_in_antidiagonal(quarto):
    #num pieces in the antidiagonal
    return np.count_nonzero(np.fliplr(quarto.get_board_status()).diagonal()!=-1)

def num_elements_in_diagonal(quarto):
    #num pieces in the diagonal
    return np.count_nonzero(quarto.get_board_status().diagonal()!=-1)

def num_pieces_in_most_used_row(quarto):
    #num pieces in the most used row
    return np.count_nonzero(quarto.get_board_status()!=-1,axis=1)[most_used_row(quarto)]

def num_pieces_in_most_used_column(quarto):
    #num pieces in the most used column
    return np.count_nonzero(quarto.get_board_status()!=-1,axis=1)[most_used_column(quarto)]

def num_pieces_in_most_used_row_not_complete(quarto):
    #num pieces in most used row not complete
    return np.count_nonzero(quarto.get_board_status()!=-1,axis=1)[most_used_row_not_complete(quarto)]

def num_pieces_in_most_used_column_not_complete(quarto):
    #num pieces in most used column not complete
    return np.count_nonzero(quarto.get_board_status()!=-1,axis=1)[most_used_column_not_complete(quarto)]

def num_pieces_in_less_used_row(quarto):
    #num pieces in less used row
    return np.count_nonzero(quarto.get_board_status()!=-1,axis=1)[less_used_column(quarto)]

def num_pieces_in_less_used_column(quarto):
    #num pieces in less used column
    return np.count_nonzero(quarto.get_board_status()!=-1,axis=1)[less_used_column(quarto)]

def element_in_less_used_column(quarto):
    #pick a place in the less used column
    column=less_used_column(quarto)
    possible_placements=[(a[1],a[0]) for a in np.argwhere(quarto.get_board_status()==-1).tolist() if a[1]==column]
    return random.choice(possible_placements)

def element_in_less_used_row(quarto):
    #pick a place in the least used row
    row=less_used_row(quarto)
    possible_placements=[(a[1],a[0]) for a in np.argwhere(quarto.get_board_status()==-1).tolist() if a[0]==row]
    return random.choice(possible_placements)

def element_in_most_used_row_not_complete(quarto):
    #pick a place in the most used row that is yet to fill
    row=most_used_row_not_complete(quarto)
    possible_placements=[(a[1],a[0]) for a in np.argwhere(quarto.get_board_status()==-1).tolist() if a[0]==row]
    return random.choice(possible_placements)

def element_in_most_used_column_not_complete(quarto):
    #pick a place in the most used column that is yet to fill
    column=most_used_column_not_complete(quarto)
    possible_placements=[(a[1],a[0]) for a in np.argwhere(quarto.get_board_status()==-1).tolist() if a[1]==column]
    return random.choice(possible_placements)


def element_in_diagonal(quarto):
    #pick a place in the diagonal
    return random.choice([a for a in POSITIONS if a[0]==a[1]])

def element_in_antidiagonal(quarto):
    #pick a place in the antidiagonal
    return random.choice([a for a in POSITIONS if a[0]+a[1]==NUMROWS-1])

def element_in_corner(quarto):
    #pick a place in the corner, so the border
    return random.choice([a for a in POSITIONS if a[0]==0 or a[0]==NUMCOLUMNS-1 or a[1]==0 or a[1]==NUMROWS-1])

def element_inside(quarto):
    #pick a place not in the border
    return random.choice([a for a in POSITIONS if a[0]!=0 and a[0]!=NUMCOLUMNS-1 and a[1]!=0 and a[1]!=NUMROWS-1])

def not_high_piece(quarto):
    #pick a short piece, the functions below are all similar
    return random.choice([a for a in range(NUMCOLUMNS*NUMROWS) if not quarto.get_piece_charachteristics(a).HIGH])
    
def not_solid_piece(quarto):
    return random.choice([a for a in range(NUMCOLUMNS*NUMROWS) if not quarto.get_piece_charachteristics(a).SOLID])

def not_coloured_piece(quarto):
    return random.choice([a for a in range(NUMCOLUMNS*NUMROWS) if not quarto.get_piece_charachteristics(a).COLOURED])

def not_square_piece(quarto):
    return random.choice([a for a in range(NUMCOLUMNS*NUMROWS) if not quarto.get_piece_charachteristics(a).SQUARE])

def high_piece(quarto):
    return random.choice([a for a in range(NUMCOLUMNS*NUMROWS) if quarto.get_piece_charachteristics(a).HIGH])

def solid_piece(quarto):
    return random.choice([a for a in range(NUMCOLUMNS*NUMROWS) if quarto.get_piece_charachteristics(a).SOLID])

def coloured_piece(quarto):
    return random.choice([a for a in range(NUMCOLUMNS*NUMROWS) if quarto.get_piece_charachteristics(a).COLOURED])

def square_piece(quarto):
    return random.choice([a for a in range(NUMCOLUMNS*NUMROWS) if quarto.get_piece_charachteristics(a).SQUARE])

def place_possible(quarto,a,b):
    #get if a is possible, or b is possible
    return a in [(a[1],a[0]) for a in np.argwhere(quarto.get_board_status()==-1).tolist()]

def choose_possible(quarto,a,b):
    #get if a is possible or b is possible
    return a in [_ for _ in range(NUMROWS*NUMCOLUMNS) if _ not in get_placed_pieces(quarto.get_board_status())]

def compare_elements_in_columns(quarto,a,b):
    #is a column more full than b one?
    board=quarto.get_board_status()
    ela,elb=np.count_nonzero(board[:,a]!=-1),np.count_nonzero(board[:,b]!=-1)
    return True if ela>elb and ela!=NUMROWS else False


def compare_elements_in_rows(quarto,a,b):
    #is a row more full than b one?
    board=quarto.get_board_status()
    ela,elb=np.count_nonzero(board[a,:]!=-1),np.count_nonzero(board[b,:]!=-1)
    return True if ela>elb and ela!=NUMCOLUMNS else False

def compare_elements_in_diag(quarto,a,b):
    #is a diagonal more full than b one?
    board=quarto.get_board_status()
    ela,elb=np.count_nonzero(np.diagonal(board,a[0]-a[1])!=-1),np.count_nonzero(np.diagonal(board,b[0]-b[1])!=-1)
    return ela>elb

def compare_elements_in_antidiag(quarto,a,b):
    #is a antidiagonal more full than b one?
    board=quarto.get_board_status()
    ela,elb=np.count_nonzero(np.diagonal(np.fliplr(board),a[0]-a[1])!=-1),np.count_nonzero(np.diagonal(np.fliplr(board),b[0]-b[1])!=-1)
    return ela>elb

def compare_uniqueness(quarto,a,b):
    #is a more unique than b?
    apiece,bpiece=quarto.get_piece_charachteristics(a),quarto.get_piece_charachteristics(b)
    board=quarto.get_board_status()
    placed_pieces=get_placed_pieces(board)
    placed_pieces_char={'high':0,'not_high':0,'coloured':0,'not_coloured':0,'solid':0,'not_solid':0,'square':0,'not_square':0}
    for piece in placed_pieces:
        piece_char=quarto.get_piece_charachteristics(piece)
        placed_pieces_char['high']+=piece_char.HIGH
        placed_pieces_char['coloured']+=piece_char.COLOURED
        placed_pieces_char['solid']+=piece_char.SOLID
        placed_pieces_char['square']+=piece_char.SQUARE
        placed_pieces_char['not_high']+=not piece_char.HIGH
        placed_pieces_char['not_coloured']+=not piece_char.COLOURED
        placed_pieces_char['not_solid']+=not piece_char.SOLID
        placed_pieces_char['not_square']+=not piece_char.SQUARE
    aval=placed_pieces_char['high' if apiece.HIGH else 'not_high'] + placed_pieces_char['coloured' if apiece.COLOURED else 'not_coloured'] + placed_pieces_char['solid' if apiece.SOLID else 'not_solid'] +placed_pieces_char['square' if apiece.SQUARE else 'not_square']
    bval=placed_pieces_char['high' if bpiece.HIGH else 'not_high'] + placed_pieces_char['coloured' if bpiece.COLOURED else 'not_coloured'] + placed_pieces_char['solid' if bpiece.SOLID else 'not_solid'] +placed_pieces_char['square' if bpiece.SQUARE else 'not_square']
    return aval>bval


def compare_trues(quarto,a,b):
    #does a have more true characteristics than b?
    apiece,bpiece=quarto.get_piece_charachteristics(a),quarto.get_piece_charachteristics(b)
    return apiece.HIGH+apiece.COLOURED+apiece.SOLID+apiece.SQUARE>bpiece.HIGH+bpiece.COLOURED+bpiece.SOLID+bpiece.SQUARE

def more_different_in_most_used_row_not_complete(quarto,a,b):
    #is a more unique in the most used row that is yet to complete than b?
    apiece,bpiece=quarto.get_piece_charachteristics(a),quarto.get_piece_charachteristics(b)
    board=quarto.get_board_status()
    placed_pieces=get_placed_pieces(board[most_used_row_not_complete(quarto),:])
    placed_pieces_char={'high':0,'not_high':0,'coloured':0,'not_coloured':0,'solid':0,'not_solid':0,'square':0,'not_square':0}
    for piece in placed_pieces:
        piece_char=quarto.get_piece_charachteristics(piece)
        placed_pieces_char['high']+=piece_char.HIGH
        placed_pieces_char['coloured']+=piece_char.COLOURED
        placed_pieces_char['solid']+=piece_char.SOLID
        placed_pieces_char['square']+=piece_char.SQUARE
        placed_pieces_char['not_high']+=not piece_char.HIGH
        placed_pieces_char['not_coloured']+=not piece_char.COLOURED
        placed_pieces_char['not_solid']+=not piece_char.SOLID
        placed_pieces_char['not_square']+=not piece_char.SQUARE
    chars=[k for k,v in placed_pieces_char.items() if v==len(placed_pieces)]
    achars=[k for k,v in {'high':apiece.HIGH,'not_high':not apiece.HIGH,'coloured':apiece.COLOURED,'not_coloured':not apiece.COLOURED,'solid':apiece.SOLID,'not_solid':not apiece.SOLID,'square':apiece.SQUARE,'not_square':not apiece.SQUARE}.items() if v]
    bchars=[k for k,v in {'high':bpiece.HIGH,'not_high':not bpiece.HIGH,'coloured':bpiece.COLOURED,'not_coloured':not bpiece.COLOURED,'solid':bpiece.SOLID,'not_solid':not bpiece.SOLID,'square':bpiece.SQUARE,'not_square':not bpiece.SQUARE}.items() if v]
    aval,bval=sum([k in chars for k in achars]),sum([k in chars for k in bchars])
    return aval>bval

def more_different_in_most_used_column_not_complete(quarto,a,b):
    #is a more unique in the most used column that is yet to complete than b?
    apiece,bpiece=quarto.get_piece_charachteristics(a),quarto.get_piece_charachteristics(b)
    board=quarto.get_board_status()
    placed_pieces=get_placed_pieces(board[:,most_used_column_not_complete(quarto)])
    placed_pieces_char={'high':0,'not_high':0,'coloured':0,'not_coloured':0,'solid':0,'not_solid':0,'square':0,'not_square':0}
    for piece in placed_pieces:
        piece_char=quarto.get_piece_charachteristics(piece)
        placed_pieces_char['high']+=piece_char.HIGH
        placed_pieces_char['coloured']+=piece_char.COLOURED
        placed_pieces_char['solid']+=piece_char.SOLID
        placed_pieces_char['square']+=piece_char.SQUARE
        placed_pieces_char['not_high']+=not piece_char.HIGH
        placed_pieces_char['not_coloured']+=not piece_char.COLOURED
        placed_pieces_char['not_solid']+=not piece_char.SOLID
        placed_pieces_char['not_square']+=not piece_char.SQUARE
    chars=[k for k,v in placed_pieces_char.items() if v==len(placed_pieces)]
    achars=[k for k,v in {'high':apiece.HIGH,'not_high':not apiece.HIGH,'coloured':apiece.COLOURED,'not_coloured':not apiece.COLOURED,'solid':apiece.SOLID,'not_solid':not apiece.SOLID,'square':apiece.SQUARE,'not_square':not apiece.SQUARE}.items() if v]
    bchars=[k for k,v in {'high':bpiece.HIGH,'not_high':not bpiece.HIGH,'coloured':bpiece.COLOURED,'not_coloured':not bpiece.COLOURED,'solid':bpiece.SOLID,'not_solid':not bpiece.SOLID,'square':bpiece.SQUARE,'not_square':not bpiece.SQUARE}.items() if v]
    aval,bval=sum([k in chars for k in achars]),sum([k in chars for k in bchars])
    return aval>bval
    
def more_different_in_less_used_row(quarto,a,b):
    #is a more unique in the less used row than b?
    apiece,bpiece=quarto.get_piece_charachteristics(a),quarto.get_piece_charachteristics(b)
    board=quarto.get_board_status()
    placed_pieces=get_placed_pieces(board[less_used_row(quarto),:])
    placed_pieces_char={'high':0,'not_high':0,'coloured':0,'not_coloured':0,'solid':0,'not_solid':0,'square':0,'not_square':0}
    for piece in placed_pieces:
        piece_char=quarto.get_piece_charachteristics(piece)
        placed_pieces_char['high']+=piece_char.HIGH
        placed_pieces_char['coloured']+=piece_char.COLOURED
        placed_pieces_char['solid']+=piece_char.SOLID
        placed_pieces_char['square']+=piece_char.SQUARE
        placed_pieces_char['not_high']+=not piece_char.HIGH
        placed_pieces_char['not_coloured']+=not piece_char.COLOURED
        placed_pieces_char['not_solid']+=not piece_char.SOLID
        placed_pieces_char['not_square']+=not piece_char.SQUARE
    chars=[k for k,v in placed_pieces_char.items() if v==len(placed_pieces)]
    achars=[k for k,v in {'high':apiece.HIGH,'not_high':not apiece.HIGH,'coloured':apiece.COLOURED,'not_coloured':not apiece.COLOURED,'solid':apiece.SOLID,'not_solid':not apiece.SOLID,'square':apiece.SQUARE,'not_square':not apiece.SQUARE}.items() if v]
    bchars=[k for k,v in {'high':bpiece.HIGH,'not_high':not bpiece.HIGH,'coloured':bpiece.COLOURED,'not_coloured':not bpiece.COLOURED,'solid':bpiece.SOLID,'not_solid':not bpiece.SOLID,'square':bpiece.SQUARE,'not_square':not bpiece.SQUARE}.items() if v]
    aval,bval=sum([k in chars for k in achars]),sum([k in chars for k in bchars])
    return aval>bval

def more_different_in_less_used_column(quarto,a,b):
    #is a more unique in the less used column than b?
    apiece,bpiece=quarto.get_piece_charachteristics(a),quarto.get_piece_charachteristics(b)
    board=quarto.get_board_status()
    placed_pieces=get_placed_pieces(board[:,less_used_column(quarto)])
    placed_pieces_char={'high':0,'not_high':0,'coloured':0,'not_coloured':0,'solid':0,'not_solid':0,'square':0,'not_square':0}
    for piece in placed_pieces:
        piece_char=quarto.get_piece_charachteristics(piece)
        placed_pieces_char['high']+=piece_char.HIGH
        placed_pieces_char['coloured']+=piece_char.COLOURED
        placed_pieces_char['solid']+=piece_char.SOLID
        placed_pieces_char['square']+=piece_char.SQUARE
        placed_pieces_char['not_high']+=not piece_char.HIGH
        placed_pieces_char['not_coloured']+=not piece_char.COLOURED
        placed_pieces_char['not_solid']+=not piece_char.SOLID
        placed_pieces_char['not_square']+=not piece_char.SQUARE
    chars=[k for k,v in placed_pieces_char.items() if v==len(placed_pieces)]
    achars=[k for k,v in {'high':apiece.HIGH,'not_high':not apiece.HIGH,'coloured':apiece.COLOURED,'not_coloured':not apiece.COLOURED,'solid':apiece.SOLID,'not_solid':not apiece.SOLID,'square':apiece.SQUARE,'not_square':not apiece.SQUARE}.items() if v]
    bchars=[k for k,v in {'high':bpiece.HIGH,'not_high':not bpiece.HIGH,'coloured':bpiece.COLOURED,'not_coloured':not bpiece.COLOURED,'solid':bpiece.SOLID,'not_solid':not bpiece.SOLID,'square':bpiece.SQUARE,'not_square':not bpiece.SQUARE}.items() if v]
    aval,bval=sum([k in chars for k in achars]),sum([k in chars for k in bchars])
    return aval>bval

def more_different_in_diagonal(quarto,a,b):
    #is a more unique in the diagonal than b?
    apiece,bpiece=quarto.get_piece_charachteristics(a),quarto.get_piece_charachteristics(b)
    board=quarto.get_board_status()
    placed_pieces=get_placed_pieces(np.diag(board))
    placed_pieces_char={'high':0,'not_high':0,'coloured':0,'not_coloured':0,'solid':0,'not_solid':0,'square':0,'not_square':0}
    for piece in placed_pieces:
        piece_char=quarto.get_piece_charachteristics(piece)
        placed_pieces_char['high']+=piece_char.HIGH
        placed_pieces_char['coloured']+=piece_char.COLOURED
        placed_pieces_char['solid']+=piece_char.SOLID
        placed_pieces_char['square']+=piece_char.SQUARE
        placed_pieces_char['not_high']+=not piece_char.HIGH
        placed_pieces_char['not_coloured']+=not piece_char.COLOURED
        placed_pieces_char['not_solid']+=not piece_char.SOLID
        placed_pieces_char['not_square']+=not piece_char.SQUARE
    chars=[k for k,v in placed_pieces_char.items() if v==len(placed_pieces)]
    achars=[k for k,v in {'high':apiece.HIGH,'not_high':not apiece.HIGH,'coloured':apiece.COLOURED,'not_coloured':not apiece.COLOURED,'solid':apiece.SOLID,'not_solid':not apiece.SOLID,'square':apiece.SQUARE,'not_square':not apiece.SQUARE}.items() if v]
    bchars=[k for k,v in {'high':bpiece.HIGH,'not_high':not bpiece.HIGH,'coloured':bpiece.COLOURED,'not_coloured':not bpiece.COLOURED,'solid':bpiece.SOLID,'not_solid':not bpiece.SOLID,'square':bpiece.SQUARE,'not_square':not bpiece.SQUARE}.items() if v]
    aval,bval=sum([k in chars for k in achars]),sum([k in chars for k in bchars])
    return aval>bval

def more_different_in_antidiagonal(quarto,a,b):
    #is a more unique in the antidiagonal than b?
    apiece,bpiece=quarto.get_piece_charachteristics(a),quarto.get_piece_charachteristics(b)
    board=quarto.get_board_status()
    placed_pieces=get_placed_pieces(np.fliplr(board).diagonal())
    placed_pieces_char={'high':0,'not_high':0,'coloured':0,'not_coloured':0,'solid':0,'not_solid':0,'square':0,'not_square':0}
    for piece in placed_pieces:
        piece_char=quarto.get_piece_charachteristics(piece)
        placed_pieces_char['high']+=piece_char.HIGH
        placed_pieces_char['coloured']+=piece_char.COLOURED
        placed_pieces_char['solid']+=piece_char.SOLID
        placed_pieces_char['square']+=piece_char.SQUARE
        placed_pieces_char['not_high']+=not piece_char.HIGH
        placed_pieces_char['not_coloured']+=not piece_char.COLOURED
        placed_pieces_char['not_solid']+=not piece_char.SOLID
        placed_pieces_char['not_square']+=not piece_char.SQUARE
    chars=[k for k,v in placed_pieces_char.items() if v==len(placed_pieces)]
    achars=[k for k,v in {'high':apiece.HIGH,'not_high':not apiece.HIGH,'coloured':apiece.COLOURED,'not_coloured':not apiece.COLOURED,'solid':apiece.SOLID,'not_solid':not apiece.SOLID,'square':apiece.SQUARE,'not_square':not apiece.SQUARE}.items() if v]
    bchars=[k for k,v in {'high':bpiece.HIGH,'not_high':not bpiece.HIGH,'coloured':bpiece.COLOURED,'not_coloured':not bpiece.COLOURED,'solid':bpiece.SOLID,'not_solid':not bpiece.SOLID,'square':bpiece.SQUARE,'not_square':not bpiece.SQUARE}.items() if v]
    aval,bval=sum([k in chars for k in achars]),sum([k in chars for k in bchars])
    return aval>bval

def characteristic_in_most_used_row_not_complete(quarto):
    #get a characteristic used in the most used row yet to complete
    board=quarto.get_board_status()
    placed_pieces=get_placed_pieces(board[most_used_row_not_complete(quarto),:])
    placed_pieces_char={'high':0,'not_high':0,'coloured':0,'not_coloured':0,'solid':0,'not_solid':0,'square':0,'not_square':0}
    for piece in placed_pieces:
        piece_char=quarto.get_piece_charachteristics(piece)
        placed_pieces_char['high']+=piece_char.HIGH
        placed_pieces_char['coloured']+=piece_char.COLOURED
        placed_pieces_char['solid']+=piece_char.SOLID
        placed_pieces_char['square']+=piece_char.SQUARE
        placed_pieces_char['not_high']+=not piece_char.HIGH
        placed_pieces_char['not_coloured']+=not piece_char.COLOURED
        placed_pieces_char['not_solid']+=not piece_char.SOLID
        placed_pieces_char['not_square']+=not piece_char.SQUARE
    chars=[k for k,v in placed_pieces_char.items() if v==len(placed_pieces)]
    return chars[0] if len(chars)>0 else 'high'

def characteristic_in_most_used_column_not_complete(quarto):
    #get a characteristic used in the most used column yet to complete
    board=quarto.get_board_status()
    placed_pieces=get_placed_pieces(board[:,most_used_column_not_complete(quarto)])
    placed_pieces_char={'high':0,'not_high':0,'coloured':0,'not_coloured':0,'solid':0,'not_solid':0,'square':0,'not_square':0}
    for piece in placed_pieces:
        piece_char=quarto.get_piece_charachteristics(piece)
        placed_pieces_char['high']+=piece_char.HIGH
        placed_pieces_char['coloured']+=piece_char.COLOURED
        placed_pieces_char['solid']+=piece_char.SOLID
        placed_pieces_char['square']+=piece_char.SQUARE
        placed_pieces_char['not_high']+=not piece_char.HIGH
        placed_pieces_char['not_coloured']+=not piece_char.COLOURED
        placed_pieces_char['not_solid']+=not piece_char.SOLID
        placed_pieces_char['not_square']+=not piece_char.SQUARE
    chars=[k for k,v in placed_pieces_char.items() if v==len(placed_pieces)]
    return chars[0] if len(chars)>0 else 'high'


def characteristic_in_less_used_column(quarto):
    #get a characteristic used in the least used column
    board=quarto.get_board_status()
    placed_pieces=get_placed_pieces(board[:,less_used_column(quarto)])
    placed_pieces_char={'high':0,'not_high':0,'coloured':0,'not_coloured':0,'solid':0,'not_solid':0,'square':0,'not_square':0}
    for piece in placed_pieces:
        piece_char=quarto.get_piece_charachteristics(piece)
        placed_pieces_char['high']+=piece_char.HIGH
        placed_pieces_char['coloured']+=piece_char.COLOURED
        placed_pieces_char['solid']+=piece_char.SOLID
        placed_pieces_char['square']+=piece_char.SQUARE
        placed_pieces_char['not_high']+=not piece_char.HIGH
        placed_pieces_char['not_coloured']+=not piece_char.COLOURED
        placed_pieces_char['not_solid']+=not piece_char.SOLID
        placed_pieces_char['not_square']+=not piece_char.SQUARE
    chars=[k for k,v in placed_pieces_char.items() if v==len(placed_pieces)]
    return chars[0] if len(chars)>0 else 'high'

def characteristic_in_less_used_row(quarto):
    #get a characteristic used in the least used row
    board=quarto.get_board_status()
    placed_pieces=get_placed_pieces(board[less_used_row(quarto),:])
    placed_pieces_char={'high':0,'not_high':0,'coloured':0,'not_coloured':0,'solid':0,'not_solid':0,'square':0,'not_square':0}
    for piece in placed_pieces:
        piece_char=quarto.get_piece_charachteristics(piece)
        placed_pieces_char['high']+=piece_char.HIGH
        placed_pieces_char['coloured']+=piece_char.COLOURED
        placed_pieces_char['solid']+=piece_char.SOLID
        placed_pieces_char['square']+=piece_char.SQUARE
        placed_pieces_char['not_high']+=not piece_char.HIGH
        placed_pieces_char['not_coloured']+=not piece_char.COLOURED
        placed_pieces_char['not_solid']+=not piece_char.SOLID
        placed_pieces_char['not_square']+=not piece_char.SQUARE
    chars=[k for k,v in placed_pieces_char.items() if v==len(placed_pieces)]
    return chars[0] if len(chars)>0 else 'high'

def characteristic_in_diagonal(quarto):
    #get a characteristic used in the diagonal
    board=quarto.get_board_status()
    placed_pieces=get_placed_pieces(np.diag(board))
    placed_pieces_char={'high':0,'not_high':0,'coloured':0,'not_coloured':0,'solid':0,'not_solid':0,'square':0,'not_square':0}
    for piece in placed_pieces:
        piece_char=quarto.get_piece_charachteristics(piece)
        placed_pieces_char['high']+=piece_char.HIGH
        placed_pieces_char['coloured']+=piece_char.COLOURED
        placed_pieces_char['solid']+=piece_char.SOLID
        placed_pieces_char['square']+=piece_char.SQUARE
        placed_pieces_char['not_high']+=not piece_char.HIGH
        placed_pieces_char['not_coloured']+=not piece_char.COLOURED
        placed_pieces_char['not_solid']+=not piece_char.SOLID
        placed_pieces_char['not_square']+=not piece_char.SQUARE
    chars=[k for k,v in placed_pieces_char.items() if v==len(placed_pieces)]
    return chars[0] if len(chars)>0 else 'high'

def characteristic_in_antidiagonal(quarto):
    #get a characteristic used in the antidiagonal
    board=quarto.get_board_status()
    placed_pieces=get_placed_pieces(np.fliplr(board).diagonal())
    placed_pieces_char={'high':0,'not_high':0,'coloured':0,'not_coloured':0,'solid':0,'not_solid':0,'square':0,'not_square':0}
    for piece in placed_pieces:
        piece_char=quarto.get_piece_charachteristics(piece)
        placed_pieces_char['high']+=piece_char.HIGH
        placed_pieces_char['coloured']+=piece_char.COLOURED
        placed_pieces_char['solid']+=piece_char.SOLID
        placed_pieces_char['square']+=piece_char.SQUARE
        placed_pieces_char['not_high']+=not piece_char.HIGH
        placed_pieces_char['not_coloured']+=not piece_char.COLOURED
        placed_pieces_char['not_solid']+=not piece_char.SOLID
        placed_pieces_char['not_square']+=not piece_char.SQUARE
    chars=[k for k,v in placed_pieces_char.items() if v==len(placed_pieces)]
    return chars[0] if len(chars)>0 else 'high'

def characteristic_not_in_most_used_row_not_complete(quarto):
    #get a characteristic NOT USED in the most used row yet to complete
    board=quarto.get_board_status()
    placed_pieces=get_placed_pieces(board[most_used_row_not_complete(quarto),:])
    placed_pieces_char={'high':0,'not_high':0,'coloured':0,'not_coloured':0,'solid':0,'not_solid':0,'square':0,'not_square':0}
    for piece in placed_pieces:
        piece_char=quarto.get_piece_charachteristics(piece)
        placed_pieces_char['high']+=piece_char.HIGH
        placed_pieces_char['coloured']+=piece_char.COLOURED
        placed_pieces_char['solid']+=piece_char.SOLID
        placed_pieces_char['square']+=piece_char.SQUARE
        placed_pieces_char['not_high']+=not piece_char.HIGH
        placed_pieces_char['not_coloured']+=not piece_char.COLOURED
        placed_pieces_char['not_solid']+=not piece_char.SOLID
        placed_pieces_char['not_square']+=not piece_char.SQUARE
    chars=[k for k,v in placed_pieces_char.items() if v==0]
    return chars[0] if len(chars)>0 else 'high'

def characteristic_not_in_most_used_column_not_complete(quarto):
    #get a characteristic NOT USED in the most used column yet to complete
    board=quarto.get_board_status()
    placed_pieces=get_placed_pieces(board[:,most_used_column_not_complete(quarto)])
    placed_pieces_char={'high':0,'not_high':0,'coloured':0,'not_coloured':0,'solid':0,'not_solid':0,'square':0,'not_square':0}
    for piece in placed_pieces:
        piece_char=quarto.get_piece_charachteristics(piece)
        placed_pieces_char['high']+=piece_char.HIGH
        placed_pieces_char['coloured']+=piece_char.COLOURED
        placed_pieces_char['solid']+=piece_char.SOLID
        placed_pieces_char['square']+=piece_char.SQUARE
        placed_pieces_char['not_high']+=not piece_char.HIGH
        placed_pieces_char['not_coloured']+=not piece_char.COLOURED
        placed_pieces_char['not_solid']+=not piece_char.SOLID
        placed_pieces_char['not_square']+=not piece_char.SQUARE
    chars=[k for k,v in placed_pieces_char.items() if v==0]
    return chars[0] if len(chars)>0 else 'high'


def characteristic_not_in_less_used_column(quarto):
    #get a characteristic NOT USED in the least used column
    board=quarto.get_board_status()
    placed_pieces=get_placed_pieces(board[:,less_used_column(quarto)])
    placed_pieces_char={'high':0,'not_high':0,'coloured':0,'not_coloured':0,'solid':0,'not_solid':0,'square':0,'not_square':0}
    for piece in placed_pieces:
        piece_char=quarto.get_piece_charachteristics(piece)
        placed_pieces_char['high']+=piece_char.HIGH
        placed_pieces_char['coloured']+=piece_char.COLOURED
        placed_pieces_char['solid']+=piece_char.SOLID
        placed_pieces_char['square']+=piece_char.SQUARE
        placed_pieces_char['not_high']+=not piece_char.HIGH
        placed_pieces_char['not_coloured']+=not piece_char.COLOURED
        placed_pieces_char['not_solid']+=not piece_char.SOLID
        placed_pieces_char['not_square']+=not piece_char.SQUARE
    chars=[k for k,v in placed_pieces_char.items() if v==0]
    return chars[0] if len(chars)>0 else 'high'

def characteristic_not_in_less_used_row(quarto):
    #get a characteristic NOT USED in the least used row
    board=quarto.get_board_status()
    placed_pieces=get_placed_pieces(board[less_used_row(quarto),:])
    placed_pieces_char={'high':0,'not_high':0,'coloured':0,'not_coloured':0,'solid':0,'not_solid':0,'square':0,'not_square':0}
    for piece in placed_pieces:
        piece_char=quarto.get_piece_charachteristics(piece)
        placed_pieces_char['high']+=piece_char.HIGH
        placed_pieces_char['coloured']+=piece_char.COLOURED
        placed_pieces_char['solid']+=piece_char.SOLID
        placed_pieces_char['square']+=piece_char.SQUARE
        placed_pieces_char['not_high']+=not piece_char.HIGH
        placed_pieces_char['not_coloured']+=not piece_char.COLOURED
        placed_pieces_char['not_solid']+=not piece_char.SOLID
        placed_pieces_char['not_square']+=not piece_char.SQUARE
    chars=[k for k,v in placed_pieces_char.items() if v==0]
    return chars[0] if len(chars)>0 else 'high'

def characteristic_not_in_diagonal(quarto):
    #get a characteristic NOT USED in the diagonal
    board=quarto.get_board_status()
    placed_pieces=get_placed_pieces(np.diag(board))
    placed_pieces_char={'high':0,'not_high':0,'coloured':0,'not_coloured':0,'solid':0,'not_solid':0,'square':0,'not_square':0}
    for piece in placed_pieces:
        piece_char=quarto.get_piece_charachteristics(piece)
        placed_pieces_char['high']+=piece_char.HIGH
        placed_pieces_char['coloured']+=piece_char.COLOURED
        placed_pieces_char['solid']+=piece_char.SOLID
        placed_pieces_char['square']+=piece_char.SQUARE
        placed_pieces_char['not_high']+=not piece_char.HIGH
        placed_pieces_char['not_coloured']+=not piece_char.COLOURED
        placed_pieces_char['not_solid']+=not piece_char.SOLID
        placed_pieces_char['not_square']+=not piece_char.SQUARE
    chars=[k for k,v in placed_pieces_char.items() if v==0]
    return chars[0] if len(chars)>0 else 'high'

def characteristic_not_in_antidiagonal(quarto):
    #get a characteristic NOT USED in the antidiagonal
    board=quarto.get_board_status()
    placed_pieces=get_placed_pieces(np.fliplr(board).diagonal())
    placed_pieces_char={'high':0,'not_high':0,'coloured':0,'not_coloured':0,'solid':0,'not_solid':0,'square':0,'not_square':0}
    for piece in placed_pieces:
        piece_char=quarto.get_piece_charachteristics(piece)
        placed_pieces_char['high']+=piece_char.HIGH
        placed_pieces_char['coloured']+=piece_char.COLOURED
        placed_pieces_char['solid']+=piece_char.SOLID
        placed_pieces_char['square']+=piece_char.SQUARE
        placed_pieces_char['not_high']+=not piece_char.HIGH
        placed_pieces_char['not_coloured']+=not piece_char.COLOURED
        placed_pieces_char['not_solid']+=not piece_char.SOLID
        placed_pieces_char['not_square']+=not piece_char.SQUARE
    chars=[k for k,v in placed_pieces_char.items() if v==0]
    return chars[0] if len(chars)>0 else 'high'

#functions that serve kinda as an export, they return function that we want the genomes to use

def get_then_place_functions():
    return [element_in_less_used_row,element_in_less_used_column,element_in_most_used_row_not_complete,element_in_most_used_column_not_complete,element_inside,element_in_diagonal,element_in_antidiagonal,element_in_corner]

def get_then_choose_functions():
    return [high_piece,not_high_piece,solid_piece,not_solid_piece,coloured_piece,not_coloured_piece,square_piece,not_square_piece]

def get_choose_functions():
    return [#num_elements_in_diagonal,num_elements_in_antidiagonal,num_pieces_in_less_used_column,num_pieces_in_less_used_row,num_pieces_in_most_used_column,
        #num_pieces_in_most_used_row,num_pieces_in_most_used_column_not_complete,num_pieces_in_most_used_row_not_complete,
        #num_pieces_chosen,num_pieces_left,
        less_used_characteristic,most_used_characteristic,characteristic_in_most_used_row_not_complete,characteristic_in_diagonal,
        characteristic_in_most_used_column_not_complete,characteristic_in_antidiagonal,characteristic_not_in_most_used_row_not_complete,characteristic_not_in_diagonal,
        characteristic_not_in_most_used_column_not_complete,characteristic_not_in_antidiagonal,characteristic_in_less_used_column,characteristic_in_less_used_row,
        characteristic_not_in_less_used_column,characteristic_not_in_less_used_row]

def get_place_functions():
    return [num_elements_in_diagonal,num_elements_in_antidiagonal,num_pieces_in_less_used_column,num_pieces_in_less_used_row,num_pieces_in_most_used_column,
        num_pieces_in_most_used_row,num_pieces_in_most_used_column_not_complete,num_pieces_in_most_used_row_not_complete,
        num_pieces_chosen,num_pieces_left,most_used_row,less_used_row,most_used_column,less_used_column,most_used_row_not_complete,most_used_column_not_complete]