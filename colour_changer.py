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

#menu functions
def r_menu_inpt_func(event):
    r_menu_inpt.tk_popup(event.x_root, event.y_root)

def r_menu_output_func(event):
    r_menu_output.tk_popup(event.x_root, event.y_root)

def select_all(text_type):
    if text_type == 'inpt':
        inpt_txt.event_generate('<<SelectAll>>')
    else:
        output_txt.event_generate('<<SelectAll>>')

def select_none(text_type):
    if text_type == 'inpt':
        inpt_txt.event_generate('<<SelectNone>>')
    else:
        output_txt.event_generate('<<SelectNone>>')

def cut(text_type):
    if text_type == 'inpt':
        inpt_txt.event_generate('<<Cut>>')
    else:
        output_txt.event_generate('<<Cut>>')

def copy(text_type): #needs work!
    select_all(text_type)
    if text_type == 'inpt':
        inpt_txt.event_generate('<<Copy>>')
    else:
        output_txt.event_generate('<<Copy>>')
    select_none(text_type)

def paste(text_type):
    if text_type == 'inpt':
        inpt_txt.event_generate('<<Paste>>')
    else:
        output_txt.event_generate('<<Paste>>')

#input
inpt_txt = Text(root, bg= '#e6e6e6', bd= '5', wrap= 'word', spacing2= '1', highlightcolor= 'white', selectbackground= '#E1F2FF')
inpt_txt.pack(fill= 'both', expand= 'yes', pady= '10', padx= '10')

y_scrollbar_inpt = Scrollbar(inpt_txt, command= inpt_txt.yview)
y_scrollbar_inpt.pack(side= RIGHT, fill= 'y')
inpt_txt.config(yscrollcommand= y_scrollbar_inpt.set)

#buttons
button_frame = Frame(root, bd= '0')

generate_button = Button(button_frame, text= 'Generate', height= '2', padx= '5', command= get_txt)
generate_button.pack(side= LEFT, padx= '10')

copy_button = Button(button_frame, text= 'Copy', height= '2', padx= '5', command= lambda: copy('output'))
copy_button.pack(side= LEFT, padx= '10')

clear_button = Button(button_frame, text= 'Clear', height= '2', padx= '5', command= clear)
clear_button.pack(side= LEFT, padx= '10')

button_frame.pack(pady= '10')

#output
output_txt = Text(root, bg= '#e6e6e6', bd= '5', wrap= 'word', spacing2= '1', highlightcolor= 'white', selectbackground= '#E1F2FF')#, state= 'disabled')
output_txt.pack(fill= 'both', expand= 'yes', pady= '10', padx= '10')

y_scrollbar_output = Scrollbar(output_txt, command= output_txt.yview)
y_scrollbar_output.pack(side= RIGHT, fill= 'y')
output_txt.config(yscrollcommand= y_scrollbar_output.set)

#right click menu input
r_menu_inpt = Menu(inpt_txt, tearoff= '0', fg= 'black')
r_menu_inpt.add_command(label= 'Cut', command= lambda: cut('inpt'))
r_menu_inpt.add_command(label= 'Copy', command= lambda: copy('inpt'))
r_menu_inpt.add_command(label= 'Paste', command= lambda: paste('inpt'))
r_menu_inpt.add_separator()
r_menu_inpt.add_command(label= 'Select All', command= lambda: select_all('inpt'))
r_menu_inpt.add_command(label= 'Deselect All', command= lambda: select_none('inpt'))

inpt_txt.bind('<Button-2>', r_menu_inpt_func)

#right click menu output
r_menu_output = Menu(output_txt, tearoff= '0', fg= 'black')
r_menu_output.add_command(label= 'Cut', command= lambda: cut('output'))
r_menu_output.add_command(label= 'Copy', command= lambda: copy('output'))
r_menu_output.add_separator()
r_menu_output.add_command(label= 'Select All', command= lambda: select_all('output'))
r_menu_output.add_command(label= 'Deselect All', command= lambda: select_none('output'))

output_txt.bind('<Button-2>', r_menu_output_func)

root.mainloop()