screen view_inventory(mode):   
    tag view_inventory
    modal True
    zorder 120

    frame:
        # need to fix why the frame is stretching 
        xalign 0.5
        yalign 0.5
        xpadding 60
        ypadding 30
        style "frame_narrow"
        
        vbox:
            text "Inventory" style "title_text" 
            null height 20

            grid 3 5:           
                spacing 10
                add "images/icons/books.jpg" as books
                text "Books: (" + str(len(pc.inv_books)) +")"  style "window_text"
                textbutton "List" action[Show("view_list", objs=pc.inv_books, name="Books", mode=mode)] style "blue_button"
                add "images/icons/potions.jpg" as potions
                text "Potions: (" + str(len(pc.inv_potions)) +")" style "window_text"
                textbutton "List" action[Show("view_list", objs=pc.inv_potions, name="Potions", mode=mode)] style "blue_button"
                add "images/icons/scrolls.jpg" as scrolls
                text "Scrolls: (" + str(len(pc.inv_scrolls)) +")" style "window_text"
                textbutton "List" action[Show("view_list", objs=pc.inv_scrolls, name="Scrolls")] style "blue_button"
                add "images/icons/rings.jpg" as rings
                text "Rings: (" + str(len(pc.inv_rings)) +")" style "window_text"
                textbutton "List" action[Show("view_list", objs=pc.inv_rings, name="Rings", mode=mode)] style "blue_button"
                add "images/icons/other.jpg" as other
                text "Misc Items: (" + str(len(pc.inv_other)) +")" style "window_text"
                textbutton "List" action[Show("view_list", objs=pc.inv_other, name="Misc Items")] style "blue_button"
            
            null height 20
            if mode == "screen":
                textbutton "Close" action Hide() style "blue_button"
            else:
                textbutton "Close" action Return() style "blue_button"

screen view_list(objs, name, mode=""):
    tag view_list
    modal True  
    zorder 180
    frame:
        xalign 0.5 
        yalign 0.5
        xpadding 60
        ypadding 30
        xmaximum 900

        vbox:
            text name + " List" style "title_text"
            if objs:

                grid 2 len(objs):
                    spacing 10

                    for obj_id in objs:
                        $ obj = next((o for o in world.all_items if o.id == obj_id), None)    

                        text "[obj.name]: [obj.description]" style "window_text" xmaximum 650 
                        if name=="Books":  
                            textbutton "Read": 
                                action [SetVariable("book", obj),
                                SetVariable("mode", mode), 
                                Hide(), 
                                Hide("view_inventory"), 
                                Jump("read_book")] 
                                style "blue_button"
                        elif name=="Potions":
                            textbutton "Drink" action [Function(drink_potion, obj, mode)] style "blue_button"
                        elif name=="Scrolls":
                            text ""
                        elif name=="Rings":
                            textbutton "Wear" action [Show("view_rings", ring=obj, mode=mode)] style "blue_button"
                        else:
                            if mode == "gift":
                                textbutton "Give" action NullAction() style "blue_button"
                            else:
                                text ""
            else:
                text "You have no " + name style "window_text"
            
            null height 20
            textbutton "Close" action Hide() style "blue_button" 

screen view_rings(ring, mode):
    tag view_rings
    modal True
    zorder 200
    frame:
        xalign 0.5
        yalign 0.5
        xpadding 60
        ypadding 30
        vbox:
            text "Ring: [ring.name]" style "title_text"
            text "[ring.description]" style "window_text"
            null height 20
            if pc.left_ring != -1:
                $ obj = next((r for r in world.all_items if r.id == pc.left_ring), None) 
                text "Left Ring: [obj.name], [obj.description]"
            else:
                text "Left Ring: None"   

            if pc.right_ring != -1:
                $ obj = next((r for r in world.all_items if r.id == pc.right_ring), None) 
                text "Right Ring: [obj.name], [obj.description]"
            else:
                text "Right Ring: None"   

            hbox:
                null height 10
                spacing 10
                textbutton "Wear on Left":
                    action [Function(wear_ring, ring, "left", mode)] 
                    style "blue_button"
                    sensitive ring.id != pc.left_ring
                textbutton "Wear on Right": 
                    action [Function(wear_ring, ring, "right", mode)] 
                    style "blue_button"
                    sensitive ring.id != pc.right_ring
                textbutton "Take Off":
                    action [Function(ring.take_off_ring), 
                    Hide("view_rings"), 
                    Hide("view_list")] 
                    style "blue_button"
                    sensitive ring.id == pc.left_ring or ring.id == pc.right_ring

            null height 20
            textbutton "Close" action Hide("view_rings") style "blue_button"            

screen give_npc:
    textbutton "Give" style "blue_button" align (0.95, 0.95) action [Show("view_list", objs=pc.inv_other, name="Misc Items", mode="gift" )]