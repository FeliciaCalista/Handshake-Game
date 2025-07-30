import copy

class Queue:                            # Konsepnya diambil dari proyek kelompok sebelumnya
    def __init__(self):
        self._queue = []

    def push(self, new_data):
        self._queue.append(new_data)

    def pop(self):
        if not self.is_empty():
            return self._queue.pop(0)
        
    def is_empty(self):
        return len(self._queue) == 0


class Pawn:
    def __init__(self, pawn, hand, right_hand, left_hand, up_hand, down_hand, 
                 arm_label, pawn_moves=None, pawn_row=None, pawn_col=None, 
                 arm_path=None, hand_ori_row=None, hand_ori_col=None):
        
        self.pawn = pawn
        self.pawn_row = pawn_row
        self.pawn_col = pawn_col
        self.pawn_moves = pawn_moves
        self.pawn_ori_moves = pawn_moves

        self.arm_label = arm_label
        self.arm_path = arm_path

        self.ori_hand = hand
        self.curr_hand = hand
        self.right_hand = right_hand
        self.left_hand = left_hand
        self.up_hand = up_hand
        self.down_hand = down_hand

        self.hand_ori_row = hand_ori_row
        self.hand_ori_col = hand_ori_col
        self.hand_curr_row = None
        self.hand_curr_col = None

        self.movement_path = [self.curr_hand]
        self.path = None

    def get_ori_hand(self):
        return self.ori_hand
    
    def get_curr_hand(self):
        return self.curr_hand

    def get_hand_label(self):        
        return [self.right_hand, self.left_hand, self.up_hand, self.down_hand]
    
    def get_pawn_label(self):
        return self.pawn
    
    def get_arm_label(self):
        return self.arm_label

    def get_arm_path(self):
        return self.arm_path
    
    def get_movement_path(self):
        return self.movement_path
    
    def get_pawn_coor(self):
        return self.pawn_row, self.pawn_col
    
    def get_hand_coor(self):
        return self.hand_curr_row, self.hand_curr_col
    
    def get_pawn_moves(self):
        return self.pawn_moves
    
    def store_ori_hand_coor(self, row, col):
        self.hand_ori_row = row
        self.hand_ori_col = col
        self.arm_path = [(self.hand_ori_row, self.hand_ori_col)]
        self.path = [(self.hand_ori_row, self.hand_ori_col)]

    def store_curr_hand_coor(self, row, col):
        self.hand_curr_row = row
        self.hand_curr_col = col

    def update_arm_path(self, new_arm_path):
        self.arm_path = new_arm_path

    def store_pawn_coor(self, row, col):
        self.pawn_row = row
        self.pawn_col = col

    def store_pawn_moves(self, moves):
        self.pawn_ori_moves = moves
        self.pawn_moves = moves

    def go_up(self, row, col):
        new_row = row - 1
        return (new_row, col), self.up_hand

    def go_down(self, row, col):
        new_row = row + 1
        return (new_row, col), self.down_hand

    def go_right(self, row, col):
        new_col = col + 1
        return (row, new_col), self.right_hand

    def go_left(self, row, col):
        new_col = col - 1
        return (row, new_col), self.left_hand

    def update_moves(self, row, col):
        if self.arm_path is not None and len(self.arm_path) > 1 and (row, col) == self.arm_path[-2]:
            self.hand_curr_row = row
            self.hand_curr_col = col

            self.pawn_moves += 1
            self.arm_path.pop(-1)
            self.path.append((row, col))
            return True
        
        elif self.pawn_moves - 1 >= 0:
            self.hand_curr_row = row
            self.hand_curr_col = col

            self.pawn_moves -= 1
            if self.arm_path is not None:
                self.arm_path.append((row, col))
            else:
                self.arm_path = [(row, col)]  

            self.path.append((row, col))        
            return True
        
        else:
            return False

    def update_movement_path(self, movement):
        self.curr_hand = movement
        self.movement_path.append(movement)

    def pop_movement_path(self):
        self.movement_path.pop(-1)

    def reset_curr_hand_coor(self):
        self.arm_path = [self.arm_path[0]]
        self.movement_path = [self.ori_hand]
        self.pawn_moves = self.pawn_ori_moves
        self.hand_curr_row = self.hand_ori_row
        self.hand_curr_col = self.hand_ori_col
        return self.hand_curr_row, self.hand_curr_col
    

