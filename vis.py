from environment import Environment
from PIL import Image, ImageTk
from agent import Agent
import tkinter as tk
from threading import Thread
from time import sleep
import tensorflow as tf
import numpy as np

env = Environment()
model = tf.keras.models.load_model('model0')
state = env.reset()

model.summary()

step = 0
running = False

def stop():
    global running
    running = False

def start():
    global running
    running = True
    run()

def run():
    global running
    global step
    global state
    if(running):
        action = np.argmax(model.predict(np.array([state]))[0])

        state, _, _ = env.step(action)
        img = ImageTk.PhotoImage(env.renderState())
        canvas.configure(image=img)
        canvas.image = img
        step += 1
        lbl.configure(text="step: "+str(step))
        lbl.text = "step: "+str(step)

        win.after(75,run)


def reset():
    global step
    global state
    
    state = env.reset()
    img = ImageTk.PhotoImage(env.renderState())
    canvas.configure(image=img)
    canvas.image = img
    step = 0
    lbl.configure(text="step: "+str(step))
    lbl.text = "step: "+str(step)

def key_pressed(event):
    global step
    global state
    if event.keysym=='Right':
        action=2
    elif event.keysym=='Left':
        action=0
    elif event.keysym=='Up':
        action=1
    elif event.keysym=='space':
        action = np.argmax(model.predict(np.array([state]))[0])
    else:
        print(event.keysym)
        action=None
    state, _, _ = env.step(action)
    img = ImageTk.PhotoImage(env.renderState())
    canvas.configure(image=img)
    canvas.image = img
    step += 1
    lbl.configure(text="step: "+str(step))
    lbl.text = "step: "+str(step)

#create a window
win = tk.Tk()
win.geometry("605x650")

#render iamge refrence so that it is not garbage collected
img = ImageTk.PhotoImage(env.renderState())

#UI
canvas = tk.Label(win,width=600,height=600,image=img)
lbl = tk.Label(win,text="step: 0",width=10,height=2)
btn_reset = tk.Button(win,width=8,height=2,text="RESET",command=reset, bg="WHITE")
btn_run = tk.Button(win,width=8,height=2,text="RUN",command=start, bg="GREEN")
btn_stop = tk.Button(win,width=8,height=2,text="STOP",command=stop, bg="RED")

canvas.place(x=0,y=0)
lbl.place(x=0,y=605)
btn_reset.place(x=200,y=605)
btn_run.place(x=275,y=605)
btn_stop.place(x=350,y=605)

win.bind('<Key>',key_pressed)
win.mainloop()
