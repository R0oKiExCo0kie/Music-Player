#Importing Modules
from tkinter import *
#For Music
import pygame as pg
from tkinter import filedialog
import time
#For the music playtime
from mutagen.mp3 import MP3
from tkinter import ttk
import os
import traceback

global playing
playing=False
global paused
paused=False
global song_length
song_length = 0 

window=Tk()
#window.resizable(False,False)
window.title("Music Player 🎶")
pg.mixer.init()
songs=[]
#song adding function
def add_song():
    global song_dir
    global current_song
    global song_list
    global my_menu
    song_dir=filedialog.askdirectory(title="Select Folder",initialdir="~/Downloads/")
    for song in os.listdir(song_dir):
        name,ext=os.path.splitext(song)
        if ext==".mp3":
          song_list.insert(END,name)
    path=os.path.basename(song_dir)
    window.title(path)
    my_menu.entryconfig(1,state="disabled")
    my_menu.entryconfig(2,state="normal")
    back_btn.config(state="normal")
    play_pause_btn.config(state="normal")
    next_btn.config(state="normal")
    song_list.select_set(0)
    song_list.activate(0)
    pos_slider.config(value=0)

#to restrict mouse clicks on listboxes
def no_op( event):
        return "break"

#delete a song function
def delete_song():
        stop()
        global playing,paused,stopped
        playing=False
        paused =False
        play_pause_btn.config(command=playy, image=pla)
        play_pause_btn.config(state="normal")
        song_list.delete(ACTIVE)
        song_list.select_set(0)
        song_list.activate(0)
        song=song_list.get(ACTIVE)
        status_label.config(text=song)
        if song_list.size()==0:
                    my_menu.entryconfig(1,state="normal")
                    my_menu.entryconfig(2,state="disabled")
                    back_btn.config(state="disabled")
                    play_pause_btn.config(state="disabled")
                    next_btn.config(state="disabled")  


     
#delete all songs function
def delete_all_songs():
    play_pause_btn.config(command=playy, image=pla)
    stop()

    status_label.config(text="")
    song_list.delete(0,END)
    pg.mixer_music.fadeout(1)
    my_menu.entryconfig(1,state="normal")
    my_menu.entryconfig(2,state="disabled")
    back_btn.config(state="disabled")
    play_pause_btn.config(state="disabled")
    next_btn.config(state="disabled")    

#Play time
def play_time():
    try:
        if stopped:
             return
        current_time = pg.mixer.music.get_pos()/1000
        converted_time=time.strftime('%M:%S',time.gmtime(current_time))
        #getting song length
        song = status_label.cget("text")
        song=os.path.join(song_dir,song+".mp3")
        mut_song=MP3(song)
        global song_length
        song_length=mut_song.info.length
        converted_length=time.strftime('%M:%S',time.gmtime(song_length))
        current_time+=1
        if paused:
            pass
        elif int(pos_slider.get())==int(song_length):
            status_bar.config(text=f"{converted_time} of {converted_length}")

        elif int(pos_slider.get()) == int(current_time):
            pos_slider.config(value=int(current_time),to=int(song_length))
        else:
            pos_slider.config(value=int(pos_slider.get()),to=int(song_length))
            converted_time=time.strftime('%M:%S',time.gmtime(int(pos_slider.get())))
            status_bar.config(text=f"{converted_time} of {converted_length}")
            #move slider by 1 sec
            global sec
            sec=int(pos_slider.get())+1
            pos_slider.config(value=sec)
    
    
    # status_bar.config(text=f"{converted_time} of {converted_length}")
    #Update Slider POsition Value to current time
  
   
    #new updated time
        status_bar.after(1000,play_time)
    except Exception as e:
        traceback.print_exc()
        print("An error occurred: ", e)

#stop function
global stopped
stopped=False
def stop():
    global stopped
    stopped=True
    status_bar.config(text="")
    pos_slider.config(value=0)
    pg.mixer.music.stop()
    song_list.selection_clear(ACTIVE)
    status_bar.config(text="")

    #CLEARING THE STATUS
                      
