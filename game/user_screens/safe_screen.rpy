screen safe_scene:
    frame:
        align (0.5, 0.3)
        xsize 1280
        ysize 720

        image "images/safe/scene-1-background.png" at half_size
        imagebutton:
            auto "images/safe/scene-1-safe-door-%s.png"
            focus_mask True
            action [Function(dial.reset),Show("safe_puzzle", Fade (1,1,1)),
            Hide("safe_scene")]
            at half_size

screen safe_opened:
    on "show" action Hide("safe_puzzle")
    image "images/safe/safe-opened-background.png" at half_size
    imagebutton:
        auto "images/safe/back-button-%s.png"
        action [Show("safe_scene", Fade(1,1,1)), Hide("safe_opened")]
        align (0.95, 0.95)
        at half_size

    imagebutton:
        auto "images/safe/book-%s.png"
        action NullAction()
        at half_size


screen safe_puzzle:
    #
    # This is where the action takes place
    # The screen shows all the components of the safe
    #
    frame:
        align(0.5, 0.3)
        xsize 1292
        ysize 732
        image "images/safe/safe-closeup-background.png" at half_size
        if dial.combination_check == "Error":
            imagebutton:
                auto "images/safe/safe-handle-ind-red-%s.png"
                focus_mask True
                action Play(file="audio/locked-door.ogg", channel = "sound")
                at half_size
        elif dial.combination_check == "Correct":
            imagebutton:
                auto "images/safe/safe-handle-ind-green-%s.png"
                focus_mask True
                action [Play(file="audio/open-door.ogg", channel = "sound"),
                Show("safe_opened", Transition=Fade(1,1,1))]
                at half_size
        elif dial.combination_check == None:
            imagebutton:
                auto "images/safe/safe-handle-ind-normal-%s.png"
                focus_mask True
                action Play(file="audio/locked-door.ogg", channel = "sound")
                at half_size
        image "images/safe/dial-shadow.png" align (0.48, 0.5) alpha 0.3 at half_size
        image "images/safe/dial-backing.png" align (0.5,0.5) at half_size
        add dial.sprite_manager
        imagebutton:
            auto "/images/safe/dial-reset-button-%s.png" 
            align (0.5, 0.5)
            focus_mask True
            action Function(dial.reset)
            at half_size
        image "/images/safe/dial-text-background.png" align (0.50, 0.17) at half_size
        imagebutton:
            auto "/images/safe/back-button-%s.png"
            align (0.95, 0.95)
            action [Show("safe_scene", Fade (1, 1, 1)),
                Hide("safe_puzzle")] at half_size
        text "[dial.dial_text]" color "#000000" align (0.505, 0.18) text_align 0.5

    

