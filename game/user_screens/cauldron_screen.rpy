screen cauldron_screen(parent):
    tag cauldron_screen
    modal True
    zorder 200

    frame:
        xalign 0.5
        yalign 0.5
        xpadding 60
        ypadding 30
        xmaximum 900
        has vbox

        $ cauldron = parent.cauldron
        hbox:
            frame:
                xsize 400
                style "no_frame"
                grid 2 1 + len(pc.inv_other):
                    xfill True
                    spacing 10
                    text "Mari"
                    text " "
                    for id in pc.inv_other:
                        $ obj = next((i for i in world.all_items if i.id == id), None)
                        text obj.name

                        textbutton "Add":
                            action [Function(parent.add_obj, obj.id), Function(obj.del_inv)]
                            style "blue_button"
            frame:
                xsize 400
                style "no_frame"
                grid 2 1 + len(parent.objs):
                    xfill True
                    spacing 10
                    text parent.name
                    text " " 
                    for id in parent.objs:
                        $ obj = next((i for i in world.all_items if i.id == id), None)
                        text obj.name
                        textbutton "Remove":
                            action [Function(parent.remove_obj, obj.id), Function(do_add_inv,"Other", obj.id)]
                            style "blue_button"

        null height 20
        vbox:
            xsize 740
            hbox:
                align (0.5, 0.0)
                spacing 10
                null height 10
                textbutton "Cook":
                    action Function(cauldron.mix)
                    style "blue_button"
                textbutton "Close":
                    action [SetVariable("error_message", ""), Hide()]
                    style "blue_button"
                null height 100

            vbox:
                yminimum 100
                if not function_success:
                    text error_message color "#f00"
                else:
                    text error_message color "#00f"