#buttons functions
def backk():
     global song_dir
     try:
         global song_list
         song=song_list.get(ACTIVE)
         next_song=song_list.curselection()
         if next_song[0]-1<0:
              pass
         else:
            next_one=next_song[0]-1
            song_list.see(next_one)
            song=song_list.get(next_one)
            if status_label.cget("text") == song and not paused:
                play_pause_toggle()
            else:
                if status_label.cget("text") == song:
                        play_pause_btn.config(command=pausee,image=pla)
                else:
                    global playing
                    play_pause_btn.config(command=playy, image=pla)
                    playing = False 
            song_list.selection_clear(0,END)
            song_list.activate(next_one)
            song_list.selection_set(next_one,last=None)
     except:
        song_list.activate(0)
        song_list.selection_set(0, last=None)

def nextt():
        global song_dir
        global song_list
        song=song_list.get(ACTIVE)
        next_song=song_list.curselection()
        if next_song:
            try:
                if next_song[0]+1>=song_list.size():
                    pass
                else:
                    next_one=next_song[0]+1
                    song_list.see(next_one)
                    song=song_list.get(next_one)
                    if status_label.cget("text") == song and not paused:
                        play_pause_toggle()
                    else:
                        if status_label.cget("text") == song:          
                            play_pause_btn.config(command=pausee,image=pla)
                        else:
                                global playing
                                play_pause_btn.config(command=playy, image=pla)
                                playing = False 

                    song_list.selection_clear(0,END)
                    song_list.activate(next_one)
                    song_list.selection_set(next_one,last=None)
            except:
                 pass
        else:
            song_list.activate(0)
            song_list.selection_set(0, last=None)



def playy():
        global paused, playing, stopped
        paused = False
        stopped=False
        song=song_list.get(ACTIVE)
        pos_slider.config(value=0)
        global song_dir
        try: 
            status_label.config(text=song)
            pg.mixer_music.load(os.path.join(song_dir,song+".mp3"))
            global playing
            if not playing and not stopped:
                        pg.mixer.music.play()
                        if not song_length:  # Only schedule play_time if it hasn't been scheduled yet
                            play_time()
                            
                        status_label.config(text=song)
                        play_pause_toggle()
##                    song_position=int(song_length)  
        except Exception as e:
                    print(e)
      
def pausee():
     global paused
     if paused == False:
        pg.mixer_music.pause()
        paused =True
        play_pause_btn.config(image=pla)
     else:
            pg.mixer_music.unpause()
            paused=False
            play_pause_btn.config(image=pau)
vol_bool=False
def vol():
     global vol_bool
     if vol_bool == False:
         window.geometry("550x600")
         vol_bool =True
     else:
          window.geometry("500x600")
          vol_bool=False

# Add a global variable to track if the slider is being dragged

# Function to handle slider value change
def on_slider_change(event):
    global dragging_slider ,dragged
    dragging_slider = True
    

# Function to handle slider release
def on_slider_release(event):
    global dragging_slider ,dragged
    dragging_slider = False
    if not paused:  # Only load/play if the music is not paused
        song = status_label.cget("text")
        song = os.path.join(song_dir, song + ".mp3")
        pg.mixer_music.load(song)
        pg.mixer_music.play(start=int(pos_slider.get()))
        
# Update your slider binding

def volume(x):
    pg.mixer.music.set_volume((vol_slider.get()/100))

def play_pause_toggle():
    global playing
    if playing:
        play_pause_btn.config( command=playy, image=pla)
        playing = False
        # Add the logic to pause the song here
    else:
        play_pause_btn.config( command=pausee, image=pau)
        playing = True
        # Add the logic to play the song here

res=False
#button images
bac=PhotoImage(file="assets/default/previous.png")
nex=PhotoImage(file="assets/default/next.png")
pla=PhotoImage(file="assets/default/play.png")
pau=PhotoImage(file="assets/default/pause.png")

