
init python:

    import io, csv


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

    def load_cauldrons_from_csv(cauldron_file, recipe_file, recipe_lines_file):
        cauldrons=[]
        with renpy.file(cauldron_file) as f1:
            text = io.TextIOWrapper(f1, encoding="utf-8")
            reader = csv.DictReader(text)
            for row in reader:
                parent=find_contents(row["parent"])
                if parent:
                    cauldrons.append(Cauldron(row["id"],row["parent"], row["cook_text"]))
                    parent.cauldron = cauldrons[-1]
                else:
                    renpy.log("Warning: content {} not found for cauldron".format(row["id"])) 
        
        recipes=[]
        with renpy.file(recipe_file) as f2:
            text = io.TextIOWrapper(f2, encoding="utf-8")
            reader = csv.DictReader(text)
            for row in reader:
                cauldron = next((c for c in cauldrons if c.id == row["cauldron_id"]), None)
                if cauldron:
                    recipes.append(Recipe(row["id"],row["name"],row["cauldron_id"],row["makes"]))
                    cauldron.recipes.append(recipes[-1])
                else:
                    renpy.log("Warning: cauldron {} not found for recipe".format(row["id"])) 
        
        with renpy.file(recipe_lines_file) as f3:
            text = io.TextIOWrapper(f3, encoding="utf-8")
            reader = csv.DictReader(text)
            for row in reader:
                recipe = next((r for r in recipes if r.id == row["recipe"]), None)
                if recipe:
                    recipe.add_ingredient(row["item"])
                else:
                    renpy.log("Warning: recipe {} not found for recipe lines".format(row["item"])) 




    # End of data loading functions