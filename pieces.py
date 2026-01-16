import numpy as np

class Piece:
    """
    Base class for pieces on the board. 
    
    A piece holds a reference to the board, its color and its currently located cell.
    In this class, you need to implement two methods, the "evaluate()" method and the "get_valid_cells()" method.
    """
    def __init__(self, board, white):
        """
        Constructor for a piece based on provided parameters

        :param board: Reference to the board this piece is placed on
        :type board: :ref:class:`board`
        """
        self.board = board
        self.white = white
        self.cell = None



    def is_white(self):
        """
        Returns whether this piece is white

        :return: True if the piece white, False otherwise
        """
        return self.white

    def can_enter_cell(self, cell):
        """
        Shortcut method to see if a cell on the board can be entered.
        Simply calls :py:meth:`piece_can_enter_cell <board.Board.piece_can_enter_cell>` from the current board class.

        :param cell: The cell to check for. Must be a unpackable (row, col) type.
        :return: True if the provided cell can enter, False otherwise
        """
        return self.board.piece_can_enter_cell(self, cell)

    def can_hit_on_cell(self, cell):
        """
        Shortcut method to see if this piece can hit another piece on a cell.
        Simply calls :py:meth:`piece_can_hit_on_cell <board.Board.piece_can_hit_on_cell>` from the current board class.

        :param cell: The cell to check for. Must be a unpackable (row, col) type.
        :return: True if the piece can hit on the provided cell, False otherwise
        """
        return self.board.piece_can_hit_on_cell(self, cell)

    def evaluate(self):
        """
        **TODO** Implement a meaningful numerical evaluation of this piece on the board.
        This evaluation happens independent of the color as later, values for white pieces will be added and values for black pieces will be substracted. 
        
        **HINT** Making this method *independent* of the pieces color is crucial to get a *symmetric* evaluation metric in the end.
         
        - The pure existance of this piece alone is worth some points. This will create an effect where the player with more pieces on the board will, in sum, get the most points assigned. 
        - Think of other criteria that would make this piece more valuable, e.g. movability or whether this piece can hit other pieces. Value them accordingly.
        
        :return: Return numerical score between -infinity and +infinity. Greater values indicate better evaluation result (more favorable).
        """
        # TODO: Implement

        # Add a value to the given piece

        if isinstance(self, Pawn):
            value = 1

        elif isinstance(self, Rook):
            value = 5

        elif isinstance(self, Knight):
            value = 3
    
        elif isinstance(self, Bishop):
            value = 3

        elif isinstance(self, Queen):
            value = 10

        elif isinstance(self, King):
            value = 9999999
        
        return value 

    def get_valid_cells(self):
        """
        **TODO** Return a list of **valid** cells this piece can move into. 
        
        A cell is valid if 
          a) it is **reachable**. That is what the :py:meth:`get_reachable_cells` method is for and
          b) after a move into this cell the own king is not (or no longer) in check.

        **HINT**: Use the :py:meth:`get_reachable_cells` method of this piece to receive a list of reachable cells.
        Iterate through all of them and temporarily place the piece on this cell. Then check whether your own King (same color)
        is in check. Use the :py:meth:`is_king_check_cached` method to test for checks. If there is no check after this move, add
        this cell to the list of valid cells. After every move, restore the original board configuration. 
        
        To temporarily move a piece into a new cell, first store its old position (self.cell) in a local variable. 
        The target cell might have another piece already placed on it. 
        Use :py:meth:`get_cell <board.BoardBase.get_cell>` to retrieve that piece (or None if there was none) and store it as well. 
        Then call :py:meth:`set_cell <board.BoardBase.set_cell>` to place this piece on the target cell and test for any checks given. 
        After this, restore the original configuration by placing this piece back into its old position (call :py:meth:`set_cell <board.BoardBase.set_cell>` again)
        and place the previous piece also back into its cell. 
        
        :return: Return True 
        """
        # TODO: Implement

        # Create an emtpy list to fill it later
        valid_cells = []

        # Get every cell a piece can move into
        reachable_cells = self.get_reachable_cells()

        # Save the intial postion, to return the piece back later on
        initial_position = self.cell 
        
        # Iterate over every possible move
        for potential_move in reachable_cells:
            # Saves the content of the cell we move the piece in to return it back later on
            target_cell_content = self.board.get_cell(potential_move)
            # Puts the piece in the reachable cell to check if the own king is checked
            self.board.set_cell(potential_move, self)
            
            # If the own king is not checked the move is valid
            if not self.board.is_king_check_cached(self.white):
                # Add the move to the list of valid_cells
                valid_cells.append(potential_move)

            # return the board to its original state
            self.board.set_cell(initial_position, self)
            self.board.set_cell(potential_move, target_cell_content)
        
        # Return the list cells the piece can move into without the own king being in check
        return valid_cells


