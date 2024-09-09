# Govern the steps taken(logic of agents), for both agents.

# import modules
import random
from Agent_behaviour_kane import hunt_and_target_behaviour
from Agent_behaviour_kane import kane_level_0_random #used during simulation
from Agent_behaviour_kane import kane_level_2_parity
from Agent_behaviour_kane import select_favourable_coordinates
from Helper_answer_check import check_answer
from Game_board import gameboard

# function governing kane's turn
def kane_turn(kane_correct_answer, kane_guess_list, hunt_and_target_state,
              hunt_coordinates, point_of_origin, continue_hunt_and_target,
              is_answer, orientation, last_used_index, shortest_ship_length):
    
    # variables
    rest_of_ship_array = []
    targetted_coordinate = 0
    kane_end_game = False
    is_first_time = False

    if(hunt_and_target_state == False):

        # Level 0 kane PP-algorithm
        targetted_coordinate = kane_level_0_random(gameboard,
                                                    kane_guess_list)
        
        # #Level 2 kane PP-algorithm
        # last_used_index = kane_level_2_parity(gameboard, last_used_index, 
        #                                     kane_guess_list, shortest_ship_length)
        # targetted_coordinate = last_used_index
        # last_used_index = last_used_index + 1
        
    # condition checking for hunt and target level 1 PP-algorithm
    if (hunt_and_target_state == True and continue_hunt_and_target == False):

        # variable
        is_first_time = True

        # return an array of coordinates where a part of
        # the remaining of the ship may reside in.
        rest_of_ship_array = hunt_and_target_behaviour(hunt_coordinates)

        # search in array and return a selected coordinate to return
        targetted_coordinate, orientation = select_favourable_coordinates(kane_guess_list, 
                                                                           rest_of_ship_array,
                                                                           hunt_and_target_state,
                                                                           is_answer,
                                                                           is_first_time,
                                                                           point_of_origin,
                                                                           orientation)

    # for second turns onwards where hunt and target is active
    # hunting down the rest of the ship level 1 PP-algorithm
    elif (hunt_and_target_state == True and continue_hunt_and_target == True
          and is_answer == True):

        # variable
        is_first_time = False

        # return an array of coordinates where a part of
        # the remaining of the ship may reside in.
        rest_of_ship_array = hunt_and_target_behaviour(hunt_coordinates)

        # search in array and return a selected coordinate to return
        targetted_coordinate, orientation = select_favourable_coordinates(kane_guess_list, 
                                                                           rest_of_ship_array,
                                                                           hunt_and_target_state,
                                                                           is_answer,
                                                                           is_first_time,
                                                                           point_of_origin, 
                                                                           orientation)

    # if the first guess is wrong, we remember previous orientation
    # and point of origin level 1 PP-algorithm
    elif (hunt_and_target_state == True and continue_hunt_and_target == True
          and is_answer == False):
        # variable is first time
        is_first_time = False

        # return an array of coordinates where a part of
        # the remaining of the ship may reside in.
        rest_of_ship_array = hunt_and_target_behaviour(point_of_origin)

        # search in array and return a selected coordinate to return
        targetted_coordinate, orientation = select_favourable_coordinates(kane_guess_list, 
                                                                           rest_of_ship_array,
                                                                           hunt_and_target_state,
                                                                           is_answer,
                                                                           is_first_time,
                                                                           point_of_origin, 
                                                                           orientation)

    # we then finally check answer, which will allow kane 
    # to decide its response next turn. This also updates
    # game state accordingly
    
    kane_end_game, hunt_and_target_state, is_answer, targetted_coordinates = check_answer(targetted_coordinate, 
                                                                                           kane_correct_answer,
                                                hunt_and_target_state, kane_guess_list,
                                                point_of_origin)
    print("kane guess list:", kane_guess_list)
    print("kane answer list", kane_correct_answer)

    return kane_end_game, hunt_and_target_state, is_answer, targetted_coordinates, orientation, last_used_index


# function governing abel's turn
def abel_turn(abel_right_answer):

    targetted_coordinate = random.randint(0, (gameboard.size - 1))

    if (targetted_coordinate not in abel_right_answer):
        return False

    elif (targetted_coordinate in abel_right_answer and
          len(abel_right_answer) > 1):

        # remove related coordinate from abel_right_answer
        abel_right_answer.remove(targetted_coordinate)

        # keep count the number of hits scored by agent
        return False

    elif (targetted_coordinate in abel_right_answer
          and len(abel_right_answer) == 1):
        # remove related coordinate from kane_correct_answer +
        # return True
        abel_right_answer.remove(targetted_coordinate)
    return True
