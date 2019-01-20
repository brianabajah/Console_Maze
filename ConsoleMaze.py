import random

top=" ___" 
midbar="   |"
b_right="___|"
non_visited_boxes=[]
visited_boxes=[]

def gridmaker(length,height):
    """makes grid of boxes
        returns a list"""
    #Boxes=list(range(1,(length*height)+1)) #Representing the boxes sequentially as int as box 1...7,8,9... etc

    toplooper=looper(top,length)
    midbarloopr=looper(midbar,length)
    b_rightlooper=looper(b_right,length)

    Grid=[toplooper,midbarloopr,b_rightlooper] #top part of the grid
    
    for x in range(1,height): #so that a height of 2 will only extend one row
        Grid.extend([list(midbarloopr),list(b_rightlooper)])

    return Grid
    
def looper(char,y):
    """loops characters to the right side 
        returns a list"""

    startbar="|" #for the indexzero of midbar and bright     
    indexzero="" #will be 1st value of list

    if char is top:
        indexzero=""+top #no edit required
    if char is midbar:
        indexzero=startbar+midbar #one vertical bar before loop begins
    elif char is b_right:
        indexzero=startbar+b_right #one vertical bar before loop begins
    
    outlist=[indexzero]

    for c in range(y-1): #-1 to cater or the 1st value of list,appended indexzero
        outlist.append(char)

    outlist[-1]=outlist[-1]+"\n" #the end of every list skips to the next line

    return outlist

def grid_printer(grid):
    """takes in a list and returns a string
        use to release final output on console"""

    word=""
    for x in range(len(grid)):
        indexwords=""
        for y in range(len(grid[x])):
            indexwords+=grid[x][y]
        word+=indexwords
    
    return word

def int_to_grid_co(box,length,height):
    """Returns the index of the int representation of
        the boxes eg box 1 is in grid[1] and grid[2]
        and sec_index represents y in grid[x][y]"""

    index=1
    row=length 
    for x in range(height-1):
        if box<=row:
            break
        else:
            index+=2
            row+=length
    sec_index=abs(row-length-box+1)
    indexes=[index,index+1,sec_index]    
    return indexes

def mazegen(grid,length,height):
    """for making the maze
        returns a list (new grid)"""
    
    grid_out = list(grid)
    non_visited_boxes = list(range(1,(length*height)+1))
    visited_boxes = []
    total_boxes = length*height
    last_row_Col_one = total_boxes-length+1 #1st box of the last row
    firstmid_column = range(1+length,last_row_Col_one,length)#middle collumn on the far left side
    lastmid_column = range(length*2,total_boxes,length)#middle collumn on the far right side
    select_box = 0
    neighbors = []
    neighbor_box = 0
    Difference = 0

           
                 
    def Break_walls_btwn_us():
        if abs(Difference) == 1 : #right and left vertical bar handler
            indx=[]   
            if Difference > 0 :    #left side delete neighbor vertical bar
                indx=int_to_grid_co(neighbor_box,length,height)
            else:
                indx=int_to_grid_co(select_box,length,height)

            for n in range(2): 
                newvalue= string_changer(grid_out[indx[n]][indx[2]])
                grid_out[indx[n]][indx[2]]=newvalue

        else:   #underscore handler
            indx=[] 
            if Difference > 0 : #top neighbor delete neighbor bottom
                indx=int_to_grid_co(neighbor_box,length,height)
            else:
                indx=int_to_grid_co(select_box,length,height)
                    
            newword=""
            for b in grid_out[indx[1]][indx[2]]:                        
                if b == "_":
                    newword+=" "  
                else:
                    newword+=b
            grid_out[indx[1]][indx[2]]=newword


    while len(visited_boxes) < total_boxes:
        if select_box == 0:
            select_box=random.choice(non_visited_boxes) #using random to select from a list of boxes not visited

        elif select_box!=0 and not neighbors:#backtrack
            select_box=visited_boxes[(visited_boxes.index(select_box)-1)]           
                                 
        else:
            select_box = neighbor_box
            
        neighbors.clear()
        if 0<select_box<=length: #dealing with top row of grid
        
            if select_box == 1: #first box of row one
                neighbors.extend([select_box+1,select_box+length]) #neighbors are on right box and box below it(select_box+length)
            elif select_box == length:#last box of row one
                neighbors.extend([select_box-1,select_box+length]) #neighbors are on left box and box below it(select_box+length)
            else:
                neighbors.extend([select_box+1,select_box-1,select_box+length])#neighbors are on right,left and below box
    
        elif last_row_Col_one<=select_box<=total_boxes: #last row    

            if select_box == last_row_Col_one: #first box of last row
                neighbors.extend([select_box+1,select_box-length])
            elif select_box == total_boxes:
                neighbors.extend([select_box-1,select_box-length])
            else:
                neighbors.extend([select_box-1,select_box+1,select_box-length])

        else: #everything else
            if select_box in firstmid_column:
                neighbors.extend([select_box+1,select_box+length,select_box-length])
            elif select_box in lastmid_column:
                neighbors.extend([select_box-1,select_box+length,select_box-length])
            else:
                neighbors.extend([select_box+1,select_box-1,select_box+length,select_box-length])
        if select_box != 0:
            a=set(neighbors)
            b=set(visited_boxes)
            neighbors=list(a-b)         

        if neighbors:
            neighbor_box = random.choice(neighbors)
            Difference = select_box-neighbor_box
            Break_walls_btwn_us()

        if select_box not in visited_boxes:
            visited_boxes.append(select_box)
        if select_box in non_visited_boxes:
            non_visited_boxes.remove(select_box)        

    return grid_out              

def string_changer(string):    
    newvalue=list(string)
    newvalue[len(newvalue)-1]=" "
    out="".join(newvalue)
    return out

# mazeraw=gridmaker(10,10)
# mazzze=mazegen(mazeraw,10,10)
# print(grid_printer(mazzze))
while True:
    length=int(input("Grid length(horizontal):"))
    height=int(input("Grid height(vertical):"))
    mazeraw=gridmaker(length,height)
    mazeready=mazegen(mazeraw,length,height)      
    print(grid_printer(mazeready))    
    outnow=input("Enter 0 to exit")
    if outnow==0:
        break
