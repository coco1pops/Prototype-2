# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.


# call init_py

default world = WorldState()
default pc = PlayerCharacter("Meri")
default g = NPC("Guardian", "A warrior with a long sword. She looks very fierce", -1)

default s = Character("Narrator")
default function_success = False
default error_message = ""


#Declare music
define audio.gamemusic = "audio/teller-of-the-tales-by-kevin-macleod-from-filmmusic-io.mp3"

# The game starts here.

label start:
    play music gamemusic
    call init_game

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene kitchen

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.

    show main no cloak

    # These display lines of dialogue.

    s "You are Mereianaville ap Cerevanian ap Cyth"
    # Temp debug
    # jump debug_1
    s "But most people just call you [pc.name]"

    s "You are an apprentice to Mwyfanwy Morriganwyn the witch"
    s "Unfortunately Mwyfanwy seems to have had an accident"
    s "You heard a big bang from her room. You rushed in but she's nowhere to be seen"
    s "You look around. Everything is where it should be. There's a strong, unpleasant smell and Mwyfanwy has disappeared"

    show main annoyed
    s "This is a disaster. You're just a novice witch. Your jobs are to keep the place tidy, grind up roots and spices, light fires, 
        do the laundry and fetch Mwyfanwy a cup of tea when she wants one. Mwyfanwy did the magic and cooked the food"
    s "The food seemed to just appear. Mwyfanwy must have used magic to conjure it. You've no idea how she did it. 
        But now she's not here"
    s "And you're hungry"   

    label debug_1:

        #
        # Start in the kitchen
        #
        $ world.location = world.all_locations[0]
        s "[world.location.description]"

    label main_loop:
  
        scene expression world.location.name.lower() 
        show main no cloak

        menu:
            "Explore [world.location.display_name]":
                jump display_location

            "Describe [world.location.display_name]":
                s "[world.location.description]"
                jump main_loop  

            "Explore Witch's Lair":
                jump witchs_lair_map

            # On hold for now
            #"Explore World" if world.worldmap_enabled:
            #    scene map base
            #    call screen worldmap_hotspots

            "Inventory":
                call inventory

            "Exit":
                jump quit

            "Unlock some Gallery images":
                ##Condition defined in gallery/galleryA.rpy, gallery/galleryB.rpy etc...)
                $ persistent.pg1_2 = True
                $ persistent.pg1_5 = True
                $ persistent.pg1_4 = True
                $ persistent.pg2_2 = True
                $ persistent.pg2_6 = True
                $ persistent.pg3_5 = True
                $ persistent.pg4_4 = True
                $ persistent.pg4_6 = True

       
        jump main_loop

    label quit:
        return

    label witchs_lair_map:
        s "You explore the witch's lair"

        call screen lair_hotspots()
        if _return == "change":
            scene expression world.location.name.lower() 
            jump changed_location
            
        jump main_loop

    label change_location:
        if target_location == world.location.name:
            # haven't actually changed
            jump main_loop

        # Find new location
        $ world.location = next((l for l in world.all_locations if l.name == target_location), None)   
        scene expression world.location.name.lower()
        s "You go to [world.location.display_name]"
        #
        # May need to change this for outside
        #

    label changed_location:

        show main no cloak
        s "[world.location.description]"
        jump main_loop

    label inventory:
        call screen view_inventory("script")
        return

    label display_location:

        call screen search_location(world.location)

        if _return == "exit":
            jump main_loop
        elif _return == "screen":
            jump display_location

        return

    label read_book:
        # Display the book contents
        # 
        s "[book.text]"
        call screen read_book(left_page=book.left_page, right_page=book.right_page)
        if mode == "screen":
            jump display_location
        jump main_loop

    label drinking_potion(potion, mode):
        scene drink potion 
        s "[potion.drink_text]"
        scene expression world.location.name.lower() 

        return mode

    label opened_door_with_scroll(door, scroll, mode):

        scene scroll
        s "[scroll.scroll_text]"
        scene scroll read with fade
        s "[error_message]"   

        $ scroll.del_inv() #Use up scroll
        $ door.enabled = True
        if isinstance(door, Location):
            # The user has opened a door to a new location
            $ world.location = door
            return "change"
        scene expression world.location.name.lower() 

        return mode

    label opened_door_with_key(door, key, mode):

        scene key use with fade
        s "[error_message]"   

        $ key.del_inv() #Use up key
        $ door.enabled = True
        if isinstance(door, Location):
            # The user has opened a door to a new location
            $ world.location = door
            return "change"

        scene expression world.location.name.lower() 

        return mode

    label wearing_ring(ring, hand, mode):
        scene wear ring
        s "[ring.ring_text]"
        scene expression world.location.name.lower() 

        return mode

    label witchs_lair:
        "You travel to the witch's lair"
        return

    label old_temple:
        s "You travel to the old temple"
        $ world.location = "Old Temple"
        scene old temple

        show guardian at left
        show user at right with moveinright
        if "old_temple" not in pc.locations_visited: 
            s "There is someone standing outside the temple. [g.description]"
            $ pc.locations_visited.add("old_temple")
            pc.c "Hello"
            g.c "Hello, who are you and what do you want?"
            pc.c "My name is [pc.name]"
        else:
            s "[g.name] is still standing outside"
            g.c "You again. What do you want?"

        scene lab
        jump main_loop