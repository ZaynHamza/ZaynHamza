import time
from tkinter import *
from tkinter import filedialog
import pygame                   # pip install pygame
from mutagen.mp3 import MP3     # pip install mutagen
import tkinter.ttk as ttk

root = Tk()
root.title(" Zayn Music Player")
root.iconbitmap("C:/Users/Zayn Hamza/PycharmProjects/musicp/icon.ico")
root.geometry("590x540")

# Initialize pygame mixer
pygame.mixer.init()


# Grab song length info
def play_time():
    # Avoid double timing
    if stopped:
        return
    current_time = pygame.mixer.music.get_pos() / 1000
    # throw up temp label to get data
    # slider_label.config(text=f"Slider: {int(slider.get())} and Song Pos: {int(current_time)}")
    # Convert time format
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
    song = song_box.get(ACTIVE)
    song = f"D:/Old Stuff/Local Disk (F)/Music (Videoclips)/{song}.mp3"
    song_mut = MP3(song)
    global song_length
    song_length = song_mut.info.length
    converted_song_long = time.strftime('%M:%S', time.gmtime(song_length))
    # Update slider position
    current_time += 1

    if int(slider.get()) == int(song_length):
        status_bar.config(text=f"{converted_song_long} / {converted_song_long}")
    elif paused:
        pass
    elif int(slider.get()) == int(current_time):
        slider_position = int(song_length)
        slider.config(to=slider_position, value=int(current_time))
    else:
        slider_position = int(song_length)
        slider.config(to=slider_position, value=int(slider.get()))
        # Convert time format
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(slider.get())))
        status_bar.config(text=f"{converted_current_time} / {converted_song_long}")
        next_time = int(slider.get()) + 1
        slider.config(value=next_time)
    status_bar.after(1000, play_time)


def add_songs():
    songs = filedialog.askopenfilenames(initialdir="D:/Old Stuff/Local Disk (F)/Music (Videoclips)", title="Choose a song", filetypes=(("mp3 Files", "*.mp3"), ))
    for song in songs:
        # Remove everything except artist & song names
        song = song.split("/")
        song = song[-1]
        song = song.replace(".mp3", "")
        # Add to the list box
        song_box.insert(END, song)


# Delete one song
def delete_song():
    stop()
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()


# Clear playlist
def clear_all():
    stop()
    song_box.delete(0, END)
    pygame.mixer.music.stop()


# Create slider
def slide(x):
    # slider_label.config(text=f"{int(slider.get())} / {int(song_length)}")
    song = song_box.get(ACTIVE)
    song = f"D:/Old Stuff/Local Disk (F)/Music (Videoclips)/{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(slider.get()))


# Create volume func
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())
    current_volume = pygame.mixer.music.get_volume()
    current_volume = current_volume * 100
    # slider_label.config(text=current_volume * 100)
    if current_volume < 1:
        volume_meter.config(image=vol0)

    elif 0 < int(current_volume) <= 35:
        volume_meter.config(image=vol35)

    elif 35 < int(current_volume) <= 70:
        volume_meter.config(image=vol70)

    elif 75 < int(current_volume) <= 100:
        volume_meter.config(image=vol100)


# Play selected song
def play():
    global stopped
    stopped = False
    song = song_box.get(ACTIVE)
    song = f"D:/Old Stuff/Local Disk (F)/Music (Videoclips)/{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    # Call the play time function to get song length
    play_time()
    # Update slider position
    # slider_position = int(song_length)
    # slider.config(to=slider_position, value=0)
    # Get current volume
    # current_volume = pygame.mixer.music.get_volume()
    # slider_label.config(text=current_volume * 100)


global stopped
stopped = False


def stop():
    # Reset slider and status bar
    status_bar.config(text='')
    slider.config(value=0)

    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)

    global stopped
    stopped = True


# Create global pause variable
global paused
paused = False


def pause(is_paused):
    global paused
    paused = is_paused
    if paused:
        # We should unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        # We should pause
        pygame.mixer.music.pause()
        paused = True


