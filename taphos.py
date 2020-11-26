"""
taphos.py

The death of a novel.

Copyright 2020 Nathan Mifsud <nathan@mifsud.org>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import json
import markovify
import nltk
import re
import time
from numpy import random
from random import choice

def build_model():
    """
    Here we load the two corpuses, and return a combined Markov model
    whose quality has been improved by using a part-of-speech tagger.
    """
    class POSifiedText(markovify.Text):
        def word_split(self, sentence):
            words = re.split(self.word_split_pattern, sentence)
            words = [ '::'.join(tag) for tag in nltk.pos_tag(words) ]
            return words

        def word_join(self, words):
            sentence = ' '.join(word.split('::')[0] for word in words)
            return sentence

    with open('death-of-the-novel.txt') as f:
        speculations = f.read()
    with open('book-of-the-dead.txt') as f:
        spells = f.read()

    model_a = markovify.Text(speculations)
    model_b = markovify.Text(spells)
    
    model = markovify.combine([model_a, model_b])

    return model


def build_novel(model):
    """
    Here we add stage and chapter headings from a human-written, pre-
    ordered list, and generate some never-before-seen, decomposed prose!
    The text is broken into arbitrary but aesthetically pleasing chunks.
    """
    with open('vars.json') as f:
        vars = json.load(f)

    text = []

    for s in range(3):
        text += '\n\n' + r'\stage{' + str(s+1) + '}{' + vars['stages'].pop(0) + '}'

        for c in range(7):
            text += '\n\n' + r'\section{' + vars['headings'].pop(0) + '}\n'
            chap = []
            step = s*7 + c
            len_chap = random.randint(20,30) + step*2

            for p in range(len_chap):
                para = []
                len_para = random.choice([1,1,1,2,2,2,3,3,4,4,5,5,5,6,7,8])

                for l in range(len_para):
                    para += model.make_sentence() + ' '

                chap += ''.join(para)
                if p < len_chap-1:
                    chap += r'\par '

            chap = ''.join(chap)
            text += decompose(chap, step, vars)

    novel = ''.join(text)

    return novel


def decompose(chap, step, vars):
    """
    Here we invoke different and overlapping decompositional processes
    depending on how far along we are in the sequence. (Note that the
    program logic does not follow the order that becomes perceptible.)
    """
    text = []
    words = chap.split()

    seed = lambda: random.randint(1,10)
    fw = ['decay','medium','semibold','bold','extrabold','black']
    cc = [768,769,771,775,776,777,786,787,795,803,804,806,807,808,823]
   
    # o - deoxygenation                 a - acidification
    # r - reduction                     c - colonisation
    # b - bloat/breakdown               f - font weights

    if   step == 1:  o,a         = 5,2
    elif step == 2:  o,a         = 6,4
    elif step == 3:  o,a         = 7,5
    elif step == 4:  o,a,  c     = 8,6,  1
    elif step == 5:  o,a,  c     = 9,7,  1
    elif step == 6:  o,a,  c     = 9,8,  1
    elif step == 7:  o,a,  c,b,f = 8,9,  1,3,fw[1:2]
    elif step == 8:  o,a,r,c,b,f = 7,9,1,3,3,fw[1:3]
    elif step == 9:  o,a,r,c,b,f = 6,8,2,6,5,fw[1:4]
    elif step == 10: o,a,r,c,b,f = 5,7,2,9,7,fw[1:6]
    elif step == 11: o,a,r,c,b,f = 4,6,2,7,9,fw[2:6]
    elif step == 12: o,a,r,c,b,f = 3,5,3,6,7,fw[0:4]
    elif step == 13: o,a,r,c,b,f = 2,4,4,5,5,fw[0:2]
    elif step == 14: o,a,r,c,b,f = 1,3,4,5,3,fw[0:1]
    elif step == 15:   a,r,c,b,f =   2,4,4,3,fw[0]
    elif step == 16:   a,r,c,b,f =   1,5,4,5,fw[0]
    elif step == 17:     r,c,b,f =     6,3,7,fw[0]
    elif step == 18:     r,c,b,f =     7,2,8,fw[0]
    elif step == 19:     r,c,b,f =     8,1,9,fw[0]
    elif step == 20:     r       =     9

    for word in words:
        # reduction of blood, flesh and bones
            # select alphanumeric characters & any escaping slashes
            # replace with tildes (which LaTeX considers non-breaking space)
            # so by the final step, only punctuation remains
        if (step >= 8) and (seed() <= r):
            x, y = r'[$&%\\\w]', '~'
        else:
            x, y = ' ', ''
        word = [re.sub(x, y, char) for char in word]
        word = ''.join(word)

        # colonisation by carrion insects
            # based on https://codegolf.stackexchange.com/a/57699
            # appends a random mix of combining chars to each letter
        if (6 <= step <= 19) and (word.isalpha()) and (seed() <= c):
            word = ''.join(l + ''.join(choice(list(map(chr,cc)))
                    for i in range(int(random.normal(c, c*2)))) for l in word)

        # cells deprived of oxygen
        if (1 <= step <= 14) and (seed() <= o):
            word = word.replace('o', '')

        # increased carbon dioxide, decreased pH (increased hydrogen ions)
        if (1 <= step <= 16) and (seed() <= a):
            word = word.replace('c', 'CO\sub{2}').replace('h', 'H\sup{+}')

        # for words that aren't deleted...
        if re.compile(r'[^~]').match(word):
            # distension of tissues
            if (7 <= step <= 14) and (seed() <= b):
                word = '{\\' + random.choice(f) + ' ' + word + '}'
            # mummification and accelerated breakdown
            elif (15 <= step <= 19) and (seed() <= b):
                word = '{\\' + f + ' ' + word + '}'
        # for those that are...
        # ...an ugly fix to preserve leading whitespace
        elif re.compile(r'^~+$').match(word):
            word = '\\phantom{' + word + '}'
        else:
            word = '\\phantom{~}' + word

        # make bacterial growth overt
        if (4 <= step <= 18) and (random.randint(1,50) <= c):
            interword = ' {\\textit{' + random.choice(vars['bacteria']) + '}} '
        else:
            interword = ' '

        text += word + interword

    return text


def build_doc(novel):
    """
    Here we use a custom template to generate a completed file, and
    make a conservative estimate of the word count sans LaTeX cruft.
    """
    with open('template.tex') as f:
        doc = f.read().replace('datestamp', time.strftime('%-d %B %Y'))
        doc = doc.replace('output', novel)
        doc = doc.replace(r'\par ', '\n\n') # fix for line buffer issue

    filename = 'taphos-' + time.strftime('%y%m%d-%H%M%S') + '.tex'
    with open(filename, 'w') as f:
        f.write(doc)

    cruft = re.compile(r'[{\\~]')
    words = len([w for w in novel.split() if not cruft.match(w)])
    count = words - words % 1000

    print('Generated ' + filename + ' (~' + str(count) + ' words)')


if __name__ == '__main__':
    build_doc(build_novel(build_model()))