class Maze:
    def __init__(self, maze, pawn_A: Pawn, pawn_B: Pawn):

        self.maze = maze
        self.wall = '#'
        self.empty = ' '
        self.barrier = '/'
        self.box = '*'

        self.pawn_A = pawn_A
        self.label_A = self.pawn_A.get_pawn_label()
        self.ori_hand_A = self.pawn_A.get_ori_hand()
        self.curr_hand_A = self.pawn_A.get_curr_hand()
        self.hand_A = self.pawn_A.get_hand_label()
        self.arm_A = self.pawn_A.get_arm_label()

        self.pawn_B = pawn_B
        self.label_B = self.pawn_B.get_pawn_label()
        self.ori_hand_B = self.pawn_B.get_ori_hand()
        self.curr_hand_B = self.pawn_B.get_curr_hand()
        self.hand_B = self.pawn_B.get_hand_label()
        self.arm_B = self.pawn_B.get_arm_label()

        self.green_button = 'G'
        self.purple_button = 'P'
        self.severed_hand = '$'
        self.shakehands = '%'

        self.green_button_barrier = {}
        self.purple_button_barrier = {}
        self.purple_button_reversed = {}

    def get_maze(self):
        return self.maze
    
    def get_pawns(self):
        return self.pawn_A, self.pawn_B
    
    def store_button(self, key, value, status):
        if status == 'G':
            if key in self.green_button_barrier:
                self.green_button_barrier[key].append(value)
            else:
                self.green_button_barrier[key] = [value]
        elif status == 'R':
            if key in self.purple_button_reversed:
                self.purple_button_reversed[key].append(value)
            else:
                self.purple_button_reversed[key] = [value]
        else:
            if key in self.purple_button_barrier:
                self.purple_button_barrier[key].append(value)
            else:
                self.purple_button_barrier[key] = [value]

    def replace_barrier(self, row, col):
        self.maze[row][col] = ' '

    def replace_pawn(self, new_pawn, status):
        if status in self.hand_A:
            self.pawn_A = new_pawn
        else:
            self.pawn_B = new_pawn

    def replace_green_button(self, row, col):
        if (row, col) in self.green_button_barrier:
            if self.maze[row][col] == self.empty:
                self.maze[row][col] = self.green_button
    
    def replace_purple_button(self, row, col):
        replace = False
        if (row, col) in self.purple_button_barrier:
            if self.maze[row][col] == self.empty:
                self.maze[row][col] = self.purple_button
                replace = True
            elif self.maze[row][col] == self.arm_A or self.maze[row][col] == self.arm_B:
                replace = True
            
            if replace:
                for barrier_row, barrier_col in self.purple_button_barrier[(row, col)]:
                    if self.maze[barrier_row][barrier_col] == self.arm_A or self.maze[barrier_row][barrier_col] in self.hand_A:
                        self.anticipate_severed_hand(self.pawn_A)
                    if self.maze[barrier_row][barrier_col] == self.arm_B or self.maze[barrier_row][barrier_col] in self.hand_B:
                        self.anticipate_severed_hand(self.pawn_B)
                    self.maze[barrier_row][barrier_col] = self.barrier
                
        if (row, col) in self.purple_button_reversed:
            if self.maze[row][col] == self.empty:
                self.maze[row][col] = self.purple_button
                replace = True
            elif self.maze[row][col] == self.arm_A or self.maze[row][col] == self.arm_B:
                replace = True

            if replace:
                for barrier_row, barrier_col in self.purple_button_reversed[(row, col)]:
                    if self.maze[barrier_row][barrier_col] == self.arm_A or self.maze[barrier_row][barrier_col] in self.hand_A:
                        self.anticipate_severed_hand(self.pawn_A)
                    if self.maze[barrier_row][barrier_col] == self.arm_B or self.maze[barrier_row][barrier_col] in self.hand_B:
                        self.anticipate_severed_hand(self.pawn_B)
                    self.maze[barrier_row][barrier_col] = self.empty

    def is_green_button(self, row, col):
        return self.maze[row][col] == self.green_button

    def is_purple_button(self, row, col):
        return self.maze[row][col] == self.purple_button

    def is_available_path(self, row, col, label):
        if label in self.hand_A:
            arm_path = self.pawn_A.get_arm_path()
            movement_path = self.pawn_B.get_movement_path()
            
            if self.maze[row][col] == self.label_B:
                return 'PAWN'
            elif self.maze[row][col] in self.hand_B:
                if label in ['→', '←'] and movement_path[-1] in ['⇒', '⇐']:     # Karakter ASCII diambil dari ChatGPT
                    return 'SHAKEHAND'
                elif label in ['↑', '↓'] and movement_path[-1] in ['⇑', '⇓']:
                    return 'SHAKEHAND'
                else:
                    return False
        else:
            arm_path = self.pawn_B.get_arm_path()
            movement_path = self.pawn_A.get_movement_path()

            if self.maze[row][col] == self.label_A:
                return 'PAWN'
            elif self.maze[row][col] in self.hand_A:
                if label in ['⇒', '⇐'] and movement_path[-1] in ['→', '←']:
                    return 'SHAKEHAND'
                elif label in ['⇑', '⇓'] and movement_path[-1] in ['↑', '↓']:
                    return 'SHAKEHAND'
                else:
                    return False

        if arm_path is not None and len(arm_path) > 1 and (row, col) == arm_path[-2]:
            return 'BACKWARD'     
        elif self.maze[row][col] == self.empty:
            return 'EMPTY'
        elif self.maze[row][col] == self.box:
            return 'BOX'
        elif self.maze[row][col] == self.severed_hand:
            return 'HAND'
        elif self.is_green_button(row, col):
            return 'GREEN'
        elif self.is_purple_button(row, col):
            return 'PURPLE'
        else:
            return False
        
    def move_box_or_severedhand(self, row, col, movement, status):
        if movement == 'UP':
            new_row = row - 1
            new_col = col
        elif movement == 'DOWN':
            new_row = row + 1
            new_col = col
        elif movement == 'RIGHT':
            new_row = row
            new_col = col + 1
        elif movement == 'LEFT':
            new_row = row
            new_col = col - 1

        available = False

        if self.maze[new_row][new_col] == self.empty:
            available = True
        elif self.maze[new_row][new_col] == self.green_button:
            available = True
        elif self.maze[new_row][new_col] == self.purple_button:
            available = True

        if available:
            if status == 'BOX':
                self.maze[new_row][new_col] = self.box
            else:
                self.maze[new_row][new_col] = self.severed_hand

            return new_row, new_col
        else:
            return False
        
    def move_pawn(self, movement, label):
        unavailable_path = [self.wall, self.barrier, self.box]

        if label in self.hand_A:
            pawn_coor, hand_coor, arm_path = self.pawn_B.get_pawn_coor(), self.pawn_B.get_hand_coor(), self.pawn_B.get_arm_path()
            unavailable_path.extend([self.label_A, self.arm_A])
        else:
            pawn_coor, hand_coor, arm_path = self.pawn_A.get_pawn_coor(), self.pawn_A.get_hand_coor(), self.pawn_A.get_arm_path()
            unavailable_path.extend([self.label_B, self.arm_B])

        new_arm_path = copy.deepcopy(arm_path)

        if movement == 'UP':
            new_pawn_row, new_pawn_col = (pawn_coor[0] - 1, pawn_coor[1])
            new_hand_ori_row, new_hand_ori_col = (new_pawn_row - 1, new_pawn_col)
            new_hand_row, new_hand_col = (hand_coor[0] - 1, hand_coor[1])
            for i in range(len(arm_path)):
                new_arm_path[i] = (arm_path[i][0] - 1, arm_path[i][1])
        elif movement == 'DOWN':
            new_pawn_row, new_pawn_col = (pawn_coor[0] + 1, pawn_coor[1])
            new_hand_ori_row, new_hand_ori_col = (new_pawn_row + 1, new_pawn_col)
            new_hand_row, new_hand_col = (hand_coor[0] + 1, hand_coor[1])
            for i in range(len(arm_path)):
                new_arm_path[i] = (arm_path[i][0] + 1, arm_path[i][1])
        elif movement == 'RIGHT':
            new_pawn_row, new_pawn_col = (pawn_coor[0], pawn_coor[1] + 1)
            new_hand_ori_row, new_hand_ori_col = (new_pawn_row, new_pawn_col + 1)
            new_hand_row, new_hand_col = (hand_coor[0], hand_coor[1] + 1)
            for i in range(len(arm_path)):
                new_arm_path[i] = (arm_path[i][0], arm_path[i][1] + 1)
        elif movement == 'LEFT':
            new_pawn_row, new_pawn_col = (pawn_coor[0], pawn_coor[1] - 1)
            new_hand_ori_row, new_hand_ori_col = (new_pawn_row, new_pawn_col - 1)
            new_hand_row, new_hand_col = (hand_coor[0], hand_coor[1] - 1)
            for i in range(len(arm_path)):
                new_arm_path[i] = (arm_path[i][0], arm_path[i][1] - 1)

        for row, col in new_arm_path:
            if self.maze[row][col] in unavailable_path:
                return False

        if self.maze[new_pawn_row][new_pawn_col] in unavailable_path:
            return False
        elif self.maze[new_hand_row][new_hand_col] in unavailable_path:
            return False
        
        self.maze[pawn_coor[0]][pawn_coor[1]] = self.empty
        self.maze[hand_coor[0]][hand_coor[1]] = self.empty
        for r, c in arm_path:
            self.maze[r][c] = self.empty

        if label in self.hand_B:
            self.pawn_A.store_pawn_coor(new_pawn_row, new_pawn_col)
            self.pawn_A.store_ori_hand_coor(new_hand_ori_row, new_hand_ori_col)
            self.pawn_A.store_curr_hand_coor(new_hand_row, new_hand_col)
            self.pawn_A.update_arm_path(new_arm_path)
            hand = self.pawn_A.get_curr_hand()

            self.maze[new_pawn_row][new_pawn_col] = self.label_A
            for row, col in new_arm_path:
                self.maze[row][col] = self.arm_A
            self.maze[new_hand_row][new_hand_col] = hand

            return ((pawn_coor[0], pawn_coor[1]), (hand_coor[0], hand_coor[1]), (new_pawn_row, new_pawn_col), (new_hand_row, new_hand_col))
        
        else:
            self.pawn_B.store_pawn_coor(new_pawn_row, new_pawn_col)
            self.pawn_B.store_ori_hand_coor(new_hand_ori_row, new_hand_ori_col)
            self.pawn_B.store_curr_hand_coor(new_hand_row, new_hand_col)
            self.pawn_B.update_arm_path(new_arm_path)
            hand = self.pawn_B.get_curr_hand()

            self.maze[new_pawn_row][new_pawn_col] = self.label_B
            for row, col in new_arm_path:
                self.maze[row][col] = self.arm_B
            self.maze[new_hand_row][new_hand_col] = hand

            return ((pawn_coor[0], pawn_coor[1]), (hand_coor[0], hand_coor[1]), (new_pawn_row, new_pawn_col), (new_hand_row, new_hand_col))

    def update_hand_move(self, curr_row, curr_col, new_row, new_col, hand, status):
        if hand in self.hand_A:
            pawn = self.pawn_A
            arm = self.arm_A
            movement_path = self.pawn_A.get_movement_path()
            curr_hand_coor = self.pawn_A.get_hand_coor()
            if curr_hand_coor != (new_row, new_col):
                return
        else:
            pawn = self.pawn_B
            arm = self.arm_B
            movement_path = self.pawn_B.get_movement_path()
            curr_hand_coor = self.pawn_B.get_hand_coor()
            if curr_hand_coor != (new_row, new_col):
                return

        if status == 'BACKWARD':
            hand = movement_path[-2]
            pawn.pop_movement_path()
            self.maze[curr_row][curr_col] = self.empty
            self.maze[new_row][new_col] = hand
        else:
            pawn.update_movement_path(hand)
            self.maze[curr_row][curr_col] = arm
            self.maze[new_row][new_col] = hand
        
    def anticipate_green_button(self, row, col):
        if self.green_button_barrier:
            if (row, col) in self.green_button_barrier:
                for barrier_row, barrier_col in self.green_button_barrier[(row, col)]:
                    if self.maze[barrier_row][barrier_col] == self.empty or self.maze[barrier_row][barrier_col] == self.box:
                        self.maze[barrier_row][barrier_col] = self.barrier

                    elif self.maze[barrier_row][barrier_col] == self.arm_A or self.maze[barrier_row][barrier_col] in self.hand_A:
                        self.anticipate_severed_hand(self.pawn_A)
                        self.maze[barrier_row][barrier_col] = self.barrier

                    elif self.maze[barrier_row][barrier_col] == self.arm_B or self.maze[barrier_row][barrier_col] in self.hand_B:
                        self.anticipate_severed_hand(self.pawn_B)
                        self.maze[barrier_row][barrier_col] = self.barrier

                    else:
                        self.maze[barrier_row][barrier_col] = self.empty

    def anticipate_severed_hand(self, hand_status):
        if hand_status == self.pawn_A:
            hand_row, hand_col = self.pawn_A.get_hand_coor()
            arm_path = self.pawn_A.get_arm_path()

            for row, col in arm_path:
                self.maze[row][col] = self.empty

            self.maze[hand_row][hand_col] = self.severed_hand

            hand_new_row, hand_new_col = self.pawn_A.reset_curr_hand_coor()
            self.maze[hand_new_row][hand_new_col] = self.ori_hand_A

        elif hand_status == self.pawn_B:
            hand_row, hand_col = self.pawn_B.get_hand_coor()
            arm_path = self.pawn_B.get_arm_path()

            for row, col in arm_path:
                self.maze[row][col] = self.empty

            self.maze[hand_row][hand_col] = self.severed_hand

            hand_new_row, hand_new_col = self.pawn_B.reset_curr_hand_coor()
            self.maze[hand_new_row][hand_new_col] = self.ori_hand_B

    def anticipate_purple_button(self, row, col):
        if self.purple_button_barrier:
            if (row, col) in self.purple_button_barrier:
                for barrier_row, barrier_col in self.purple_button_barrier[(row, col)]:
                    self.maze[barrier_row][barrier_col] = self.empty

        if self.purple_button_reversed:
            if (row, col) in self.purple_button_reversed:
                for barrier_row, barrier_col in self.purple_button_reversed[(row, col)]:
                
                    if self.maze[barrier_row][barrier_col] == self.empty or self.maze[barrier_row][barrier_col] == self.box:
                        self.maze[barrier_row][barrier_col] = self.barrier

                    elif self.maze[barrier_row][barrier_col] == self.arm_A or self.maze[barrier_row][barrier_col] in self.hand_A:
                        self.anticipate_severed_hand(self.pawn_A)
                        self.maze[barrier_row][barrier_col] = self.barrier

                    elif self.maze[barrier_row][barrier_col] == self.arm_B or self.maze[barrier_row][barrier_col] in self.hand_B:
                        self.anticipate_severed_hand(self.pawn_B)
                        self.maze[barrier_row][barrier_col] = self.barrier
                    

    def shakehand(self, row, col):
        self.maze[row][col] = self.shakehands


