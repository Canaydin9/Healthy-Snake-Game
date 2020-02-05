import turtle
#import tkinter
import time
import random

delay = 0.1
image_face = "/Users/canaydin/Desktop/output3.gif"
image_foodbad = "/Users/canaydin/Desktop/hamburger1.gif"
image_food = "/Users/canaydin/Desktop/download.gif"
screen_y = 500
screen_x = 500
coll_dist = 30/2 + 30/2

# Score
score = 0
high_score = 0

# Set up the screen
wn = turtle.Screen()
wn.title("Healthy Snake Game")
wn.bgcolor("green")
wn.setup(width=screen_x, height=screen_y)
wn.tracer(0) # Turns off the screen updates

# Snake head
head = turtle.Turtle()
head.speed(0)
#head.shape("square")
#head.color("black")
wn.addshape(image_face)
head.shape(image_face)
head.penup()
head.goto(0,0)
head.direction = "stop"

# Snake food
food = turtle.Turtle()
food.speed(0)
#head.shape("square")
#head.color("black")
wn.addshape(image_food)
food.shape(image_food)
food.penup()
food.goto(0,100)


# Snake bad food
bad = turtle.Turtle()
bad.speed(0)
#head.shape("square")
#head.color("black")
wn.addshape(image_foodbad)
bad.shape(image_foodbad)
bad.penup()
bad.goto(0,60)

bad2 = turtle.Turtle()
bad2.speed(0)
#head.shape("square")
#head.color("black")
wn.addshape(image_foodbad)
bad2.shape(image_foodbad)
bad2.penup()
bad2.goto(0,60)

bad3 = turtle.Turtle()
bad3.speed(0)
#head.shape("square")
#head.color("black")
wn.addshape(image_foodbad)
bad3.shape(image_foodbad)
bad3.penup()
bad3.goto(0,60)

bad4 = turtle.Turtle()
bad4.speed(0)
#head.shape("square")
#head.color("black")
wn.addshape(image_foodbad)
bad4.shape(image_foodbad)
bad4.penup()
bad4.goto(0,60)

segments = []

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, screen_y/2-40)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))

# Functions
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"
        

def go_right():
    if head.direction != "left":
        head.direction = "right"
        

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

# Keyboard bindings
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")

# Main game loop
while True:
    wn.update()

    # Check for a collision with the border
    if head.xcor()>(screen_x/2)-30 or head.xcor()<-((screen_x/2)-30) or head.ycor()>((screen_y/2)-30) or head.ycor()<-((screen_y/2)-30):
        time.sleep(1)
        head.goto(0,0)
        head.direction = "stop"

        # Hide the segments
        for segment in segments:
            segment.goto(1000, 1000)
        
        # Clear the segments list
        segments.clear()

        # Reset the score
        score = 0

        # Reset the delay
        delay = 0.1

        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal")) 


    # Check for a collision with the food
    if head.distance(food) < coll_dist :
        # Move the food to a random spot
        x = random.randint(-screen_x/2-10, screen_x/2-10)
        y = random.randint(-screen_y/2-10, screen_y/2-10)
        food.goto(x,y)
        x = random.randint(-screen_x/2-10, screen_x/2-10)
        y = random.randint(-screen_y/2-10, screen_y/2-10)
        bad.goto(x,y)
        x = random.randint(-screen_x/2-10, screen_x/2-10)
        y = random.randint(-screen_y/2-10, screen_y/2-10)
        bad2.goto(x,y)
        x = random.randint(-screen_x/2-10, screen_x/2-10)
        y = random.randint(-screen_y/2-10, screen_y/2-10)
        bad3.goto(x,y)
        x = random.randint(-screen_x/2-10, screen_x/2-10)
        y = random.randint(-screen_y/2-10, screen_y/2-10)
        bad4.goto(x,y)

        # Add a segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.shapesize(stretch_wid=1.4,stretch_len=1.4)
        new_segment.color("light goldenrod yellow")
        new_segment.penup()
        segments.append(new_segment)

        # Shorten the delay
        delay -= 0.001

        # Increase the score
        score += 10




    if head.distance(bad) < coll_dist or head.distance(bad2) < coll_dist or head.distance(bad3) < coll_dist or head.distance(bad4) < coll_dist:

        # Move the food to a random spot
        x = random.randint(-screen_x/2-10, screen_x/2-10)
        y = random.randint(-screen_y/2-10, screen_y/2-10)
        food.goto(x,y)
        x = random.randint(-screen_x/2-10, screen_x/2-10)
        y = random.randint(-screen_y/2-10, screen_y/2-10)
        bad.goto(x,y)
        x = random.randint(-screen_x/2-10, screen_x/2-10)
        y = random.randint(-screen_y/2-10, screen_y/2-10)
        bad2.goto(x,y)
        x = random.randint(-screen_x/2-10, screen_x/2-10)
        y = random.randint(-screen_y/2-10, screen_y/2-10)
        bad3.goto(x,y)
        x = random.randint(-screen_x/2-10, screen_x/2-10)
        y = random.randint(-screen_y/2-10, screen_y/2-10)
        bad4.goto(x,y)

        # Remove a segment
        if len(segments) !=0:
        	segments[-1].hideturtle()

        	segments.pop()

        # Shorten the delay
        delay -= 0.001

        # Increase the score
        score -= 10





    if score > high_score:
        high_score = score
        
    pen.clear()
    pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal")) 

    # Move the end segments first in reverse order
    for index in range(len(segments)-1, 0, -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x, y)

    # Move segment 0 to where the head is
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x,y)

    move()    

    # Check for head collision with the body segments
    for segment in segments:
        if segment.distance(head) < 20:
            time.sleep(1)
            head.goto(0,0)
            head.direction = "stop"
        
            # Hide the segments
            for segment in segments:
                segment.goto(1000, 1000)
        
            # Clear the segments list
            segments.clear()

            # Reset the score
            score = 0

            # Reset the delay
            delay = 0.1
        
            # Update the score display
            pen.clear()
            pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

    time.sleep(delay)

wn.mainloop()