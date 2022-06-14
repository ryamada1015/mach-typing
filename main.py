import curses
from curses import wrapper
import time 

def start_screen(stdscr):
    stdscr.clear()
    # addstr(row_num, col_num, string) or
    # addstr(string)
    stdscr.addstr('Welcome to Mach Speed Test!')
    stdscr.addstr('\nPress any key to begin.')
    # refreshes the screen and wait for user input
    stdscr.getkey()

def display_text(stdscr, target, current, wpm=0):
    char_count = 0
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f'WPM: {wpm}')

    # if reached the end of text, display result
    if len(current) == len(target):
        stdscr.addstr(2, 0, f"Final WPM: {wpm}")
        if "".join(current) == target:
            stdscr.addstr(1,  0, "You've perfectly typed the text!")
        else:
            stdscr.addstr(1, 0, "You've miss typed some characters...")
        stdscr.addstr(3, 0, "Press any key to continue...")

    # enumerate method returns en enumerate object assigning a counter as a key to each item in the object so it can be iterated 
    # enumerate current for character matching with target 
    for i, char in enumerate(current):
        correct_char = target[i]
        # overwrite the corresponding character in target text with a character typed by user 
        if char == correct_char:
            stdscr.addstr(0, i, char, curses.color_pair(1))
            char_count += 1
        else:
            stdscr.addstr(0, i, char, curses.color_pair(2))

    
def wpm_test(stdscr):
    target_text = 'Hello world this is some text for testing this app!'
    current_text = []
    wpm = 0
    start_time = time.time()
    # make getkey() non-blocking 
    stdscr.nodelay(True)

    while True:

        # get time elapsed in seconds
        # get max to avoid zero division error
        time_elapsed = max(time.time() - start_time, 1)
        # divid by 5 to get wpm assuming words are 5 chars long at average 
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        # clear screen every time user types; otherwise, all the previous strings contained in screen buffer will show
        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        # update the screen 
        stdscr.refresh()

        # when reached the end of text
        if len(current_text) == len(target_text):
            stdscr.nodelay(False)
            break

        # wait for user input, if no input, skip the following code and go back to the beginning of loop 
        # without try and except, program will crash 
        try:
            key = stdscr.getkey()
        except:
            continue

        # ord(key) returns ascii value of key 
        # if key = esc, exit
        if ord(key) == 27:
            break

        # if user hit backspace, remove the lastly typed character
        if key in ('KEY_BACKSPACE', '\b', '\x7f'):
            if len(current_text) > 0:
                current_text.pop()            
        elif len(current_text) < len(target_text):
            current_text.append(key)

    # stdscr.clear()
    # display_text(stdscr, target_text, current_text, wpm)
    # stdscr.refresh()
    # stdscr.getkey()
        




#initialize the terminal taking over the current module 
#restore the previous state after the program finishes
def main(stdscr):
    #set initial foreground and background colors with id=1
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    wpm_test(stdscr)
    stdscr.getkey()

#call main function while initializing the screen
wrapper(main)