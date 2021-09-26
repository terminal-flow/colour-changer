from tkinter import *
import random
from webcolors import rgb_to_name
import sys
import platform

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

#global storage vars
sentence_list_store = None
col_list_store = None

#functions
def generate():
    txt_get = inpt_txt.get('1.0', 'end-1c')

    sentence_list, col_list = get_lists(txt_get)
    index_list = ['1.0']
    output_txt.delete('1.0', END)
    #loop through sentences and add colour tag per sentence
    for i in range(len(sentence_list)):
        current_col = col_list[i]
        output_txt.insert(END, sentence_list[i])
        #add index position of end of sentence
        index_list.append(output_txt.index('end-1c'))

        output_txt.tag_add(f'{current_col} {i}', index_list[0], index_list[1])
        output_txt.tag_config(f'{current_col} {i}', foreground= current_col)
        #delete used index
        del index_list[0]

#get random rgb colour
def random_colour(previous_col= None):
    colours = [(255, 0, 0), (50, 205, 50), (0, 0, 255), (255, 215, 0)]
    colour = random.choice(colours)
    #remove duplicate colours
    while colour == previous_col:
        colour = random.choice(colours)
    return colour

def get_lists(text):
    global sentence_list_store
    global col_list_store
    #mark sentence position
    indices = [0]
    for i in range(len(text)):
        if text[i] == '.' and len(text) != i+1:
            indices.append(i+1)

    #get list of sentences
    sentence_list = [text[i:j] for i,j in zip(indices, indices[1:]+[None])]

    #get english colour list
    recent = None
    col_list = []
    for i in range(len(sentence_list)):
        rgb = random_colour(recent)
        rgb_name = rgb_to_name(rgb)
        if rgb_name == 'lime':
            rgb_name = 'green'
        col_list.append(rgb_name)
        recent = rgb

    sentence_list_store = sentence_list
    col_list_store = col_list
    return sentence_list, col_list

#translate colour to rtf var
def translate_colour_rtf(col_list_to_translate):
    rtf_col_dic = {'red':'cf1', 'limegreen':'cf2', 'blue':'cf3', 'gold':'cf4'}
    col_list_rtf = []
    for i in range(len(col_list_to_translate)):
        col_list_rtf.insert(i, rtf_col_dic[col_list_to_translate[i]])

    return col_list_rtf

def clear():
    inpt_txt.delete('1.0', END)
    output_txt.delete('1.0', END)

#menu functions
def r_menu_inpt_func(event):
    r_menu_inpt.tk_popup(event.x_root, event.y_root)

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

def cut():
    inpt_txt.event_generate('<<Cut>>')

def copy(text_type):
    select_all(text_type)
    if text_type == 'inpt':
        inpt_txt.event_generate('<<Copy>>')
    else:
        #translate current col_list to rtf
        if sentence_list_store == None and col_list_store == None:
            txt_get = output_txt.get('1.0', 'end-1c')
            sentence_list, col_list = get_lists(txt_get)
            #translate colour name to rtf var
            col_list_rtf = translate_colour_rtf(col_list)
        else:
            #translate colour name to rtf var
            col_list_rtf = translate_colour_rtf(col_list_store)

            #create local sentence list
            sentence_list = sentence_list_store

        #merge each sentences with col_list_rtf
        semi_merge_list = []
        for i in range(len(sentence_list)):
            #restrict to one space
            if sentence_list[i].startswith(' '):
                semi_merge_list.insert(i, f'\\{col_list_rtf[i]}{sentence_list[i]}')
            else:
                semi_merge_list.insert(i, f'\\{col_list_rtf[i]} {sentence_list[i]}')

        #copy text as rtf
        #MacOS
        if platform.system() == 'Darwin':
            from richxerox import pasteboard

            r = ("{\\rtf1\\ansi\\ansicpg1252\\cocoartf2580\n" \
                "\\cocoatextscaling0\\cocoaplatform0{\\fonttbl{\\f0\\fswiss Helvetica;}}\n" \
                "{\\colortbl;\\red255\\green0\\blue0;\\red50\\green205\\blue50;\\red0\\green0\\blue255;\\red255\\green215\\blue0;}\n" \
                "\n\\f0\\fs30" + ' '.join(semi_merge_list) + "}")

            pasteboard.set_contents(text= ''.join(sentence_list), rtf= r)
        #Windows
        elif platform.system() == 'Windows':
            import win32clipboard

            cf_rtf = win32clipboard.RegisterClipboardFormat('Rich Text Format')

            r = ("{\\rtf1\\ansi\\deff0\n" \
                "{\\fonttbl{\\f0\\fswiss Helvetica;}}\n" \
                "{\\colortbl;\\red255\\green0\\blue0;\\red50\\green205\\blue50;\\red0\\green0\\blue255;\\red255\\green215\\blue0;}\n" \
                "\n\\f0\\fs30" + ' '.join(semi_merge_list) + "}")

            r = bytearray(r, 'utf-8')

            win32clipboard.OpenClipboard(0)
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(cf_rtf, r)
            win32clipboard.CloseClipboard()
        #Linux
        elif platform.system() == 'Linux':
            import subprocess

            r = ("{\\rtf1\\ansi\\deff0\n" \
                "{\\fonttbl{\\f0\\fswiss Helvetica;}}\n" \
                "{\\colortbl;\\red255\\green0\\blue0;\\red50\\green205\\blue50;\\red0\\green0\\blue255;\\red255\\green215\\blue0;}\n" \
                "\n\\f0\\fs30" + ' '.join(semi_merge_list) + "}")

            if str(type(r)) == "<class 'str'>":
                r = bytearray(r, 'utf-8')
            subprocess.Popen(['xclip', '-selection', 'clipboard', '-t', 'text/rtf'], stdin= subprocess.PIPE).communicate(r)

    select_none(text_type)

def paste():
    inpt_txt.event_generate('<<Paste>>')
    inpt_txt.delete('end-1c', END)

#input
inpt_txt = Text(root, bg= '#e6e6e6', bd= '5', wrap= 'word', spacing2= '1', highlightcolor= 'white', selectbackground= '#E1F2FF')
inpt_txt.pack(fill= 'both', expand= 'yes', pady= '10', padx= '10')

y_scrollbar_inpt = Scrollbar(inpt_txt, command= inpt_txt.yview)
y_scrollbar_inpt.pack(side= RIGHT, fill= 'y')
inpt_txt.config(yscrollcommand= y_scrollbar_inpt.set)

#buttons
button_frame = Frame(root, bd= '0')

generate_button = Button(button_frame, text= 'Generate', height= '2', padx= '5', command= generate)
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
r_menu_inpt.add_command(label= 'Cut', command= cut)
r_menu_inpt.add_command(label= 'Copy', command= lambda: copy('inpt'))
r_menu_inpt.add_command(label= 'Paste', command= paste)
r_menu_inpt.add_separator()
r_menu_inpt.add_command(label= 'Select All', command= lambda: select_all('inpt'))
r_menu_inpt.add_command(label= 'Deselect All', command= lambda: select_none('inpt'))

inpt_txt.bind('<Button-2>', r_menu_inpt_func)

root.mainloop()