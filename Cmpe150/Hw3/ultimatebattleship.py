
# Ultimate Battleships

def print_ships_to_be_placed():
    print("Ships to be placed:", end=" ")
    if FILE_OUTPUT_FLAG:
        f.write("Ships to be placed: ")


# elem expected to be a single list element of a primitive type.
def print_single_element(elem):
    print(str(elem), end=" ")
    if FILE_OUTPUT_FLAG:
        f.write(str(elem) + " ")


def print_empty_line():
    print()
    if FILE_OUTPUT_FLAG:
        f.write("\n")


# n expected to be str or int.
def print_player_turn_to_place(n):
    print("It is Player {}'s turn to place their ships.".format(n))
    if FILE_OUTPUT_FLAG:
        f.write("It is Player {}'s turn to place their ships.\n".format(n))


def print_to_place_ships():
    print("Enter a name, coordinates and orientation to place a ship (Example: Carrier 1 5 h) :", end=" ")
    if FILE_OUTPUT_FLAG:
        f.write("Enter a name, coordinates and orientation to place a ship (Example: Carrier 1 5 h) : \n")
        # There is a \n because we want the board to start printing on the next line.


def print_incorrect_input_format():
    print("Input is in incorrect format, please try again.")
    if FILE_OUTPUT_FLAG:
        f.write("Input is in incorrect format, please try again.\n")


def print_incorrect_coordinates():
    print("Incorrect coordinates given, please try again.")
    if FILE_OUTPUT_FLAG:
        f.write("Incorrect coordinates given, please try again.\n")


def print_incorrect_ship_name():
    print("Incorrect ship name given, please try again.")
    if FILE_OUTPUT_FLAG:
        f.write("Incorrect ship name given, please try again.\n")


def print_incorrect_orientation():
    print("Incorrect orientation given, please try again.")
    if FILE_OUTPUT_FLAG:
        f.write("Incorrect orientation given, please try again.\n")


# ship expected to be str.
def print_ship_is_already_placed(ship):
    print(ship, "is already placed, please try again.")
    if FILE_OUTPUT_FLAG:
        f.write(ship + " is already placed, please try again.\n")


# ship expected to be str.
def print_ship_cannot_be_placed_outside(ship):
    print(ship, "cannot be placed outside the board, please try again.")
    if FILE_OUTPUT_FLAG:
        f.write(ship + " cannot be placed outside the board, please try again.\n")


# ship expected to be str.
def print_ship_cannot_be_placed_occupied(ship):
    print(ship, "cannot be placed to an already occupied space, please try again.")
    if FILE_OUTPUT_FLAG:
        f.write(ship + " cannot be placed to an already occupied space, please try again.\n")


def print_confirm_placement():
    print("Confirm placement Y/N :", end=" ")
    if FILE_OUTPUT_FLAG:
        f.write("Confirm placement Y/N : \n")


# n expected to be str or int.
def print_player_turn_to_strike(n):
    print("It is Player {}'s turn to strike.".format(n))
    if FILE_OUTPUT_FLAG:
        f.write("It is Player {}'s turn to strike.\n".format(n))


def print_choose_target_coordinates():
    print("Choose target coordinates :", end=" ")
    if FILE_OUTPUT_FLAG:
        f.write("Choose target coordinates : ")


def print_miss():
    print("Miss.")
    if FILE_OUTPUT_FLAG:
        f.write("Miss.\n")


# n expected to be str or int.
def print_type_done_to_yield(n):
    print("Type done to yield your turn to player {} :".format(n), end=" ")
    if FILE_OUTPUT_FLAG:
        f.write("Type done to yield your turn to player {} : \n".format(n))


def print_tile_already_struck():
    print("That tile has already been struck. Choose another target.")
    if FILE_OUTPUT_FLAG:
        f.write("That tile has already been struck. Choose another target.\n")


def print_hit():
    print("Hit!")
    if FILE_OUTPUT_FLAG:
        f.write("Hit!\n")


# n expected to be str or int.
def print_player_won(n):
    print("Player {} has won!".format(n))
    if FILE_OUTPUT_FLAG:
        f.write("Player {} has won!\n".format(n))


def print_thanks_for_playing():
    print("Thanks for playing.")
    if FILE_OUTPUT_FLAG:
        f.write("Thanks for playing.\n")