def handshakes_bfs(maze: Maze, pawn_A: Pawn, pawn_B: Pawn):     # Konsepnya diambil dari proyek kelompok sebelumnya
    q = Queue()

    q.push((maze, pawn_A, pawn_B, [maze]))
    history = [maze.get_maze()]

    while not q.is_empty():
        maze, pawn_A, pawn_B, maze_path = q.pop()

        handA_row, handA_col = pawn_A.get_hand_coor()
        handB_row, handB_col = pawn_B.get_hand_coor()

        if (handA_row, handA_col) == (handB_row, handB_col):
            display_maze(maze_path)
            return 'Success'
        
        else:
            # Pawn B UP
            upB, hand = pawn_B.go_up(handB_row, handB_col)
            status = next_path(maze, handB_row, handB_col, upB, 'UP', hand)
            if status:
                new_maze = status
                new_maze_path = copy.deepcopy(maze_path)                        # Cara duplikasi diajari oleh ChatGPT
                new_maze_path.append(new_maze)
                new_pawn_A, new_pawn_B = new_maze.get_pawns()
                if new_maze.get_maze() not in history:
                    history.append(new_maze.get_maze())
                    q.push((new_maze, new_pawn_A, new_pawn_B, new_maze_path))

            # Pawn B Down
            downB, hand = pawn_B.go_down(handB_row, handB_col)
            status = next_path(maze, handB_row, handB_col, downB, 'DOWN', hand)
            if status:
                new_maze = status
                new_maze_path = copy.deepcopy(maze_path)
                new_maze_path.append(new_maze)
                new_pawn_A, new_pawn_B = new_maze.get_pawns()
                if new_maze.get_maze() not in history:
                    history.append(new_maze.get_maze())
                    q.push((new_maze, new_pawn_A, new_pawn_B, new_maze_path))

            # Pawn B Right
            rightB, hand = pawn_B.go_right(handB_row, handB_col)
            status = next_path(maze, handB_row, handB_col, rightB, 'RIGHT', hand)
            if status:
                new_maze = status
                new_maze_path = copy.deepcopy(maze_path)
                new_maze_path.append(new_maze)
                new_pawn_A, new_pawn_B = new_maze.get_pawns()
                if new_maze.get_maze() not in history:
                    history.append(new_maze.get_maze())
                    q.push((new_maze, new_pawn_A, new_pawn_B, new_maze_path))

            # Pawn B Left
            leftB, hand = pawn_B.go_left(handB_row, handB_col)
            status = next_path(maze, handB_row, handB_col, leftB, 'LEFT', hand)
            if status:
                new_maze = status
                new_maze_path = copy.deepcopy(maze_path)
                new_maze_path.append(new_maze)
                new_pawn_A, new_pawn_B = new_maze.get_pawns()
                if new_maze.get_maze() not in history:
                    history.append(new_maze.get_maze())
                    q.push((new_maze, new_pawn_A, new_pawn_B, new_maze_path))

            # Pawn A Up
            upA, hand = pawn_A.go_up(handA_row, handA_col)
            status = next_path(maze, handA_row, handA_col, upA, 'UP', hand)
            if status:
                new_maze = status
                new_maze_path = copy.deepcopy(maze_path)
                new_maze_path.append(new_maze)
                new_pawn_A, new_pawn_B = new_maze.get_pawns()
                if new_maze.get_maze() not in history:
                    history.append(new_maze.get_maze())
                    q.push((new_maze, new_pawn_A, new_pawn_B, new_maze_path))

            # Pawn A Down
            downA, hand = pawn_A.go_down(handA_row, handA_col)
            status = next_path(maze, handA_row, handA_col, downA, 'DOWN', hand)
            if status:
                new_maze = status
                new_maze_path = copy.deepcopy(maze_path)
                new_maze_path.append(new_maze)
                new_pawn_A, new_pawn_B = new_maze.get_pawns()
                if new_maze.get_maze() not in history:
                    history.append(new_maze.get_maze())
                    q.push((new_maze, new_pawn_A, new_pawn_B, new_maze_path))

            # Pawn A Right
            rightA, hand = pawn_A.go_right(handA_row, handA_col)
            status = next_path(maze, handA_row, handA_col, rightA, 'RIGHT', hand)
            if status:
                new_maze = status
                new_maze_path = copy.deepcopy(maze_path)
                new_maze_path.append(new_maze)
                new_pawn_A, new_pawn_B = new_maze.get_pawns()
                if new_maze.get_maze() not in history:
                    history.append(new_maze.get_maze())
                    q.push((new_maze, new_pawn_A, new_pawn_B, new_maze_path))

            # Pawn A Left
            leftA, hand = pawn_A.go_left(handA_row, handA_col)
            status = next_path(maze, handA_row, handA_col, leftA, 'LEFT', hand)
            if status:
                new_maze = status
                new_maze_path = copy.deepcopy(maze_path)
                new_maze_path.append(new_maze)
                new_pawn_A, new_pawn_B = new_maze.get_pawns()
                if new_maze.get_maze() not in history:
                    history.append(new_maze.get_maze())
                    q.push((new_maze, new_pawn_A, new_pawn_B, new_maze_path))

    return 'Impossible to solve!'


