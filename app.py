from flask import Flask, request, jsonify, make_response


class Bowling:
    def __init__(self, _rolls):
        self.rolls = [int(roll) for roll in _rolls.split(' ')]
        self.frames = [0] * 10
        self.bonuses = {}

    def strike(self, roll, first_frame_roll):
        return roll == 10 and first_frame_roll

    def spear(self, roll, current_frame_points, first_frame_roll):
        return roll + current_frame_points == 10 and not first_frame_roll

    def add_points_to_frame(self, frame_ind, roll):
        self.frames[frame_ind] += roll

    def set_bonus(self, bonus_type, frame_ind):
        bonus_count = 1 if bonus_type == 'spear' else 2
        self.bonuses[frame_ind] = bonus_count

    def check_for_bonus(self, roll):
        for frame_ind in self.bonuses.keys():
            self.bonuses[frame_ind] -= 1
            self.add_points_to_frame(frame_ind, roll)
        self.bonuses = {ind: value for ind, value in self.bonuses.items() if value != 0}

    def show_score(self):
        return sum(self.frames)

    def play(self):
        frame_ind = 0
        first_frame_roll = True
        current_frame_points = 0
        while self.rolls:
            roll = self.rolls.pop(0)
            self.check_for_bonus(roll)
            try:
                if self.strike(roll, first_frame_roll):
                    self.add_points_to_frame(frame_ind, roll)
                    self.set_bonus('strike', frame_ind)
                    frame_ind += 1
                elif self.spear(roll, current_frame_points, first_frame_roll):
                    self.add_points_to_frame(frame_ind, current_frame_points + roll)
                    self.set_bonus('spear', frame_ind)
                    first_frame_roll = True
                    frame_ind += 1
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


app = Flask(__name__)

games = {}


@app.route('/')
def home():
    return '200 OK'


@app.route('/api/game/game=<game_id>/user=<user_id>', methods=['POST'])
def game_request(game_id, user_id):
    content = request.json
    if content is None:
        return make_response('Bad request', 400)
    games.setdefault(game_id, {user_id: Bowling(content['rolls'])})
    return jsonify({'success': []})


@app.route('/api/game/game=<game_id>/user=<user_id>', methods=['GET'])
def show_score(game_id, user_id):
    try:
        games[game_id][user_id].play()
        return {'success': [games[game_id][user_id].show_score()]}
    except KeyError:
        return make_response('Bad request', 400)


if __name__ == '__main__':
    app.run()
