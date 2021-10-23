# -------------------------------------------- IMPORTS --------------------------------------------------------#
from tkinter import *
from PIL import ImageTk, Image
import math

# --------------------------------------------- CONSTANTS ------------------------------------------------------ #
timer = None
content_list = []
wrong_word_list = []
counting = True


# ----------------------------------------------FUNCTIONS---------------------------------------------------- #


def set_stopwatch():
    stopwatch(0)
    # ENABLING THE TEXT INPUT( INITIALLY DISABLED)
    text.config(state=NORMAL)


# STOPWATCH
def stopwatch(count):
    global timer
    if not counting:
        return
    min = math.floor(count / 60)
    sec = count % 60
    if sec < 10:
        sec = f"0{sec}"
    canvas.itemconfig(timer_text, text=f"0{min}:{sec}")
    timer = window.after(1000, stopwatch, count + 1)
    return timer


# For counting words per minute and collecting misspelled words
def text_check():
    global counting
    global wrong_word_list
    set_stopwatch()
    counting = False  # for stopping the stopwatch

    # -------------------converting words in content to list -------------------------------------#
    with open("story.txt") as file:
        content = file.read()
    word_list = content.split(" ")
    for word in word_list:
        if "\n" in word:
            rex = word.split("\n")
            for word in rex:
                content_list.append(word)
        else:
            content_list.append(word)

    # ----------------------converting text input to list----------------------------------------- #
    result = text.get("1.0", "end-1c")
    input_list = result.split(" ")
    length = len(input_list)

    # ----------------------------Checking input text with content-------------------------------- #
    for i in range(length):
        if input_list[i] != content_list[i]:
            wrong_word_list.append(input_list[i])

    # correct_words_len = length - len(wrong_word_list)

    # --------------------------------calculating words per minute ------------------------------ #
    seconds = timer.split("#")
    seconds = int(seconds[-1])
    wpm = round(length * 60 / seconds)
    canvas.itemconfig(words_per_min, text=f"{wpm} words/min")

    # ----------------------------- Providing misspelled words ---------------------------------- #
    root = Tk()
    root.title('Misspelled Words')
    root.config(padx=10, pady=10)
    title = Label(root, text="Misspelled words", font=('Devanagari MT', 40), pady=20)
    title.grid(column=1, row=0)

    column = 0
    row = 1
    for word in wrong_word_list:
        misspelled_word = Label(root, text=word, font=('Devanagari MT', 20))
        misspelled_word.grid(column=column, row=row)
        if column == 2:
            column = 0
            row += 1
        else:
            column += 1


# -------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------UI Setup-------------------------------------------------------- #

window = Tk()
window.title('TypoSpeed')
window.config(padx=20, pady=10, bg="#916BBF")

# Title
title_label = Label(text='TypoSpeed', fg="#1C0C5B", bg="#916BBF", font=('Devanagari MT', 50))
title_label.grid(column=1, row=0)

# OPENS CANVAS IN WINDOW
canvas = Canvas(window, width=900, height=600, bg="#916BBF", highlightthickness=0)

# STOPWATCH
timer_text = canvas.create_text(200, 60, text="00:00", fill="#1C0C5B",
                                font=('Devanagari MT', 25, "bold"), state='disabled')

# WORDS PER MINUTE CALCULATOR
words_per_min = canvas.create_text(650, 60, text="000 words/min", fill="#1C0C5B", font=('Devanagari MT', 25, "bold"))

# OPENS IMAGE IN CANVAS
img = Image.open('laptop.jpg')
img = img.resize((800, 450))
img = ImageTk.PhotoImage(img)
canvas.create_image(60, 110, image=img, anchor=NW)

# --------------------------------------------------Content----------------------------------------------------------- #
with open("story.txt") as file:
    content = file.read()
# -------------------------------------------------------------------------------------------------------------------- #

# DISPLAYS CONTENT ON OPENED IMAGE
canvas.create_text(450, 323, text=content, fill="black", font=('DecoType Naskh', 20))
canvas.grid(column=0, row=1, columnspan=3)

# CREATE SPACE TO TAKE USER INPUT
text = Text(window, height=1, width=60, highlightthickness=0, font=("DecoType Naskh", 20), bg="white", state=DISABLED)
text.grid(column=0, row=2, columnspan=3)

# START BUTTON TO ENABLE INPUT TEXT AND START STOPWATCH
start_button = Button(text="Start", highlightthickness=0, bg='#3D2C8D',
                      fg='white', font=('DecoType Naskh', 20),
                      padx=22, command=set_stopwatch)
start_button.grid(column=0, row=3, pady=10)

# SUBMIT BUTTON --> AFTER CLICKING DISPLAYS MISSPELLED WORDS AND WORDS/MIN
submit_text = Button(text="Submit", highlightthickness=0, bg='#3D2C8D',
                     fg='white', font=('DecoType Naskh', 20),
                     padx=22, command=text_check)
submit_text.grid(column=2, row=3, pady=10)

window.mainloop()
