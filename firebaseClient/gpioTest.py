
from gpiozero import Button


##### pin definitions

IN1 = 5
OUT1 = 6
IN2 = 13
OUT2 = 19

in1_button = Button(IN1, pull_up=False)
out1_button = Button(OUT1, pull_up=False)
in2_button = Button(IN2, pull_up=False)
out2_button = Button(OUT2, pull_up=False)


def in1():
    print("in1!")

def out1():
    print("out1!")

def in2():
    print("in2!")

def out2():
    print("out2!")


while True:
    pass
