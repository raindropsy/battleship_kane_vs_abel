# This is where all the helper functions are stored.
# Self-made functions that are not supported by libs,
# that attempt to solve a problem via a sequence of operation.

# import modules
import time
import random

# function to split 2 value integer to seperate single digits.
def split_int(coordinate):
    coordinate_strings = str(coordinate)
    # edge cases where parsed coordinate is already in single digit
    if coordinate < 10:
        x_coordinate = 0
        y_coordinate = int(coordinate_strings[0])
        return x_coordinate, y_coordinate
    # else where majority of the cases, 2 digit is parsed in instead.
    else:
        x_coordinate = int(coordinate_strings[0])
        y_coordinate = int(coordinate_strings[1])
        return x_coordinate, y_coordinate


# function to join single digit integer to 2 value integers.
def join_int(x_coordinate, y_coordinate):
    x_coordinate_strings = str(x_coordinate)
    y_coordinate_strings = str(y_coordinate)
    joined_string = x_coordinate_strings + y_coordinate_strings
    return int(joined_string)

# function to check if selected coordinates will potentially clash
# with existing ships.
def check_coordinates(coordinate, ship_location, ship_length,
                      orientation):
    # taken_coordinates stores projection of the required
    # coordinates acounting for ship length.
    horizontal_coordinates = [coordinate + i for i in range(ship_length)]
    vertical_coordinates = [coordinate + (i*10) for i in range(ship_length)]

    # return on custom function split int to single digits
    x_coordinate, y_coordinate = split_int(coordinate)

    # if horizontal is selected, proceed with horizontal check
    if (orientation == False):

        # for both False, relying on dummy coordinate values
        # return False if coordinate is out of range
        if (y_coordinate + ship_length) < 0 or (y_coordinate + ship_length) > 9:
            return False, 0, 0

        # compare projected coordinate and current coordinate,
        # return False if values are the same.
        if any(num in ship_location for num in horizontal_coordinates):
            return False, 0, 0

        # else return True to plot ship along length of ship.
        else:
            return True, x_coordinate, y_coordinate

    # if vertical is selected, proceed with vertical check
    if (orientation == True):

        # for both False, relying on dummy coordinate values
        # return False if coordinate is out of range
        if (x_coordinate + ship_length) < 0 or (x_coordinate + ship_length) > 9:
            return False, 0, 0

        # compare projected coordinate and current coordinate,
        # return False if values are the same.
        if any(num in ship_location for num in vertical_coordinates):
            return False, 0, 0

        # else return True to plot ship along length of ship.
        else:
            return True, x_coordinate, y_coordinate


# function storing and defining time
def check_time(time_now, deduct_time=False):
    current_time = time.time()
    if (deduct_time == False):
        return current_time

    elif (deduct_time == True):
        return round((current_time - time_now), 4)

    else:
        print("something went wrong")


# function to return favourable single integers depending on the
# condition
def check_favourable_coordinate(coordinate):

    # define favourable to be returned for hunt and target
    favourable_negative = coordinate - 1
    favourable_positive = coordinate + 1

    # if coordinate is at most bottom or right axis
    if (coordinate == 9):
        # return favourable + dummy values, indicate corner case True
        return favourable_negative, 0, True

    # if coordinate is at most top or left axis
    elif (coordinate == 0):
        # return favourable + dummy values, indicate corner case True
        return favourable_positive, 0, True

    else:
        # return favourables, indicate corner case False
        return favourable_negative, favourable_positive, False


# we match the favourable coordinate systematically, the first
# in the array have the priority
def match_favourable_coordinate(orientation, kane_guess_list,
                                rest_of_ship_array_length):

    # returns coordinate and orientation
    coordinate, orientation = array_from_orientation(orientation,
                                                     rest_of_ship_array_length)

    # if length is one, simply check and return, if coordinate
    # is already being used as an attempt, we return False
    if (type(coordinate) == int):

        # if the chosen coordinate has not been matched yet.
        if (coordinate not in kane_guess_list):
            rest_of_ship_array_length.remove(coordinate)
            return coordinate, True, orientation

        # if the coordinate has already been matched
        elif (coordinate in kane_guess_list):
            return 0, False, orientation  # unable to match

    # if length is more than 1, we select the first coordinate
    # and check if the coordinate is already attempted, else
    # we picked the second remaining coordinate.
    if (len(coordinate) == 2):

        # we first separate the coordinate array
        coordinate_1 = coordinate[0]
        coordinate_2 = coordinate[1]

        # if is first coordinate
        if (coordinate_1 not in kane_guess_list):
            return coordinate_1, True, orientation

        # else if 2nd coordinate
        elif (coordinate_2 not in kane_guess_list):
            return coordinate_2, True, orientation

    # in such a scenario where both returned coordinate is already
    # guessed, we return to point of origin. It may be an orientation
    # problem or we are guessing in the wrong direction
        elif (coordinate_1 in kane_guess_list and coordinate_2 in kane_guess_list):
            return 0, False, orientation


