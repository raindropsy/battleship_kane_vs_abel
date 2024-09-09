#Main file, where the top level function is called.
#import modules
from enum import Enum
from Game_board import clear_the_board
from Game_turn_manager import play_game
from Game_set_board import set_ship
from Helper_printout import display_con_output
from Helper_printout import export_dataframe

#variables
simulation_count = 1


#Enum class
class Agent (Enum) :
    KANE = "kane"
    ABEL = "abel"

#variables
turn_number = 0 #Count the number of turn before 1 sides win the game
current_agent = Agent.KANE #First agent to take a turn

def start_simulation(current_agent,turn_number, simulation_count):
    # for x in range(simulation_count):
    while(simulation_count > 0):
        set_ship()
        play_game(current_agent,turn_number)
        simulation_count = simulation_count - 1
        clear_the_board()
        if(simulation_count % 1000 == 0):
            display_con_output(simulation_count)
    export_dataframe()



#Call function
start_simulation(current_agent, turn_number, simulation_count)

