


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
            load_cauldrons_from_csv("db/cauldrons.csv", "db/recipes.csv", "db/recipe_items.csv")

            # Temp fix to add the cat to the kitchen and to accept the gift of cat treats
            world.all_locations[0].NPC = c
            c.dialogue_type = "intro"
            c.gift = "403" 

label safe_init:
    #
    # Dial variables
    #
    $ dial = Dial("images/safe/dial.png", 660/2, 1280/2, 720/2, 68.2 ) 

    $ combinations = {"safe_1": [5, 15, 47, 63], "safe_2": [23, 5, 75, 44]}
    $ dial.set_combo(combinations["safe_1"])


   
return