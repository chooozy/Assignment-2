# NAME: Cameron Chen
# EMAIL: camerm3@uci.edu
# STUDENT ID: 49753193

'''Core Game Logic for Dr. Mario Inspired Game: Split into 3 Classes: Faller, Field, Virus'''

def format_cell(content: str) -> str:
    return content[:3].ljust(3)

class Faller:
   def __init__(self, left_color, right_color, row=0, left_col=None, right_col=None):
       self.left_color = left_color
       self.right_color = right_color
       self.row = row 
       self.left_col = left_col 
       self.right_col = right_col
       self.state = 'falling' 
       self.rotation_state = 0 
  
   def move_down(self):
       self.row += 1
  
   def move_left(self):
       if self.rotation_state in [0, 2]: 
           self.left_col -= 1
           self.right_col -= 1
       else: 
           self.left_col -= 1
           self.right_col = self.left_col
      
   def move_right(self):
       if self.rotation_state in [0, 2]: 
           self.left_col += 1
           self.right_col += 1
       else: 
           self.left_col += 1
           self.right_col = self.left_col


   def rotate_clockwise(self):
    if self.rotation_state in [1, 3]:
        right_col = self.left_col + 1
        if right_col < self.right_col:
            self.right_col = right_col

    elif self.rotation_state in [0, 2]:
        pass 

    new_state = (self.rotation_state + 1) % 4

    if self.rotation_state in [1, 3]:
        right_col = self.left_col + 1
        if right_col >= self.field.columns or not self.field.is_field_empty_at(self.row, right_col):
            if self.left_col - 1 >= 0 and self.field.is_field_empty_at(self.row, self.left_col - 1):
                self.left_col -= 1
                self.right_col = self.left_col + 1
                self.rotation_state = new_state
                return
            else:
                return  
        else:
            self.right_col = right_col
            self.rotation_state = new_state
            return

#no wallkick needed
    if new_state == 0:
        self.right_col = self.left_col + 1
    elif new_state == 1:
        self.right_col = self.left_col
    elif new_state == 2:
        self.right_col = self.left_col + 1
    elif new_state == 3:
        self.right_col = self.left_col

    self.rotation_state = new_state


   def rotate_counterclockwise(self):
       self.rotation_state = (self.rotation_state - 1) % 4
      
       if self.rotation_state == 0: 
           self.right_col = self.left_col + 1
       elif self.rotation_state == 1: 
           self.right_col = self.left_col
       elif self.rotation_state == 2: 
           self.right_col = self.left_col + 1
       elif self.rotation_state == 3: 
           self.right_col = self.left_col

   def land(self):
       self.state = 'landed'

   def freeze(self):
       self.state = 'frozen'

   def is_frozen(self):
       return self.state == 'frozen'

class Virus:
   def __init__(self, color, row, col):
       self.color = color  
       self.row = row
       self.col = col
       self.matched = False  

   def get_display(self):
       
        if self.matched:
            return f"*{self.color.lower()}*"
        else:
            return f" {self.color} "

