import tkinter as tk
import os
from tkinter import ttk
from tkinter import scrolledtext
import code_main_vrsion4 as cmv4

win=tk.Tk()
win.title('Github Top Repository')
'''if win.iconbitmap('./icon/icon.ico'):
    pass
else:
    pass'''
win.geometry('825x660')
win.resizable(0,0)
###################################################
def get_topics(): #topics list extracted and added to text_area
    clear_text()
    topics=cmv4.get_topic_title(cmv4.get_topic_page('https://github.com/topics'))
    content=''.join([str(i+1)+' :'+x+'\n' for i,x in enumerate(topics)])
    text_area.insert('end',content)

def clear_text():
    text_area.delete("1.0",tk.END)

def download_topics():
    cmv4.scrape_topics()
    text_area.insert('end', './data/topic/Topics.csv file saved.\n')

def display_selected_repo():
    topics = cmv4.get_topic_title(cmv4.get_topic_page('https://github.com/topics'))
    selected_topic=topic_chose.get().strip()
    if selected_topic=='C++':
        content=cmv4.get_topic_repos(cmv4.get_topic_page('https://github.com/topics'+'/'+'cpp'))
    else:
        content=cmv4.get_topic_repos(cmv4.get_topic_page('https://github.com/topics'+'/'+selected_topic))
    clear_text()
    text_area.insert('end',content)

def download_selected_repo():
    topics = cmv4.get_topic_title(cmv4.get_topic_page('https://github.com/topics'))
    selected_topic=topic_chose.get()
    os.makedirs('./data',exist_ok=True)
    cmv4.scrape_topic('https://github.com/topics/'+selected_topic,'{0}.csv'.format('./data/'+selected_topic))
    if  os.path.exists('data/'+selected_topic+'.csv'):
        text_area.insert('end','./data/{0} file saved.\n'.format(selected_topic))

def download_all_repo():
    text_area.insert('end','Downloading......')
    cmv4.scrape_topics_repos()
    text_area.insert('end','\nDownload completed.')
#########################buttons##########################
buton_frame=tk.LabelFrame(win,text='WELCOME')
buton_frame.pack()
####################buttons###############################
topic_names=tk.Button(buton_frame,text="Top-Topics",command=get_topics,width=30)
topic_names.grid(row=0,column=0,pady=5)
download_topic_names=tk.Button(buton_frame,text="Download-Topics",command=download_topics,width=30)
download_topic_names.grid(row=0,column=1,pady=5)
selected_topic_repo_display=tk.Button(buton_frame,text="Display_Selected_Repository",command=display_selected_repo,width=30)
selected_topic_repo_display.grid(row=0,column=2,pady=5)
selected_topic_repo_download=tk.Button(buton_frame,text="Download-Selected-Repository",command=download_selected_repo,width=30)
selected_topic_repo_download.grid(row=1,column=0,pady=5)
download_all_repo=tk.Button(buton_frame,text="Download-All",command=download_all_repo,width=30)
download_all_repo.grid(row=1,column=2,pady=5)
###########select-topic from combo box########################
s_topic=tk.StringVar()
tk.Label(buton_frame,text='Chose the topic :').grid(row=1,column=1)
topic_chose=ttk.Combobox(buton_frame,width=30,textvariable=s_topic,state='readonly')
topic_chose['values']=cmv4.get_topic_title(cmv4.get_topic_page('https://github.com/topics'))
topic_chose.current(0)
# topic_chose.configure(state='readonly')
topic_chose.grid(row=2,column=1)
####################Display-Area#########################
scroll_w=100
scrol_h=20
# scr=scrolledtext.ScrolledText(buton_frame,width=scroll_w,height=scrol_h,wrap=tk.WORD)
# scr.grid(column=0,columnspan=3)
text_area=tk.Text(buton_frame,width=scroll_w,height=scrol_h)
text_area.grid(column=0,columnspan=3)
####################Display-Area#########################
######################Made-By###########################
intro=tk.LabelFrame(win,text='Intro')
how_to=tk.LabelFrame(win,text='How To Use')
how_to.pack()
intro.pack()
text_intro=tk.Label(intro,width=114,height=5,state='normal')
text_intro.grid(row=0,columnspan=3)
text_intro.configure(text=f'Designed By :\n{"1. Vishnu kumar 12017539"}\n{"2. Payal 12016203"}\n{"3. Lipsika"}',justify=tk.LEFT)

use=tk.Text(how_to,width=100,height=6,state='normal')
use.grid(row=0,columnspan=3)
msg='\t\t\t\t\tHOW TO USE :\nTop-TOPICS :click to get all top topics in github repository.\n' \
    'DOWNLOAD-TOPICS :click to download list of topics.\n' \
    'DISPLAY-SELECTED-REPO :select any repo from COMBOBOX and click this button to see the contents.\n' \
    'DOWNLOAD-SELECTED-REPO :click this button to download selected repo insted of displaying it.\n' \
    'DOWNLOAD-ALL :click this to download all repository corresponding to their topic.'
use.insert('end',msg)
use.configure(state='disabled')

######################Made-By###########################



win.resizable(False,False)
win.mainloop()