# we return the array based on the orientation chosen
def array_from_orientation(orientation, rest_of_ship_array_length):
    # we obtain the array based on orientation propagation
    array1, array2 = split_array_by_orientation(rest_of_ship_array_length)

    if (orientation == 0):
        return array1, orientation
    elif (orientation == 1):
        return array2, orientation


# return 2 sets of array, one focusing on horizontal propagation
# the other vertical propagation.
def split_array_by_orientation(rest_of_ship_array):

    if (len(rest_of_ship_array) == 2):
        array1 = rest_of_ship_array[0]
        array2 = rest_of_ship_array[1]

    elif (len(rest_of_ship_array) == 3):
        array1 = rest_of_ship_array[0]
        array2 = rest_of_ship_array[1:]

    elif (len(rest_of_ship_array) == 4):
        array1 = rest_of_ship_array[:2]
        array2 = rest_of_ship_array[2:]

    return array1, array2


# return True if point of origin is detected.
def check_point_of_origin(previous_turn_state,
                          current_turn_state, targetted_coordinates,
                          point_of_origin):

    # if this is the first turn where hunt and target has
    # been triggered
    if (previous_turn_state == False and current_turn_state == True):

        # targetted_coordinate is stored as point of origin
        return True, targetted_coordinates

    # else if this is subsequent turns
    elif (previous_turn_state == True and current_turn_state == True):

        # we return point of origin instead.
        return True, point_of_origin

    # else for all other cases (this should not happen but more
    # of a fail safe.)
    else:
        return False, 0


# custom function check if guess_list matches ship_coordinate
# if so return True. Assisted by chatGPT
# https://chatgpt.com/share/c9c9f701-c752-46ab-acbc-79c763a0e7b7
def check_ship_sunk(guess_list, ship_coordinates):
    if not guess_list:
        return False
    else:
        # Check if all ship coordinates are in the guess list
        result = all(elem in guess_list for elem in ship_coordinates)
        return result


# function checking all ships, if any ship has sunk
def check_all_ship(guess_list, patrol_boat, submarine, destroyer,
                   battleship, carrier):

    #check if any of the existing ship has been sunk
    boo_patrol = check_ship_sunk(guess_list, patrol_boat)
    boo_submarine = check_ship_sunk(guess_list, submarine)
    boo_destroyer = check_ship_sunk(guess_list, destroyer)
    boo_battleship = check_ship_sunk(guess_list, battleship)
    boo_carrier = check_ship_sunk(guess_list, carrier)

    #we return boo depending if any has been sunk
    if (boo_patrol == True):
        return True, "patrol_boat"
    
    elif (boo_submarine == True):
        return True, "submarine"
    
    elif (boo_destroyer == True):
        return True, "destroyer"
    
    elif (boo_battleship == True):
        return True, "battleship"
    
    elif (boo_carrier == True):
        return True, "carrier"
    
    else:
        return False, "none"

#custom function emptying list so that check_all_ship only 
#returns True the same turn that the ship has sunk.
def remove_sunk_ship(ship_name, patrol_boat, submarine, 
                     destroyer, battleship, carrier):
    
    #we put an impossible number if ship name is True
    #inelegant solution may fix if time allows.
    if(ship_name == "patrol_boat"):
        patrol_boat = [101]

    elif(ship_name == "submarine"):
        submarine = [101]

    elif(ship_name == "destroyer"):
        destroyer = [101]

    elif(ship_name == "battleship"):
        battleship = [101]

    elif(ship_name == "carrier"):
        carrier = [101]

    elif(ship_name == "none"):
        #this here is inelegant, will fix if time permits
        ship_name = ship_name 

    return patrol_boat, submarine, destroyer, battleship, carrier


# function returning True or False if hunt and target is completed
# this is dependant if ship has sunk.
def to_disable_hunt_and_target(has_ship_sunk,
                               continue_hunt_and_target,
                               hunt_and_target_state):

    # if ship have not sunk, we return the variable
    if (has_ship_sunk == False):
        return continue_hunt_and_target, hunt_and_target_state

    # else if ship has sunk, we switch both to False
    elif (has_ship_sunk == True):
        return False, False


# function to select orientation
def select_orientation(hunt_and_target_state, orientation,
                       is_answer, is_first_time):

    # if we are in hunt and target, and answer is correct
    # we proceed with the old orientation
    if (hunt_and_target_state == True and is_answer == True):
        return orientation

    # if we are in hunt and target and answer is wrong, we change
    # orientation
    elif (hunt_and_target_state == True and is_answer == False):
        return not orientation

    # we random an orientation to start guessing
    elif (hunt_and_target_state == True and is_first_time == True):
        orientation = random.randint(0, 1)
        return orientation


