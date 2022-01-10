# wordle_tool
A tool to help play the game Wordle.

## Prerequisites
You will need the following before you can unleash the full power of wordle_tool:
- Python 3.8 or newer
- A dictionary file with only 5-letter words, all upper case, one word per line

## How to use wordle_tool

Download wordle_tool.py and put it in the same directory as the dictionary file, prepared as described above.

Open your terminal/command prompt and navigate to the directory with wordle_tool.py and run
```sh
$ python wordle_tool.py
Welcome to Wordle Tool!
For help, type `help`.
>
```

The first thing you need to do is load a dictionary
```sh
> load dictionary.txt
> 
```

The `help` command will print out all the commands with a short description
```
> help

Supported commands are:
    help        - prints this text
    load [file] - reloads the default file, or an optional file named <file>
    f [letters] - filters out words containing any of <letters>
    fi [letters]- filters to only words containing *all* of <letters>
    fpu [filt]  - filters out words without the letter. format ___x_
    fpk [filt]  - filters out words without letters in position. format _x___
    p           - prints all current words
    ps          - prints stats on all current words
    undo        - undoes the previous command
    exit        - quit

>
```
### Command Reference
#### Filter command
The `f` command will filter out all words that have the given letters. Use this for the black letters in Wordle.  All commands are cumulative, so the following command
```
> f asdf
```
is the same as
```
> f a
> f s
> f d
> f f
```

If the list of words was
```
HELLO
JOKER
LACKS
SMILE
```
and you run the command `> f e`
the list of words would be 
```
LACKS
```

#### Filter Inclusive command
The `fi` command is the opposite of the `f` command, it filters out all words that DON'T have the given letters. So given the word list
```
HELLO
JOKER
LACKS
SMILE
```
and you run the command `> fi e`
the list of words would be
```
HELLO
JOKER
SMILE
```

#### Filter Position Unknown command
The `fpu` command is used when you get a yellow letter in Wordle. It will filter out words that don't contain the letter, and words that contain the letter in the given position.
The filter syntax uses underscore, `_`, for the other positions, and then the letter to filter to.  This filter syntax only supports one letter at a time.
```
> fpu ____s
```
Will filter out all words without an 's', and all words that end with 's'.
Given the words
```
HELLO
FLASK
LAKES
SLEET
```
the command `> fpu ____s` will give
```
FLASK
SLEET
```

#### Filter Position Known command
The `fpk` command is used when you get a green letter in Wordle.  It will filter out words that do not contain the letter in the given position.
The filter syntax uses underscore, `_`, for the other positions, and the letter in the known position. This filter syntax supports multiple letters.
The command `> fpk ___e_` will filter out all words without an 'e' in the 4th position.
Given the words
```
HELLO
FLASK
LAKES
SLEET
```
`> fpk ___e_` will give the words
```
LAKES
SLEET
```

#### Print command
The `p` command will print the current words
```
> p
['AAHED', 'AALII', 'AARGH', 'AARTI', 'ABACA', 'ABACI', 'ABACK', 'ABACS', 'ABAFT', 'ABAKA', 'ABAMP', 'ABAND', 'ABASE',
...
'ZOUKS', 'ZOWIE', 'ZULUS', 'ZUPAN', 'ZUPAS', 'ZURFS', 'ZUZIM', 'ZYGAL', 'ZYGON', 'ZYMES', 'ZYMIC']
>
```

#### Print Stats command
The `ps` command will print the letter stats of the current words. It prints the frequency a letter appears at least once is a word, and also the frequency that letter appears in a given position in a word.
It is sorted from the most common letter, to the least common.
```
> ps
S:  45.83% ->     26.6     1.6     8.9     8.8    66.5
E:  44.19% ->      5.2    28.5    15.4    40.9    26.8
A:  41.05% ->     14.0    42.1    23.5    20.1    12.3
R:  30.36% ->     16.1    24.0    30.6    18.3    17.3
O:  30.00% ->      6.9    53.6    25.6    17.6     9.8
I:  27.54% ->      4.6    38.8    29.6    24.2     7.4
L:  24.17% ->     18.3    22.4    27.2    25.1    15.4
T:  23.64% ->     26.7     7.9    20.3    29.8    24.1
N:  21.59% ->     11.8    12.4    34.6    28.1    19.0
U:  18.65% ->      7.6    48.9    27.6    16.3     2.7
D:  17.74% ->     29.4     3.8    16.9    20.4    36.5
Y:  15.64% ->      9.0    13.5    10.3     5.0    64.2
C:  14.75% ->     48.2     9.4    20.3    21.1     6.7
P:  14.56% ->     45.2    12.6    18.9    22.3     8.0
M:  14.47% ->     36.9     9.7    27.5    21.7     9.9
H:  13.08% ->     29.2    32.2     6.6    13.7    21.4
G:  11.84% ->     41.1     4.9    23.7    27.7     9.1
B:  11.60% ->     60.2     5.5    21.8    15.7     3.8
K:  11.00% ->     25.7     6.7    18.4    35.3    17.8
W:   8.04% ->     40.1    15.8    26.4    12.6     6.2
F:   7.64% ->     60.3     2.4    17.6    23.6     8.4
V:   5.15% ->     36.0     8.1    35.2    23.1     0.6
Z:   2.97% ->     26.4     7.5    36.7    32.1     8.4
J:   2.15% ->     71.3     3.4    15.7     9.7     0.7
X:   2.14% ->      5.6    19.9    46.4     4.1    24.3
Q:   0.83% ->     73.1    13.5     9.6     1.0     2.9
total: 12478 words
>
```

#### Undo command
The `undo` command will undo the previous command. There is no history, and you can't undo an `undo`. Used to fix typos while running a command.
