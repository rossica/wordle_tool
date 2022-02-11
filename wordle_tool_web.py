from browser import document, alert
from browser.html import *
from urllib.request import urlopen
from wordle_tool import IsLetter, sort_letter_position_stats, letter_position_stats, letter_stats_uniq, filter_words, filter_letters_known_position, filter_letter_unknown_position

INPUT_BLACK = "inputblack"
INPUT_YELLOW = "inputyellow"
INPUT_GREEN = "inputgreen"
INPUT_PURPLE = "inputpurple"

WORD_LENGTH = 5

def update_words(new_words):
    global previous_words
    global words
    if words != None:
        previous_words.append(words)
    words = new_words

def load_words():
    url = './dictionary.txt'
    file = urlopen(url).read()
    new_words = list()
    for line in file.split('\n'):
        new_words.append(line.strip())
    update_words(new_words)

def print_button(event):
    document['output'].innerHTML = " ".join(words)

def print_stats_button(event):
    count = len(words)
    div = lambda x,y: x / y if y else 0
    stats = sort_letter_position_stats(letter_position_stats(words), letter_stats_uniq(words))
    table = TABLE()
    table <= TR(TH('Letter') + TH('Frequency') + TH('1st Freq.') + TH('2nd Freq.') + TH('3rd Freq.') + TH('4th Freq.') + TH('5th Freq.') + TH('Multi'))
    for t in stats:
        if t[1] > 0:
            table <= TR(
                TD(t[0]) +
                TD('{:.2f}'.format((t[1]/count)*100)) +
                TD('{:.1f}'.format(div(t[2][0], t[1])*100)) +
                TD('{:.1f}'.format(div(t[2][1],t[1])*100)) +
                TD('{:.1f}'.format(div(t[2][2],t[1])*100)) +
                TD('{:.1f}'.format(div(t[2][3],t[1])*100)) +
                TD('{:.1f}'.format(div(t[2][4],t[1])*100)) +
                TD('X' if sum(t[2]) > t[1] else ''))
    document['stats'].clear()
    document['stats'] <= table
    if document['divider'].hidden is True:
        document['divider'].hidden = False

def filter_incl_button(event):
    new_words = filter_words(words, document["cmd"].value)
    update_words(new_words)
    update_log(document["cmd"].value, INPUT_PURPLE)
    print_stats_button(None)
    print_button(None)

def filter_excl_button(event):
    new_words = filter_words(words, document["cmd"].value, False)
    update_words(new_words)
    update_log(document["cmd"].value, INPUT_BLACK)
    print_stats_button(None)
    print_button(None)

def filter_pos_known(event):
    new_words = filter_letters_known_position(words, document["cmd"].value)
    update_words(new_words)
    update_log(document["cmd"].value, INPUT_GREEN)
    print_stats_button(None)
    print_button(None)

def filter_pos_unknown(event):
    new_words = filter_letter_unknown_position(words, document["cmd"].value)
    update_words(new_words)
    update_log(document["cmd"].value, INPUT_YELLOW)
    print_stats_button(None)
    print_button(None)

def adv_help_button(event):
    help_text = """
    Load                    - Loads dictionary file
    Filter (incl.)          - Filters to words containing letters
    Filter (excl.)          - Filters out words containing letters
    Filter position known   - Filters to words with letters in given position.
        e.g. __a__. Allows multiple letters, e.g. ___ly.
    Filter position unknown - Filters to words with letters *not* in position.
        e.g. _b___. Allows multiple letters, e.g. a_l__.
    """
    alert(help_text)

def text_click(event):
    if event.currentTarget.class_name == INPUT_BLACK:
        event.currentTarget.class_name = INPUT_YELLOW
    elif event.currentTarget.class_name == INPUT_YELLOW:
        event.currentTarget.class_name = INPUT_GREEN
    else:
        event.currentTarget.class_name = INPUT_BLACK