class Field:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        
        self.field = [['   ' for _ in range(columns)] for _ in range(rows)]
        self.faller = None
        self.viruses = []  

    def is_field_empty_at(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.columns:
            return self.field[row][col] == "   "
        return False
        
    def print_field(self, suppress_level_cleared=False):
        
        for r in range(self.rows):
            row_str = "|"
            for c in range(self.columns):
                cell_content = self.field[r][c]
                row_str += cell_content
                    
            row_str += "|"
            print(row_str)
        
        print(" " + "-" * (self.columns * 3) + " ")
        
        if not suppress_level_cleared and not self._has_viruses():
            print("LEVEL CLEARED")
            
    def _has_viruses(self):
        return len(self.viruses) > 0
    
    def add_virus(self, row, col, color):
        if 0 <= row < self.rows and 0 <= col < self.columns:
            if self.is_field_empty_at(row, col):
                virus = Virus(color, row, col)
                self.viruses.append(virus)
                self.field[row][col] = virus.get_display()
                return self.process_matches()
        return None

    def calculate_mid_column(self):
        if self.columns == 4:
            return 1 
        else:
            if self.columns % 2 == 1:  
                return self.columns // 2
            else:  
                return self.columns // 2 - 1

    def check_game_over_condition(self):
        mid_col = self.calculate_mid_column()
        
        left_col = mid_col
        right_col = mid_col + 1
        
        if (1 < self.rows and 
            (not self.is_field_empty_at(1, left_col) or 
             not self.is_field_empty_at(1, right_col))):
            return True
            
        return False
        
    def add_faller(self, left_color, right_color):
        mid_col = self.calculate_mid_column()
        row = 0
        left_col = mid_col
        right_col = mid_col + 1
        
        if self.check_game_over_condition():
            return 'GAME_OVER'
        
        self.faller = Faller(left_color, right_color, row=row, left_col=left_col, right_col=right_col)
        
        next_row = self.faller.row + 1
        if next_row >= self.rows or not self.is_field_empty_at(next_row, self.faller.left_col) or not self.is_field_empty_at(next_row, self.faller.right_col):
            self.faller.land()
        
        self.draw_faller()
        return None  
    
    def check_and_update_faller_state(self):
        if self.faller is None:
            return
            
        next_row = self.faller.row + 1
        can_move_down = True
        
        if self.faller.rotation_state in [0, 2]:  # Horizontal
            if next_row >= self.rows:
                can_move_down = False
            elif not self.is_field_empty_at(next_row, self.faller.left_col) or not self.is_field_empty_at(next_row, self.faller.right_col):
                can_move_down = False
        else:  # Vertical 
            if next_row >= self.rows:
                can_move_down = False
            elif not self.is_field_empty_at(next_row, self.faller.left_col):
                can_move_down = False
                
        if can_move_down:
            self.faller.state = 'falling'
        elif self.faller.state == 'falling':
            self.faller.land()
            
    def handle_rotation(self, direction):
        if self.faller is None or self.faller.state == 'frozen':
            return False
            
        if not self.can_rotate():
            return False
            
        self.clear_faller()
        
        if direction == 'clockwise':
            self.faller.rotate_clockwise()
        else:  # Counter
            self.faller.rotate_counterclockwise()
        
      
        self.check_and_update_faller_state()
        
        self.draw_faller()
        return True
        
    def draw_faller(self):  
        if self.faller is None:
            return
            
        self.clear_faller()
        row = self.faller.row
        left_col = self.faller.left_col
        right_col = self.faller.right_col
        state = self.faller.state
        rotation_state = self.faller.rotation_state
        
        if 0 <= row < self.rows:
            if rotation_state in [0, 2]:  # Horizontal 
                if 0 <= left_col < self.columns and 0 <= right_col < self.columns:
                    if state == 'falling':

                        if rotation_state == 0:  # Normal 
                            self.field[row][left_col] = f"[{self.faller.left_color}--"
                            self.field[row][right_col] = f"{self.faller.right_color}]"
                        else:  # Flipped 
                            self.field[row][left_col] = f"[{self.faller.right_color}--"
                            self.field[row][right_col] = f"{self.faller.left_color}]"
                            
                    elif state == 'landed':

                        if rotation_state == 0:  # Normal 
                            self.field[row][left_col] = f"|{self.faller.left_color}--"
                            self.field[row][right_col] = f"{self.faller.right_color}|"
                        else:  # Flipped 
                            self.field[row][left_col] = f"|{self.faller.right_color}--"
                            self.field[row][right_col] = f"{self.faller.left_color}|"
                            
                    else:  # Frozen 
                        if rotation_state == 0:  # Normal 
                            self.field[row][left_col] = f" {self.faller.left_color}--"
                            self.field[row][right_col] = f"{self.faller.right_color} "
                        else:  # Flipped 
                            self.field[row][left_col] = f" {self.faller.right_color}--"
                            self.field[row][right_col] = f"{self.faller.left_color} "
            
            else:  # Vertical faller
                if 0 <= left_col < self.columns:
                    if 0 <= row - 1 < self.rows:
                        if state == 'falling':
                           
                            if rotation_state == 1:  
                                self.field[row - 1][left_col] = f"[{self.faller.left_color}]"
                                self.field[row][left_col] = f"[{self.faller.right_color}]"
                            else:  
                                self.field[row - 1][left_col] = f"[{self.faller.right_color}]"
                                self.field[row][left_col] = f"[{self.faller.left_color}]"
                                
                        elif state == 'landed':
                            if rotation_state == 1: 
                                self.field[row - 1][left_col] = f"|{self.faller.left_color}|"
                                self.field[row][left_col] = f"|{self.faller.right_color}|"
                            else:  
                                self.field[row - 1][left_col] = f"|{self.faller.right_color}|"
                                self.field[row][left_col] = f"|{self.faller.left_color}|"
                        
                        else:  
                            if rotation_state == 1:  
                                self.field[row - 1][left_col] = f" {self.faller.left_color} "
                                self.field[row][left_col] = f" {self.faller.right_color} "
                            else: 
                                self.field[row - 1][left_col] = f" {self.faller.right_color} "
                                self.field[row][left_col] = f" {self.faller.left_color} "
                    else:
                        if state == 'falling':
                            if rotation_state == 1:
                                self.field[row][left_col] = f"[{self.faller.right_color}]"
                            else:
                                self.field[row][left_col] = f"[{self.faller.left_color}]"
                        elif state == 'landed':
                            if rotation_state == 1:
                                self.field[row][left_col] = f"|{self.faller.right_color}|"
                            else:
                                self.field[row][left_col] = f"|{self.faller.left_color}|"
                        else:  
                            if rotation_state == 1:
                                self.field[row][left_col] = f" {self.faller.right_color} "
                            else:
                                self.field[row][left_col] = f" {self.faller.left_color} "
        
    def clear_faller(self):
        if self.faller is None:
            return
            
        row = self.faller.row
        left_col = self.faller.left_col
        right_col = self.faller.right_col
        rotation_state = self.faller.rotation_state
        
        if rotation_state in [0, 2]:  # Horizontal
            if 0 <= row < self.rows:
                if 0 <= left_col < self.columns:
                    self.field[row][left_col] = "   "
                    
                if 0 <= right_col < self.columns:
                    self.field[row][right_col] = "   "
        else:  # Vertical
            if 0 <= row - 1 < self.rows and 0 <= left_col < self.columns:
                self.field[row - 1][left_col] = "   "
                
            if 0 <= row < self.rows and 0 <= left_col < self.columns:
                self.field[row][left_col] = "   "
                
    def advance_time(self):
        if self.faller is None:
            return
            
        self.clear_faller()
        next_row = self.faller.row + 1
        
        can_move_down = True
        if self.faller.rotation_state in [0, 2]:  # Horizontal
        
            if next_row >= self.rows:
                can_move_down = False
            elif not self.is_field_empty_at(next_row, self.faller.left_col) or not self.is_field_empty_at(next_row, self.faller.right_col):
                can_move_down = False
        else:  # Vertical
            if next_row >= self.rows:
                can_move_down = False
            elif not self.is_field_empty_at(next_row, self.faller.left_col):
                can_move_down = False
                
        if not can_move_down:
            if self.faller.state == 'falling':
                self.faller.land()
            elif self.faller.state == 'landed':
                self.faller.freeze()
                self.commit_faller()
                return
        else:
            self.faller.state = 'falling'
            self.faller.move_down()
            
            next_row = self.faller.row + 1
            can_move_further = True
            
            if self.faller.rotation_state in [0, 2]:  # Horizontal
                if next_row >= self.rows or not self.is_field_empty_at(next_row, self.faller.left_col) or not self.is_field_empty_at(next_row, self.faller.right_col):
                    can_move_further = False
            else:  # Vertical
                if next_row >= self.rows or not self.is_field_empty_at(next_row, self.faller.left_col):
                    can_move_further = False
                    
            if not can_move_further:
                self.faller.land()
            
        self.draw_faller()
        
    def commit_faller(self):
        if self.faller is None:
            return
        row = self.faller.row
        left_col = self.faller.left_col
        right_col = self.faller.right_col
        rotation_state = self.faller.rotation_state
        
        if rotation_state in [0, 2]:  # Horizontal
            if 0 <= row < self.rows:
                if 0 <= left_col < self.columns and 0 <= right_col < self.columns:
                    if rotation_state == 0:  # Normal 
                        self.field[row][left_col] = f" {self.faller.left_color}--"
                        self.field[row][right_col] = f"{self.faller.right_color} "
                    else:  # Flipped 
                        self.field[row][left_col] = f" {self.faller.right_color}--"
                        self.field[row][right_col] = f"{self.faller.left_color} "
        else:  # Vertical
            if 0 <= row - 1 < self.rows and 0 <= row < self.rows and 0 <= left_col < self.columns:
                if rotation_state == 1: 
                    self.field[row - 1][left_col] = f" {self.faller.left_color} "
                    self.field[row][left_col] = f" {self.faller.right_color} "
                else:  
                    self.field[row - 1][left_col] = f" {self.faller.right_color} "
                    self.field[row][left_col] = f" {self.faller.left_color} "
                
        self.faller = None
        
        self.process_matches()
    
    def add_content(self, row, col, char):
        if 0 <= row < self.rows and 0 <= col < self.columns:
            if char.islower():  
                virus = Virus(char, row, col)
                self.viruses.append(virus)
                self.field[row][col] = f" {char} "
            else: 
                self.field[row][col] = f" {char} "
    
    def add_horizontal_pair(self, row, col, left_char, right_char):
        if (0 <= row < self.rows and 
            0 <= col < self.columns and 
            0 <= col + 1 < self.columns):
            self.field[row][col] = f" {left_char}--"
            self.field[row][col + 1] = f"{right_char} "
    
    def get_cell_color(self, r, c):
        if r < 0 or r >= self.rows or c < 0 or c >= self.columns:
            return None
            
        cell = self.field[r][c]
        
        for virus in self.viruses:
            if virus.row == r and virus.col == c:
                return virus.color  
        for char in cell:
            if char.lower() in 'rby':
                return char  
                
        return None
        
    def check_matches(self):
        
        matches_found = False
        matched_cells = set()  
        for r in range(self.rows):
            current_color_lower = None
            current_run = []
            
            for c in range(self.columns):
                cell_color = self.get_cell_color(r, c)
                
                if cell_color and '*' not in self.field[r][c]: 
                    cell_color_lower = cell_color.lower() 
                    
                    if current_color_lower is None:
                        current_color_lower = cell_color_lower
                        current_run = [(r, c)]
                    elif cell_color_lower == current_color_lower:
                        current_run.append((r, c))
                    else:
                        if len(current_run) >= 4:
                            matched_cells.update(current_run)
                            matches_found = True
                        
                        current_color_lower = cell_color_lower
                        current_run = [(r, c)]
                else:
                    if current_color_lower is not None and len(current_run) >= 4:
                        matched_cells.update(current_run)
                        matches_found = True
                    
                    current_color_lower = None
                    current_run = []
            
            if current_color_lower is not None and len(current_run) >= 4:
                matched_cells.update(current_run)
                matches_found = True
        
        for c in range(self.columns):
            current_color_lower = None
            current_run = []
            
            for r in range(self.rows):
                cell_color = self.get_cell_color(r, c)
                
                if cell_color and '*' not in self.field[r][c]: 
                    cell_color_lower = cell_color.lower() 
                    
                    if current_color_lower is None:
                        current_color_lower = cell_color_lower
                        current_run = [(r, c)]
                    elif cell_color_lower == current_color_lower:
                        current_run.append((r, c))
                    else:
                        if len(current_run) >= 4:
                            matched_cells.update(current_run)
                            matches_found = True
                        
                        current_color_lower = cell_color_lower
                        current_run = [(r, c)]
                else:
                    if current_color_lower is not None and len(current_run) >= 4:
                        matched_cells.update(current_run)
                        matches_found = True
                    
                    current_color_lower = None
                    current_run = []
            
            if current_color_lower is not None and len(current_run) >= 4:
                matched_cells.update(current_run)
                matches_found = True
        
        for r, c in matched_cells:
            self.mark_matched(r, c)
        
        return matches_found

    def mark_matched(self, row, col):
        cell_content = self.field[row][col]
        cell_color = self.get_cell_color(row, col)
        if not cell_color:
            return
            
        for virus in self.viruses:
            if virus.row == row and virus.col == col:
                virus.matched = True
                self.field[row][col] = f"*{cell_color}*"
                return

        if '--' in cell_content:  
            right_color = self.get_cell_color(row, col + 1)
            self.field[row][col] = f"*{cell_color}*"
            if right_color and col + 1 < self.columns:
                self.field[row][col + 1] = f"-{right_color} "  
        elif col > 0 and '--' in self.field[row][col-1]:  
            self.field[row][col] = f"*{cell_color}*"
        else: 
            self.field[row][col] = f"*{cell_color}*"

    def clear_matches(self):
        cells_cleared = False
        matched_positions = set()
    
        for r in range(self.rows):
            for c in range(self.columns):
                if '*' in self.field[r][c]:
                    matched_positions.add((r, c))
                    self.field[r][c] = "   "
                    cells_cleared = True
    
        for r in range(self.rows):
            for c in range(self.columns):
                current_cell = self.field[r][c]
                if '-' in current_cell:
                    color = self.get_cell_color(r, c)
                    if ((r, c-1) in matched_positions or 
                        (r, c+1) in matched_positions):
                        self.field[r][c] = f" {color} "
    
        return cells_cleared
    
    def apply_gravity(self):
        
        moved = False
        for r in range(self.rows - 2, -1, -1):
            for c in range(self.columns):
                # skip if cell  empty
                if self.field[r][c] == "   ":
                    continue
                is_virus = any(v.row == r and v.col == c for v in self.viruses)
                if is_virus:
                    continue
                if r + 1 < self.rows and self.field[r + 1][c] == "   ":
                    self.field[r + 1][c] = self.field[r][c]
                    self.field[r][c] = "   "
                    moved = True
    
        return moved

    def process_matches(self, input_func=None):
        get_input = input_func if input_func is not None else input
        matches_found = self.check_matches()
        if not matches_found:
            return None
        while True:
            self.print_field()
            
            command = get_input()
            if command == 'Q':  
                return 'Q'
            self.clear_matches()
            while True:
                moved = self.apply_gravity()
                if not moved:
                    break
                self.print_field()
                command = get_input()
                if command == 'Q':
                    return 'Q'   
            new_matches = self.check_matches()
            if not new_matches:
                break
        return None

    def can_move_left(self):
        if self.faller is None:
            return False
        left_col = self.faller.left_col - 1
        if left_col < 0:
            return False
        row = self.faller.row
        
        if self.faller.rotation_state in [0, 2]:  # Horizontal
            return self.is_field_empty_at(row, left_col)
        else:  # Vertical
            return (self.is_field_empty_at(row - 1, left_col) and 
                    self.is_field_empty_at(row, left_col))
                    
    def can_move_right(self):
        if self.faller is None:
            return False
            
        if self.faller.rotation_state in [0, 2]:  # Horizontal
            right_col = self.faller.right_col + 1
            
            if right_col >= self.columns:
                return False
                
            return self.is_field_empty_at(self.faller.row, right_col)
        else:  # Vertical
            right_col = self.faller.left_col + 1
            
            if right_col >= self.columns:
                return False
                
            return (self.is_field_empty_at(self.faller.row - 1, right_col) and 
                    self.is_field_empty_at(self.faller.row, right_col))
                    
    def can_rotate(self):
        
        if self.faller is None:
            return False
            
        row = self.faller.row
        left_col = self.faller.left_col
        rotation_state = self.faller.rotation_state
        
        if rotation_state in [0, 2]:
            return 0 <= row - 1 < self.rows and self.is_field_empty_at(row - 1, left_col)

        else:  
            right_col = left_col + 1
            return 0 <= right_col < self.columns and self.is_field_empty_at(row, right_col)
        