class Pawn(Piece):  # Bauer
    def __init__(self, board, white):
        super().__init__(board, white)

    def get_reachable_cells(self):
        """
        **TODO** Implement the movability mechanik for `pawns <https://de.wikipedia.org/wiki/Bauer_(Schach)>`_. 

        **NOTE**: Here you do not yet need to consider whether your own King would become checked after a move. This will be taken care of by
        the :py:meth:`is_king_check <board.Board.is_king_check>` and :py:meth:`get_valid_cells <pieces.Piece.get_valid_cells>` methods.

        **HINT**: Pawns can move only forward (towards the opposing army). Depening of whether this piece is black of white, this means pawn
        can move only to higher or lower rows. Normally a pawn can only move one cell forward as long as the target cell is not occupied by any other piece. 
        If the pawn is still on its starting row, it can also dash forward and move two pieces at once (as long as the path to that cell is not blocked).
        Pawns can only hit diagonally, meaning they can hit other pieces only the are one cell forward left or one cell forward right from them. 

        You can call :py:meth:`cell_is_valid_and_empty <board.Board.cell_is_valid_and_empty>`, 
        :py:meth:`can_hit_on_cell <pieces.Piece.can_hit_on_cell>` and :py:meth:`can_enter_cell <pieces.Piece.can_enter_cell>` 
        to check for necessary conditions to implement the pawn movability mechanics. 

        **NOTE**: For all you deep chess experts: Hitting `en passant <https://de.wikipedia.org/wiki/En_passant>`_ does not need to be implemented.
        
        :return: A list of reachable cells this pawn could move into.
        """
        # TODO: Implement a method that returns all cells this piece can enter in its next move

        # Save the direction and home row for every pawn (if piece is black self.white=False)
        direction, home_row = (1, 1) if self.white else (-1, 6)

        # Empty list which is getting returned at the end
        reachable_cells = []
        # Unpack the cell the pawn is in
        row, col = self.cell

        # If the pawn is on it's home row it can either move one or two steps in the direction (one and two steps depends on the given color of the piece (- and + direction))
        one_step = row + direction, col
        two_step = row + direction*2,col

        # Checks if one step is valid and the cell is empty
        if self.board.cell_is_valid_and_empty((one_step)):
            # If so appends the move to the list
            reachable_cells.append((one_step))

            # Only needs to check if two steps are valid if one step is valid
            # Two steps are only possible if the piece is on its home row
            if row == home_row and self.board.cell_is_valid_and_empty(two_step):
                # Adds the move (cell) to the list
                reachable_cells.append(two_step)
        
        # creates a list of two possible hit options (tuples)
        # Can only hit in the direction it can move and diagonally, which is why we add + and - 1 to the cell
        hit_moves = [(row + direction, col + 1), (row + direction, col - 1)]

        # Iterates throught the two hit options
        for i, j in hit_moves:
            # tuple out of the list
            hit_cell = (i, j)
            # Checks if pawn can hit on the cell (opposing color)
            if self.board.piece_can_hit_on_cell(self, hit_cell):
                # Adds the move to the reachable cells list
                reachable_cells.append(hit_cell)

        # returns list with reachable cells
        return reachable_cells
        

class Rook(Piece):  # Turm
    def __init__(self, board, white):
        super().__init__(board, white)

    def get_reachable_cells(self):
        """
        **TODO** Implement the movability mechanic for `rooks <https://de.wikipedia.org/wiki/Turm_(Schach)>`_. 

        **NOTE**: Here you do not yet need to consider whether your own King would become checked after a move. This will be taken care of by
        the :py:meth:`is_king_check <board.Board.is_king_check>` and :py:meth:`get_valid_cells <pieces.Piece.get_valid_cells>` methods.

        **HINT**: Rooks can move only horizontally or vertically. They can move an arbitrary amount of cells until blocked by an own piece
        or an opposing piece (which they could hit and then being stopped).

        You can call :py:meth:`cell_is_valid_and_empty <board.Board.cell_is_valid_and_empty>`, 
        :py:meth:`can_hit_on_cell <pieces.Piece.can_hit_on_cell>` and :py:meth:`can_enter_cell <pieces.Piece.can_enter_cell>` 
        to check for necessary conditions to implement the rook movability mechanics. 

        :return: A list of reachable cells this rook could move into.
        """
        # TODO: Implement a method that returns all cells this piece can enter in its next move       
    
        # List with possible moves
        reachable_cells = []

        # List of directions the rook can move
        direction = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        # Unpack tuple cell to row and col
        row, col = self.cell

        # Iterate through every possible direction
        # Unpack the tuple directions
        for i, j in direction:
            # Create a new cell based on the cell the piece is placed on to check possible cells the rook could move into
            new_cell = (row + i, col + j)
            
            # Loop through every cell that is valid and empty, based on the possible cells the rook could move into
            while self.board.cell_is_valid_and_empty(new_cell):
                # If cell is valid and empty it's getting added to the reachable_cells list
                reachable_cells.append(new_cell)
                # Unpack the new cell into row and col
                new_row, new_col = new_cell
                # Based on the new cell we created with the direction the rook can move into, we create a new cell which checks another cell in the direction
                new_cell = (new_row + i, new_col + j)
            
            # Checks if piece can hit or move into the new cell
            if self.board.piece_can_hit_on_cell(self, new_cell):
                # If so the new cell is getting added to the reachable cells list
                reachable_cells.append(new_cell)

        # returns list with reachable cells
        return reachable_cells



