init python:

    #
    # Define utility functions
    #
    def read_lines(filename):
        with open(renpy.loader.transfn(filename), "r", encoding="utf-8") as f:
            return f.readlines()
    
    def take_all_from_content(content):
        for obj_id in content.objs[:]:  # Use a copy of the list to avoid modification issues
            obj = next((o for o in world.all_items if o.id == obj_id), None)    
            if obj:
                do_add_inv(obj.type, obj_id)
                content.remove_obj(obj_id)
        renpy.log("Took all items from content ID {}".format(content.id))   

    def do_add_inv(typ, oid):
            if typ == "book":
                pc.inv_books.append(oid)
                print ("Added book", oid, "to inventory")
            elif typ == "potion":
                pc.inv_potions.append(oid)
                print ("Added potion", oid, "to inventory")
            elif typ == "scroll":
                pc.inv_scrolls.append(oid)
            elif typ == "ring":
                pc.inv_rings.append(oid)
            else:
                pc.inv_other.append(oid)

    def check_scroll(door, scroll, mode):
        # Check that the scroll has opened the door
        global function_success, error_message
        attempt = {
            "type" : "scroll",
            "solution" : scroll.id }
        function_success, error_message = door.puzzle.check_solution(attempt) 
 
        if not function_success:
            renpy.restart_interaction()
            return
        # 
        # Close modal windows
        #
        renpy.hide_screen("pick_item")
        renpy.hide_screen("open_door")
        if mode == "screen":
            renpy.hide_screen("view_content") # This will only be necessary for the location screen
        #
        # Jump to the success dialogue
        #
        renpy.call("opened_door_with_scroll", door=door, scroll=scroll, mode=mode)

    def check_key(door, key, mode):
        # Check that the scroll has opened the door
        global function_success, error_message
        attempt = {
            "type" : "key",
            "solution" : key.id }
        function_success, error_message = door.puzzle.check_solution(attempt) 
 
        if not function_success:
            renpy.restart_interaction()
            return
        # 
        # Close modal windows
        #
        renpy.hide_screen("pick_item")
        renpy.hide_screen("open_door")
        if mode == "screen":
            renpy.hide_screen("view_content") # This will only be necessary for the location screen
        #
        # Jump to the success dialogue
        #
        renpy.call("opened_door_with_key", door=door, key=key, mode=mode)

    def wear_ring(ring, finger, mode):
        renpy.hide_screen("view_rings")
        renpy.hide_screen("view_list")
        renpy.hide_screen("view_inventory")
        ring.wear_ring(finger)
        renpy.call("wearing_ring", ring, finger, mode)

    def drink_potion(potion, mode):
        renpy.hide_screen("view_list")
        renpy.hide_screen("view_inventory")
        potion.drink_potion()
        #
        # Need to check the return state here. If it is a dream
        # potion then need to call a script indicated by the potion
        #
        # Could either save the current location in world or just run the script
        # as is
        #
        renpy.call("drinking_potion", potion, mode)
    
    def find_contents(id):
        for l in world.all_locations:
            for c in l.contents:
                if c.id == id:
                    return c
        return False
    
    def hunger_color(value):
        if value <= 1:
            return "#0f0"   # green
        elif value <= 3:
            return "#ff0"   # yellow
        else:
            return "#f00"   # red