# my_list expected to be a 3-dimensional list, formed from two 2-dimensional lists containing the boards of each player.
def print_3d_list(my_list):
    first_d = len(my_list[0])
    for row_ind in range(first_d):
        second_d = len(my_list[0][row_ind])
        print("{:<2}".format(row_ind+1), end=' ')
        for col_ind in range(second_d):
            print(my_list[0][row_ind][col_ind], end=' ')
        print("\t\t\t", end='')
        print("{:<2}".format(row_ind+1), end=' ')
        for col_ind in range(second_d):
            print(my_list[1][row_ind][col_ind], end=' ')
        print()
    print("", end='   ')
    for row_ind in range(first_d):
        print(row_ind + 1, end=' ')
    print("\t\t", end='   ')
    for row_ind in range(first_d):
        print(row_ind + 1, end=' ')
    print("\nPlayer 1\t\t\t\t\t\tPlayer 2")
    print()

    if FILE_OUTPUT_FLAG:
        first_d = len(my_list[0])
        for row_ind in range(first_d):
            second_d = len(my_list[0][row_ind])
            f.write("{:<2} ".format(row_ind + 1))
            for col_ind in range(second_d):
                f.write(my_list[0][row_ind][col_ind] + " ")
            f.write("\t\t\t")
            f.write("{:<2} ".format(row_ind + 1))
            for col_ind in range(second_d):
                f.write(my_list[1][row_ind][col_ind] + " ")
            f.write("\n")
        f.write("   ")
        for row_ind in range(first_d):
            f.write(str(row_ind + 1) + " ")
        f.write("\t\t   ")
        for row_ind in range(first_d):
            f.write(str(row_ind + 1) + " ")
        f.write("\nPlayer 1\t\t\t\t\t\tPlayer 2\n")
        f.write("\n")


def print_rules():
    print("Welcome to Ultimate Battleships")
    print("This is a game for 2 people, to be played on two 10x10 boards.")
    print("There are 5 ships in the game:  Carrier (occupies 5 spaces), Battleship (4), Cruiser (3), Submarine (3), and Destroyer (2).")
    print("First, the ships are placed. Ships can be placed on any unoccupied space on the board. The entire ship must be on board.")
    print("Write the ship's name, followed by an x y coordinate, and the orientation (v for vertical or h for horizontal) to place the ship.")
    print("If a player is placing a ship with horizontal orientation, they need to give the leftmost coordinate.")
    print("If a player is placing a ship with vertical orientation, they need to give the uppermost coordinate.")
    print("Player 1 places first, then Player 2 places. Afterwards, players take turns (starting from Player 1) to strike and sink enemy ships by guessing their location on the board.")
    print("Guesses are again x y coordinates. Do not look at the board when it is the other player's turn.")
    print("The last player to have an unsunk ship wins.")
    print("Have fun!")
    print()

    if FILE_OUTPUT_FLAG:
        f.write("Welcome to Ultimate Battleships\n")
        f.write("This is a game for 2 people, to be played on two 10x10 boards.\n")
        f.write(
            "There are 5 ships in the game:  Carrier (occupies 5 spaces), Battleship (4), Cruiser (3), Submarine (3), and Destroyer (2).\n")
        f.write(
            "First, the ships are placed. Ships can be placed on any unoccupied space on the board. The entire ship must be on board.\n")
        f.write(
            "Write the ship's name, followed by an x y coordinate, and the orientation (v for vertical or h for horizontal) to place the ship.\n")
        f.write("If a player is placing a ship with horizontal orientation, they need to give the leftmost coordinate.\n")
        f.write("If a player is placing a ship with vertical orientation, they need to give the uppermost coordinate.\n")
        f.write(
            "Player 1 places first, then Player 2 places. Afterwards, players take turns (starting from Player 1) to strike and sink enemy ships by guessing their location on the board.\n")
        f.write("Guesses are again x y coordinates. Do not look at the board when it is the other player's turn.\n")
        f.write("The last player to have an unsunk ship wins.\n")
        f.write("Have fun!\n")
        f.write("\n")


# Create the game
board_size = 10
f = open('UltimateBattleships.txt', 'w')
FILE_OUTPUT_FLAG = True  # You can change this to True to also output to a file so that you can check your outputs with diff.

print_rules()

# Remember to use list comprehensions at all possible times.
# If we see you populate a list that could be done with list comprehensions using for loops, append/extend/insert etc. you will lose points.

# Make sure to put comments in your code explaining your approach and the execution.

# We defined all the functions above for your use so that you can focus only on your code and not the formatting.
# You need to call them in your code to use them of course.

# If you have questions related to this homework, direct them to utku.bozdogan@boun.edu.tr please.

# Do not wait until the last day or two to start doing this homework, it requires serious effort.