def next_path(maze: Maze, curr_row, curr_col, new_coor, movement: str, hand):
    new_row, new_col = new_coor
    status = maze.is_available_path(new_row, new_col, hand)
    
    if status:
        new_maze = copy.deepcopy(maze)
        pawn_A, pawn_B = new_maze.get_pawns()
        new_pawn_A, new_pawn_B = copy.deepcopy(pawn_A), copy.deepcopy(pawn_B)
        hand_A = new_pawn_A.get_hand_label()
        
        new_maze.replace_pawn(new_pawn_A, '↑')
        new_maze.replace_pawn(new_pawn_B, '⇑')

        available = True

        if status == 'BOX' or status == 'HAND':
            available = new_maze.move_box_or_severedhand(new_row, new_col, movement, status)
        
        elif status == 'PAWN':
            available = new_maze.move_pawn(movement, hand)

        if available:
            
            if hand in hand_A:
                result = new_pawn_A.update_moves(new_row, new_col)
            else:
                result = new_pawn_B.update_moves(new_row, new_col)

            if result:
                new_maze.update_hand_move(curr_row, curr_col, new_row, 
                                        new_col, hand, status)
                
                if status == 'SHAKEHAND':
                    new_maze.shakehand(new_row, new_col)
                
                else:
                    new_maze.anticipate_green_button(new_row, new_col)
                    new_maze.anticipate_purple_button(new_row, new_col)
                    new_maze.replace_green_button(curr_row, curr_col)
                    new_maze.replace_purple_button(curr_row, curr_col)
                    
                    if status == 'BOX' or status == 'HAND':
                        after_row, after_col = available
                        new_maze.anticipate_green_button(after_row, after_col)
                        new_maze.anticipate_purple_button(after_row, after_col)
                    elif status == 'PAWN':
                        old_pawn_coor, old_hand_coor, pawn_coor, hand_coor = available
                        new_maze.replace_green_button(old_pawn_coor[0], old_pawn_coor[1])
                        new_maze.replace_green_button(old_hand_coor[0], old_hand_coor[1])
                        new_maze.replace_purple_button(old_pawn_coor[0], old_pawn_coor[1])
                        new_maze.replace_purple_button(old_hand_coor[0], old_hand_coor[1])

                        new_maze.anticipate_green_button(pawn_coor[0], pawn_coor[1])
                        new_maze.anticipate_green_button(hand_coor[0], hand_coor[1])
                        new_maze.anticipate_purple_button(pawn_coor[0], pawn_coor[1])
                        new_maze.anticipate_purple_button(pawn_coor[0], pawn_coor[1])

                return new_maze
    
    return False                


