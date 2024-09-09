#Govern towards handling the statte of the game, in this case the
#array housing ship information

#import modules
from Helper_functions import split_int
import numpy as np

#borrows the zeroes function from np library, return array 
#filled with 0 for a given shape. gameboard is an array.
ship_location = []
gameboard = np.zeros((10, 10), int)


#This function is used to clear information from the previous run
#from ship_location and gameboard.
def clear_the_board():
    list_to_clear = ship_location[:]
    for i in range(len(list_to_clear)):
        x_coordinate, y_coordinate = split_int(list_to_clear[i])
        gameboard[x_coordinate, y_coordinate] =\
              gameboard[x_coordinate, y_coordinate] -1
    ship_location.clear()
    


