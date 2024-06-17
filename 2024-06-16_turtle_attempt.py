from turtle import *


setup(800,800)
width(1)
hideturtle()
tracer(False)

penup()
setpos(-25,-25)

pendown()
for i in range(4):
    forward(50)
    left(90)
penup()

setpos(-50,-50)
pendown()
for i in range(4):
    forward(100)
    left(90)

tracer(True)
exitonclick()