from browser import document, alert
from urllib.request import urlopen
from wordle_tool import sort_letter_position_stats, letter_position_stats, letter_stats_uniq, filter_words, filter_letters_known_position, filter_letter_unknown_position

def load_button(event):
    global words
    document['print_button'].disabled = False
    document['print_stats_button'].disabled = False
    document['filter_incl_button'].disabled = False
    document['filter_excl_button'].disabled = False
    document['filter_pos_known_button'].disabled = False
    document['filter_pos_unknown_button'].disabled = False
    url = './dictionary.txt'
    file = urlopen(url).read()
    new_words = list()
    for line in file.split('\n'):
        new_words.append(line.strip())
    words = new_words
    document['output'].innerHTML = 'Loaded {} words from dictionary file'.format(len(words))


def print_button(event):
    document['output'].innerHTML = ", ".join(words)

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
    document['output'].innerHTML = stats_text

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

def help_button(event):
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

words = list()
document['load_button'].bind("click", load_button)
document['print_button'].bind("click", print_button)
document['print_stats_button'].bind("click", print_stats_button)
document['filter_incl_button'].bind("click", filter_incl_button)
document['filter_excl_button'].bind("click", filter_excl_button)
document['filter_pos_known_button'].bind("click", filter_pos_known)
document['filter_pos_unknown_button'].bind("click", filter_pos_unknown)
document['help_button'].bind("click", help_button)
