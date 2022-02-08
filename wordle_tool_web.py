from turtle import width
from browser import document, alert, html
from urllib.request import urlopen
from wordle_tool import IsLetter, sort_letter_position_stats, letter_position_stats, letter_stats_uniq, filter_words, filter_letters_known_position, filter_letter_unknown_position

INPUT_BLACK = "inputblack"
INPUT_YELLOW = "inputyellow"
INPUT_GREEN = "inputgreen"

def load_words():
    global words
    url = './dictionary.txt'
    file = urlopen(url).read()
    new_words = list()
    for line in file.split('\n'):
        new_words.append(line.strip())
    words = new_words

def load_button(event):
    load_words()
    global words
    document['output'].innerHTML = 'Loaded {} words from dictionary file'.format(len(words))

def print_button(event):
    document['output'].innerHTML = " ".join(words)

def print_stats_button(event):
    global words
    count = len(words)
    div = lambda x,y: x / y if y else 0
    stats = sort_letter_position_stats(letter_position_stats(words), letter_stats_uniq(words))
    stats_text = "<table><tr><th>Letter</th><th>Frequency</th><th>1st Freq.</th><th>2nd Freq.</th><th>3rd Freq.</th><th>4th Freq.</th><th>5th Freq.</th><th>Multi</th></tr>"
    for t in stats:
        if t[1] > 0:
            stats_text += "<tr><td>{}</td><td>{:.2f}</td><td>{:.1f}</td><td>{:.1f}</td><td>{:.1f}</td><td>{:.1f}</td><td>{:.1f}</td><td>{}</td></tr>".format(t[0], (t[1]/count)*100, div(t[2][0], t[1])*100, div(t[2][1],t[1])*100, div(t[2][2],t[1])*100, div(t[2][3],t[1])*100, div(t[2][4],t[1])*100, "X" if sum(t[2]) > t[1] else '')
    stats_text += "</table>"
    document['stats'].innerHTML = stats_text

def filter_incl_button(event):
    global words
    words = filter_words(words, document["cmd"].value)
    document['output'].innerHTML = "{} words remaining".format(len(words))

def filter_excl_button(event):
    global words
    words = filter_words(words, document["cmd"].value, False)
    document['output'].innerHTML = "{} words remaining".format(len(words))

def filter_pos_known(event):
    global words
    words = filter_letters_known_position(words, document["cmd"].value)
    document['output'].innerHTML = "{} words remaining".format(len(words))

def filter_pos_unknown(event):
    global words
    words = filter_letter_unknown_position(words, document["cmd"].value)
    document['output'].innerHTML = "{} words remaining".format(len(words))

def adv_help_button(event):
    help_text = """
    Load                    - Loads dictionary file
    Print                   - Shows all filtered words
    Print stats             - Prints stats for filtered words
    Filter (incl.)          - Filters to words containing letters
    Filter (excl.)          - Filters out words containing letters
    Filter position known   - Filters to words with letters in given position.
        e.g. __a__. Allows multiple letters, e.g. ___ly.
    Filter position unknown - Filter to words with letter not in position
        e.g. _b___. Only one letter at a time
    """
    alert(help_text)

def text_click(event):
    if event.currentTarget.class_name == INPUT_BLACK:
        event.currentTarget.class_name = INPUT_YELLOW
    elif event.currentTarget.class_name == INPUT_YELLOW:
        event.currentTarget.class_name = INPUT_GREEN
    else:
        event.currentTarget.class_name = INPUT_BLACK

def update_log():
    document['log'].hidden = False
    t = html.TABLE()
    t <= html.TR(
        html.TD(document['one'].value, Class=document['one'].class_name) +
        html.TD(document['two'].value, Class=document['two'].class_name) +
        html.TD(document['three'].value, Class=document['three'].class_name) +
        html.TD(document['four'].value, Class=document['four'].class_name) +
        html.TD(document['five'].value, Class=document['five'].class_name))
    document['log'] <= t
    # document['log'] <= html.DIV(document['one'].value, Class=document['one'].class_name, width="1em")
    # document['log'] <= html.DIV(document['two'].value, Class=document['two'].class_name, width="1em")
    # document['log'] <= html.DIV(document['three'].value, Class=document['three'].class_name, width="1em")
    # document['log'] <= html.DIV(document['four'].value, Class=document['four'].class_name, width="1em")
    # document['log'] <= html.DIV(document['five'].value, Class=document['five'].class_name, width="1em")


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
    if len(extras) > 0:
        excl.extend(extras)

    if len(excl) != 0:
        temp = filter_words(words, "".join(excl), False)
    else:
        temp = words
    if contains_letter(fpk):
        temp = filter_letters_known_position(temp, "".join(fpk))
    if contains_letter(fpu):
        temp = filter_letter_unknown_position(temp, "".join(fpu))
    words = temp
    update_log()
    print_stats_button(None)
    print_button(None)

def simple_help_button(event):
    pass

def show_adv_controls_button(event):
    document['simple_input'].hidden = True
    document['advanced_input'].hidden = False

# On page load, the following is executed
words = list()
document['load_button'].bind("click", load_button)
document['print_button'].bind("click", print_button)
document['print_stats_button'].bind("click", print_stats_button)
document['filter_incl_button'].bind("click", filter_incl_button)
document['filter_excl_button'].bind("click", filter_excl_button)
document['filter_pos_known_button'].bind("click", filter_pos_known)
document['filter_pos_unknown_button'].bind("click", filter_pos_unknown)
document['adv_help_button'].bind("click", adv_help_button)

document['one'].bind("click", text_click)
document['two'].bind("click", text_click)
document['three'].bind("click", text_click)
document['four'].bind("click", text_click)
document['five'].bind("click", text_click)
document['simple_filter_button'].bind("click", simple_filter_button)
document['simple_print_button'].bind("click", print_button)
document['simple_print_stats_button'].bind("click", print_stats_button)
document['simple_help_button'].bind("click", simple_help_button)
document['show_adv_controls_button'].bind("click", show_adv_controls_button)

load_words()