#we disable hunt and target if we encounter an edge case
#this is identified if we have more than one of the same
#value in kane_guess_list
def kane_self_check(kane_guess_list, hunt_and_target):
    boolean_check = check_list_duplicate(kane_guess_list)
    if(boolean_check == True):
        hunt_and_target = False
    return hunt_and_target


#customized function to check list for duplicates
#debugged with chatGPT 
# #https://chatgpt.com/share/c9c9f701-c752-46ab-acbc-79c763a0e7b7
def check_list_duplicate(kane_guess_list):

    # Use a set comprehension to find duplicates
    duplicate = {i for i in kane_guess_list if kane_guess_list.count(i) > 1}
    if(duplicate):
        return True
    else:
        return False


#customized function to check for shortest ship length
def check_shortest_ship_length(patrol_boat, 
                               submarine, destroyer, 
                               battleship, carrier):

    list_of_length = [] #an array housing ship_length

    #individually check for array 
    list_of_length.append(check_ship_length(patrol_boat))
    list_of_length.append(check_ship_length(submarine))
    list_of_length.append(check_ship_length(destroyer))
    list_of_length.append(check_ship_length(battleship))
    list_of_length.append(check_ship_length(carrier))

    #find the lowest value
    min_value = min(list_of_length)

    #return value
    return min_value


#customized function to check for current ship length
def check_ship_length(ship_list):

    #this is to account for any ship list coordinate
    #being filled with the value 101 in the function
    #remove_sunk_ship as an in-elegant solution.
    if(len(ship_list) < 2):
        return 10 #dummy number
    
    #else, we return the corresponding size of the
    #list length.
    else:
        return len(ship_list)


#customized function checkng if there is a need to call 
#remove_sunk_ship function.
def check_has_ship_sunk(sunk_state, ship_name, patrol_boat, 
                        submarine, destroyer, battleship, 
                        carrier, shortest_ship_length):
    
    if(sunk_state == True):
        patrol_boat, submarine, destroyer, battleship, carrier = remove_sunk_ship(
            ship_name, patrol_boat, submarine, destroyer, battleship, carrier)

        shortest_ship_length = 0            
        #function to update shortest length of ship
        shortest_ship_length = check_shortest_ship_length(patrol_boat, 
                                                        submarine, destroyer, 
                                                        battleship, carrier)
        print("lowest ship length is now:", shortest_ship_length)

    return patrol_boat, submarine, destroyer, battleship, carrier, shortest_ship_length

#customized function to check top and left of board
#to check if it has alrdy been taken by existing 
#indexes for level 2 & 3 kane behaviour (PP-agent)
#similar to check_coordinates function but only top 
#and left is checked, rather than horizontal or vertical
#direction.
def check_left_and_top(last_used_index, kane_guess_list,
                       shortest_ship_length):
    print("given coordinate is", last_used_index)
    #we split the indexes so as to easier manipulate
    #the indexes.
    x_coordinate, y_coordinate = split_int(last_used_index)

    #we check individual coordinates against array corners.
    x_boolean = deduct_left_top(x_coordinate, shortest_ship_length)
    y_boolean = deduct_left_top(y_coordinate, shortest_ship_length)

    #if both x and y coordinate is ok
    if((x_boolean is True or y_boolean is True) or (x_boolean is True and y_boolean is True)):
        return last_used_index
    
    #else we add one and try again
    elif(x_boolean is False and y_boolean is False):
        new_index = last_used_index + 1
        return check_left_and_top(new_index, kane_guess_list,
                           shortest_ship_length)


#customized function strictly for check_left_and_top
#this function return False if 0 (most left/most top)
#of the indexes, but deducts (move left or top) if 
#it is possible to do so.
#also consider ship length for its deduction
def deduct_left_top(coordinates, shortest_ship_length):
    #create array to return
    coordinates_array = []
    deduct_answer = False

    #for range of 1 - length of deduction
    for i in range(1, shortest_ship_length):

        #we derive the interested coordinates
        coordinates = coordinates - i

        #if value is 0 and above
        if(coordinates > -1):

            #we collate it in an array for return
            coordinates_array.append(coordinates)

    #if coordinates_array is still empty after
    #the above operation
    if(not coordinates_array or len(coordinates_array) < shortest_ship_length - 2):

        #This shows that cannot be deducted, index 
        #shldnt be used
        deduct_answer = False
    elif(len(coordinates_array) == shortest_ship_length - 1):

        #Can be deducted, we return True
        deduct_answer = True

    #we return array
    return deduct_answer
