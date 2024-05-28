class Agent:
    def __init__(self, start_position):
        self.position = start_position
        self.direction = 'East'
        self.arrows = 3
        self.dead = False
        self.has_gold = False
        self.previous_states = []

    def save_state(self):
        self.previous_states.append((self.position, self.direction, self.arrows, self.dead, self.has_gold))

    def display_status(self):
        print(f"현재 위치: {self.position}, 방향: {self.direction}, 화살: {self.arrows}, 금 획득: {self.has_gold}")

    def execute_action(self, action, world):
        if action == 'GoForward':
            self.move_forward(world)
        elif action == 'TurnLeft':
            self.turn_left()
        elif action == 'TurnRight':
            self.turn_right()
        elif action == 'Grab':
            self.grab(world)
        elif action == 'Shoot':
            self.shoot(world)
        elif action == 'Climb':
            self.climb()
        
        # Check if agent is in the same position as the Wumpus
        if 'Wumpus' in world.grid[self.position[0]][self.position[1]]:
            choice = input("Wumpus에게 죽었습니다 끝내신다면 (yes) 직전으로 돌아갈거면 (no)? ")
            if choice.lower() == 'yes':
                self.dead = True
                return True
            else:
                self.revert_state()
                return False
        return self.dead

    def move_forward(self, world):
        new_position = self.position
        if self.direction == 'North':
            new_position = (self.position[0] + 1, self.position[1])
        elif self.direction == 'East':
            new_position = (self.position[0], self.position[1] + 1)
        elif self.direction == 'South':
            new_position = (self.position[0] - 1, self.position[1])
        elif self.direction == 'West':
            new_position = (self.position[0], self.position[1] - 1)

        if world.is_valid_position(new_position):
            self.position = new_position
        else:
            print("벽과 충돌")

    def turn_left(self):
        directions = ['North', 'West', 'South', 'East']
        current_index = directions.index(self.direction)
        self.direction = directions[(current_index + 1) % 4]

    def turn_right(self):
        directions = ['North', 'West', 'South', 'East']
        current_index = directions.index(self.direction)
        self.direction = directions[(current_index - 1) % 4]

    def grab(self, world):
        if 'Glitter' in world.grid[self.position[0]][self.position[1]]:
            self.has_gold = True
            world.grid[self.position[0]][self.position[1]].remove('Glitter')
            print("금을 획득")

    def shoot(self, world):
        if self.arrows > 0:
            self.arrows -= 1
            print("화살발사!!")
            # wumpus랑 마주보고 있는가?
            if self.direction == 'North':
                wumpus_position = (self.position[0] + 1, self.position[1])
            elif self.direction == 'East':
                wumpus_position = (self.position[0], self.position[1] + 1)
            elif self.direction == 'South':
                wumpus_position = (self.position[0] - 1, self.position[1])
            elif self.direction == 'West':
                wumpus_position = (self.position[0], self.position[1] - 1)
            
            if 'Wumpus' in world.grid[wumpus_position[0]][wumpus_position[1]]:
                print("WUMPUS사냥 성공!!")
                world.grid[wumpus_position[0]][wumpus_position[1]].remove('Wumpus')
        else:
            print("화살없음 --> 다 썻음")


    def climb(self):
        if self.position == (0, 0):
            if self.has_gold:
                print("금과 함께 탈출성공!")
                self.dead = True
            else:
                print("금없이 탈출하셧네요...")
                self.dead = True
        else:
            print("여기서는 탈출이 안됩니다.")

    def revert_state(self):
        if self.previous_states:
            self.position, self.direction, self.arrows, self.dead, self.has_gold = self.previous_states.pop()
