screen search_location(loc):
    tag search_location    # ensures only one copy exists at a time
    imagemap:
        ground "images/background/{}.png".format(loc.name.lower())
        hover "images/background/{} hover.png".format(loc.name.lower())
        for content in loc.contents:
            hotspot (content.x, content.y, content.w, content.h) alt content.name action Show("view_content",content=content)  
    hbox:
        align 0.95,0.95
        spacing 10 
        textbutton "Inventory" action [Show("view_inventory",mode="screen")] style "blue_button"
        textbutton "Exit" action Return("exit") style "blue_button"
        
screen view_content(content):
    tag view_content    
    modal True
    zorder 100
    frame:  
        xalign 0.5
        yalign 0.5
        xpadding 60
        ypadding 30
        xmaximum 800
        has vbox
        text content.name.title() style "title_text"
        text content.description
        null height 20

        hbox:
            spacing 10
            if content.enabled:
                textbutton "Open" action [Hide("view_content"), Show("view_objects",content=content)] style "blue_button"
            else:
                textbutton "Open" action [Show("open_door",door=content)] style "blue_button"          
            textbutton "Exit" action Hide("view_content") align (0.75, 0.9) style "blue_button"

screen view_objects(content):   
    tag view_objects
    modal True
    zorder 110

    frame:
        xalign 0.5
        yalign 0.5
        xpadding 60
        ypadding 30
        xmaximum 800
        
        vbox:
            text content.text + "..." style "title_text" 
            text "Inside the " + content.name.lower() + " you find:" style "window_text" 
            null height 20

            if content.objs:

                grid 2 len(content.objs):
                    spacing 10

                    for obj_id in content.objs:
                        $ obj = next((o for o in world.all_items if o.id == obj_id), None)    

                        text "[obj.name]: [obj.description]" style "window_text" xmaximum 650   
                        textbutton "Take" action [Function(do_add_inv, obj.type, obj_id), Function(content.remove_obj,obj_id), 
                            Hide("view_objects")] style "blue_button"
            else:
                text "The " + content.name + " is empty" style "window_text"
            
            null height 20

            hbox:
                spacing 10
                textbutton  "Take All" action [
                    Function(take_all_from_content, content),
                    Hide("view_objects")
                    ] style "blue_button" sensitive (content.objs) 
                #
                # Adding Cauldron functionality
                # textbutton "Use":
                #    action [Show use_cauldron(cauldron=content)]
                #   style blue_button
                #   sensitive content.cauldron
                textbutton "Close" action Hide("view_objects") style "blue_button"
                  