def read_maze(file):
    maze = []
    green_button = []
    purple_button = []
    barrier_list = []

    curr_hand_A = None
    curr_hand_B = None

    hand_A = ['→', '←', '↑', '↓']
    hand_B = ['⇒', '⇐', '⇑', '⇓']

    pawn_A_coor = None
    pawn_B_coor = None

    hand_A_coor = None
    hand_B_coor = None

    pawn_A_label = '@'
    pawn_B_label = '&'

    maze_object = None
    pawn_A = None
    pawn_B = None
    
    with open(file, 'r', encoding='utf-8') as file:                 # Pembacaan karakter ASCII dari text file 'utf-8' diajari oleh ChatGPT
        lines = file.readlines()
        for line_idx, line in enumerate(lines):                     # Cara looping dengan enumerate juga diinspirasi oleh ChatGPT
            if line_idx == 0:
                a, b = line.split(' ')
            else:
                line = list(line.strip())
                if line[0] == '#':

                    if pawn_A_label in line:
                        pawn_A_col = line.index(pawn_A_label)        # Cara pengambilan indeks juga dikonfirmasi oleh ChatGPT
                        pawn_A_coor = (line_idx - 1, pawn_A_col)
                    if pawn_B_label in line:
                        pawn_B_col = line.index(pawn_B_label)
                        pawn_B_coor = (line_idx - 1, pawn_B_col)
                    for hand in hand_A:
                        if hand in line:
                            hand_A_col = line.index(hand)
                            hand_A_coor = (line_idx - 1, hand_A_col)
                            curr_hand_A = hand
                            break
                    for hand in hand_B:
                        if hand in line:
                            hand_B_col = line.index(hand)
                            hand_B_coor = (line_idx - 1, hand_B_col)
                            curr_hand_B = hand
                            break

                    if 'G' in line:
                        for col, x in enumerate(line):
                            if x == 'G':
                                green_button.append((line_idx - 1, col))
                    if 'P' in line:
                        for col, x in enumerate(line):
                            if x == 'P':
                                purple_button.append((line_idx - 1, col))
                    if '/' in line:
                        for col, x in enumerate(line):
                            if x == '/':
                                barrier_list.append((line_idx - 1, col))

                    maze.append(line)
                
                elif line[0] == 'd':
                    pawn_A = Pawn(pawn_A_label, curr_hand_A, hand_A[0], hand_A[1], hand_A[2], hand_A[3], '•')
                    pawn_A.store_pawn_coor(pawn_A_coor[0], pawn_A_coor[1])
                    pawn_A.store_ori_hand_coor(hand_A_coor[0], hand_A_coor[1])
                    pawn_A.store_curr_hand_coor(hand_A_coor[0], hand_A_coor[1])
                    pawn_A.store_pawn_moves(int(a))

                    pawn_B = Pawn(pawn_B_label, curr_hand_B, hand_B[0], hand_B[1], hand_B[2], hand_B[3], '○')
                    pawn_B.store_pawn_coor(pawn_B_coor[0], pawn_B_coor[1])
                    pawn_B.store_ori_hand_coor(hand_B_coor[0], hand_B_coor[1])
                    pawn_B.store_curr_hand_coor(hand_B_coor[0], hand_B_coor[1])
                    pawn_B.store_pawn_moves(int(b))

                    maze_object = Maze(maze, pawn_A, pawn_B)

                elif line[0] == '-':
                    button = line[1]
                    barrier = line[2:]
                    button_index = int(button)
                    key = purple_button[button_index]
                    for barrier_index in barrier:
                        barrier_index = int(barrier_index)
                        value = barrier_list[barrier_index]
                        barrier_list.pop(barrier_index)
                        maze_object.replace_barrier(value[0], value[1])
                        maze_object.store_button(key, value, 'R')

                else:
                    if len(green_button) != 0:
                        button = line[0]
                        barrier = line[1:]
                        button_index = int(button)
                        key = green_button[button_index]
                        green_button.pop(button_index)
                        for barrier_index in barrier:
                            barrier_index = int(barrier_index)
                            value = barrier_list[barrier_index]
                            barrier_list.pop(barrier_index)
                            maze_object.store_button(key, value, 'G')
                    else:
                        button = line[0]
                        barrier = line[1:]
                        button_index = int(button)
                        key = purple_button[button_index]
                        purple_button.pop(button_index)
                        for barrier_index in barrier:
                            barrier_index = int(barrier_index)
                            value = barrier_list[barrier_index]
                            barrier_list.pop(barrier_index)
                            maze_object.store_button(key, value, 'P')

    return maze_object, pawn_A, pawn_B


def display_maze(maze_path):
    for maze in maze_path:
        maze_list = maze.get_maze()
        for row in maze_list:
            print(''.join(row))
        pawn_A, pawn_B = maze.get_pawns()
        print(f'Pawn A: {pawn_A.get_pawn_moves()}')
        print(f'Pawn B: {pawn_B.get_pawn_moves()}')
        print()


maze_object, pawn_A, pawn_B = read_maze('Level_1.txt')
result = handshakes_bfs(maze_object, pawn_A, pawn_B)
print(result)