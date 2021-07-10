import random
from webcolors import rgb_to_name
from termcolor import colored

text = input('Input text: ')

#mark sentence position
indices = [0]
for i in range(len(text)):
    if text[i] == '.' and len(text) != i+1:
        indices.append(i+1)

#get list of sentences
sentences = [text[i:j] for i,j in zip(indices, indices[1:]+[None])]

#get random rgb colour
def random_colour(previous_col= None):
    colours = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
    colour = random.choice(colours)
    #remove duplicate colours
    while colour == previous_col:
        colour = random.choice(colours)
    return colour

#get english colour list
recent = None
col_list = []
for i in range(len(sentences)):
    rgb = random_colour(recent)
    rgb_name = rgb_to_name(rgb)
    if rgb_name == 'lime':
        rgb_name = 'green'
    col_list.append(rgb_name)
    recent = rgb

#print coloured text out in terminal
for i in range(len(sentences)):
    current_col = col_list[i]
    output = colored(sentences[i], current_col)
    print(output, end= '\n' if i+1 == len(sentences) else '')