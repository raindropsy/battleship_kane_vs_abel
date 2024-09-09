#import modules
from Game_board import gameboard #The array storing information regarding board.
from Game_board import ship_location 
from Helper_functions import join_int
from Helper_functions import check_coordinates
import random


#function to generate ship as a cluster of 1 along its lengths    
def generate_ships(ship_length):
    #variable to track if check coordinates has resolve all 
    #conflicts.
    coordinate_check = False

    #variable tracking if ship generation is horizontal or 
    #vertical. False for horizontal. True for vertical.
    orientation = random.choice([True, False])

    #set random coordinate to plot ship
    coordinate = random.randint(0, gameboard.size - 1)

    #function to check if coordinate has already been taken
    #by prior generation, checks for and correct any out
    #of array bounds scenario's due to the random nature of
    #the generation.
    ##returns True/False, valid x_coordinate & y_coordinate
    #if true
    coordinate_check, x_coordinate, y_coordinate, =\
        check_coordinates(coordinate, ship_location, ship_length,
                          orientation)
    
    if coordinate_check == False:
        return False
    #if check passed (True) generate ship along coordinates.
    #(horizontal) 
    elif(coordinate_check == True and orientation == False):
        for i in range(ship_length):
            gameboard[x_coordinate, y_coordinate + i] =\
                gameboard[x_coordinate, y_coordinate + i] +1
            #we can keep an array containing only index of ship 
            #placed instead of tracking the entire gameboard.   
            ship_location.append(join_int(x_coordinate,\
                                          (y_coordinate + i)))
        return True
    elif(coordinate_check == True and orientation == True):
    #if check passed (True) generate ship along coordinates.
    #(vertical) 
        for i in range(ship_length):
            gameboard[x_coordinate + i, y_coordinate] =\
                gameboard[x_coordinate + i, y_coordinate] +1
            #we can keep an array containing only index of ship 
            #placed instead of tracking the entire gameboard. 
            ship_location.append(join_int(x_coordinate + i,
                                          (y_coordinate)))
        return True
    else:
        print("something went wrong with generate ship of length:",
              ship_length)


#this function runs with multiple while loop to generate the
#required ship quantity along with its length.   
def set_ship():

    #variable check to indicate if ship has been generated 
    #successfully or not.
    patrol_boat = False
    submarine = False
    destroyer = False
    battleship = False
    carrier = False

    #while loop will keep trying until True, return False 
    #if there is a conflict.
    while patrol_boat == False:
        patrol_boat = generate_ships(2)

    while patrol_boat == True and submarine == False:
        submarine = generate_ships(3)
    
    while submarine == True and destroyer == False:
         destroyer = generate_ships(3)
    
    while destroyer == True and battleship == False:
         battleship = generate_ships(4)
    
    while battleship == True and carrier == False:
         carrier = generate_ships(5)
    