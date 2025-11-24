screen worldmap_hotspots():
    tag world_map    # ensures only one copy exists at a time
    
    # Transparent clickable regions
    imagebutton:
        xpos 33
        ypos 33
        xsize 260
        ysize 50
        idle Solid((0, 0, 0, 0))
        hover Solid((255, 255, 0, 64))
        action Jump("witchs_lair")

    imagebutton:
        xpos 500
        ypos 19
        xsize 270
        ysize 56
        idle Solid((0, 0, 0, 0))
        hover Solid((255, 255, 0, 64))
        action Jump("spooky_cave")
        sensitive world.spooky_cave_enabled

    imagebutton:
        xpos 534
        ypos 384
        xsize 255
        ysize 49
        idle Solid((0, 0, 0, 0))
        hover Solid((255, 255, 0, 64))
        action Jump("dark_forest")
        sensitive world.dark_forest_enabled


    imagebutton:
        xpos 1150
        ypos 372
        xsize 244
        ysize 53
        idle Solid((0, 0, 0, 0))
        hover Solid((255, 255, 0, 64))
        action Jump("old_temple")

    imagebutton:
        xpos 101
        ypos 867
        xsize 327
        ysize 52
        idle Solid((0, 0, 0, 0))
        hover Solid((255, 255, 0, 64))
        action Jump("desolate_heath")
        sensitive world.desolate_heath_enabled

    imagebutton:
        xpos 1480
        ypos 689
        xsize 342
        ysize 49
        idle Solid((0, 0, 0, 0))
        hover Solid((255, 255, 0, 64))
        action Jump("ancient_cemetery")
        sensitive world.ancient_cemetery_enabled
    hbox:
        xpos 1850 
        ypos 1000
        spacing 10
        textbutton "Inventory" action [Show("view_inventory")] style "blue_button"
        textbutton "Exit"  action Return() style "blue_button"

screen lair_hotspots():
    tag lair_map    # ensures only one copy exists at a time

    add "images/background/witch lair.png"
    # Transparent clickable regions
    # Kitchen
    imagebutton:
        xpos 193
        ypos 381
        xsize 127
        ysize 44
        idle Solid((0, 0, 0, 0))
        hover Solid((0, 255, 0, 64))
        action [SetVariable("target_location", "kitchen"),Jump("change_location")]

    # Library
    imagebutton:
        xpos 911
        ypos 333
        xsize 146
        ysize 44
        idle Solid((0, 0, 0, 0))
        hover Solid((0, 255, 0, 64))
        action [SetVariable("target_location", "library"),Jump("change_location")]
        sensitive world.all_locations[3].enabled

    imagebutton:
        xpos 911
        ypos 333
        xsize 146
        ysize 44
        idle Solid((0, 0, 0, 0))
        hover Solid((255, 0, 0, 64))
        action Show("notification", loc="library", msg="The Library is Locked")
        sensitive not world.all_locations[3].enabled

    # Laboratory
    imagebutton:
        xpos 1465
        ypos 334
        xsize 182
        ysize 42
        idle Solid((0, 0, 0, 0))
        hover Solid((0, 255, 0, 64))
        action [SetVariable("target_location", "laboratory"),Jump("change_location")]
        sensitive world.all_locations[2].enabled

    imagebutton:
        xpos 1465
        ypos 334
        xsize 182
        ysize 42
        idle Solid((0, 0, 0, 0))
        hover Solid((255, 0, 0, 64))
        action Show("notification", loc="laboratory", msg="The Laboratory is Locked")
        sensitive not world.all_locations[2].enabled

    # Witch's Room
    imagebutton:
        xpos 453
        ypos 743
        xsize 131
        ysize 82
        idle Solid((0, 0, 0, 0))
        hover Solid((0, 255, 0, 64))
        action [SetVariable("target_location", "witchs_room"),Jump("change_location")]
        sensitive world.all_locations[4].enabled

    imagebutton:
        xpos 453
        ypos 743
        xsize 131
        ysize 82
        idle Solid((0, 0, 0, 0))
        hover Solid((255, 0, 0, 64))
        action Show("notification", loc="witchs_room", msg="The Witch's Room is Locked")
        sensitive not world.all_locations[4].enabled

    # Mia's Room
    imagebutton:
        xpos 1217
        ypos 768
        xsize 209
        ysize 44
        idle Solid((0, 0, 0, 0))
        hover Solid((0, 255, 0, 64))
        action [SetVariable("target_location", "meris_room"),Jump("change_location")]

    hbox:
        align 0.95, 0.95 
        spacing 10
        textbutton "Inventory" action [Jump("inventory")] style "blue_button"
        textbutton "Exit"  action Return() style "blue_button"

screen notification(loc, msg):
    modal True
    tag notification
    zorder 100

    frame:
        align (0.5, 0.5)
        padding (20, 20)
        has vbox
        text msg color "#111" size 34 xalign 0.5 yalign 0.5
        null height 20

        $ door = next((l for l in world.all_locations if l.name == loc), None)

        hbox:
            align (0.5, 0.0)
            spacing 10
            textbutton "Unlock":
                action [Hide(), Show("open_door", door=door)]
                style "blue_button"
            textbutton "Cancel":
                action Hide()
                style "blue_button"


