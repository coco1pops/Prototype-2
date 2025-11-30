screen status_bar():
    zorder 300
    frame:
        xalign 0.5
        yalign 0.0
        xfill True
        yminimum 40
        background "#2228"

        hbox:
            spacing 40
            xalign 0.5
            yalign 0.5

            text "Day: [world.day]" size 26 color "#fff"
            text "Time: [world.ampm]" size 26 color "#fff"
            text "Charisma: [pc.charisma]" size 26 color "#fff"
            text "XP: [pc.experience]" size 26 color "#fff"
            text "Phase: [world.phase]" size 26 color "#fff"

            hbox:
                spacing 20
                text "Hunger:" size 26 color "#fff" xalign 0.5
                bar:
                    value pc.hunger
                    range 5
                    xmaximum 100
                    ymaximum 15
                    left_bar hunger_color(pc.hunger)
                    right_bar "#444"   # background color