class Knight(Piece):  # Springer
    def __init__(self, board, white):
        super().__init__(board, white)

    def get_reachable_cells(self):
        """
        **TODO** Implement the movability mechanic for `knights <https://de.wikipedia.org/wiki/Springer_(Schach)>`_. 

        **NOTE**: Here you do not yet need to consider whether your own King would become checked after a move. This will be taken care of by
        the :py:meth:`is_king_check <board.Board.is_king_check>` and :py:meth:`get_valid_cells <pieces.Piece.get_valid_cells>` methods.

        **HINT**: Knights can move in a special pattern. They can move two rows up or down and then one column left or right. Alternatively, they can
        move one row up or down and then two columns left or right. They are not blocked by pieces in between. 

        You can call :py:meth:`cell_is_valid_and_empty <board.Board.cell_is_valid_and_empty>`, 
        :py:meth:`can_hit_on_cell <pieces.Piece.can_hit_on_cell>` and :py:meth:`can_enter_cell <pieces.Piece.can_enter_cell>` 
        to check for necessary conditions to implement the rook movability mechanics. 

        :return: A list of reachable cells this knight could move into.
        """
        # TODO: Implement a method that returns all cells this piece can enter in its next move

        # List with possible moves
        reachable_cells = []

        # List of directions the knight can move
        directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]

        # Unpack tuple cell to row and col
        row, col = self.cell

        # Iterate through every possible direction
        # Unpack the tuple possible moves
        for i, j in directions:
            # Create a new cell based on the cell the piece is placed on to check possible cells the knight could move into
            new_cell = (row + i, col + j)
            # The knight can enter if the cell is valid and empty or and opposing piece is placed on
            if self.board.piece_can_enter_cell(self, new_cell):
                # If it's the case the new cell is added to the reachable cells list
                reachable_cells.append(new_cell)
        
        # returns list with reachable cells
        return reachable_cells


class Bishop(Piece):  # Läufer
    def __init__(self, board, white):
        super().__init__(board, white)

    def get_reachable_cells(self):
        """
        **TODO** Implement the movability mechanic for `bishop <https://de.wikipedia.org/wiki/L%C3%A4ufer_(Schach)>`_. 

        **NOTE**: Here you do not yet need to consider whether your own King would become checked after a move. This will be taken care of by
        the :py:meth:`is_king_check <board.Board.is_king_check>` and :py:meth:`get_valid_cells <pieces.Piece.get_valid_cells>` methods.

        **HINT**: Bishops can move diagonally an arbitrary amount of cells until blocked.

        You can call :py:meth:`cell_is_valid_and_empty <board.Board.cell_is_valid_and_empty>`, 
        :py:meth:`can_hit_on_cell <pieces.Piece.can_hit_on_cell>` and :py:meth:`can_enter_cell <pieces.Piece.can_enter_cell>` 
        to check for necessary conditions to implement the rook movability mechanics. 

        :return: A list of reachable cells this bishop could move into.
        """
        # TODO: Implement a method that returns all cells this piece can enter in its next move
    
        # List with possible moves
        reachable_cells = []

        # List of directions the bishop can move
        directions = [(1, -1), (1, 1), (-1, 1), (-1, -1)]

        # Unpack the tuple cell to row and col
        row, col = self.cell

        # Iterate through every possible direction
        # Unpack the tuple directions
        for i, j in directions:
            # Unpack the new cell into row and col
            new_cell = (row + i, col + j)

            # Loop through every cell that is valid and empty, based on the possible cells the bishop could move into
            while self.can_enter_cell(new_cell):
                # If cell is valid and empty it's getting added to the reachable_cells list
                reachable_cells.append(new_cell)
                # Unpack the new cell into row and col
                new_row, new_col = new_cell
                # Based on the new cell we created with the direction the rook can move into, we create a new cell which checks another cell in the direction
                new_cell = (new_row + i, new_col + j)
            
            # Loop stops if it finds cell which isn't empty, now cheks if piece is of the opposing color (we can hit)
            if self.board.piece_can_hit_on_cell(self, new_cell):
                # if so append to the list
                reachable_cells.append(new_cell)
        
        # returns list with reachable cells
        return reachable_cells



