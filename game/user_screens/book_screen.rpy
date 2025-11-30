
screen read_book(left_page, right_page, book_type):
    tag read_book    
    modal True
    zorder 150
    frame:
        add "images/background/book back.png" as book_back  
        background None

        frame:
            xpos 370
            ypos 130
            xmaximum 550
            background None
            has vbox
            if book_type == "image":
                add "[left_page]"
            else:
                text left_page style "book_text"

        frame:
            xpos 1005
            ypos 140 
            xmaximum 550
    
            background None
            has vbox
            if book_type == "image":
                add "[right_page]"
            else:
                text right_page style "book_text"
            

        textbutton "Exit" action Return() align (1.0, 1.0) style "blue_button"