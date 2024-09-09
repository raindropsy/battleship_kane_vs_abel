#manages console out, and also act as the main page for functions
#relating to export.

#import modules
from Helper_dataframe_manager import simulation_record_kane
from Helper_functions import check_time
import pandas as pd

# from IPython.display import display

#print out console and manipulates dataframes.
def display_con_output(simulation_count):
    print("current iteration is left:", simulation_count)
    print ("game has ended")

    
#appened to specific field of array in preparation to convert to 
#dataframe
def append_game_statistics(statistics, field):
    simulation_record_kane[field].append(statistics)

#function appending values to fields
def record_game_statistics(turn_number, time_now, hit_counter, 
                           answer_list, end_game):
    #turn number is used as number of tries required to down all
    #5 ships. As the game rule would not be changing a magic
    #number is used.
    hits_per_ship = (turn_number / 5)

    #function here call upon append_game_statistics from the above
    append_game_statistics(turn_number ,"turn_required_per_game")
    append_game_statistics(check_time(time_now, True), 
                                   "game_time_duration")
    append_game_statistics(hit_counter, 
                                   "number_of_hits_per_game")
    append_game_statistics((len(answer_list) - 
                                    hit_counter), 
                                    "number_of_misses_per_game")
    append_game_statistics(hits_per_ship, 
                           "average_shots_taken_per_ship")
    if(end_game == True):
        append_game_statistics(1, "number_of_wins")
    else:
        append_game_statistics(0, "number_of_wins")
    
def export_dataframe():
    df = pd.DataFrame(simulation_record_kane)
    df.to_csv("simulation_result.csv", index = True)