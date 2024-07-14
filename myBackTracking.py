#imports
import numpy as np
import random
import copy
import time
global AssignmentCount, ConsistancyChecks;
AssignmentCount=0;
ConsistancyChecks=0;
#init state 4x10----------------------------------------------------------------------------------------------------------------
class State:
    def __init__(self):
      self.Rows= [[3, -1, 6,1,-1,5,8,7,9,2],[-1,-1,-1,3,-1,-1,-1,4,-1,-1],[0,1,-1,4,-1,7,9,8,-1,2]]
      self.ColumnSums=[11,7,18,8,15,13,23,19,12,9]


    def print_state(self):
        print("Rows:")
        for row in self.Rows:
            print(row)
        print("Coloumns Sums:\n", self.ColumnSums)

#end init state------------------------------------------------------------------------------------------------------------

class Variable:
  def __init__(self):
    row=self.row
    col= self.col
    self.Domain = [0,1,2,3,4,5,6,7,8,9]
    self.DomainCount= 10


#check
state = State()
#state.print_state()



def select_unassigned_variable(state):
    for row_idx, row in enumerate(state.Rows):
        for col_idx, value in enumerate(row):
            if value == -1:
                return (row_idx, col_idx)


def BackTrack(state, row, col):
    global AssignmentCount
    if row==2 and col==10:
      #state.print_state()
      return state # reached final cell 2,9

    if col==10:
      row+=1
      col=0


    if state.Rows[row][col] != -1:
      return BackTrack(state, row, col+1)


    for value in range(10): # are you sure
        #BeforeState = copy.deepcopy(state)  # Make a copy of the state before making a move
        if ConstraintCheck(row, col, state, value):
          state.Rows[row][col] = value # Assign the value to the variable
          AssignmentCount+=1
          result = BackTrack(state, row, col +1)  # Recursively backtrack
          if result :
              return True  # If a solution is found, return it
          state.Rows[row][col] = -1  # Undo the assignment if no solution is found
    return False  # If no solution is found after trying all values, return None


def ForwardChecking(state, row, col):
    global AssignmentCount
    if row==2 and col==10:
      #state.print_state()
      return state # reached final cell 2,9

    if col==10:
      row+=1
      col=0


    if state.Rows[row][col] != -1:
      return BackTrack(state, row, col+1)




def ConstraintCheck(VariableRow, VariableCol, state, value):
    global ConsistancyChecks
    # Check horizontally within the row
    for i in range(10):
      if i!=VariableCol:
        if state.Rows[VariableRow][i] == value:
          ConsistancyChecks+=1;
          return False

    # Check vertically above the current position
    if VariableRow > 0 and state.Rows[VariableRow - 1][VariableCol] == value:
        ConsistancyChecks+=1;
        return False

    # Check vertically below the current position
    if VariableRow < len(state.Rows) -1 and state.Rows[VariableRow + 1][VariableCol] == value:
        ConsistancyChecks+=1;
        return False

###############################################################################################################################################

    # check the diagonal values if we are in first row
    if VariableRow == 0 :
      if VariableCol == 0:
        if state.Rows[1][1] == value:
          ConsistancyChecks+=1;
          return False#  0,0
      if VariableCol == 9:
        if state.Rows[1][8] == value:
          ConsistancyChecks+=1;
          return False#  0,9


      elif state.Rows[VariableRow +1][VariableCol +1] == value or state.Rows[VariableRow +1][VariableCol -1] == value :
        ConsistancyChecks+=1;
        return False #  0,1  0,2  0,3  0,4  0,5  0,6  0,7  0,8

##############################################################################################################################

    # check the diagonal values if we are in last row
    if VariableRow == len(state.Rows) -1 :
      if VariableCol == 0:
        if state.Rows[VariableRow - 1][1] == value:
          ConsistancyChecks+=1;
          return False#  2,0
      if VariableCol == 9:
        if state.Rows[VariableRow - 1][8] == value:
          ConsistancyChecks+=1;
          return False#  2,9


      elif state.Rows[VariableRow -1][VariableCol +1] == value or state.Rows[VariableRow -1][VariableCol -1] == value :
        ConsistancyChecks+=1;
        return False #2,1  2,2  2,3  2,4  2,5  2,6  2,7  2,8

###################################################################################################################################

     # check the diagonal values if we are in middle rows
    if VariableCol == 0 and VariableRow != 0 and VariableRow != len(state.Rows) -1:
      if state.Rows[VariableRow -1][VariableCol +1] == value or state.Rows[VariableRow +1][VariableCol +1] == value :
        ConsistancyChecks+=1;
        return False#   1,0

    if VariableCol == 9 and VariableRow != 0 and VariableRow != len(state.Rows) -1:
      if state.Rows[VariableRow -1][VariableCol -1] == value or state.Rows[VariableRow +1][VariableCol -1] == value :
        ConsistancyChecks+=1;
        return False #  1,9


    if VariableRow > 0 and VariableCol < len(state.Rows[0]) -1 and VariableRow< len(state.Rows) -1 and VariableCol> 0:
      if state.Rows[VariableRow -1][VariableCol -1] == value or state.Rows[VariableRow +1][VariableCol -1] == value or state.Rows[VariableRow -1][VariableCol +1] == value or state.Rows[VariableRow +1][VariableCol +1] == value :
        ConsistancyChecks+=1;
        return False

    sum=0;
    for i in range (len(state.Rows)):
      if state.Rows[i][VariableCol] !=-1:
        sum+=state.Rows[i][VariableCol]

    #check sum constraints
    if sum + value > state.ColumnSums[VariableCol]:
      ConsistancyChecks+=1;
      return False

    #if sum+value == state.ColumnSums[VariableCol] :
     # return True



    # If no constraints are violated, the move is valid
    return True




print('----------Before State----------')
state.print_state()
print('\n--------------------------------')
startime = time.time()
new= BackTrack(state, row=0, col=0)
elapsed_time = time.time() - startime

print(f"\nBacktracking Time: {elapsed_time:.4f} seconds")
print('Number of Assignments :',AssignmentCount)
print('Number of Consistancy Checks :',ConsistancyChecks)
print('\n---------Final Solution---------')
state.print_state()
