
from gpiozero import Button
from time import sleep

##### pin definitions

IN1 = 6
OUT1 = 13
IN2 = 19
OUT2 = 26

def in1():
    print("in1!")

def out1():
    print("out1!")

def in2():
    print("in2!")

def out2():
    print("out2!")


in1_button = Button(IN1, pull_up=False)
out1_button = Button(OUT1, pull_up=False)
in2_button = Button(IN2, pull_up=False)
out2_button = Button(OUT2, pull_up=False)


in1_button.when_pressed = in1
out1_button.when_pressed = out1
in2_button.when_pressed = in2
out2_button.when_pressed = out2


while True:
    sleep(0.2)
