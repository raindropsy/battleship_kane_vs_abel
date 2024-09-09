#Govern more towards the flow of the game, dealing more towards 
#game conditions.

#import modules
from Game_agents_turn import kane_turn, abel_turn
from Game_set_board import ship_location
from Helper_functions import check_all_ship
from Helper_functions import check_has_ship_sunk
from Helper_functions import check_time
from Helper_functions import check_point_of_origin
from Helper_functions import kane_self_check
from Helper_printout import record_game_statistics
from Helper_functions import to_disable_hunt_and_target
from enum import Enum

#Enum class
class Agent (Enum) :
    KANE = "kane"
    ABEL = "abel"

#play_game function, uses a while loop, to loop infinitely until 
#conditon is met uses a break function to end the loop early if
#either player dies at 0 health or exceeds game turn limit.
def play_game(current_agent, turn_number):
    
    #variables
    current_agent = Agent.KANE #First agent to take a turn
    kane_end_game = False #only change to signal end game
    abel_end_game = False #only change to signal end game

    #previous hunt and target to determine if point of origin needs
    #to be saved.
    previous_hunt_and_target_state = False

    #trigger hunt and target behaviour in kane
    hunt_and_target_state = False 

    #to signify that this is the second turn using hunt and
    #target consecutively, hence we will use point of origin
    #as our targetted coordinate.
    continue_hunt_and_target = False

    #used to store coordinates used for hunt and target
    targetted_coordinates = 0 

    #keep a lookup table to avoid looping through entire board
    #this should hopefully reduce operations needed per game
    kane_correct_answer = ship_location[:]
    abel_correct_answer = ship_location[:]

    #keep guessed coordinate in a lookup table, used to
    #prevent re-guessing the same coordinate.
    kane_guess_list = []
    abel_guess_list = []#used only for ML agent

    #how many right guesses per game? This is placed here because
    #the rule of the game will not be changing.
    kane_hit_counter = 17

    #variable storing last used orientation
    orientation = False

    #only used by level 2 parity (kane)

    #tracks largest index required by level 2 parity
    last_used_index = 0

    #tracks shortest ship length
    shortest_ship_length = 2

    #arrays containing coordinates about individual ships
    patrol_coordinate = []
    submarine_coordinate = []
    destroyer_coordinate = []
    battleship_coordinate = []
    carrier_coordinate = []

    #point of origin saves the point where kane manages to first
    #correctly guess the beggining of the ship
    point_of_origin = 0

    #turn limit to prevent infinite looping.
    turn_allowed = 100

    #variable time to keep track of time taken to complete
    #a single game loop.
    time_now = 0

    #variable to keep track if this is answer
    is_answer = False

    #obtain time as loop starts.
    time_now = check_time(time_now)

    #assign coordinates to ship_coordinate
    patrol_coordinate = kane_correct_answer[0:2]
    submarine_coordinate = kane_correct_answer[2:5]
    destroyer_coordinate = kane_correct_answer[5:8]
    battleship_coordinate = kane_correct_answer[8:12]
    carrier_coordinate = kane_correct_answer[12:17]

    while True:
        #For kane (The PP-agent)
        if (current_agent == Agent.KANE and kane_end_game
            == False and abel_end_game == False and turn_number 
            < turn_allowed):

            #function triggering kane's set of action.
            kane_end_game, hunt_and_target_state, is_answer, targetted_coordinates, orientation, last_used_index = kane_turn(
                kane_correct_answer, kane_guess_list, 
                hunt_and_target_state, targetted_coordinates,
                point_of_origin, continue_hunt_and_target, 
                is_answer, orientation, last_used_index,
                shortest_ship_length)
            
            #helper function to determine if there is a need
            #to store current coordinate as point of origin
            continue_hunt_and_target, point_of_origin = check_point_of_origin(previous_hunt_and_target_state,
                                    hunt_and_target_state, 
                                    targetted_coordinates,
                                    point_of_origin)
            
            #check if ship sunk
            has_ship_sunk, ship_name = check_all_ship(kane_guess_list, 
                                           patrol_coordinate,
                                           submarine_coordinate,
                                           destroyer_coordinate,
                                           battleship_coordinate,
                                           carrier_coordinate)

            #function to change hunt and target to False if 
            #condition is met. Where a ship has sunk
            continue_hunt_and_target, hunt_and_target_state = to_disable_hunt_and_target(has_ship_sunk,
                                                                                         continue_hunt_and_target,
                                                                                         hunt_and_target_state)
            
            #function to update ship_list when ship has sunk
            patrol_coordinate, submarine_coordinate, destroyer_coordinate, battleship_coordinate, carrier_coordinate, shortest_ship_length  = check_has_ship_sunk(
            has_ship_sunk, ship_name, patrol_coordinate, 
            submarine_coordinate, destroyer_coordinate,
            battleship_coordinate, carrier_coordinate,
            shortest_ship_length)
            

            #update hunt and target state
            previous_hunt_and_target_state = hunt_and_target_state

            #we do a self check to see if there is repeated 
            #numbers in kane_guess_list (inelegant hot fix)
            hunt_and_target_state =  kane_self_check(kane_guess_list,
                                                     hunt_and_target_state)

            #change player to abel
            current_agent = Agent.ABEL
        
        #For abel (The ML-agent)
        elif (current_agent == Agent.ABEL and abel_end_game == 
              False and kane_end_game == False and turn_number < 
            turn_allowed):
            abel_end_game = abel_turn(abel_correct_answer)
            turn_number += 1
            current_agent = Agent.KANE
        
        #if game already won by one of the agents.
        elif (kane_end_game == True or abel_end_game == True
            and turn_number < turn_allowed):
            kane_hit_counter = kane_hit_counter - len(kane_correct_answer)
            
            #record kane's agent performance.
            record_game_statistics(turn_number, time_now, 
                                   kane_hit_counter, kane_guess_list,
                                   kane_end_game)
            break
        
        #if something were to went wrong (which shouldnt happen in this controlled
        #environment.)
        else:
            print("something went wrong, turn number\
                  is currently:", turn_number, "or, end game logic\
                    maybe off.")
            break
