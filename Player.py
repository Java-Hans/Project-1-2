class Player:
    def __init__(self, seat_number):
        self.seat_number = seat_number
        self.active = False
        self.position = None
        self.stack = -1
        self.player_name = ''

    def get_seat_number(self):
        return self.seat_number

    # takes a list in the form [x1, x2, y1, y2]
    def set_hole_card_crop(self, hold_card_crop):
        self.hole_card_crop = hold_card_crop

    def get_hole_card_crop(self):
        return self.hole_card_crop

    def set_active(self, active):
        self.active = active

    def get_active(self):
        return self.active

    def set_position(self, position):
        self.position = position

    def get_position(self):
        return self.position

    def print_position(self):
        print(self.position)

    def print_active(self):
        print(self.active)

    def set_hole_cards(self, hole_card_list):
        self.hole_card_list = hole_card_list

    def get_hole_cards(self):
        return tuple(self.hole_card_list)

    def set_stack(self, stack):
        self.stack = stack

    def get_stack(self):
        return self.stack

    def set_player_name(self, player_name):
        self.player_name = player_name

    def get_player_name(self):
        return self.player_name