def next_song():
    # Get the current song tuple index and add 1 to it
    next_song = song_box.curselection()
    next_song = next_song[0]+1
    song = song_box.get(next_song)
    song = f"D:/Old Stuff/Local Disk (F)/Music (Videoclips)/{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    # Selection
    song_box.selection_clear(0, END)
    song_box.activate(next_song)
    song_box.selection_set(next_song, last=None)
    slider_position = int(song_length)
    slider.config(to=slider_position, value=0)


def previous():
    # Get the current song tuple index and subtract 1 from it
    previous_song = song_box.curselection()
    previous_song = previous_song[0]-1
    song = song_box.get(previous_song)
    song = f"D:/Old Stuff/Local Disk (F)/Music (Videoclips)/{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    # Selection
    song_box.selection_clear(0, END)
    song_box.activate(previous_song)
    song_box.selection_set(previous_song, last=None)
    slider_position = int(song_length)
    slider.config(to=slider_position, value=0)


# Create master frame
master_frame = Frame(root)
master_frame.pack(pady=20)

# Create playlist box
song_box = Listbox(master_frame, bg="black", fg="grey", width=70, height=19, selectbackground="grey", selectforeground="black")
song_box.grid(row=0, column=0)

# Define player control buttons icons
play_icon = PhotoImage(file="C:/Users/Zayn Hamza/PycharmProjects/musicp/play.png")
pause_icon = PhotoImage(file="C:/Users/Zayn Hamza/PycharmProjects/musicp/pause.png")
stop_icon = PhotoImage(file="C:/Users/Zayn Hamza/PycharmProjects/musicp/stop.png")
next_song_icon = PhotoImage(file="C:/Users/Zayn Hamza/PycharmProjects/musicp/forward.png")
backward_icon = PhotoImage(file="C:/Users/Zayn Hamza/PycharmProjects/musicp/backward.png")

# Define volume control images
vol0 = PhotoImage(file="C:/Users/Zayn Hamza/PycharmProjects/musicp/0%.png")
vol35 = PhotoImage(file="C:/Users/Zayn Hamza/PycharmProjects/musicp/35%.png")
vol70 = PhotoImage(file="C:/Users/Zayn Hamza/PycharmProjects/musicp/70%.png")
vol100 = PhotoImage(file="C:/Users/Zayn Hamza/PycharmProjects/musicp/100%.png")

# Create player control frame
controls_frame = Frame(master_frame)
controls_frame.grid(row=1, column=0)

# Create volume meter
volume_meter = Label(master_frame, image=vol100)
volume_meter.grid(row=1, column=1)

# Create volume label frame
volume_frame = LabelFrame(master_frame, text="Volume")
volume_frame.grid(row=0, column=1, padx=30)

# Create player control buttons
play_btn = Button(controls_frame, image=play_icon, borderwidth=0, command=play)
pause_btn = Button(controls_frame, image=pause_icon, borderwidth=0, command=lambda: pause(paused))
stop_btn = Button(controls_frame, image=stop_icon, borderwidth=0, command=stop)
next_song_btn = Button(controls_frame, image=next_song_icon, borderwidth=0, command=next_song)
backward_btn = Button(controls_frame, image=backward_icon, borderwidth=0, command=previous)

backward_btn.grid(row=0, column=1)
stop_btn.grid(row=0, column=2)
play_btn.grid(row=0, column=3)
pause_btn.grid(row=0, column=4)
next_song_btn.grid(row=0, column=5)

# Create menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Add add song menu
file_menu = Menu(my_menu)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Add songs to playlist", command=add_songs)
file_menu.add_command(label="Remove song", command=delete_song)
file_menu.add_command(label="Clear playlist", command=clear_all)

# Create status bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# Create music slider
slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=350)
slider.grid(row=2, column=0, pady=20)

# Create volume slider
volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, value=1, command=volume, length=200)
volume_slider.pack(pady=10)

# Create temporary slider label
slider_label = Label(root, text="0")
slider_label.pack(pady=10)

root.mainloop()