def update_log(cmd=None, op=None):
    global next_log
    document['log_container'].hidden = False
    t = TABLE(id='log-{}'.format(next_log))
    if op != None:
        tr = TR()
        idx = 0
        for c in cmd:
            if IsLetter(c.upper()):
                tr <= TD(c, Class=op)
            else:
                tr <= TD('&nbsp;', Class=INPUT_BLACK)
            idx += 1
        while idx < WORD_LENGTH:
            tr <= TD('&nbsp;', Class=INPUT_BLACK)
            idx += 1
        t <= tr
    else:
        t <= TR(
            TD(document['one'].value, Class=document['one'].class_name) +
            TD(document['two'].value, Class=document['two'].class_name) +
            TD(document['three'].value, Class=document['three'].class_name) +
            TD(document['four'].value, Class=document['four'].class_name) +
            TD(document['five'].value, Class=document['five'].class_name))
    document['log'] <= t
    next_log += 1

def get_letter(elem, excl, fpu, fpk):
    letter = elem.value.upper()
    if IsLetter(letter):
        if elem.class_name == INPUT_BLACK:
            excl.append(letter)
            fpu.append('_')
            fpk.append('_')
        elif elem.class_name == INPUT_YELLOW:
            fpu.append(letter)
            fpk.append('_')
        else:
            fpk.append(letter)
            fpu.append('_')
    else:
        fpu.append('_')
        fpk.append('_')

def contains_letter(string_like):
    for c in string_like:
        if IsLetter(c):
            return True
    return False

def simple_filter_button(event):
    global words
    excl = []
    fpu = []
    fpk = []
    get_letter(document['one'], excl, fpu, fpk)
    get_letter(document['two'], excl, fpu, fpk)
    get_letter(document['three'], excl, fpu, fpk)
    get_letter(document['four'], excl, fpu, fpk)
    get_letter(document['five'], excl, fpu, fpk)
    # if there's a letter that is excluded and in `fpu/fpk`,
    # add it again to `excl` so duplicates are filtered,
    # not simply all occurrences.
    extras = []
    for l in excl:
        if l in fpu:
            extras.append(l)
        if l in fpk:
            extras.append(l)
    excl.extend(extras)

    if len(excl) != 0:
        temp = filter_words(words, "".join(excl), False)
    else:
        temp = words
    if contains_letter(fpk):
        temp = filter_letters_known_position(temp, "".join(fpk))
    if contains_letter(fpu):
        temp = filter_letter_unknown_position(temp, "".join(fpu))
    update_words(temp)
    update_log()
    print_stats_button(None)
    print_button(None)

def simple_help_button(event):
    simple_help_text = """
    Enter the output from Wordle(tm) into the boxes.
    Click on each box to change the color to yellow, green, or black.
    Click on "Filter" to get the output.
    """
    alert(simple_help_text)

def show_adv_controls_button(event):
    document['simple_controls'].hidden = True
    document['advanced_controls'].hidden = False

def show_simple_controls_button(event):
    document['simple_controls'].hidden = False
    document['advanced_controls'].hidden = True

def undo_button(event):
    global words
    global next_log
    if len(previous_words) > 0:
        words = previous_words.pop()
        del document['log-{}'.format(next_log - 1)]
        next_log -= 1
        if next_log == 1:
            document['log_container'].hidden = True
            document['stats'].clear()
            document['output'].clear()
            document['divider'].hidden = True
        else:
            print_stats_button(None)
            print_button(None)

# On page load, the following is executed
words = None
previous_words = list()
next_log = 1
document['filter_incl_button'].bind("click", filter_incl_button)
document['filter_excl_button'].bind("click", filter_excl_button)
document['filter_pos_known_button'].bind("click", filter_pos_known)
document['filter_pos_unknown_button'].bind("click", filter_pos_unknown)
document['adv_help_button'].bind("click", adv_help_button)
document['show_simple_controls_button'].bind("click", show_simple_controls_button)

document['one'].bind("click", text_click)
document['two'].bind("click", text_click)
document['three'].bind("click", text_click)
document['four'].bind("click", text_click)
document['five'].bind("click", text_click)
document['simple_filter_button'].bind("click", simple_filter_button)
document['simple_help_button'].bind("click", simple_help_button)
document['show_adv_controls_button'].bind("click", show_adv_controls_button)

document['undo_button'].bind("click", undo_button)

load_words()
