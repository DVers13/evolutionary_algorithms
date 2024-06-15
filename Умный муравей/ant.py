import numpy as np
class Ant():
    __slots__ = ("field", "field_copy", "start_pos", "max_step", "step", "current_pos", "old_pos_smb", "rotate_idx", "score", "max_score", "isFood", "useState")
    def __init__(self, field, max_step=500):
        self.field = np.array(field)
        self.field_copy = self.field.copy()
        self.start_pos = [0, 0]
        self.max_step = max_step
        self.step = 0
        self.current_pos = self.start_pos
        self.old_pos_smb = field[self.start_pos[0]][self.start_pos[1]]
        self.rotate_idx = 0
        self.score = 0
        self.max_score = 89
        self.isFood = self.check_start_food()
        self.useState = []

    def reset(self):
        self.field = self.field_copy.copy()
        self.start_pos = [0, 0]
        self.step = 0
        self.current_pos = self.start_pos
        self.old_pos_smb = self.field[self.start_pos[0]][self.start_pos[1]]
        self.rotate_idx = 0
        self.score = 0
        self.isFood = self.check_start_food()

    def check_start_food(self):
        return self.field[0][1] == "S"

    def check_next_food(self):
        x, y = self.current_pos
        if self.rotate_idx == 0:  # right
            y = (y + 1) % len(self.field[0])
        elif self.rotate_idx == 1:  # down
            x = (x + 1) % len(self.field)
        elif self.rotate_idx == 2:  # left
            y = (y - 1) % len(self.field[0])
        elif self.rotate_idx == 3:  # up
            x = (x - 1) % len(self.field)
        return self.field[x][y] == "S"

    def step_to(self):
        x, y = self.current_pos
        if self.rotate_idx == 0:  # right
            y = (y + 1) % len(self.field[0])
        elif self.rotate_idx == 1:  # down
            x = (x + 1) % len(self.field)
        elif self.rotate_idx == 2:  # left
            y = (y - 1) % len(self.field[0])
        elif self.rotate_idx == 3:  # up
            x = (x - 1) % len(self.field)

        self.old_pos_smb = self.field[x][y]
        self.field[x][y] = "M"
        self.current_pos = [x, y]
        self.isFood = self.check_next_food()

    def move_forward(self):
        self.field[self.current_pos[0]][self.current_pos[1]] = self.old_pos_smb
        self.step_to()
        self.step += 1
        if self.old_pos_smb == "S":
            self.old_pos_smb = "*"
            self.score += 1
        else:
            self.old_pos_smb = "R"

    def rotate(self, direction):
        self.rotate_idx = (self.rotate_idx + (1 if direction == 1 else -1)) % 4
        self.step += 1
        self.isFood = self.check_next_food()

    def info(self):
        return {"step": self.step, "current_pos": self.current_pos, "score": self.score, "rotate_idx": self.rotate_idx, "isFood": self.isFood}

    def run_automat(self, automat): # [[1, 2, 1, 2], [1, 2, 3, 2], ...]
        current_state = 0
        self.useState = set()
        e = False
        c = 0
        s = current_state
        v = []
        for _ in range(self.max_step):
            if self.score == self.max_score:
                break
            if current_state not in self.useState:
                self.useState.add(current_state)
            if self.isFood:
                current_state = automat[current_state][2]
                s = current_state
                self.move_forward()
            else:
                if current_state == s:
                    c += 1
                else:
                    s = current_state
                    c = 0
                if c >= 10:
                    e = True
                    if s not in v:
                        v.append(s)
                action = automat[current_state]
                current_state = action[0]
                if action[1] == 2:
                    self.move_forward()
                else:
                    self.rotate(action[1])
        return e, v