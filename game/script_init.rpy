
init python:

    import io, csv

    #
    # Define game classes
    #
    class WorldState:
        def __init__(self):
            self.day = 1
            self.location = None
            self.worldmap_enabled = False
            self.spooky_cave_enabled = False
            self.dark_forest_enabled = False
            self.ancient_cemetery_enabled = False
            self.desolate_heath_enabled = False
            self.all_items = []
            self.all_locations = []
            
    class PlayerCharacter:
        def __init__(self, name):
            self.name = name
            self.charisma = 0
            self.experience = 0
            self.locations_visited = set()
            self.inv_books = []
            self.inv_potions = []
            self.inv_scrolls = []
            self.inv_rings = []
            self.left_ring = -1
            self.right_ring = -1
            self.inv_other = []
            self.c = Character(name)

        def is_wearing_ring(self, ring_id):
            return (self.left_ring == ring_id or self.right_ring == ring_id)

    class NPC:
        def __init__(self, name, description, attitude):
            self.name = name
            self.description = description
            self.attitude = attitude
            self.c = Character(name)
    
    class Obj:
        def __init__(self, id, name, description, func):
            self.id = id
            self.name = name
            self.description = description
            self.func_name = func
            self.type = ""

        def del_inv(self):
            match self.type:
                case "book":
                    pc.inv_books.remove(self.id)
                case "potion":
                    pc.inv_potions.remove(self.id)
                case "scroll":
                    pc.inv_scrolls.remove(self.id)
                case "ring":
                    pc.inv_rings.remove(self.id)
                case _:
                    pc.inv_other.remove(self.id)
        
        def use(self):
            if func:
                obj_actions[self.func](pc, self)

    class Book(Obj):
        def __init__(self, id, name, description, func, text):
            super().__init__(id, name, description, func)
            self.text = text
            self.type = "book"
            self.left_page = ""
            self.right_page = ""
        
        def load_pages(self):
            filename = "db/books/{}_l.txt".format(self.id) 
            self.left_page = "".join(read_lines(filename))
            filename = "db/books/{}_r.txt".format(self.id) 
            self.right_page = "".join(read_lines(filename))
        
        def read_book(self):
            if func:
                book_actions[self.func](self)

    class Potion(Obj):
        def __init__(self, id, name, description, func, drink_text):
            super().__init__(id, name, description, func)
            self.drink_text = drink_text
            self.type = "potion"
            self.charisma = 0
            self.experience = 0

        def drink_potion(self):
            pc.charisma += self.charisma
            pc.experience += self.experience
            self.del_inv()

    class Scroll(Obj):
        def __init__(self, id, name, description, func, scroll_text):
            super().__init__(id, name, description, func)
            self.scroll_text = scroll_text
            self.type = "scroll"

    class Ring(Obj):
        def __init__(self, id, name, description, func, ring_text):
            super().__init__(id, name, description, func)
            self.ring_text = ring_text
            self.type = "ring"
            self.charisma = 0
            self.experience = 0
        
        def wear_ring(self, pos):
            if pc.left_ring == self.id or pc.right_ring == self.id:
                self.take_off_ring()

            if pos == "left":
                if pc.left_ring != -1:
                    cur_ring = next((r for r in world.all_items if r.id == pc.left_ring), None)
                    cur_ring.take_off_ring()
                pc.left_ring = self.id
            else:
                if pc.right_ring != -1:
                    cur_ring = next((r for r in world.all_items if r.id == pc.right_ring), None)
                    cur_ring.take_off_ring()
                pc.right_ring = self.id
            
            self.update_stats("wear")
        
        def take_off_ring(self):
            if pc.left_ring == self.id:
                pc.left_ring = -1
            elif pc.right_ring == self.id:
                pc.right_ring = -1
            
            self.update_stats("remove")
    
        def update_stats(self, mode):
            if mode == "wear":
                pc.charisma += self.charisma
                pc.experience += self.experience
            else:
                pc.charisma -= self.charisma
                pc.experience -= self.experience


    class Location:
        def __init__(self, id, name, display_name, description, enabled):
            self.id = id
            self.name = name
            self.display_name = display_name
            self.description = description
            self.enabled = enabled
            self.puzzle = ""
            self.visited = False
            self.contents = []
        
        def add_content(self, content):
            self.contents.append(content)

    class Content:
        def __init__(self, id, name, location, description, enabled, x, y, w, h, text):
            self.id = id
            self.name = name
            self.location = location
            self.description = description
            self.enabled = enabled
            self.puzzle = ""
            self.x = x            
            self.y = y
            self.w = w
            self.h = h
            self.text = text
            self.objs = []

        def add_obj(self, obj):
            self.objs.append(obj)   

        def remove_obj(self, obj):
            self.objs.remove(obj)

    class Puzzle:
        def __init__(self, id, name, description, typ, solution):    
            self.id = id
            self.name = name
            self.description = description
            self.type = typ # scroll, key, combination, sequence
            self.solution = solution  # scroll=scroll id, key=key id, combination=list of inputs, sequence=list of inputs      
        
        def check_solution(self, attempt): 
            if attempt["type"] == "scroll" and self.type == "key":
                error="The lock does not have any symbols or writing on it. It doesn't look like the sort of lock that a scroll would open."
                return False, error
            if attempt["type"] == "key" and self.type == "scroll":
                error="There is no keyhole and there are strange symbols on the lock. It looks like you need something magical to open it."
                return False, error
            if self.type in ["combination", "sequence"] and attempt["type"] in ["scroll", "key"]:
                error="That won't work. You need to solve the puzzle."
                return False, error
            if self.type == "scroll" and attempt["type"] == "scroll" and self.solution != attempt["solution"]:
                error="On inspection, the symbols on the scroll doesn't match the lock."
                return False, error
            if self.type == "key" and attempt["type"] == "key" and self.solution != attempt["solution"]:
                error="The key doesn't fit the lock."   
                return False, error
            if self.type in ["combination", "sequence"] and attempt["type"] in ["combination", "sequence"] and self.solution != attempt["solution"]:
                error="That is not the correct solution to the puzzle."
                return False, error
            if self.type == "scroll":
                success="The symbols on the scroll glow briefly as they match those on the lock, and with a click the lock opens."
                return True, success
            if self.type == "key":
                success="The key fits the lock perfectly, and with a turn the lock opens."
                return True, success
            if self.type in ["combination", "sequence"]:
                success="With a satisfying click, the lock opens."
                return True, success


    # End of class definitions

    #
    # Define data loading functions
    #
    def load_items_from_csv(filename):
        items = []
        with renpy.file(filename) as f:
            text = io.TextIOWrapper(f, encoding="utf-8")
            reader = csv.DictReader(text)
            for row in reader:
                match row["type"]:
                    case "book":
                        items.append(Book(row["id"], row["name"], 
                            row["description"], row["func_name"], row["text"]))
                        new_book = items[-1]
                        new_book.load_pages()
                    case "potion":
                        items.append(Potion(row["id"], row["name"], 
                            row["description"], row["func_name"], row["text"]))
                    case "scroll":
                        items.append(Scroll(row["id"], row["name"], 
                            row["description"], row["func_name"], row["text"]))
                    case "ring":
                        items.append(Ring(row["id"], row["name"], 
                            row["description"], row["func_name"], row["text"]))
                    case _:
                        items.append(Obj(row["id"], row["name"], 
                            row["description"], row["func_name"]))

        return items

    def load_locations_from_csv(filename):
        locations = []
        with renpy.file(filename) as f:
            text = io.TextIOWrapper(f, encoding="utf-8")
            reader = csv.DictReader(text)
            for row in reader:
                locations.append(Location(row["id"], row["name"], row["display_name"],
                    row["description"], row["enabled"] == "True"))
            renpy.log("Added {} locations from {}".format(len(locations), filename))
        return locations

    def load_contents_from_csv(filename):
        contents = []
        with renpy.file(filename) as f:
            text = io.TextIOWrapper(f, encoding="utf-8")
            reader = csv.DictReader(text)
            for row in reader:
                contents.append(Content(row["id"], row["name"], 
                    row["location"], row["description"], row["enabled"].strip().upper() =="TRUE",
                    int(row["x"]), int(row["y"]), int(row["w"]), int(row["h"]), row["text"]))  
                loc = next((l for l in world.all_locations if l.id == row["location"]), None)
                if loc:
                    loc.add_content(contents[-1])
                else:
                    renpy.log("Warning: Location ID {} not found for content ID {}".format(row["location"], row["id"])) 

        return contents     

    def map_contents_to_items(filename, all_contents):
        with renpy.file(filename) as f:
            text = io.TextIOWrapper(f, encoding="utf-8")
            reader = csv.DictReader(text)
            for row in reader:
                content = next((c for c in all_contents if c.id == row["c_id"]), None)
                item = next((i for i in world.all_items if i.id == row["o_id"]), None)
                if content and item:
                    content.add_obj(item.id)
                else:
                    renpy.log("Warning: Content ID {} or Item ID {} not found".format(row["content"], row["item"]))     
    
    def load_puzzles_from_csv(filename):
        puzzles = []    
        with renpy.file(filename) as f:
            text = io.TextIOWrapper(f, encoding="utf-8")
            reader = csv.DictReader(text)
            for row in reader:
                puzzles.append(Puzzle(row["id"], row["name"], 
                    row["description"], row["typ"], row["solution"]))  
                if row["contents_id"]:
                    content = next((c for c in all_contents if c.id == row["contents_id"]), None)
                    if content:
                        content.puzzle = puzzles[-1]
                    else:
                        renpy.log("Warning: Content ID {} not found for puzzle ID {}".format(row["contents_id"], row["id"]))
                elif row["location_id"]:
                    location = next((l for l in world.all_locations if l.id == row["location_id"]), None)
                    if location:
                        location.puzzle = puzzles[-1]
                    else:
                        renpy.log("Warning: Location ID {} not found for puzzle ID {}".format(row["location_id"], row["id"]))  

    def load_modifiers_from_csv(filename):
        with renpy.file(filename) as f:
            text = io.TextIOWrapper(f, encoding="utf-8")
            reader = csv.DictReader(text)
            for row in reader:
                item = next((i for i in world.all_items if i.id == row["id"]), None)
                if item:
                    item.charisma = int(row["charisma"])
                    item.experience = int(row["experience"])
                else:
                    renpy.log("Warning: Item {} not found for modifier".format(row["id"])) 


    # End of data loading functions

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
        renpy.call("drinking_potion", potion, mode)

#
# Initialize game state
#

label init_game:
    # This creates a world object. It will be created when a game is loaded


    python:
        if not world.all_items:
            world.all_items = load_items_from_csv("db/items.csv")
            world.all_locations = load_locations_from_csv("db/locations.csv")
            all_contents = load_contents_from_csv("db/contents.csv") 
            map_contents_to_items("db/objs_in_contents.csv", all_contents)
            load_puzzles_from_csv("db/puzzles.csv")
            load_modifiers_from_csv("db/modifiers.csv")

return