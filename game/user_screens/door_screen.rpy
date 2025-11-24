screen open_door(door):
    #
    # This screen allows the player to attempt to open a locked door
    # door contains either a door to another location or a container
    # It provides options to use a scroll, an item, or solve a puzzle
    # puzzle is stored as door.puzzle
    # For scroll and item, the id is compared to door.puzzle.solution and door.puzzle.type to determine if it
    # is the correct key. This is a method of puzzle.
    #
    #
    tag open_door    
    modal True
    zorder 150

    
    frame:
        background Frame("/images/background/frame_edged.png", gui.frame_borders, tile=gui.frame_tile)
        padding (60,70)
        xalign 0.5
        yalign 0.5
        xmaximum 860
        has vbox
        add "images/doors/{}.png".format(door.name) as door_image align (0.5, 0.0)
        text "The " + door.name.lower() + " is locked. Would you like to try to open it with a...?" style "title_text"
        null height 10

        hbox:      
            align (0.5, 1.0)      
            spacing 10
            
            textbutton "Scroll":
                action [Show("pick_item", door=door, objs=pc.inv_scrolls, name="Scrolls")] 
                style "blue_button" 
                sensitive pc.inv_scrolls
            textbutton "Item": 
                action [Show("pick_item", door=door, objs=pc.inv_other, name="Misc Items")] 
                style "blue_button" 
                sensitive pc.inv_other
            textbutton "Puzzle":
                action [Show("solve_puzzle", puzzle=door.puzzle)] 
                style "blue_button" 
                sensitive door.puzzle.type == "combination" or door.puzzle.type == "sequence"
            textbutton "Exit" action Hide()  style "blue_button" 


screen pick_item(door, objs, name):
    tag pick_item
    modal True  
    zorder 180
    frame:
        xalign 0.5 
        yalign 0.5
        xpadding 60
        ypadding 30
        xmaximum 1000

        vbox:
            text "[name] List" style "title_text"
            grid 2 len(objs):

                spacing 10

                for obj_id in objs:
                    $ obj = next((o for o in world.all_items if o.id == obj_id), None)
                    text "[obj.name]: [obj.description]" style "window_text" xmaximum 650 
                    if name == "Scrolls":    
                        textbutton "Read": 
                            action [Function(check_scroll, door, obj, "screen")]
                            style "blue_button" 
                    else: 
                        textbutton "Use": 
                            action [Function(check_key, door, obj, "screen")]
                            style "blue_button" 
            
            null height 20        
            textbutton "Exit" action [SetVariable("error_message", ""), Hide()]  style "blue_button" 
            vbox:
                yminimum 100
                if not function_success:
                    text error_message color "#f00"