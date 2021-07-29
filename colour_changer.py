from tkinter import *
import random
from webcolors import rgb_to_name

#get current screen w + h
def get_curr_screen_geometry():
    window = Tk()
    window.update_idletasks()
    window.attributes('-fullscreen', True)
    window.state('iconic')
    width = window.winfo_width()
    height = window.winfo_height()

    #resize to w:30%, h:50%
    default_width = int(width * 0.25)
    default_height = int(height * 0.5)
    #resize to 75% of default
    min_width = int(default_width * 0.75)
    min_height = int(default_height * 0.75)

    default_txt = f'{default_width}x{default_height}'

    window.attributes('-fullscreen', False)
    window.destroy()
    return default_txt, min_width, min_height

#main
root = Tk()
root.title('Colour Changer')
default_geom, min_width, min_height = get_curr_screen_geometry()
root.minsize(width= min_width, height= min_height)
root.geometry(default_geom)

#functions
def get_txt():
    txt_get = inpt_txt.get('1.0', 'end-1c')

    sentences, col_list = get_sentences(txt_get)
    index_list = ['1.0']
    #output_txt.config(state= 'normal')
    output_txt.delete('1.0', END)
    for i in range(len(sentences)):
        current_col = col_list[i]
        output_txt.insert(END, sentences[i])
        #add index position of end of sentence
        index_list.append(output_txt.index('end-1c'))

        output_txt.tag_add(f'{current_col} {i}', index_list[0], index_list[1])
        output_txt.tag_config(f'{current_col} {i}', foreground= current_col)
        del index_list[0]
    #output_txt.config(state= 'disabled')

#get random rgb colour
def random_colour(previous_col= None):
    colours = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
    colour = random.choice(colours)
    #remove duplicate colours
    while colour == previous_col:
        colour = random.choice(colours)
    return colour

def get_sentences(text):
    #mark sentence position
    indices = [0]
    for i in range(len(text)):
        if text[i] == '.' and len(text) != i+1:
            indices.append(i+1)

    #get list of sentences
    sentences = [text[i:j] for i,j in zip(indices, indices[1:]+[None])]

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

    return sentences, col_list

def clear():
    inpt_txt.delete('1.0', END)
    output_txt.delete('1.0', END)


inpt_txt = Text(root, bg= '#e6e6e6', bd= '5', wrap= 'word', spacing2= '1', highlightcolor= 'white', selectbackground= '#E1F2FF')
inpt_txt.pack(fill= 'both', expand= 'yes', pady= '10', padx= '10')

y_scrollbar_inpt = Scrollbar(inpt_txt, command= inpt_txt.yview)
y_scrollbar_inpt.pack(side= RIGHT, fill= 'y')
inpt_txt.config(yscrollcommand= y_scrollbar_inpt.set)

button_frame = Frame(root, bd= '0')

generate_button = Button(button_frame, text= 'Generate', height= '2', padx= '5', command= get_txt)
generate_button.pack(side= LEFT, padx= '10')

copy_button = Button(button_frame, text= 'Copy', height= '2', padx= '5', command= None)
copy_button.pack(side= LEFT, padx= '10')

clear_button = Button(button_frame, text= 'Clear', height= '2', padx= '5', command= clear)
clear_button.pack(side= LEFT, padx= '10')

button_frame.pack(pady= '10')

output_txt = Text(root, bg= '#e6e6e6', bd= '5', wrap= 'word', spacing2= '1', highlightcolor= 'white', selectbackground= '#E1F2FF')#, state= 'disabled')
output_txt.pack(fill= 'both', expand= 'yes', pady= '10', padx= '10')

y_scrollbar_output = Scrollbar(output_txt, command= output_txt.yview)
y_scrollbar_output.pack(side= RIGHT, fill= 'y')
output_txt.config(yscrollcommand= y_scrollbar_output.set)

root.mainloop()