try:  # The entire code is in this try block, if there ever is an error during execution, we can safely close the file.
    # DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE

    turn = 1  # or 2

    while turn == 1:
        # Creating the board of two players.
        player1_board = [["-" for col in range(board_size)] for row in range(board_size)]
        player2_board = [["-" for col in range(board_size)] for row in range(board_size)]
        myList = [player1_board, player2_board]

        player1OccupiedPlaces = []
        # Ships
        ship_list = ["Carrier", "Battleship", "Cruiser", "Submarine", "Destroyer"]
        shipLengths = [5,4,3,3,2]
        shipAndLength = dict()
        for i in range(len(ship_list)):
            shipAndLength[ship_list[i].lower()] = shipLengths[i]

        # Printing the board
        print_3d_list(myList)
        print_ships_to_be_placed()
        for ship in ship_list:
            print_single_element(ship)
        print_empty_line()
        # Game starts for Player 1
        print_player_turn_to_place(turn)
        print_to_place_ships()

        while len(ship_list) != 0:

            # Correct Format Check
            isCorrectInputFormat = False
            # First Input Check
            isCorrectShipInput = False
            # Second and Third Input Check
            isCorrectCoordinates = False
            # Last Input Check
            isCorrectAlignment = False
            # Ship Inside Check
            isShipPlacedInside = False
            # Ship Availability Check
            isShipAvailable = False
            # Coordinate Availability Check
            isCoordinateAvailable = False

            # Input Error Handling
            while isCorrectInputFormat == False or isCorrectShipInput == False or isCorrectCoordinates == False or isCorrectAlignment == False or isShipPlacedInside == False or isShipAvailable == False or isCoordinateAvailable == False:

                # Correct Format Check
                isCorrectInputFormat = False
                # First Input Check
                isCorrectShipInput = False
                # Second and Third Input Check
                isCorrectCoordinates = False
                # Last Input Check
                isCorrectAlignment = False
                # Ship Inside Check
                isShipPlacedInside = False
                # Ship Availability Check
                isShipAvailable = False
                # Coordinate Availability Check
                isCoordinateAvailable = False
                allowedCoordinateInputs = ["1","2","3","4","5","6","7","8","9","10"]

                # Input from the user
                place_input_from_user = input().lower().strip().split() #is a list

                if len(place_input_from_user) < 4 or "." in place_input_from_user[1] or "." in place_input_from_user[2]:
                    print_incorrect_input_format() # Error message

                    # Printing the board
                    print_3d_list(myList)
                    print_ships_to_be_placed()
                    for ship in ship_list:
                        print_single_element(ship)
                    print_empty_line()
                    print_player_turn_to_place(turn)
                    print_to_place_ships()
                    continue;
                else:
                    place_input_from_user = [place_input_from_user[i] for i in range(4)] # Take the first 4 inputs
                    isCorrectInputFormat = True

                # Second and Third Input Check
                if place_input_from_user[1].isdigit() and place_input_from_user[2].isdigit():
                    place_input_from_user[1] = int(place_input_from_user[1])
                    place_input_from_user[2] = int(place_input_from_user[2])
                    if 0 < place_input_from_user[1] < 11 and 0 < place_input_from_user[2] < 11:
                        isCorrectCoordinates = True
                    else:
                        print_incorrect_coordinates() # Error message

                        # Printing the board
                        print_3d_list(myList)
                        print_ships_to_be_placed()
                        for ship in ship_list:
                            print_single_element(ship)
                        print_empty_line()
                        print_player_turn_to_place(turn)
                        print_to_place_ships()
                        continue;
                else:
                    print_incorrect_input_format() # Error message

                    # Printing the board
                    print_3d_list(myList)
                    print_ships_to_be_placed()
                    for ship in ship_list:
                        print_single_element(ship)
                    print_empty_line()
                    print_player_turn_to_place(turn)
                    print_to_place_ships()
                    continue;

                # First Input Check
                if place_input_from_user[0].lower() == "carrier" or place_input_from_user[0].lower() == "battleship" or place_input_from_user[0].lower() == "cruiser" or place_input_from_user[0].lower() == "submarine" or place_input_from_user[0].lower() == "destroyer":
                    isCorrectShipInput = True
                else:
                    print_incorrect_ship_name() # Error message

                    # Printing the board
                    print_3d_list(myList)
                    print_ships_to_be_placed()
                    for ship in ship_list:
                        print_single_element(ship)
                    print_empty_line()
                    print_player_turn_to_place(turn)
                    print_to_place_ships()
                    continue;

                # Last Input Check
                allowedAlignmentInputs = ["h","v","H","V"]
                isCorrectAlignment = False
                if place_input_from_user[3] in allowedAlignmentInputs:
                    isCorrectAlignment = True
                    if place_input_from_user[3] == "h" or place_input_from_user[3] == "H":
                        place_input_from_user[3] = "h"
                    if place_input_from_user[3] == "v" or place_input_from_user[3] == "V":
                        place_input_from_user[3] = "v"
                else:
                    print_incorrect_orientation()  # Error message

                    # Printing the board
                    print_3d_list(myList)
                    print_ships_to_be_placed()
                    for ship in ship_list:
                        print_single_element(ship)
                    print_empty_line()
                    print_player_turn_to_place(turn)
                    print_to_place_ships()
                    continue;
                # Input Error Handling Over

                # Ship Placement Errors Handling
                # From now on, first input is lower string, second & third inputs are integer and last input is lower string.
                # It is time to place our ships with our correct inputs

                # Creating the placement of player 1.

                # Ship is Available Check
                if place_input_from_user[0].capitalize() in ship_list:
                    isShipAvailable = True
                else:
                    print_ship_is_already_placed(place_input_from_user[0].capitalize()) # Error message
                    # Printing the board
                    print_3d_list(myList)
                    print_ships_to_be_placed()
                    for ship in ship_list:
                        print_single_element(ship)
                    print_empty_line()
                    print_player_turn_to_place(turn)
                    print_to_place_ships()
                    continue;

                # Ship Placement Inside Check
                if place_input_from_user[3] == "h":
                    if place_input_from_user[1] + shipAndLength[place_input_from_user[0]] <= 11:
                        isShipPlacedInside = True
                    else:
                        print_ship_cannot_be_placed_outside(place_input_from_user[0].capitalize()) # Error message
                        # Printing the board
                        print_3d_list(myList)
                        print_ships_to_be_placed()
                        for ship in ship_list:
                            print_single_element(ship)
                        print_empty_line()
                        print_player_turn_to_place(turn)
                        print_to_place_ships()
                        continue;
                elif place_input_from_user[3] == "v":
                    if place_input_from_user[2] + shipAndLength[place_input_from_user[0]] <= 11:
                        isShipPlacedInside = True
                    else:
                        print_ship_cannot_be_placed_outside(place_input_from_user[0].capitalize()) # Error message
                        # Printing the board
                        print_3d_list(myList)
                        print_ships_to_be_placed()
                        for ship in ship_list:
                            print_single_element(ship)
                        print_empty_line()
                        print_player_turn_to_place(turn)
                        print_to_place_ships()
                        continue;

                # Coordinate Availability Check
                if place_input_from_user[3] == "h":
                    for i in range(shipAndLength[place_input_from_user[0]]):
                        if (place_input_from_user[1]+i, place_input_from_user[2]) not in player1OccupiedPlaces:
                            isCoordinateAvailable = True
                        else:
                            isCoordinateAvailable = False
                            break;
                elif place_input_from_user[3] == "v":
                    for i in range(shipAndLength[place_input_from_user[0]]):
                        if (place_input_from_user[1], place_input_from_user[2]+i) not in player1OccupiedPlaces:
                            isCoordinateAvailable = True
                        else:
                            isCoordinateAvailable = False
                            break;
                if isCoordinateAvailable == False:
                    print_ship_cannot_be_placed_occupied((place_input_from_user[0].capitalize())) # Error message
                    # Printing the board
                    print_3d_list(myList)
                    print_ships_to_be_placed()
                    for ship in ship_list:
                        print_single_element(ship)
                    print_empty_line()
                    print_player_turn_to_place(turn)
                    print_to_place_ships()
                    continue;

                # Ship Placement Errors Handling Over

                # Ship Placements
                if place_input_from_user[3] == "h":
                    #Ship horizontal alignment
                    for i in range(shipAndLength[place_input_from_user[0]]):
                        player1_board[place_input_from_user[2]-1][place_input_from_user[1]+i-1] = "#"
                    myList = [player1_board, player2_board]
                    ship_list.remove(place_input_from_user[0].capitalize())

                    for i in range(shipAndLength[place_input_from_user[0]]):
                        player1OccupiedPlaces.append( (place_input_from_user[1]+i, place_input_from_user[2]) )

                    if len(ship_list) == 0:
                        # Printing the board
                        print_3d_list(myList)
                        for ship in ship_list:
                            print_single_element(ship)
                    else:
                        # Printing the board
                        print_3d_list(myList)
                        print_ships_to_be_placed()
                        for ship in ship_list:
                            print_single_element(ship)
                        print_empty_line()
                        print_player_turn_to_place(turn)
                        print_to_place_ships()

                elif place_input_from_user[3] == "v":
                    #Ship vertical alignment
                    for i in range(shipAndLength[place_input_from_user[0]]):
                        player1_board[place_input_from_user[2]+i-1][place_input_from_user[1]-1] = "#"
                    myList = [player1_board, player2_board]
                    ship_list.remove(place_input_from_user[0].capitalize())

                    for i in range(shipAndLength[place_input_from_user[0]]):
                        player1OccupiedPlaces.append((place_input_from_user[1], place_input_from_user[2]+i))

                    if len(ship_list) == 0:
                        # Printing the board
                        print_3d_list(myList)
                        for ship in ship_list:
                            print_single_element(ship)

                    else:
                        # Printing the board
                        print_3d_list(myList)
                        print_ships_to_be_placed()
                        for ship in ship_list:
                            print_single_element(ship)
                        print_empty_line()
                        print_player_turn_to_place(turn)
                        print_to_place_ships()

        if len(ship_list) == 0:
            print_confirm_placement()
            isCorrectConfirmMessage = False
            while isCorrectConfirmMessage == False:
                okOrNot = input()
                if okOrNot == "y" or okOrNot == "Y":
                    turn = 2
                    isCorrectConfirmMessage = True
                elif okOrNot == "n" or okOrNot == "N":
                    turn = 1
                    isCorrectConfirmMessage = True
                else:
                    isCorrectConfirmMessage = False
                    print_confirm_placement()
    player1LastBoard = player1_board.copy()

    while turn == 2:
        # Creating the board of two players.
        player1_board = [["-" for col in range(board_size)] for row in range(board_size)]
        player2_board = [["-" for col in range(board_size)] for row in range(board_size)]
        myList = [player1_board, player2_board]

        player2OccupiedPlaces = []
        # Ships
        ship_list = ["Carrier", "Battleship", "Cruiser", "Submarine", "Destroyer"]
        shipLengths = [5,4,3,3,2]
        shipAndLength = dict()
        for i in range(len(ship_list)):
            shipAndLength[ship_list[i].lower()] = shipLengths[i]

        # Printing the board
        print_3d_list(myList)
        print_ships_to_be_placed()
        for ship in ship_list:
            print_single_element(ship)
        print_empty_line()
        # Game starts for Player 2
        print_player_turn_to_place(turn)
        print_to_place_ships()

        while len(ship_list) != 0:

            # Correct Format Check
            isCorrectInputFormat = False
            # First Input Check
            isCorrectShipInput = False
            # Second and Third Input Check
            isCorrectCoordinates = False
            # Last Input Check
            isCorrectAlignment = False
            # Ship Inside Check
            isShipPlacedInside = False
            # Ship Availability Check
            isShipAvailable = False
            # Coordinate Availability Check
            isCoordinateAvailable = False

            # Input Error Handling
            while isCorrectInputFormat == False or isCorrectShipInput == False or isCorrectCoordinates == False or isCorrectAlignment == False or isShipPlacedInside == False or isShipAvailable == False or isCoordinateAvailable == False:

                # Correct Format Check
                isCorrectInputFormat = False
                # First Input Check
                isCorrectShipInput = False
                # Second and Third Input Check
                isCorrectCoordinates = False
                # Last Input Check
                isCorrectAlignment = False
                # Ship Inside Check
                isShipPlacedInside = False
                # Ship Availability Check
                isShipAvailable = False
                # Coordinate Availability Check
                isCoordinateAvailable = False
                allowedCoordinateInputs = ["1","2","3","4","5","6","7","8","9","10"]

                # Input from the user
                place_input_from_user = input().lower().strip().split() #is a list

                if len(place_input_from_user) < 4 or "." in place_input_from_user[1] or "." in place_input_from_user[2]:
                    print_incorrect_input_format() # Error message

                    # Printing the board
                    print_3d_list(myList)
                    print_ships_to_be_placed()
                    for ship in ship_list:
                        print_single_element(ship)
                    print_empty_line()
                    print_player_turn_to_place(turn)
                    print_to_place_ships()
                    continue;
                else:
                    place_input_from_user = [place_input_from_user[i] for i in range(4)] # Take the first 4 inputs
                    isCorrectInputFormat = True

                # Second and Third Input Check
                if place_input_from_user[1].isdigit() and place_input_from_user[2].isdigit():
                    place_input_from_user[1] = int(place_input_from_user[1])
                    place_input_from_user[2] = int(place_input_from_user[2])
                    if 0 < place_input_from_user[1] < 11 and 0 < place_input_from_user[2] < 11:
                        isCorrectCoordinates = True
                    else:
                        print_incorrect_coordinates() # Error message

                        # Printing the board
                        print_3d_list(myList)
                        print_ships_to_be_placed()
                        for ship in ship_list:
                            print_single_element(ship)
                        print_empty_line()
                        print_player_turn_to_place(turn)
                        print_to_place_ships()
                        continue;

                else:
                    print_incorrect_input_format() # Error message

                    # Printing the board
                    print_3d_list(myList)
                    print_ships_to_be_placed()
                    for ship in ship_list:
                        print_single_element(ship)
                    print_empty_line()
                    print_player_turn_to_place(turn)
                    print_to_place_ships()
                    continue;

                # First Input Check
                if place_input_from_user[0].lower() == "carrier" or place_input_from_user[0].lower() == "battleship" or place_input_from_user[0].lower() == "cruiser" or place_input_from_user[0].lower() == "submarine" or place_input_from_user[0].lower() == "destroyer":
                    isCorrectShipInput = True
                else:
                    print_incorrect_ship_name() # Error message

                    # Printing the board
                    print_3d_list(myList)
                    print_ships_to_be_placed()
                    for ship in ship_list:
                        print_single_element(ship)
                    print_empty_line()
                    print_player_turn_to_place(turn)
                    print_to_place_ships()
                    continue;

                # Last Input Check
                allowedAlignmentInputs = ["h","v","H","V"]
                isCorrectAlignment = False
                if place_input_from_user[3] in allowedAlignmentInputs:
                    isCorrectAlignment = True
                    if place_input_from_user[3] == "h" or place_input_from_user[3] == "H":
                        place_input_from_user[3] = "h"
                    if place_input_from_user[3] == "v" or place_input_from_user[3] == "V":
                        place_input_from_user[3] = "v"
                else:
                    print_incorrect_orientation()  # Error message

                    # Printing the board
                    print_3d_list(myList)
                    print_ships_to_be_placed()
                    for ship in ship_list:
                        print_single_element(ship)
                    print_empty_line()
                    print_player_turn_to_place(turn)
                    print_to_place_ships()
                    continue;
                # Input Error Handling Over

                # Ship Placement Errors Handling
                # From now on, first input is lower string, second & third inputs are integer and last input is lower string.
                # It is time to place our ships with our correct inputs

                # Creating the placement of player 2.

                # Ship is Available Check
                if place_input_from_user[0].capitalize() in ship_list:
                    isShipAvailable = True
                else:
                    print_ship_is_already_placed(place_input_from_user[0].capitalize()) # Error message
                    # Printing the board
                    print_3d_list(myList)
                    print_ships_to_be_placed()
                    for ship in ship_list:
                        print_single_element(ship)
                    print_empty_line()
                    print_player_turn_to_place(turn)
                    print_to_place_ships()
                    continue;

                # Ship Placement Inside Check
                if place_input_from_user[3] == "h":
                    if place_input_from_user[1] + shipAndLength[place_input_from_user[0]] <= 11:
                        isShipPlacedInside = True
                    else:
                        print_ship_cannot_be_placed_outside(place_input_from_user[0].capitalize()) # Error message
                        # Printing the board
                        print_3d_list(myList)
                        print_ships_to_be_placed()
                        for ship in ship_list:
                            print_single_element(ship)
                        print_empty_line()
                        print_player_turn_to_place(turn)
                        print_to_place_ships()
                        continue;
                elif place_input_from_user[3] == "v":
                    if place_input_from_user[2] + shipAndLength[place_input_from_user[0]] <= 11:
                        isShipPlacedInside = True
                    else:
                        print_ship_cannot_be_placed_outside(place_input_from_user[0].capitalize()) # Error message
                        # Printing the board
                        print_3d_list(myList)
                        print_ships_to_be_placed()
                        for ship in ship_list:
                            print_single_element(ship)
                        print_empty_line()
                        print_player_turn_to_place(turn)
                        print_to_place_ships()
                        continue;

                # Coordinate Availability Check
                if place_input_from_user[3] == "h":
                    for i in range(shipAndLength[place_input_from_user[0]]):
                        if (place_input_from_user[1]+i, place_input_from_user[2]) not in player2OccupiedPlaces:
                            isCoordinateAvailable = True
                        else:
                            isCoordinateAvailable = False
                            break;
                elif place_input_from_user[3] == "v":
                    for i in range(shipAndLength[place_input_from_user[0]]):
                        if (place_input_from_user[1], place_input_from_user[2]+i) not in player2OccupiedPlaces:
                            isCoordinateAvailable = True
                        else:
                            isCoordinateAvailable = False
                            break;
                if isCoordinateAvailable == False:
                    print_ship_cannot_be_placed_occupied((place_input_from_user[0].capitalize())) # Error message
                    # Printing the board
                    print_3d_list(myList)
                    print_ships_to_be_placed()
                    for ship in ship_list:
                        print_single_element(ship)
                    print_empty_line()
                    print_player_turn_to_place(turn)
                    print_to_place_ships()
                    continue;

                # Ship Placement Errors Handling Over

                # Ship Placements
                if place_input_from_user[3] == "h":
                    #Ship horizontal alignment
                    for i in range(shipAndLength[place_input_from_user[0]]):
                        player2_board[place_input_from_user[2]-1][place_input_from_user[1]+i-1] = "#"
                    myList = [player1_board, player2_board]
                    ship_list.remove(place_input_from_user[0].capitalize())

                    for i in range(shipAndLength[place_input_from_user[0]]):
                        player2OccupiedPlaces.append( (place_input_from_user[1]+i, place_input_from_user[2]) )

                    if len(ship_list) == 0:
                        # Printing the board
                        print_3d_list(myList)
                        for ship in ship_list:
                            print_single_element(ship)
                    else:
                        # Printing the board
                        print_3d_list(myList)
                        print_ships_to_be_placed()
                        for ship in ship_list:
                            print_single_element(ship)
                        print_empty_line()
                        print_player_turn_to_place(turn)
                        print_to_place_ships()

                elif place_input_from_user[3] == "v":
                    #Ship vertical alignment
                    for i in range(shipAndLength[place_input_from_user[0]]):
                        player2_board[place_input_from_user[2]+i-1][place_input_from_user[1]-1] = "#"
                    myList = [player1_board, player2_board]
                    ship_list.remove(place_input_from_user[0].capitalize())

                    for i in range(shipAndLength[place_input_from_user[0]]):
                        player2OccupiedPlaces.append((place_input_from_user[1], place_input_from_user[2]+i))

                    if len(ship_list) == 0:
                        # Printing the board
                        print_3d_list(myList)
                        for ship in ship_list:
                            print_single_element(ship)

                    else:
                        # Printing the board
                        print_3d_list(myList)
                        print_ships_to_be_placed()
                        for ship in ship_list:
                            print_single_element(ship)
                        print_empty_line()
                        print_player_turn_to_place(turn)
                        print_to_place_ships()

        if len(ship_list) == 0:
            print_confirm_placement()
            isCorrectConfirmMessage = False
            while isCorrectConfirmMessage == False:
                okOrNot = input()
                if okOrNot == "y" or okOrNot == "Y":
                    turn = 1
                    isCorrectConfirmMessage = True
                elif okOrNot == "n" or okOrNot == "N":
                    turn = 2
                    isCorrectConfirmMessage = True
                else:
                    isCorrectConfirmMessage = False
                    print_confirm_placement()

    player2LastBoard = player2_board.copy()

    # Savaş zamanı Allahını seven defansa gelsin.

    isBattleOver = False
    player1HitCount = 0
    player2HitCount = 0

    player1_board = [["-" for col in range(board_size)] for row in range(board_size)]
    player2_board = [["-" for col in range(board_size)] for row in range(board_size)]

    while isBattleOver == False:

        while turn == 1:
            myList = [player1LastBoard, player2_board]
            # Printing the board
            print_3d_list(myList)

            # Strike
            # Strike Input Error Handling
            isStrikeInputCorrect = False
            isTargetAvailable = False

            while isStrikeInputCorrect == False or isTargetAvailable == False:
                # Strike
                print_player_turn_to_strike(turn)
                print_choose_target_coordinates()
                # Strike Input
                strikeInput = input().lower().strip().split()
                if len(strikeInput) != 2:
                    isStrikeInputCorrect = False
                    print_incorrect_input_format()
                    myList = [player1LastBoard, player2_board]
                    # Printing the board
                    print_3d_list(myList)
                    continue
                else:
                    if strikeInput[0].isdigit() and strikeInput[1].isdigit():
                        (targetRow, targetCol) = tuple(strikeInput)
                    else:
                        isStrikeInputCorrect = False
                        print_incorrect_input_format()
                        myList = [player1LastBoard, player2_board]
                        # Printing the board
                        print_3d_list(myList)
                        continue

                if targetRow.isdigit() and targetCol.isdigit():
                    targetRow = int(targetRow)
                    targetCol = int(targetCol)
                    if 0 < targetRow < 11 and 0 < targetCol < 11:
                        isStrikeInputCorrect = True
                    else:
                        print_incorrect_coordinates()
                        myList = [player1LastBoard, player2_board]
                        # Printing the board
                        print_3d_list(myList)
                        continue
                else:
                    if targetRow.count(".") > 0 or targetCol.count(".") > 0:
                        print_incorrect_input_format()
                    elif len(targetRow) >= 3 or len(targetCol) >= 3:
                        print_incorrect_input_format()
                    else:
                        print_incorrect_coordinates()
                    myList = [player1LastBoard, player2_board]
                    # Printing the board
                    print_3d_list(myList)
                    continue

                if player2_board[targetCol-1][targetRow-1] == "!" or player2_board[targetCol-1][targetRow-1] == "O":
                    print_tile_already_struck()
                    myList = [player1LastBoard, player2_board]
                    # Printing the board
                    print_3d_list(myList)
                    isTargetAvailable = False
                    continue;
                else:
                    isTargetAvailable = True
            if (targetRow, targetCol) in player2OccupiedPlaces:
                print_hit()
                player1HitCount +=1
                player2LastBoard[targetCol-1][targetRow-1] = "!"
                player2_board[targetCol-1][targetRow-1] = "!"

                turn = 1

                if player1HitCount == 17:
                    isBattleOver = True
                    break;
            else:
                print_miss()
                player2LastBoard[targetCol-1][targetRow-1] = "O"
                player2_board[targetCol-1][targetRow-1] = "O"

                isDoneInputCorrect = False
                while isDoneInputCorrect == False:
                    print_type_done_to_yield(turn+1)
                    doneInput = input().lower().strip()
                    if doneInput == "done":
                        isDoneInputCorrect = True
                        turn = 2
            if player1HitCount == 17:
                isBattleOver = True
                break;

        while turn == 2:
            myList = [player1_board, player2LastBoard]
            # Printing the board
            print_3d_list(myList)

            # Strike
            # Strike Input Error Handling
            isStrikeInputCorrect = False
            isTargetAvailable = False

            while isStrikeInputCorrect == False or isTargetAvailable == False:
                # Strike
                print_player_turn_to_strike(turn)
                print_choose_target_coordinates()
                # Strike Input
                strikeInput = input().lower().strip().split()
                if len(strikeInput) != 2:
                    isStrikeInputCorrect = False
                    print_incorrect_input_format()
                    myList = [player1_board, player2LastBoard]
                    # Printing the board
                    print_3d_list(myList)
                    continue
                else:
                    if strikeInput[0].isdigit() and strikeInput[1].isdigit():
                        (targetRow, targetCol) = tuple(strikeInput)
                    else:
                        isStrikeInputCorrect = False
                        print_incorrect_input_format()
                        myList = [player1_board, player2LastBoard]
                        # Printing the board
                        print_3d_list(myList)
                        continue

                if targetRow.isdigit() and targetCol.isdigit():
                    targetRow = int(targetRow)
                    targetCol = int(targetCol)
                    if 0 < targetRow < 11 and 0 < targetCol < 11:
                        isStrikeInputCorrect = True
                    else:
                        print_incorrect_coordinates()
                        myList = [player1_board, player2LastBoard]
                        # Printing the board
                        print_3d_list(myList)
                        continue
                else:
                    if targetRow.count(".") > 0 or targetCol.count(".") > 0:
                        print_incorrect_input_format()
                    elif len(targetRow) >= 3 or len(targetCol) >= 3:
                        print_incorrect_input_format()
                    else:
                        print_incorrect_coordinates()
                    myList = [player1_board, player2LastBoard]
                    # Printing the board
                    print_3d_list(myList)
                    continue

                if player1_board[targetCol-1][targetRow-1] == "!" or player1_board[targetCol-1][targetRow-1] == "O":
                    print_tile_already_struck()
                    myList = [player1_board, player2LastBoard]
                    # Printing the board
                    print_3d_list(myList)
                    isTargetAvailable = False
                    continue;
                else:
                    isTargetAvailable = True
            if (targetRow, targetCol) in player1OccupiedPlaces:
                print_hit()
                player2HitCount +=1
                player1LastBoard[targetCol-1][targetRow-1] = "!"
                player1_board[targetCol-1][targetRow-1] = "!"

                turn = 2

                if player2HitCount == 17:
                    isBattleOver = True
                    break;
            else:
                print_miss()
                player1LastBoard[targetCol-1][targetRow-1] = "O"
                player1_board[targetCol-1][targetRow-1] = "O"

                isDoneInputCorrect = False
                while isDoneInputCorrect == False:
                    print_type_done_to_yield(turn-1)
                    doneInput = input().lower().strip()
                    if doneInput == "done":
                        isDoneInputCorrect = True
                        turn = 1
            if player2HitCount == 17:
                isBattleOver = True
                break;

    myList = [player1LastBoard, player2LastBoard]
    # Printing the board
    print_3d_list(myList)

    if isBattleOver == True:
        if player1HitCount == 17:
            print_player_won(1)
        elif player2HitCount == 17:
            print_player_won(2)
    print_thanks_for_playing()

# DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE
except:
    f.close()