class Queen(Piece):  # Königin
    def __init__(self, board, white):
        super().__init__(board, white)

    def get_reachable_cells(self):
        """
        **TODO** Implement the movability mechanic for the `queen <https://de.wikipedia.org/wiki/Dame_(Schach)>`_. 

        **NOTE**: Here you do not yet need to consider whether your own King would become checked after a move. This will be taken care of by
        the :py:meth:`is_king_check <board.Board.is_king_check>` and :py:meth:`get_valid_cells <pieces.Piece.get_valid_cells>` methods.

        **HINT**: Queens can move horizontally, vertically and diagonally an arbitrary amount of cells until blocked. They combine the movability
        of rooks and bishops. 

        You can call :py:meth:`cell_is_valid_and_empty <board.Board.cell_is_valid_and_empty>`, 
        :py:meth:`can_hit_on_cell <pieces.Piece.can_hit_on_cell>` and :py:meth:`can_enter_cell <pieces.Piece.can_enter_cell>` 
        to check for necessary conditions to implement the rook movability mechanics. 

        :return: A list of reachable cells this queen could move into.
        """
        # TODO: Implement a method that returns all cells this piece can enter in its next move

        # List with possible moves
        reachable_cells = []

        # List of directions the Queen can move
        directions = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, -1), (1, 1), (-1, 1), (-1, -1)]

        # Unpack the tuple cell to row and col
        row, col = self.cell

        # Iterate through every possible direction
        # Unpack the tuple directions
        for i, j in directions:
            # Unpack the new cell into row and col
            new_cell = (row + i, col + j)
            # Loop through every cell that is valid and empty, based on the possible cells the Queen could move into
            while self.board.cell_is_valid_and_empty(new_cell):
                # If cell is valid and empty it's getting added to the reachable_cells list
                reachable_cells.append(new_cell)
                # Unpack the new cell into row and col
                new_row, new_col = new_cell
                # Based on the new cell we created with the direction the rook can move into, we create a new cell which checks another cell in the direction
                new_cell = (new_row + i, new_col + j)
            # If cell isn't empty anymore, we need to check if we can hit the piece
            if self.board.piece_can_hit_on_cell(self, new_cell):
                # If so append the cell to the reachable cell
                reachable_cells.append(new_cell)
        
        # returns list with reachable cells
        return reachable_cells


class King(Piece):  # König
    def __init__(self, board, white):
        super().__init__(board, white)

    def get_reachable_cells(self):
        """
        **TODO** Implement the movability mechanic for the `king <https://de.wikipedia.org/wiki/K%C3%B6nig_(Schach)>`_. 

        **NOTE**: Here you do not yet need to consider whether your own King would become checked after a move. This will be taken care of by
        the :py:meth:`is_king_check <board.Board.is_king_check>` and :py:meth:`get_valid_cells <pieces.Piece.get_valid_cells>` methods.

        **HINT**: Kings can move horizontally, vertically and diagonally but only one piece at a time.

        You can call :py:meth:`cell_is_valid_and_empty <board.Board.cell_is_valid_and_empty>`, 
        :py:meth:`can_hit_on_cell <pieces.Piece.can_hit_on_cell>` and :py:meth:`can_enter_cell <pieces.Piece.can_enter_cell>` 
        to check for necessary conditions to implement the rook movability mechanics. 

        :return: A list of reachable cells this king could move into.
        """
        # TODO: Implement a method that returns all cells this piece can enter in its next move

        # List with possible moves
        reachable_cells = []

        # List of directions the King can move
        directions = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, -1), (1, 1), (-1, 1), (-1, -1)]

        # Unpack the tuple cell to row and col
        row, col = self.cell

        # Iterate through every possible direction
        # Unpack the tuple directions
        for i, j in directions:
            # Unpack the new cell into row and col
            new_cell = (row + i, col + j)
            # Checks if cell is valid and empty
            if self.board.cell_is_valid_and_empty(new_cell):
                # If so add it to the list of reachavle cells
                reachable_cells.append(new_cell)
            # If Cell isn't empty we need to check if the piece is of the opposing color
            elif self.board.piece_can_hit_on_cell(self, new_cell):
                # if so, add it to the list
                reachable_cells.append(new_cell)
        
        # returns list with reachable cells
        return reachable_cells
