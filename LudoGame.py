

class Player:
    """The Player object represents the player who plays the game at a certain position.
    There will be 2-4 Player objects per game."""

    def __init__(self, position):
        """
        This method initializes the Player class with an objet with the required private data members.
        Parameters: Position - assigning each player a position of A, B, C, or D.
        """
        self._position = position
        # each player's letter
        # the position the player chooses (A, B, C, or D).
        if position == "A":
            self._start = 1
            self._end = 50
        elif position == "B":
            self._start = 15
            self._end = 8
        elif position == "C":
            self._start = 29
            self._end = 22
        else:
            self._start = 43
            self._end = 36
        # used for token_movement - will always be numbers unless H/R
        self._current_p_position = "H"
        self._current_q_position = "H"
        # used for token_location - will be the name of the spaces on the board.
        self._current_q_space = "H"
        self._current_p_space = "H"
        self._current_state = "is still playing"
        # the positions will be: "Home Yard (H)", "Ready to Go", "somewhere on the board", " Has Finished".
        # state will be: "won / finished game" or "is still playing".

    def get_completed(self):
        """
        This function will return True or False depending on if the player has finished the game or not.
        No Parameters
        """
        if self._current_p_position == 57 and self._current_q_position == 57:
            # print("True")
            return True
            # means the player is done.
        else:  # if the player is still in the game:
            # print("False")
            return False

    def get_token_p_step_count(self):
        """
        Returns the total steps the token p has taken on the board. (token p is the first token).
        No Parameters.
        use steps = -1 for home yard position and steps = 0 for ready to go position.
        The total step should not be larger than 57.
        Please note that if the token is bounced back in the home squares, this bounced part should be subtracted from
        the step count.
        For example, when token p is at space A5, the total step is 55 now.
        If it moves 5 steps and bounces back to A4, the total step should be 54, not 60.
        """
        if self._current_p_position == "H":
            return -1
        elif self._current_p_position == "R":
            return 0

        elif self._current_p_position == "E":
            return 57
        else:
            if int(self._current_p_position) < self._start:
                new_end = int(self._current_p_position) + 50
                return new_end - self._start
            else:
                traveled_steps = int(self._current_p_position) - self._start + 1
                return traveled_steps

    def get_token_q_step_count(self):
        """
        Returns the total steps the token q has taken on the board. (the other token / second token).
        No Parameters.
        """
        # TODO: how to get position for other tokens beside A?
        if self._current_q_position == "H":
            return -1
        elif self._current_q_position == "R":
            return 0
        elif self._current_p_position == "E":
            return 57
        else:
            if int(self._current_q_position) < self._start:
                new_end = int(self._current_q_position) + 50
                return new_end - self._start

            else:
                traveled_steps = int(self._current_q_position) - self._start
                return traveled_steps

    def get_space_name(self, total_steps):
        """
        Returns the name of the space the token has landed on the board as a string, the home yard position ("H"), and
        the ready to go position ("R").
        Parameters: total steps taken by the token.
        """
        # print(f"total steps: {total_steps}")
        if total_steps == "H" or total_steps == -1:
            return "H"
        elif total_steps == "R" or total_steps == 0:
            return "R"
        elif total_steps == 57 or total_steps == "E":
            return "E"
        else:
            if total_steps > 50:  # player A, B, C, and D - when in home squares.
                home_step = total_steps - 50
                # print(f"home step: {home_step}")
                return f"{self._position}{home_step}"

            elif total_steps < self._start:  # for B, C, D
                if total_steps + self._start >= 57:
                    return f"{total_steps + self._start - 57}"
                else:
                    return f"{self._start + total_steps - 1}"

            elif total_steps > self._start and total_steps + self._start > 57:
                added_steps = total_steps + self._start
                current_space = added_steps - 57
                return f"{current_space}"

            elif total_steps > self._start and total_steps + self._start < 57: # for A, B, C, D,
                current_space = total_steps + self._start
                return f"{current_space - 1}"

            else:  # need for position A
                return f"{total_steps - self._start + 1}"


