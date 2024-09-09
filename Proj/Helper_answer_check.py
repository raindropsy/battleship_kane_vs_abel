# focuses on checking answers

def check_answer(targetted_coordinate,  kane_correct_answer,
                 hunt_and_target_state, kane_guess_list,
                 point_of_origin):
    # if selected coordinate is incorrect, remember it,
    # via kane_guess_list, and do not add to hit count.
    if (targetted_coordinate not in kane_correct_answer and
            hunt_and_target_state == False):
        kane_guess_list.append(targetted_coordinate)
        return False, False, False, 0

    # if selected coordinate is incorrect, remember it,
    # via kane_guess_list, do not add hit count 
    elif (targetted_coordinate not in kane_correct_answer and
          hunt_and_target_state == True):
        kane_guess_list.append(targetted_coordinate)
        return False, True, False, 0

    # if selected coordinate is correct, remember it,
    # reduce from kane_correct_answer list and add hit count.
    elif (targetted_coordinate in kane_correct_answer and
          len(kane_correct_answer) > 1 and hunt_and_target_state == False):
        kane_correct_answer.remove(targetted_coordinate)
        kane_guess_list.append(targetted_coordinate)
        return False, True, True, targetted_coordinate

    # if selected coordinate is correct, remember it,
    # reduce from kane_correct_answer list and add hit count.
    elif (targetted_coordinate in kane_correct_answer and
          len(kane_correct_answer) > 1 and hunt_and_target_state == True):
        kane_correct_answer.remove(targetted_coordinate)
        kane_guess_list.append(targetted_coordinate)
        return False, True, True, targetted_coordinate

    # if selected coordinate is correct, and kane wins this turn,
    # reduce from kane_correct_answer list and declare winner.
    elif (targetted_coordinate in kane_correct_answer
          and len(kane_correct_answer) == 1):
        kane_correct_answer.remove(targetted_coordinate)
        return True, False, True, 0



# we check if coordinate has already been previously attempted
# if not we have to search again.
def check_if_guess_attempted(kane_guess_list, coordinates):
    if (coordinates in kane_guess_list):
        return coordinates
