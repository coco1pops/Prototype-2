init -1 python:
    #
    # Define game classes
    #
    class WorldState:
        def __init__(self):
            self.day = 1
            self.ampm = "am"
            self.time = 0
            self.location = None
            self.worldmap_enabled = False
            self.spooky_cave_enabled = False
            self.dark_forest_enabled = False
            self.ancient_cemetery_enabled = False
            self.desolate_heath_enabled = False
            self.phase = "Intro"
            self.all_items = []
            self.all_locations = []
        
        def add_time(self, val):
            self.time += val
            if self.time >= 3:
                if self.ampm == "am":
                    self.ampm = "pm"
                else:
                    self.ampm = "night"
                self.time = 0

            
    class PlayerCharacter:
        def __init__(self, name):
            self.name = name
            self.charisma = 0
            self.experience = 0
            self.hunger = 0
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
            self.dialogue_id = 1
            self.dialogue_type = None
            self.gift = -1
            self.counter = -1

        def get_dialogue(self):
            return f"{self.name}_dialogue_{self.dialogue_id}"
    
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
            self.book_type = func # func will indicate text or image
        
        def load_pages(self):
            if self.func_name == "image":
                filename = "db/books/{}_l.png".format(self.id) 
                self.left_page = filename
                filename = "db/books/{}_r.png".format(self.id) 
                self.right_page = filename
            else:
                filename = "db/books/{}_l.txt".format(self.id) 
                self.left_page = "".join(read_lines(filename))
                filename = "db/books/{}_r.txt".format(self.id) 
                self.right_page = "".join(read_lines(filename))
        
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
            self.NPC = None
        
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
            self.cauldron = ""

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

    class Cauldron:
        def __init__(self, id, parent, cook_text):
            self.id = id
            self.parent = parent
            self.recipes=[]
            self.cook_text = cook_text
     
        def mix(self):
            global function_success, error_message
            parent = find_contents(self.parent)
            function_success, recipe = self._check(parent)
            if function_success:
                made = self._make(parent, recipe)
                tmp_txt = self.cook_text +". You have made "+ made
                error_message = tmp_txt 
            else:
                error_message = "You can't make anything from those ingredients"

        def _check(self, parent):
            
            found = True
            for r in self.recipes:
                # Do the ingredients match the recipe?
                for i in r.ingredients:
                    
                    if i not in parent.objs:
                        found = False

                # Are there any extra ingredients?
                if len(r.ingredients) != len(parent.objs):
                    found = False
                
                if found:
                    return True, r
            
            return False, 0

        def _make(self, parent, recipe):
            parent.objs=[]
            obj = next((i for i in world.all_items if i.id == recipe.makes), None)
            parent.objs.append(recipe.makes)
            return obj.name


    class Recipe:
        def __init__(self, id, name, cauldron, makes):
            self.id=id
            self.name=name
            self.cauldron=cauldron
            self.ingredients=[]
            self.makes=makes

        def add_ingredient(self, obj_id):
            self.ingredients.append(obj_id)

    # End of class definitions
