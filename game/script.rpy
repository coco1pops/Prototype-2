# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.


default world = WorldState()
default pc = PlayerCharacter("Meri")
default g = NPC("Guardian", "A warrior with a long sword. She looks very fierce", -1)
default c = NPC("Caramanlys", "Myfanwy's well-fed striped, ginger cat with green eyes", -1 )

default s = Character("Narrator")
default function_success = False
default error_message = ""


#Declare music
define audio.gamemusic = "audio/teller-of-the-tales-by-kevin-macleod-from-filmmusic-io.mp3"

transform half_size:
    zoom 0.5

# The game starts here.


label start:
    play music gamemusic
    call init_game

    show screen skip_button
    jump intro

    label out_intro:
    hide screen skip_button

    scene kitchen
    show main no cloak

    # These display lines of dialogue.

    s "You are Mereianaville ap Cerevanian"
    s "Let's just call you [pc.name]"

    s "You are in the kitchen wondering what to do. Myfanwy the witch has disappeared and you are alone in her lair"
    
    #
    # Start in the kitchen
    #
    $ world.location = world.all_locations[0]
    s "[world.location.description]"
    $ lcase_name = world.location.display_name.lower()
    s "In [lcase_name] is [world.location.NPC.name], [world.location.NPC.description]"
            
    label main_loop:

        show screen status_bar
        scene expression world.location.name.lower() 

        if world.location.NPC != None:
            show main no cloak at right
            show expression "images/characters/[world.location.NPC.name].png" at left
            if world.location.NPC.dialogue_type == "intro":
                $ t = world.location.NPC.get_dialogue()
                call expression t 
        else:
            show main no cloak

        menu:
            "Explore [world.location.display_name]":
                jump display_location

            "Describe [world.location.display_name]":
                s "[world.location.description]"

            "Speak to [world.location.NPC.name]" if world.location.NPC :
                $ t = world.location.NPC.get_dialogue()
                call expression t

            "Explore Witch's Lair":
                jump witchs_lair_map

            # On hold for now
            #"Explore World" if world.worldmap_enabled:
            #    scene map base
            #    call screen worldmap_hotspots

            "Inventory":
                call inventory
                call check_time(1)
            
            "Safe Puzzle":
                call screen safe_scene

            "Exit":
                jump quit

            # "Unlock some Gallery images":
                ##Condition defined in gallery/galleryA.rpy, gallery/galleryB.rpy etc...)
                #$ persistent.pg1_2 = True
                #$ persistent.pg1_5 = True
                #$ persistent.pg1_4 = True
                #$ persistent.pg2_2 = True
                #$ persistent.pg2_6 = True
                #$ persistent.pg3_5 = True
                #$ persistent.pg4_4 = True
                #$ persistent.pg4_6 = True
       
        jump main_loop

    label quit:
        return

    label witchs_lair_map:
        hide screen status_bar
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
        $ lcase_name = world.location.display_name.lower()
        scene expression  world.location.name.lower()
        s "You go to [lcase_name]"
        if world.location.NPC:
            s "In [lcase_name] is [world.location.NPC.name], [world.location.NPC.description]"
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
            call check_time(2)
            jump main_loop
        elif _return == "screen":
            jump display_location

        return

    label read_book:
        # Display the book contents
        # 
        s "[book.text]"
        call screen read_book(left_page=book.left_page, right_page=book.right_page, book_type=book.book_type)
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
        $ error_message = ""   

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
        $ error_message = ""

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

    label check_time(inc):
        $ world.add_time(inc)
        if world.ampm == "night":
            jump process_night
        return

    label process_night:
        s "You are tired and need to go to sleep"
        s "You head to your room"
        scene night
        $ world.location = world.all_locations[1]
        s "Night Falls"

        $ world.day += 1
        $ world.ampm="am"
        $ pc.hunger += 1

        if pc_hunger > 5:
            s "Your stomach rumbles with hunger. You feel so weak"
            s "You try to sit up but your head spins and you collapse back on the bed"
            scene Caramanlys big
            s "As your vision fades, you see Caramanlys slinking through the door, his green eyes fixed on you"
            s "He licks his lips as you pass out"
            s "You have lost..."
            jump quit
        if pc.hunger > 3:
            s "You are very hungry"
        elif pc.hunger > 1:
            s "You are hungry"

        if c.counter > -1:
            $ c.counter -=1
        if c.counter == -1:
            $ c.dialogue_id +=1

        jump main_loop

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