class LudoGame:
    """
    The LudoGame object represents the game as played.
    The class should contain information about the players and information about the board.
    """

    def __init__(self):
        # holds all Player objects of the round.
        self._player_records = {}
        # keys: player object
        # values: player position, current p steps, current q steps, status, current p location, current q location.

    def get_player_by_position(self, position):
        """
        This method returns the player object by using the player's position.
        Parameter: player's position as a string.
        If an invalid string parameter is used, it will return "Player not found!"
        """
        # print(f"position - get player by position: {position}")
        for player_object in self._player_records:
            # print(f"self._player_records[player_object][0]: {self._player_records[player_object][0]}")
            if position == self._player_records[player_object][0]:
                # print("returning player_object - get player by position")
                return player_object

        return "Player not found!"

    def move_token(self, player_object, token_name, future_moves):
        """
        This method will move the tokens on the board, update the token's total steps, and will kick out other opponent
        tokens if needed.
        The play_game method will use this method.
        Parameters: player object, the name of the token being moved (p or q), and the moves rolled from the die.
        """

        # retrieve the player_object and find the current position using the token name.
        # using the future moves parameter, see if the move is doable or needs to be bounced back.
        # then update the token accordingly.

        # print("IN MOVE TOKEN")
        # TODO: moving the token CHECK THIS
        # token p steps
        token_p_steps = self._player_records[player_object][1]
        # if token_p_steps == "H":
        #     token_p_steps = -1

        if self._player_records[player_object][1] == "R":
            token_p_steps = 0
            self._player_records[player_object][1] = 0

        # token p location:
        token_p_location = self._player_records[player_object][4]

        # token q steps
        token_q_steps = self._player_records[player_object][2]
        # if token_q_steps == "H":
        #     token_q_steps = -1

        if self._player_records[player_object][2] == "R":
            token_q_steps = 0
            self._player_records[player_object][2] = 0

        # token q location:
        token_q_location = self._player_records[player_object][5]

        # if a token is not at "H":
        if token_p_steps != "H" and token_q_steps != "H":
            # print("NO H'S")

            # player has rolled a 6:
            if future_moves == 6:
                # print("FUTURE MOVES = 6")

                # if tokens are not stacked:
                # if tokens are not stacked but at "R" together - move "p".
                if token_p_location == "R" and token_q_location == "R":
                    if token_p_steps == "R":
                        token_p_steps = 0
                    new_step = token_p_steps + future_moves
                    new_location = player_object.get_space_name(new_step)
                    self.update_everything(player_object, "p", new_step, new_location)
                    return

                elif token_p_location != token_q_location:
                    # print("move_token: not stacked")

                    # if token p is done, only token q moves:
                    if token_p_steps == 57:
                        # print("move_token: third elif")
                        token_name = "q"
                        if token_q_steps != "H":
                            # print("move_token: third elif - first if")
                            token_q_location += future_moves
                            new_step = token_q_steps
                            new_location = player_object.get_space_name(new_step)
                            self.update_everything(player_object, token_name, new_step, new_location)
                            # token_name should be q here because token p is finished.
                            # print(self._player_records)
                            # print("returning to next turn")
                            return

                    # if token q is done, only token p moves:
                    elif token_q_steps == 57:
                        # print("move_token: fourth elif")
                        token_name = "p"
                        if token_p_steps != "H":
                            # print("move_token: fourth elif - first if")
                            token_p_steps += future_moves
                            new_step = token_p_steps
                            new_location = player_object.get_space_name(new_step)
                            self.update_everything(player_object, token_name , new_step, new_location)

                            # token_name should be p here because token q is finished.
                            # print(self._player_records)
                            # print("returning to next turn")
                            return

                    # if p != "H" and q != "H" and they're both not done yet - treated like a normal 6.
                    else:
                        # print("move_token: else")

                        # deciding which token gets to make the move:
                        token_p_distance = 57 - self._player_records[player_object][1]
                        token_q_distance = 57 - self._player_records[player_object][2]

                        if token_p_distance < token_q_distance:
                            token_name = "q"
                        else:
                            token_name = "p"
                        # print(f"token_name: {token_name}")

                        ############### HOME SQUARES ###############################
                        # if player is in home squares - regardless of what token_name is:
                        # for token p:
                        if 49 < token_p_steps < 57:
                            # so the spot is 50 - 56 because 57 is "E".
                            winning_roll = 57 - self._player_records[player_object][1]
                            # print("entered here")

                            if future_moves + token_p_steps == 57:
                                # print(f"perfect roll")
                                self._player_records[player_object][1] = 57
                                self.token_in(player_object, token_name)
                                # print(self._player_records)
                                return

                            # no need to bounce back:
                            elif future_moves + token_p_steps < 57:
                                # print(f" not bouncing back")
                                token_p_steps += future_moves
                                # print(f" IN HOME SQUARES - BOUNCING BACK: {self._player_records[player_object][1]}")
                                new_step = token_p_steps
                                new_location = player_object.get_space_name(new_step)
                                self.update_everything(player_object, "p", new_step, new_location)
                                return

                            # need to bounce back:
                            elif future_moves + token_p_steps > 57:
                                # print(f" bouncing back")
                                leftover_moves = future_moves - winning_roll
                                token_p_steps = 57 - leftover_moves
                                new_step = token_p_steps
                                new_location = player_object.get_space_name(new_step)
                                self.update_everything(player_object, "p", new_step, new_location)
                                return

                        # for token q - if token q can win:
                        elif future_moves + token_q_steps == 57:
                            # print("PERFECT ROLL !!")
                            self._player_records[player_object][2] = 57
                            self.token_in(player_object, token_name)
                            return

                        # for token q - moving in the home squares:
                        elif 49 < token_q_steps < 57 and token_p_distance > 49:
                            # so the spot is 50 - 56 because 57 is E
                            winning_roll = 57 - token_q_steps
                            # print("entered here !!")

                            # no need to bounce back:
                            if future_moves + token_q_steps < 57:
                                token_q_steps += future_moves
                                # print(f" IN HOME SQUARES - BOUNCING BACK: {self._player_records[player_object][1]}")
                                new_step = token_q_steps
                                new_location = player_object.get_space_name(new_step)
                                self.update_everything(player_object, "q", new_step, new_location)
                                return

                            # need to bounce back:
                            elif future_moves + token_q_steps > 57:
                                leftover_moves = future_moves - winning_roll
                                token_q_steps = 57 - leftover_moves
                                new_step = token_q_steps
                                new_location = player_object.get_space_name(new_step)
                                self.update_everything(player_object, "q", new_step, new_location)
                                return

                        ############################ END OF HOME SQUARES ##################################

                        # if token is nowhere near home squares and is just moving along the board:
                        else:
                            # print(f" in the else")
                            # print("HERE AS WELL")

                            # if an opponent token can be kicked, move that token.
                            for other_player in self._player_records:
                                if other_player != player_object:
                                    # print("entered hereS")

                                    # other player's locations:
                                    opponent_p = self._player_records[other_player][4]
                                    opponent_q = self._player_records[other_player][5]

                                    # if we need to move token p - MAKE SURE THEY DON'T EQUAL H OR R
                                    if token_p_location != "H" or token_p_location != "R":
                                        possible_step = token_p_steps + future_moves
                                        possible_location = player_object.get_space_name(possible_step)

                                        if possible_location == opponent_p or possible_location == opponent_q:
                                            # print("entered here - P TOKENS")
                                            new_step = "H"
                                            new_location = other_player.get_space_name(new_step)
                                            if possible_location == opponent_p:
                                                token_name = "p"
                                            elif possible_location == opponent_q:
                                                token_name = "q"
                                            self.update_everything(other_player, token_name, new_step, new_location)
                                            self.update_everything(player_object, "p", possible_step, possible_location)
                                            return
                                            # TODO: SHOULD A RETURN STATEMENT BE HERE?

                                    # if we need to move token q - MAKE SURE THEY DON'T EQUAL H OR R:
                                    if token_q_location != "H" or token_q_location != "R":
                                        possible_step = token_q_steps + future_moves
                                        possible_location = player_object.get_space_name(possible_step)

                                        if possible_location == opponent_p or possible_location == opponent_q:
                                            # print("entered here - Q TOKENS")
                                            new_step = "H"
                                            new_location = other_player.get_space_name(new_step)
                                            if possible_location == opponent_q:
                                                token_name = "q"
                                            elif possible_location == opponent_p:
                                                token_name = "p"
                                            self.update_everything(other_player, token_name, new_step, new_location)
                                            self.update_everything(player_object, "q", possible_step, possible_location)
                                            return
                                            # TODO: KEEP RETURN?
                            # print("TEST")
                            # print(f"token_name: {token_name}")

                            # no token to kick - just moving player's token p
                            if token_name == "p":
                                # print(f" here")
                                token_p_steps += future_moves
                                new_step = token_p_steps
                                new_location = player_object.get_space_name(new_step)
                                self.update_everything(player_object, "p", new_step, new_location)
                                # token_name should be p here unless token p is finished.
                                # print(self._player_records)
                                # print("returning to next turn")
                                return

                            # no token to kick - just moving player's token q
                            else:  # token name = q
                                # print('HERE')
                                token_q_steps += future_moves
                                new_step = token_q_steps
                                new_location = player_object.get_space_name(new_step)
                                self.update_everything(player_object, "q", new_step, new_location)
                                # print(self._player_records)
                                return

                # if tokens are stacked with no "H":
                if token_p_location == token_q_location:
                    # print("HERE")

                    ###################### HOME SQUARES FOR STACKED - NO H #####################
                    # #if player is in home squares:
                    # for both token:
                    if 49 < token_p_steps < 57:  # so the spot is 50 - 56 because 57 is "E".
                        winning_roll = 57 - self._player_records[player_object][1]

                        # if winning roll:
                        if future_moves + token_p_steps == 57:
                            self._player_records[player_object][1] = 57
                            self._player_records[player_object][2] = 57
                            self.token_in(player_object, "both")

                        # no need to bounce back:
                        elif future_moves + token_p_steps < 57:
                            token_p_steps += future_moves

                            new_step = token_p_steps
                            new_location = player_object.get_space_name(new_step)
                            self.update_everything(player_object, "both", new_step, new_location)
                            return

                        # need to bounce back:
                        elif future_moves + token_p_steps > 57:
                            leftover_moves = future_moves - winning_roll
                            token_p_steps = 57 - leftover_moves
                            new_step = token_p_steps
                            new_location = player_object.get_space_name(new_step)
                            self.update_everything(player_object, "both", new_step, new_location)
                            return
                    #################################################################################################

                    # moving stacked tokens normally - No H's present and not in home squares.
                    elif token_p_steps != "H":
                        # print("currently stacked")
                        token_p_steps += future_moves
                        token_q_steps = token_p_steps
                        new_step = token_q_steps
                        new_location = player_object.get_space_name(new_step)
                        self.update_everything(player_object, "both", new_step, new_location)
                        # print(self._player_records)
                        return

            elif future_moves != 6:
                # print(f"self._player_records[player_object][1]: {self._player_records[player_object][1]} - line 448")
                # print(f"self._player_records[player_object][2]: {self._player_records[player_object][2]} - line 449")

                # if tokens are at "R" - SHOULD NOT BE STACKED AND JUST P SHOULD MOVE FIRST.
                if token_p_location == "R" and token_q_location == "R":
                    # print("R'S HERE")
                    token_p_steps = 0
                    new_step = token_p_steps + future_moves
                    new_location = player_object.get_space_name(new_step)
                    self.update_everything(player_object, "p", new_step, new_location)
                    return

                # not stacked at all
                if token_p_location != token_q_location:

                    # deciding which token gets to make the move:
                    token_p_distance = 57 - self._player_records[player_object][1]
                    token_q_distance = 57 - self._player_records[player_object][2]

                    if token_p_distance < token_q_distance:
                        token_name = "q"
                    else:
                        token_name = "p"

                    # print(f"token_name: {token_name}")

                    ############### HOME SQUARES ############################################################
                    # if p or q is in home squares - NOT STACKED:
                    if 49 < token_p_steps < 57 or 49 < token_q_steps < 57:

                        # if token p can "E", move token p
                        if future_moves + token_p_steps == 57:
                            self._player_records[player_object][1] = 57
                            self.token_in(player_object, "p")
                            return

                        # if token q can "E", move token q
                        elif future_moves + token_q_steps == 57:
                            self._player_records[player_object][2] = 57
                            self.token_in(player_object, "q")
                            return

                        # if token p is in home squares and token q is not:
                        elif 49 < token_p_steps < 57 and token_q_steps < 50:
                            new_step = token_q_steps + future_moves
                            new_location = player_object.get_space_name(new_step)
                            self.update_everything(player_object, "q", new_step, new_location)
                            return

                        # if token q is in home squares and token p is not:
                        elif 49 < token_q_steps < 57 and token_p_steps < 50:
                            new_step = token_p_steps + future_moves
                            new_location = player_object.get_space_name(new_step)
                            self.update_everything(player_object, "p", new_step, new_location)
                            return

                        # if both tokens are in home squares:
                        elif 49 < token_p_steps < 57 and 49 < token_q_steps < 57:

                            winning_roll = 57 - token_p_steps

                            # moving token q
                            if token_p_distance < token_q_distance:

                                # bouncing back:
                                if future_moves + token_q_steps > 57:
                                    leftover_moves = future_moves - winning_roll
                                    token_q_steps = 57 - leftover_moves
                                    new_step = token_q_steps
                                    new_location = player_object.get_space_name(new_step)
                                    self.update_everything(player_object, "q", new_step, new_location)
                                    return

                                # no need to bounce back:
                                elif future_moves + token_q_steps < 57:
                                    token_q_steps += future_moves
                                    # print(f" IN HOME SQUARES - BOUNCING BACK: {self._player_records[player_object][1]}")
                                    new_step = token_q_steps
                                    new_location = player_object.get_space_name(new_step)
                                    self.update_everything(player_object, "q", new_step, new_location)
                                    return

                            # moving token p:
                            if token_p_distance > token_q_distance:
                                # bouncing back:
                                if future_moves + token_p_steps > 57:
                                    leftover_moves = future_moves - winning_roll
                                    token_p_steps = 57 - leftover_moves
                                    new_step = token_p_steps
                                    new_location = player_object.get_space_name(new_step)
                                    self.update_everything(player_object, "p", new_step, new_location)
                                    return

                                # no need to bounce back:
                                elif future_moves + token_p_steps < 57:
                                    token_p_steps += future_moves
                                    # print(f" IN HOME SQUARES - BOUNCING BACK: {self._player_records[player_object][1]}")
                                    new_step = token_p_steps
                                    new_location = player_object.get_space_name(new_step)
                                    self.update_everything(player_object, "p", new_step, new_location)
                                    return
                    ############################ END OF HOME SQUARES #################################

                    # if token is nowhere near home squares and is just moving along the board:
                    else:
                        # print(f" NO WHERE NEAR HOME SQUARES")

                        token_p_steps = self._player_records[player_object][1]
                        token_p_location = self._player_records[player_object][4]

                        token_q_steps = self._player_records[player_object][2]
                        token_q_location = self._player_records[player_object][5]

                        # if an opponent token can be kicked, move that token.
                        for other_player in self._player_records:
                            if other_player != player_object:

                                # if we need to move according to token p:
                                if token_p_location == "R":
                                    token_p_steps = 0
                                future_p_movement = future_moves + token_p_steps
                                future_p_space = player_object.get_space_name(future_p_movement)

                                    # print(f"future_p_space: {future_p_space}")

                                opponent_p = self._player_records[other_player][4]
                                opponent_q = self._player_records[other_player][5]

                                if future_p_space == opponent_p or future_p_space == opponent_q:
                                    new_step = "H"
                                    new_location = other_player.get_space_name(new_step)
                                    if future_p_space == opponent_p:
                                        token_name = "p"
                                    elif future_p_space == opponent_q:
                                        token_name = "q"
                                    # update other player's information
                                    self.update_everything(other_player, token_name, new_step, new_location)

                                    # update player's information
                                    self.update_everything(player_object, "p", future_p_movement, future_p_space)
                                    return

                                # if we need to move according to token q:
                                if token_q_location == "R":
                                    token_q_steps = 0

                                future_q_movement = future_moves + token_q_steps
                                future_q_space = player_object.get_space_name(future_q_movement)

                                opponent_p = self._player_records[other_player][4]
                                opponent_q = self._player_records[other_player][5]

                                # print(f"future_p_space: {future_p_space}")

                                if future_q_space == opponent_q or future_q_space == opponent_p:
                                    new_step = "H"
                                    new_location = other_player.get_space_name(new_step)
                                    if future_q_space == opponent_p:
                                        token_name = "p"
                                    elif future_q_space == opponent_q:
                                        token_name = "q"
                                    # update other player's information
                                    self.update_everything(other_player, token_name, new_step, new_location)

                                    # update player's information
                                    self.update_everything(player_object, "q", future_q_movement, future_q_space)
                                    return

                        # else - just move the tokens normally.
                        # deciding which token gets to make the move:
                        token_p_distance = 57 - self._player_records[player_object][1]
                        token_q_distance = 57 - self._player_records[player_object][2]

                        if token_p_distance < token_q_distance:
                            token_name = "q"
                        else:
                            token_name = "p"


                        if token_name == "p":
                            new_step = token_p_steps + future_moves
                            new_location = player_object.get_space_name(new_step)
                            self.update_everything(player_object, "p", new_step, new_location)
                            print(self._player_records)
                            return

                        elif token_name == "q":
                            new_step = token_q_steps + future_moves
                            new_location = player_object.get_space_name(new_step)
                            self.update_everything(player_object, "q", new_step, new_location)

                            print(self._player_records)
                            return

                # if tokens are stacked - no "H":
                elif token_p_location == token_q_location:
                    # print("ENTERED STACKED NO 'H'")

                    ###################################### HOME SQUARES WITH NO H AND STACKED ################

                    # if player is in home squares:
                    # for both tokens but only checking p since they should be stacked - bouncing back:
                    if 49 < token_p_steps < 57:  # so the spot is 50 - 56 because 57 is "E".
                        winning_roll = 57 - token_p_steps

                        # no need to bounce back:
                        if future_moves + token_p_steps < 57:
                            token_p_steps += future_moves
                            new_step = token_p_steps
                            new_location = player_object.get_space_name(new_step)
                            self.update_everything(player_object, "both", new_step, new_location)
                            return

                        # need to bounce back:
                        elif future_moves + token_p_steps > 57:
                            leftover_moves = future_moves - winning_roll
                            token_p_steps = 57 - leftover_moves
                            new_step = token_p_steps
                            new_location = player_object.get_space_name(new_step)
                            self.update_everything(player_object, "both", new_step, new_location)
                            return

                        # for perfect roll:
                        # TODO: MIGHT HAVE TO CHECK THIS LATER - 8/3/22
                        elif token_p_steps + future_moves == 57:
                            self._player_records[player_object][1] += future_moves
                            self._player_records[player_object][2] += future_moves
                            # print(f"checking to see if token updates for perfect winning roll: {self._player_records[player_object]}")
                            self.token_in(player_object, "both")
                            return

                    # else not in home squares:
                    else:
                        token_distance = 57 - self._player_records[player_object][1]
                        # print(f"token_distance: {token_distance}")

                        new_step = token_p_steps + future_moves
                        new_location = player_object.get_space_name(new_step)
                        self.update_everything(player_object, "both", new_step, new_location)

                        # print(self._player_records)
                        # print("returning to next turn")
                        return

        # if a token is at "H":
        elif token_p_steps == "H" or token_q_steps == "H":
            # print("H'S PRESENT")

            # if future moves == 6:
            if future_moves == 6:

                # if tokens are not stacked:
                # print("TOKEN'S NOT STACKED")
                # print(self._player_records)

                # token p and token q are both "H" - token name will be "p" and p will move first:
                if token_p_steps == "H" and token_q_steps == "H":
                    # print("move_token: first if")
                    new_step = "R"
                    new_location = player_object.get_space_name(new_step)
                    self.update_everything(player_object, "p", new_step, new_location)
                    # # token_name should be p here.
                    return

                # if tokens are both at "R" - should not be stacked - p should be moved.
                elif token_p_steps == "R" and token_q_steps == "R":
                    new_location = player_object.get_space_name(future_moves)
                    self.update_everything(player_object, "p", future_moves, new_location)
                    return

                elif token_p_steps != token_q_steps:
                    # print(f" self._player_records[player_object][1]: {self._player_records[player_object][1]}")

                    ############################### IN HOME SQUARES - NOT STACKED WITH H'S. #################################
                    # if in home square and the perfect roll came out:
                    if token_p_steps != "H" and token_q_steps != "H":

                        # if token p or q is perfect roll:
                        if 49 < token_p_steps < 57 or 49 < token_q_steps < 57:
                            if future_moves + token_p_steps == 57:
                                self._player_records[player_object][1] = 57
                                self.token_in(player_object, "p")
                                return

                            elif future_moves + token_q_steps == 57:
                                self._player_records[player_object][2] = 57
                                self.token_in(player_object, "q")
                                return

                        # if token p bounces:
                        elif 49 < token_p_steps < 57 and token_p_steps + future_moves > 57:
                            winning_roll = 57 - token_p_steps
                            leftover_moves = future_moves - winning_roll
                            token_p_steps = 57 - leftover_moves
                            new_step = token_p_steps
                            new_location = player_object.get_space_name(new_step)
                            self.update_everything(player_object, "p", new_step, new_location)
                            return

                        # if token p bounces:
                        elif 49 < token_q_steps < 57 and token_q_steps + future_moves > 57:
                            winning_roll = 57 - token_q_steps
                            leftover_moves = future_moves - winning_roll
                            token_q_steps = 57 - leftover_moves
                            new_step = token_q_steps
                            new_location = player_object.get_space_name(new_step)
                            self.update_everything(player_object, "q", new_step, new_location)
                            return

                        # if token p does not need to bounce:
                        elif 49 < token_p_steps < 57 and token_p_steps + future_moves < 57:
                            winning_roll = 57 - token_p_steps
                            new_step = token_p_steps
                            new_location = player_object.get_space_name(new_step)
                            self.update_everything(player_object, "p", new_step, new_location)
                            return

                        # if token q does not need to bounce:
                        elif 49 < token_q_steps < 57 and token_q_steps + future_moves < 57:
                            winning_roll = 57 - token_q_steps
                            new_step = token_q_steps
                            new_location = player_object.get_space_name(new_step)
                            self.update_everything(player_object, "q", new_step, new_location)
                            return


                    ####################### END OF HOME SQUARES #######################################

                    # token p != "H" (might be done) and token q = "H" - token q moves to "R"/0
                    elif token_p_steps != "H" and token_q_steps == "H":
                        # print("move_token: first elif")
                        new_step = "R"
                        new_location = player_object.get_space_name(new_step)
                        self.update_everything(player_object, "q", new_step, new_location)
                        # print(self._player_records)
                        return

                    # p == "H" and q != "H" - token p got kicked back to "H" - move token p
                    elif token_p_steps == "H" and token_q_steps != "H":
                        # print("move_token: second elif")
                        new_step = "R"
                        new_location = player_object.get_space_name(new_step)
                        self.update_everything(player_object, "p", new_step, new_location)

                        # print(self._player_records)
                        # print("returning to next turn")
                        return

                    # if p != H and q! - move like a regular roll.
                    else:
                        token_p_distance = 57 - token_p_steps
                        token_q_distance = 57 - token_q_steps

                        if token_p_distance > token_q_distance:
                            token_name = "p"
                        elif token_p_distance < token_q_distance:
                            token_name = "q"

                        # if kicking is possible:
                        for other_player in self._player_records:
                            opponent_p = self._player_records[other_player][4]
                            opponent_q = self._player_records[other_player][5]

                            future_p_space = future_moves + token_p_steps
                            future_p_location = player_object.get_space_name(future_p_space)

                            future_q_space = future_moves + token_q_steps
                            future_q_location = player_object.get_space_name(future_q_space)

                            # player's p can kick
                            if future_p_location == opponent_p or future_p_location == opponent_q:
                                if future_p_location == opponent_p:
                                    token_name = "p"
                                elif future_p_location == opponent_q:
                                    token_name = "q"
                                self.update_everything(other_player, token_name, "H", "H")
                                self.update_everything(player_object, "p", future_p_space, future_p_location)
                                return

                            # player's q can kick
                            if future_q_location == opponent_p or future_q_location == opponent_q:
                                    if future_q_location == opponent_p:
                                        token_name = "p"
                                    elif future_q_location == opponent_q:
                                        token_name = "q"
                                    self.update_everything(other_player, token_name, "H", "H")
                                    self.update_everything(player_object, "q", future_q_space, future_q_location)
                                    return

                        # just moving token according to distance rule
                        else:
                            if token_name == "p":
                                new_step = token_p_steps + future_moves
                                new_location = player_object.get_space_name(new_step)
                                self.update_everything(player_object, "p", new_step, new_location)
                                return
                            else:
                                new_step = token_q_steps + future_moves
                                new_location = player_object.get_space_name(new_step)
                                self.update_everything(player_object, "q", new_step, new_location)
                                return

            elif future_moves != 6:

                # if tokens are not stacked:
                if token_p_location != token_q_location:
                    # print(f" checking to see if here")
                    # print(f"token_q_steps: {token_q_steps} - line 876")
                    # p == "H" and q == "H" - basically skips turn
                    if self._player_records[player_object][1] == "H" and self._player_records[player_object][2] == "H":
                        # print("SKIPPING TURN AND RETURNING TO NEW TURN")
                        return

                    ################################# HOME SQUARES ###########################################

                    # if perfect roll is rolled, move that token.
                    elif token_q_steps != "H" and token_q_steps + future_moves == 57:
                        self._player_records[player_object][2] = token_q_steps + future_moves
                        self.token_in(player_object, "q")
                        return

                    elif token_p_steps != "H" and token_p_steps + future_moves == 57:
                        self._player_records[player_object][1] = token_p_steps + future_moves
                        self.token_in(player_object, "p")
                        return

                    # if p and q are both in home squares:
                    elif token_p_steps == 57 and token_q_steps == 57:
                        token_p_distance = 57 - token_p_steps
                        token_q_distance = 57 - token_q_steps

                        if token_p_distance > token_q_distance: # moving token p
                            winning_roll = 57 - token_p_steps
                            # not a perfect roll- no need to bounce back:
                            if future_moves + token_p_steps < 57:
                                token_p_steps += future_moves
                                # print(f" IN HOME SQUARES - BOUNCING BACK: {self._player_records[player_object][1]}")
                                new_step = token_p_steps
                                new_location = player_object.get_space_name(new_step)
                                self.update_everything(player_object, "p", new_step, new_location)
                                return

                            # need to bounce back:
                            elif future_moves + token_p_steps > 57:
                                leftover_moves = future_moves - winning_roll
                                token_p_steps = 57 - leftover_moves
                                new_step = token_p_steps
                                new_location = player_object.get_space_name(new_step)
                                self.update_everything(player_object, "p", new_step, new_location)
                                return

                        elif token_p_distance < token_q_distance: # moving token q
                            winning_roll = 57 - token_q_steps
                            # not a perfect roll- no need to bounce back:
                            if future_moves + token_q_steps < 57:
                                token_q_steps += future_moves
                                # print(f" IN HOME SQUARES - BOUNCING BACK: {self._player_records[player_object][1]}")
                                new_step = token_q_steps
                                new_location = player_object.get_space_name(new_step)
                                self.update_everything(player_object, "q", new_step, new_location)
                                return

                            # need to bounce back:
                            elif future_moves + token_q_steps > 57:
                                leftover_moves = future_moves - winning_roll
                                token_q_steps = 57 - leftover_moves
                                new_step = token_q_steps
                                new_location = player_object.get_space_name(new_step)
                                self.update_everything(player_object, "q", new_step, new_location)
                                return

                    # if only token p is in home square
                    elif token_p_steps != "H" and 49 < token_p_steps < 57:
                        # print("entered home squares for p")
                        winning_roll = 57 - token_p_steps

                        # not a perfect roll- no need to bounce back:
                        if future_moves + token_p_steps < 57:
                            token_p_steps += future_moves
                            # print(f" IN HOME SQUARES - BOUNCING BACK: {self._player_records[player_object][1]}")
                            new_step = token_p_steps
                            new_location = player_object.get_space_name(new_step)
                            self.update_everything(player_object, "p", new_step, new_location)
                            return

                        # need to bounce back:
                        elif future_moves + token_p_steps > 57:
                            leftover_moves = future_moves - winning_roll
                            token_p_steps = 57 - leftover_moves
                            new_step = token_p_steps
                            new_location = player_object.get_space_name(new_step)
                            self.update_everything(player_object, "p", new_step, new_location)
                            return

                    # if only token q is in home square
                    elif token_q_steps != "H" and 49 < token_q_steps < 57:
                        # print("entered home squares for p")
                        winning_roll = 57 - token_q_steps

                        # not a perfect roll- no need to bounce back:
                        if future_moves + token_q_steps < 57:
                            token_q_steps += future_moves
                            # print(f" IN HOME SQUARES - BOUNCING BACK: {self._player_records[player_object][1]}")
                            new_step = token_q_steps
                            new_location = player_object.get_space_name(new_step)
                            self.update_everything(player_object, "q", new_step, new_location)
                            return

                        # need to bounce back:
                        elif future_moves + token_q_steps > 57:
                            leftover_moves = future_moves - winning_roll
                            token_q_steps = 57 - leftover_moves
                            new_step = token_q_steps
                            new_location = player_object.get_space_name(new_step)
                            self.update_everything(player_object, "q", new_step, new_location)
                            return
                    ########################### HOME SQUARES END ########################

                    # IF NOT IN HOME SQUARES
                    # if p == H and q != H, move q
                    if token_p_steps == "H" and token_q_steps != "H":
                        new_step = token_q_steps + future_moves
                        new_location = player_object.get_space_name(new_step)
                        self.update_everything(player_object, "q", new_step, new_location)
                        return

                    # if p != H and q == H, move p
                    elif token_p_steps != "H" and token_q_steps == "H":
                        new_step = token_p_steps + future_moves
                        new_location = player_object.get_space_name(new_step)
                        self.update_everything(player_object, "p", new_step, new_location)
                        return

                    # if p != H and q != H - see if kicking is available.
                    elif token_p_steps != "H" and token_q_steps != "H":
                        token_p_distance = 57 - token_p_steps
                        token_q_distance = 57 - token_q_steps

                        if token_p_distance > token_q_distance:
                            token_name = "p"
                        elif token_p_distance < token_q_distance:
                            token_name = "q"

                        # if kicking is possible:
                        for other_player in self._player_records:
                            opponent_p = self._player_records[other_player][4]
                            opponent_q = self._player_records[other_player][5]

                            future_p_space = future_moves + token_p_steps
                            future_p_location = player_object.get_space_name(future_p_space)

                            future_q_space = future_moves + token_q_steps
                            future_q_location = player_object.get_space_name(future_q_space)

                            # player's p can kick
                            if future_p_location == opponent_p or future_p_location == opponent_q:
                                if future_p_location == opponent_p:
                                    token_name = "p"
                                elif future_p_location == opponent_q:
                                    token_name = "q"
                                self.update_everything(other_player, token_name, "H", "H")
                                self.update_everything(player_object, "p", future_p_space, future_p_location)
                                return

                            # player's q can kick
                            if future_q_location == opponent_p or future_q_location == opponent_q:
                                if future_q_location == opponent_p:
                                    token_name = "p"
                                elif future_q_location == opponent_q:
                                    token_name = "q"
                                self.update_everything(other_player, token_name, "H", "H")
                                self.update_everything(player_object, "q", future_q_space, future_q_location)
                                return

                        # just moving token according to distance rule
                        else:
                            if token_name == "p":
                                new_step = token_p_steps + future_moves
                                new_location = player_object.get_space_name(new_step)
                                self.update_everything(player_object, "p", new_step, new_location)
                                return
                            else:
                                new_step = token_q_steps + future_moves
                                new_location = player_object.get_space_name(new_step)
                                self.update_everything(player_object, "q", new_step, new_location)
                                return

            # if player's 2 tokens are on the same spot/ STACKING:
            if self._player_records[player_object][4] == self._player_records[player_object][5]:
                self._player_records[player_object][1] = self._player_records[player_object][2]
                new_step = self._player_records[player_object][1]
                new_location = player_object.get_space_name(new_step)
                self.update_everything(player_object, "both", new_step, new_location)
                return

    def play_game(self, players_list, turns_list):
        """
        This method will create the player list first using the players list pass in, then move the tokens according to
        the returns list following the priority rule and update the tokens positions and the player's game state.
        After all the moving is done in the turns_list, the method will return a list of strings representing the
        current spaces of all the tokens for each player in the list after moving the tokens.
        """
        game_players = []
        returning_list = []
        # this is the list that will be returned once the method is done.

        for player in players_list:
            self._player_records[Player(player)] = [player, Player(player)._current_p_position,
                                                    Player(player)._current_q_position, Player(player)._current_state,
                                                    Player(player).get_space_name("H"),
                                                    Player(player).get_space_name("H")]
            game_players.append(player)
        # print(self._player_records)

        turns_list_copy = list(turns_list)

        self.continuing_game(game_players, turns_list_copy)


        for player_object in self._player_records:
            returning_list.append(self._player_records[player_object][4])
            returning_list.append(self._player_records[player_object][5])

            if self._player_records[player_object][1] == 57 and self._player_records[player_object][2] == 57:
                player_object._current_state = "won and finished game"

            print(f"current_state: {player_object._current_state}")
            # print(f" current_p: {player_object._current_p_position}")

        return returning_list

    def continuing_game(self, game_players, turns_list_copy):
        """
        This method is to allow the program to edit the turns list without starting a new game.
        Parameters: game_players (the players_list) and the turns_list_copy
        """
        previous_turn = ("", "")
        token_stacked = ""
        # if an illegal move occurs - such as a turn for a player that does not exist.
        for turn in turns_list_copy:
            position = turn[0]
            if position not in game_players:
                turns_list_copy.remove(turn)
            if previous_turn[1] == 6 and turn[1] == 6:
                next_turn = turn.next()
                if next_turn[0] == turn[0]:
                    turns_list_copy.remove(next_turn)

        for turn in turns_list_copy:  # this list copy is a newly edited list.
            print(f"        current turn: {turn}")
            position = turn[0]
            move = turn[1]

            player_object = self.get_player_by_position(position)

            print(f"current p: {player_object._current_p_position}")
            print(f" current q: {player_object._current_q_position}")


            # if a player was won the game:
            if player_object._current_state == "won and finished game":
                self.skipping_turn()

            else:
                previous_turn = turn
                # print(f"previous turn: {previous_turn}")
                # print("going to move_token")
                self.move_token(self.get_player_by_position(position), "p", move)

                # if kicking is needed:
                self.kicking(player_object)
        return
            # no "return" statement, otherwise the code will stop after only one turn.
            # print(f" Turn CHECK: {self._player_records}")
        # print("NO MORE TURNS")

    def skipping_turn(self):
        """
        This method will be used in multiple cases:
        Player has finished but excess turns are given.
        """
        return

    def token_in(self, player_object, token_name):
        """
        This method is set to trigger if a token is in 'E'
        """
        # if both tokens are done - winner:
        if self._player_records[player_object][1] == 57 and self._player_records[player_object][2] == 57:
            player_object._current_state = "won and finished game"
            self._player_records[player_object][3] = player_object._current_state
            new_step = 57
            # print("TOKEN IN")
            new_location = player_object.get_space_name(new_step)
            self.update_everything(player_object, "both", new_step, new_location)
            # print(self._player_records)
            return

        # if token p is done:
        elif token_name == "p":
            if self._player_records[player_object][1] == 57:
                # self._player_records[player_object][4] = "E"
                new_step = 57
                new_location = player_object.get_space_name(new_step)
                self.update_everything(player_object, "p", new_step, new_location)
                token_name = "q"
                # the only available token
                # print(f" NEW DICT: {self._player_records}")
                return
                # TODO: check this later

        # if token q is done:
        elif token_name == "q":
            if self._player_records[player_object][2] == 57:
                new_step = 57
                new_location = player_object.get_space_name(new_step)
                self.update_everything(player_object, "q", new_step, new_location)
                token_name = "p"
                # now the only available token
                return

        # if no tokens are done:
        else:
            return  # just return

    def kicking(self, player_object):
        """
        This method is to kick out other opponent tokens at the end of the turn:
        """
        # kicking out opponents:
        # print("KICKING")

        player_p_space = self._player_records[player_object][4]
        player_q_space = self._player_records[player_object][5]

        for other_player in self._player_records:
            # making sure they're not the same player:
            if self._player_records[other_player][0] != self._player_records[player_object][0]:
                opponent_p = self._player_records[other_player][4]
                opponent_q = self._player_records[other_player][5]


                # if player's token p land on the same space as other player's token, kick other player.
                if player_p_space != "H" or player_p_space != "R":
                    if opponent_p == player_p_space or opponent_q == player_p_space:
                        new_step = "H"
                        new_location = other_player.get_space_name(new_step)
                        # if opponent is stacked:
                        if self._player_records[other_player][4] == self._player_records[other_player][5]:
                            token_name = "both"
                            self.update_everything(other_player, token_name, new_step, new_location)
                            return
                        # if not stacked:
                        elif opponent_p == player_p_space:
                            token_name = "p"
                            self.update_everything(other_player, token_name, new_step, new_location)
                            return
                        elif opponent_q == player_p_space:
                            token_name = "q"
                            self.update_everything(other_player, token_name, new_step, new_location)
                            return


                # if player's token q is on the same space, kick other player:
                if player_q_space != "H" or player_q_space != "R":

                    if opponent_p == player_q_space or opponent_q == player_q_space:
                        # print("SHOULD BE IN HERE!")

                        # if opponent stacked:
                        if self._player_records[other_player][4] == self._player_records[other_player][5]:
                            token_name = "both"
                            self.update_everything(other_player, "both", "H", "H")
                            return

                        # if not stacked:
                        elif opponent_q == player_q_space:
                            self.update_everything(other_player, "q", "H", "H")
                            return

                        elif opponent_p == player_q_space:
                            self.update_everything(other_player, "p", "H", "H")
                            return

    def update_everything(self, player_object, token_name, step, location):
        """
        This method is to update all the attributes of the player in a single method instead of writing out a bunch of code for it.
        """
        # step comes in as "H" or "R", not as numbers??

        # print(f" token_name - IN UPDATE EVERYTHING: {token_name}")
        if step == -1:
            step = "H"
        elif step == 0:
            step = "R"

        if token_name == "both":
            # update the p:
            self._player_records[player_object][1] = step
            player_object._current_p_position = step
            self._player_records[player_object][4] = location
            player_object._current_p_location = location

            # update the q:
            self._player_records[player_object][2] = step
            player_object._current_q_position = step
            self._player_records[player_object][5] = location
            player_object._current_q_location = location
            return

        elif token_name == "p":
            self._player_records[player_object][1] = step
            player_object._current_p_position = step
            self._player_records[player_object][4] = location
            player_object._current_p_location = location
            # print(f"self._player_records IN UPDATE EVERYTHING: {self._player_records}")
            return

        elif token_name == "q":
            self._player_records[player_object][2] = step
            player_object._current_p_position = step
            self._player_records[player_object][5] = location
            player_object._current_p_location = location

            # print(f"self._player_records IN UPDATE EVERYTHING: {self._player_records}")
            return


