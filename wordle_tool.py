#
# Wordle Tool copyright rossica 2022
#
#   This program is free software: you can redistribute it and/or modify it
#   under the terms of the GNU General Public License as published by the
#   Free Software Foundation, version 3 of the License.
#
#   This program is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
#   or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
#   more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program. If not, see <https://www.gnu.org/licenses/>.
#
import shlex

def read_words(file_name = "dictionary.txt"):
    f = open(file_name, 'r')
    words = []
    for line in f:
        words.append(line.strip())
    return words

def letter_stats_uniq(words):
    letters = [0] * 26
    for word in words:
        seen = set()
        for c in word:
            if c not in seen:
                letters[ord(c) - ord('A')] +=  1
                seen.add(c)
    return letters

def print_letter_stats(letters, count):
    letter = 65
    for num in letters:
        print("{}: {:.2f}%".format(chr(letter), (num/count)*100))
        letter += 1
    print("total: {} words".format(count))

def sort_letter_stats(letters, count):
    chars = [chr(x+65) for x in range(26)]
    l = list(zip(chars, letters))
    l.sort(key = lambda x: x[1], reverse=True)
    for t in l:
        print("{}: {:.2f}%".format(t[0], (t[1]/count)*100))
    print("total: {} words".format(count))

def word2dict(word):
    d = dict()
    for c in word:
        if c in d:
            d[c] += 1
        else:
            d[c] = 1
    return d

def filter_words(words, filter, containing=True):
    hits = []
    filter_dict = word2dict(filter.upper())
    for word in words:
        match = True
        word_dict = word2dict(word)
        for k in filter_dict.keys():
            if (k not in word_dict or word_dict[k] < filter_dict[k]) == containing:
                match = False
                break
        if match:
            hits.append(word)
    return hits

def filter_letter_unknown_position(words, filter):
    hits = []
    letter = ''
    for c in filter:
        if c != '_':
            letter = c.upper()
            break
    for word in words:
        match = False
        idx = 0
        for c in word:
            if c == filter[idx].upper():
                # This means the filter letter matched in the disallow position
                match = False
                break
            elif c == letter and filter[idx] == '_':
                match = True
            idx += 1
        if match:
            hits.append(word)
    return hits

def filter_letters_known_position(words, filter):
    hits = []
    filter = filter.upper()
    for word in words:
        match = True
        idx = 0
        for c in filter:
            if c == '_':
                pass
            elif c == word[idx]:
                match = True
            else:
                match = False
                break
            idx += 1

        if match:
            hits.append(word)
    return hits

def letter_position_stats(words):
    stats = [[0,0,0,0,0] for x in range(26)]
    for word in words:
        idx = 0
        for c in word:
            stats[ord(c) - ord('A')][idx] += 1
            idx += 1
    return stats

def sort_letter_position_stats(pos_stats, letters, count, all=False):
    chars = [chr(x+65) for x in range(26)]
    l = list(zip(chars, letters, pos_stats))
    l.sort(key = lambda x: x[1], reverse=True)
    div = lambda x,y: x / y if y else 0
    for t in l:
        if all or t[1] > 0:
            print("{}: {: >6.2f}% -> {: >8.1f}{: >8.1f}{: >8.1f}{: >8.1f}{: >8.1f} {: >8}".format(t[0], (t[1]/count)*100, div(t[2][0], t[1])*100, div(t[2][1],t[1])*100, div(t[2][2],t[1])*100, div(t[2][3],t[1])*100, div(t[2][4],t[1])*100, "multi" if sum(t[2]) > t[1] else ''))
    print("total: {} words".format(count))

def print_help():
    print(
    """
Supported commands are:
    help        - prints this text
    load [file] - reloads the default file, or an optional file named <file>
    f [letters] - filters out words containing any of <letters>
    fi [letters]- filters to only words containing *all* of <letters>
    fpu [filt]  - filters out words without the letter. format ___x_
    fpk [filt]  - filters out words without letters in position. format _x___
    p           - prints all current words
    ps [all]    - prints stats on current words, omitting unused letters without <all>.
    undo        - undoes the previous command
    exit        - quit
    """)

def print_words(words):
    print(words)

if __name__ == '__main__':
    print("Welcome to Wordle Tool!")
    print("For help, type `help`.")
    words = None
    previous_words = None
    while True:
        try:
            current_input = input("> ")
        except EOFError:
            break

        if len(current_input) == 0:
            continue
        cmd, *args = shlex.split(current_input)

        if cmd == 'help':
            print_help()
        elif cmd == 'load':
            previous_words = words
            if len(args) == 0:
                words = read_words()
            else:
                words = read_words(args[0])
        elif cmd == 'exit':
            break
        elif cmd == 'f':
            if len(args) != 1:
                print("Invalid args for command `{}`: {}".format(cmd, args))
                continue
            if words == None:
                print("Need to run `load` before `{}` command is valid.".format(cmd))
                continue
            letters = args[0]
            previous_words = words
            words = filter_words(words, letters, False)
        elif cmd == 'fi':
            if len(args) != 1:
                print("Invalid args for command `{}`: {}".format(cmd, args))
                continue
            if words == None:
                print("Need to run `load` before `{}` command is valid.".format(cmd))
                continue
            letters = args[0]
            previous_words = words
            words = filter_words(words, letters)
        elif cmd == 'fpu':
            if len(args) != 1:
                print("Invalid args for command `{}`: {}".format(cmd, args))
                continue
            if words == None:
                print("Need to run `load` before `{}` command is valid.".format(cmd))
                continue
            filter = args[0]
            previous_words = words
            words = filter_letter_unknown_position(words, filter)
        elif cmd == 'fpk':
            if len(args) != 1:
                print("Invalid args for command `{}`: {}".format(cmd, args))
                continue
            if words == None:
                print("Need to run `load` before `{}` command is valid.".format(cmd))
                continue
            filter = args[0]
            previous_words = words
            words = filter_letters_known_position(words, filter)
        elif cmd == 'p':
            if words == None:
                print("Need to run `load` before `{}` command is valid.".format(cmd))
                continue
            print_words(words)
        elif cmd == 'ps':
            all = False
            if len(args) == 1 and args[0] == 'all':
                all = True
            if words == None:
                print("Need to run `load` before `{}` command is valid.".format(cmd))
                continue
            sort_letter_position_stats(letter_position_stats(words), letter_stats_uniq(words), len(words), all)
        elif cmd == 'undo':
            if previous_words == None:
                print("No commands to undo!")
            else:
                words = previous_words
                previous_words = None
        else:
            print("Command {} unrecognized".format(cmd))

    print("Goodbye!")
