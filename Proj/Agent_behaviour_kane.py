#focuses on the bahaviour of kane's way of solving battleship as a
#PP agent

#import modules
from Helper_functions import check_left_and_top
from Helper_functions import check_favourable_coordinate
from Helper_functions import match_favourable_coordinate
from Helper_functions import join_int
from Helper_functions import split_int
from Helper_functions import select_orientation
import random

#hunt and target function trying to assemble the possibilities of
#the remaining coordinates of the ship.
def hunt_and_target_behaviour(hunt_coordinates):
    #split hunt_coordinate to individual integer
    x_coordinate, y_coordinate = split_int(hunt_coordinates)
    
    #to check if any of the coordinate is at the corner
    corner_cases_x = False 
    corner_cases_y = False

    #to return favourable integers
    favourable_left, favourable_right, corner_cases_x = check_favourable_coordinate(x_coordinate)
    favourable_top, favourable_bottom, corner_cases_y = check_favourable_coordinate(y_coordinate)
    #if corner cases in the x coordinate
    if(corner_cases_x == True and corner_cases_y == False):

        #we assemble +right or +left, followed by bottom 
        #and top coordinates
        favourable_coordinate1 = join_int(favourable_left, 
                                          y_coordinate)
        favourable_coordinate2 = join_int(x_coordinate, 
                                          favourable_top)
        favourable_coordinate3 = join_int(x_coordinate, 
                                          favourable_bottom)
        
        #we append the favourable coordinates into an array
        favourable_coordinates = [favourable_coordinate1, 
                                favourable_coordinate2,
                                favourable_coordinate3]

    
    #else if corner cases is in the y coordinate
    elif(corner_cases_y == True and corner_cases_x == False):

        #we assemble the +top or +bottom, followed by 
        #left and right coordinates
        favourable_coordinate1 = join_int(x_coordinate, 
                                          favourable_top)
        favourable_coordinate2 = join_int(favourable_left, 
                                          y_coordinate)
        favourable_coordinate3 = join_int(favourable_right,
                                          y_coordinate)
        
        #we append the favourable coordinates into an array
        favourable_coordinates = [favourable_coordinate1, 
                                favourable_coordinate2,
                                favourable_coordinate3]

    #else if both are corner cases    
    elif(corner_cases_x == True and corner_cases_y == True):
        #we assemble the remaining the 2 possibilities that
        #the ship could exist
        favourable_coordinate1 = join_int(x_coordinate, 
                                          favourable_top)
        favourable_coordinate2 = join_int(favourable_left, 
                                          y_coordinate)
        
        #we append the favourable coordinates into an array
        favourable_coordinates = [favourable_coordinate1, 
                                favourable_coordinate2]

    #under normal circumstances where no values is at the
    #corner
    elif(corner_cases_x == False and corner_cases_y == False):
        favourable_coordinate1 = join_int(favourable_left, 
                                          y_coordinate)
        favourable_coordinate2 = join_int(favourable_right,
                                          y_coordinate)
        favourable_coordinate3 = join_int(x_coordinate, 
                                          favourable_bottom)
        favourable_coordinate4 = join_int(x_coordinate, 
                                          favourable_top)

        #we append the favourable coordinates into an array
        favourable_coordinates = [favourable_coordinate1, 
                                favourable_coordinate2,
                                favourable_coordinate3,
                                favourable_coordinate4]
        
    else:
        print("somethinng went wrong in hunt and target",
              "the values of favourable coordinates 1, 2, 3, 4,",
              "respectively are:", favourable_coordinate1, " ",
              favourable_coordinate2, " ", favourable_coordinate3,
              " ", favourable_coordinate4)
    
    #to return array back to parent function
    return favourable_coordinates

#function to ensure the selected coordinate hunt down the
#entire ship, before hunt and target behaviour can be switched off.
def select_favourable_coordinates(kane_guess_list, 
                                  rest_of_ship_array,
                                  hunt_and_target_state,
                                  is_answer,
                                  is_first_time,
                                  point_of_origin,
                                  orientation):
    
    #choose orientation to tackle
    orientation = select_orientation(hunt_and_target_state, 
                                     orientation,
                                     is_answer, is_first_time)

    #variable to indicate first search
    search_success_state = False

    #we select coordinate suitable for the job
    selected_coordinate, search_success_state, orientation = match_favourable_coordinate(
        orientation, kane_guess_list, rest_of_ship_array)
    
    #if search has been successful we return coordinate for use
    if(search_success_state == True):
        return selected_coordinate, orientation
    
    #if search is not successful, this suggest that our search
    #has arrived at an dead end or the orientation is plain up
    #wrong
    elif(search_success_state == False):
        #return an array of coordinates where a part of
        #the remaining of the ship may reside in.
        rest_of_ship_array = hunt_and_target_behaviour(point_of_origin)
        is_answer = False

        #we swapped the orientation around as existing orientation
        #has no more valid options to choose from
        orientation = not orientation

        #retrieve point of origin and orientation to reconsider
        #what other options do we have left as our favourable
        #coordinate
        #we select coordinate suitable for the job
        selected_coordinate, search_success_state, orientation = match_favourable_coordinate(
            orientation, kane_guess_list, rest_of_ship_array)
    
        #search state should be successful this time round
        return selected_coordinate, orientation

#customized function selecting random without repeat
def kane_level_0_random(gameboard, kane_guess_list):
    # random a number for i = 0 to boardsize. and do not repeat
    # the numbers once called. (stack overflow assisted)
    targetted_coordinate = random.choice([i for i in range(0, (gameboard.size - 1))
                       if i not in kane_guess_list])
    return targetted_coordinate


#customized fuction selecting coordinates by
#parity without repeats
def kane_level_2_parity(gameboard, last_used_index, kane_guess_list, 
                        shortest_ship_length):
    
    #we return the value if this index can be used for guessing
    last_used_index = check_left_and_top(last_used_index, kane_guess_list,
                       shortest_ship_length)
    return last_used_index

        