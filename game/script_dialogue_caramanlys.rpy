label Caramanlys_dialogue_1:
    #
    # Initial intro to the cat
    #
    s "Caramanlys is like his mistress. Grumpy and dangerous"
    s "The cat looks at you dubiously, his green eyes half open"
    c.c "That explosion didn't sound good"
    pc.c "You can speak!"
    c.c "Of course I can speak. I'm a magic cat for goodness sake. I wouldn't be much use if I couldn't speak"
    pc.c "Err... Do you know what happened to Myfanwy?"
    c.c "No. She seems to have disappeared. All the locks have triggered shut too. We're stuck in here"
    pc.c "Oh no! What are we going to do?"
    c.c "Well the first thing you need to do is find me some food"
    pc.c "I don't have any food either!"
    c.c "I suppose I could wait until you pass out but there's not much meat on you. You'd be better off finding some food or cooking"
    show main annoyed at right
    pc.c "What makes you think I'm going to help you?"
    c.c "Well you're not going to be able to get out without me. I've been here a lot longer than you and I know where Myfanwy used to squirrel things away"
    s "You frown at Caramanlys. He really is very annoying. What do you want to do next.....?"
    $ world.phase = "Find Food"
    $ c.counter = 2
    $ c.dialogue_id = 2
    $ c.dialogue_type = "menu"
    return

label Caramanlys_dialogue_2:
    #
    # Help menu. Sets the user off to find food
    # Once the user has found food and given some to Caramanlys then they can proceed to the next quest.
    #

    show screen give_npc

    label cd2_menu:

        menu: 
            "Ask about Kitchen":
                s "Caramanlys pauses for a second, seemingly wondering how stupid you can be"
                c.c "Well it's where you cook food"
                c.c "I suggest you find some ingredients and cook them"

            "Ask about Cooking":
                s "Caramanlys looks at you with thinly disguised contempt"
                c.c "See that big cauldron in the middle of the room? You put ingredients in there and cook them"

            "Ask about Ingredients":
                c.c "There might be some ingredients in here. Myfanwy also used to use some ingredients when she made her potions"

            "Ask about Recipes":
                c.c "Goodness knows. I don't think Myfanwy used recipes but there might be a book somewhere"
                pc.c "That wasn't very much help"
                s "The cat appears to shrug and yawns"

            "Ask about Main Door":
                c.c "Myfanwy had a complex charm to lock the door in case of danger. It's going to be difficult for you to crack it"

            "Exit":
                hide screen give_npc
                return

        jump cd2_menu

label Caramanlys_dialogue_3:
    s "The cat looks at you furiously"
    c.c "I'm starving. Get me some food! Now!"
    return