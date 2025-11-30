init python:

    class Dial:
        def __init__(self, image, size, win_x, win_y, tx_offset):
            self.image = image
            self.size = (size, size)
            t = Transform(child=self.image, zoom=0.5)
            self.sprite_manager =  SpriteManager(event=dial_events)
            self.sprite = self.sprite_manager.create(t)
            self.offset = tx_offset
            self.combination = {}
            self.win_x = win_x
            self.win_y = win_y

            self.reset()

        def reset(self):
            self.sprite.x = self.win_x - self.size[0]/2
            self.sprite.y = self.win_y - self.size[1]/2
            self.sprite.rotate_amount = 0

            t = Transform(child=self.image, zoom=0.5)
            self.sprite.set_child(t)

            self.rotate = 0
            self.start_rotate = False
            self.number = 0
            self.dial_text = 0
            self.previous_dial_text = 0
            self.changed = False

            self.old_mousepos = (0.0, 0.0)
            self.degrees = 0
            self.old_degrees = 0

            self.completed_combination_numbers = []
            self.combination_check = None
            self.combination_length = 0

        def set_combo(self, combination):
            self.combination = combination

#
# Safe Functions
#
    import math

    def dial_events(event, x, y, st):

        if event.type == renpy.pygame_sdl2.MOUSEBUTTONDOWN:
            if event.button == 1: #Left mouse button
                if dial.start_rotate:
                    offset = dial.offset
                else:
                    offset = 0

                if dial.sprite.x <= x <= dial.sprite.x + dial.size[0] + offset \
                    and dial.sprite.y <= y <= dial.sprite.y + dial.size[1] + offset:
                    # The cursor is within the sprite area
                    dial.rotate=True
                    dial.old_mousepos = (x, y)
                    # The angle at which the mouse is to the centre of the dial is 
                    # calculated from the arc-tangent of the y and x distance
                    angle_radians = math.atan2((dial.sprite.y + dial.size[1] - offset /2 - y),
                        (dial.sprite.x + dial.size[0] - offset /2 - x))
                    # This converts -180 to + 180 degrees to 0 to 360
                    dial.old_degrees = math.degrees(angle_radians) % 360

        elif event.type == renpy.pygame_sdl2.MOUSEBUTTONUP:
            if event.button == 1:
                dial.rotate=False
                if dial.changed:
                    if dial.combination_length < 4:
                        dial.changed = False
                        dial.combination_check = None
                        if len(dial.completed_combination_numbers) == 0:
                            dial.completed_combination_numbers = []
                        dial.completed_combination_numbers.append(dial.dial_text)
                        dial.combination_length += 1

                    if dial.combination_length == 4:
                        if dial.completed_combination_numbers == dial.combination:
                            dial.combination_check = "Correct"
                            renpy.play("audio/success.ogg", "sound")
                        else:
                            dial.combination_check = "Error"
                            renpy.play("audio/error.ogg", "sound")
    
                        dial.changed = False
                        dial.combination_length = 0
                        dial.completed_combination_numbers = {}

                renpy.restart_interaction()


        elif event.type == renpy.pygame_sdl2.MOUSEMOTION:
            if dial.rotate:
                    angle_radians = math.atan2((dial.sprite.y + dial.size[1]/2 - y),
                        (dial.sprite.x + dial.size[0]/2 - x))
                    dial.degrees = math.degrees(angle_radians) % 360
                    rotate_amount = math.hypot(x - dial.old_mousepos[0],
                        y - dial.old_mousepos[1]) / 5
                    if dial.degrees > dial.old_degrees:
                        dial.sprite.rotate_amount += rotate_amount
                    else:
                        dial.sprite.rotate_amount -= rotate_amount

                    t = Transform(child=dial.image, zoom=0.5)
                    # only move in 3.6 increments
                    t.rotate=3.6 * round(dial.sprite.rotate_amount/3.6)
                    if int(t.rotate/3.6) % 100 == 0 and int(t.rotate) != 0:
                        dial.number = 0
                        dial.sprite.rotate_amount = 0.0
                    else:
                        dial.number = int(t.rotate/ 3.6)

                    if dial.number  > 0:
                        dial.dial_text = 100 - dial.number
                    elif dial.number < 0:
                        dial.dial_text = abs(dial.number)
                    else:
                        dial.dial_text = dial.number

                    if dial.dial_text != dial.previous_dial_text:
                        renpy.music.play("audio/dial.ogg", "sound", relative_volume = 0.3)
                        dial.changed = True

                    # Smooths the movement
                    t.subpixel = True
                    dial.start_rotate = True
                    dial.sprite.set_child(t)
                    dial.sprite.x = 1280/2 - dial.size[0]/2 - dial.offset
                    dial.sprite.y = 720/2 - dial.size[1]/2 - dial.offset
                    dial.old_degrees = math.degrees(angle_radians) % 360
                    dial.old_mousepos = (x, y)
                    dial.previous_dial_text = dial.dial_text

                    dial.sprite.manager.redraw(0)
                    renpy.restart_interaction()
                    