#listbox and volume frame
display_frame=Frame(window)
display_frame.pack()
#playlist bg=PISTACHIO
window.geometry("500x600")
song_list=Listbox(display_frame,bg="#33ccff",fg="black",width=61,height=20,selectbackground="black",font="Calibri 12",selectforeground="white",activestyle=None)
song_list.grid(padx=5,row=0,column=0)
song_list.bind("<1>",no_op)  # Left mouse button click
song_list.bind("<Double-1>",no_op)  # Double left mouse button click
song_list.bind("<B1-Motion>",no_op)


wong_list=[]
#music_volume slider

vol_slider=ttk.Scale(display_frame,from_=100,to=0,value=50,orient=VERTICAL,length=400,command=volume)
vol_slider.grid(padx=10,row=0,column=1,sticky=E)
#=====

songg=""
status_label=Label(window)
status_label.pack()
#-----

#Play Time status
status_bar=Label(window,text='',bd=1,relief=GROOVE,anchor=E)
status_bar.pack(fill=X,ipady=2,side=BOTTOM)

#POsition SLider
pos_slider=ttk.Scale(window,from_=0,to=100,length=400,orient=HORIZONTAL,value=0)
pos_slider.pack(pady=10)
pos_slider.bind("<B1-Motion>", on_slider_change)
pos_slider.bind("<ButtonRelease-1>", on_slider_release)

#Control panel with buttons

control_panel=Frame(window)
control_panel.pack()
global back_btn
global next_btn
global play_pause_btn
back_btn=Button(control_panel,image=bac,command=backk,borderwidth=0)
back_btn.grid(row=0,column=0,padx=10)
next_btn=Button(control_panel,image=nex,command=nextt,borderwidth=0)
next_btn.grid(row=0,column=3,padx=5)
play_pause_btn=Button(control_panel,image=pla,command=playy,borderwidth=0)
play_pause_btn.grid(row=0,column=2,padx=10)

##loop_btn=Button(control_panel,text="Loop",command=loop)
##loop_btn.grid(row=0,column=4,padx=10)


###############THEMES###################################

def neon_theme():
    window.configure(bg="#000000")
    back_btn.config(bg="#00FFD1", activebackground="#00FFD1")  # Cyan
    play_pause_btn.config(bg="#FF00FF", activebackground="#FF00FF")  # Magenta
    next_btn.config(bg="#FFD700", activebackground="#FFD700")  # Gold
    display_frame.config(bg="#000000")
    control_panel.config(bg="#000000")
    song_list.config(bg="#000000", fg="#00FFD1", selectbackground="blue")
    # PhotoImage paths
    global bac, nex, pla
    bac = PhotoImage(file="assets/neon/previous.png")
    nex = PhotoImage(file="assets/neon/next.png")
    pla = PhotoImage(file="assets/neon/play.png")
    # Apply images and configure buttons
    back_btn.config(image=bac)
    play_pause_btn.config(image=pla)
    next_btn.config(image=nex)
    # Status label
    status_label.config(bg="#000000", fg="#00FFD1")  

#==================================================
back_btn.config(state="disabled")
play_pause_btn.config(state="disabled")
next_btn.config(state="disabled")

#menu
global add_song_menu
my_menu=Menu(window)
window.config(menu=my_menu)
#creating menu buttons 
add_song_menu=Menu(my_menu,tearoff=False)
delete_song_menu=Menu(my_menu,tearoff=False)
volume=Menu(my_menu,tearoff=False)
add_themes=Menu(my_menu,tearoff=False)
#menu cascading
my_menu.add_cascade(label="File",menu=add_song_menu)
my_menu.add_cascade(label="Remove songs",menu=delete_song_menu)
my_menu.add_cascade(label="Volume",command=vol)
my_menu.add_cascade(label="Theme",menu=add_themes)
#adding submenu_label
add_song_menu.add_command(label="Select Folder",command=add_song)
delete_song_menu.add_command(label="Delete a song",command=delete_song)
delete_song_menu.add_command(label="Delete all the songs",command=delete_all_songs)
add_themes.add_command(label="Neon",command=neon_theme)
my_menu.entryconfig(2,state="disabled")

window.mainloop()

