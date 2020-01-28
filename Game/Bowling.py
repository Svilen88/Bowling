class Bowling:
    def __init__(self, _rolls):
        self.rolls = [int(roll) for roll in _rolls.split(' ')]
        self.frames = [0] * 10
        self.bonuses = {}

    def strike(self, roll, first_frame_roll):
        return roll == 10 and first_frame_roll

    def spear(self, roll, current_frame_points, first_frame_roll):
        return roll + current_frame_points == 10 and not first_frame_roll

    def add_points_to_frame(self, frame_ind, points):
        self.frames[frame_ind] += points

    def set_bonus(self, bonus_type, frame_ind):
        bonus_count = 1 if bonus_type == 'spear' else 2
        self.bonuses[frame_ind] = bonus_count

    def check_for_bonus(self, roll):
        for frame_ind in self.bonuses.keys():
            self.bonuses[frame_ind] -= 1
            self.add_points_to_frame(frame_ind, roll)
        self.bonuses = {ind: value for ind, value in self.bonuses.items() if value > 0}

    def play(self):
        frame_ind = 0
        first_frame_roll = True
        current_frame_points = 0
        while self.rolls:
            roll = self.rolls.pop(0)
            try:

                if self.strike(roll, first_frame_roll):
                    self.add_points_to_frame(frame_ind, roll)
                    frame_ind += 1
                elif self.spear(roll, current_frame_points, first_frame_roll):
                    self.add_points_to_frame(frame_ind, current_frame_points + roll)
                    first_frame_roll = True
                else:
                    if first_frame_roll:
                        current_frame_points = roll
                        first_frame_roll = False
                    else:
                        self.add_points_to_frame(frame_ind, current_frame_points + roll)
                        current_frame_points = 0
                        first_frame_roll = True
                        frame_ind += 1
            except IndexError:
                self.frames[-1] += roll

