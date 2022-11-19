import math
import random
import time
import turtle

# Set up the game window
window = turtle.Screen()
window.tracer(0)
window.setup(0.6, 0.6)
window.title("The Python Lunar Landing Game")
window.bgcolor("black")

width = window.window_width()
height = window.window_height()

# Game parameters
n_of_stars = 100
# Lunar module design parameters
branch_size = width / 16
n_of_discs = 5
disc_colour = "light gray"
centre_colour = "gold"
landing_gear_colour = "red"
# Lunar module movement parameters
rotation_step = 0.2
speed_step = 0.1
# Landing parameters
landing_pad_position = 0, -height / 2.1
module_landing_position = (
    landing_pad_position[0],
    landing_pad_position[1] + branch_size,
)
landing_pos_tolerance_x = 20
landing_pos_tolerance_y = 5
landing_orientation = 270  # vertically downwards
landing_orientation_tolerance = 15

gravity = 0.03

# Create stars and moon
stars = turtle.Turtle()
stars.hideturtle()
stars.penup()
stars.color("white")
for _ in range(n_of_stars):
    # Use floor division // to ensure ints in randint()
    x_pos = random.randint(-width // 2, width // 2)
    y_pos = random.randint(-height // 2, height // 2)
    stars.setposition(x_pos, y_pos)
    stars.dot(random.randint(2, 6))

moon = turtle.Turtle()
moon.penup()
moon.color("slate gray")
moon.sety(-height * 2.8)
moon.dot(height * 5)

# Create landing pad
landing_pad = turtle.Turtle()
landing_pad.hideturtle()
landing_pad.penup()
landing_pad.setposition(landing_pad_position)
landing_pad.pendown()
landing_pad.pensize(10)
landing_pad.forward(branch_size / 2)
landing_pad.forward(-branch_size)
landing_pad.forward(branch_size / 2)

# Create the lunar module
lunar_module = turtle.Turtle()
lunar_module.penup()
lunar_module.hideturtle()
lunar_module.setposition(-width / 3, height / 3)
lunar_module.rotation = random.randint(-9, 9)
lunar_module.clockwise_thruster = False
lunar_module.anticlockwise_thruster = False
lunar_module.travel_speed = random.randint(1, 3)
lunar_module.travel_direction = random.randint(-45, 0)

def draw_lunar_module():
    lunar_module.clear()
    # "save" the starting position and orientation
    position = lunar_module.position()
    heading = lunar_module.heading()

    lunar_module.pendown()
    lunar_module.pensize(5)
    # Landing gear
    lunar_module.color(landing_gear_colour)
    lunar_module.forward(branch_size)
    lunar_module.left(90)
    lunar_module.forward(branch_size / 2)
    lunar_module.forward(-branch_size)
    lunar_module.forward(branch_size / 2)
    lunar_module.right(90)
    lunar_module.forward(-branch_size)
    lunar_module.pensize(1)
    # Pods around the edge of the module
    lunar_module.color(disc_colour)
    for _ in range(n_of_discs - 1):
        lunar_module.right(360 / n_of_discs)
        lunar_module.forward(branch_size)
        lunar_module.dot(branch_size / 2)
        lunar_module.forward(-branch_size)
    # Centre part of the lunar module
    lunar_module.color(centre_colour)
    lunar_module.dot(branch_size)
    lunar_module.penup()

    # reset the turtle to initial position and orientation
    lunar_module.setposition(position)
    lunar_module.setheading(heading)

# Create burning fuel
burning_fuel = turtle.Turtle()
burning_fuel.penup()
burning_fuel.hideturtle()

def draw_burning_fuel(thruster):
    # Place turtle in the correct location
    # depending on which thruster is on
    if thruster == "clockwise":
        direction = 1
    elif thruster == "anticlockwise":
        direction = -1
    burning_fuel.penup()
    burning_fuel.setposition(lunar_module.position())
    burning_fuel.setheading(lunar_module.heading())
    burning_fuel.right(direction * 360 / n_of_discs)
    burning_fuel.forward(branch_size)
    burning_fuel.left(direction * 360 / n_of_discs)

    # Draw burning fuel
    burning_fuel.pendown()
    burning_fuel.pensize(8)
    burning_fuel.color("yellow")
    burning_fuel.forward(branch_size)
    burning_fuel.backward(branch_size)
    burning_fuel.left(5)
    burning_fuel.color("red")
    burning_fuel.pensize(5)
    for _ in range(2):
        burning_fuel.forward(branch_size)
        burning_fuel.backward(branch_size)
        burning_fuel.right(10)

def turn_on_clockwise_thruster():
    lunar_module.clockwise_thruster = True

def turn_on_anticlockwise_thruster():
    lunar_module.anticlockwise_thruster = True

def turn_off_clockwise_thruster():
    lunar_module.clockwise_thruster = False

def turn_off_anticlockwise_thruster():
    lunar_module.anticlockwise_thruster = False

window.onkeypress(turn_on_clockwise_thruster, "Right")
window.onkeypress(turn_on_anticlockwise_thruster, "Left")
window.onkeyrelease(turn_off_clockwise_thruster, "Right")
window.onkeyrelease(turn_off_anticlockwise_thruster, "Left")
window.listen()

# Applying forces to translate the lunar module
def apply_force(mode):
    # Initial components of lunar module velocity
    tangential = lunar_module.travel_speed
    normal = 0

    if mode == "gravity":
        force_direction = -90
        step = gravity
    elif mode == "thrusters":
        force_direction = lunar_module.heading() + 180
        step = speed_step

    angle = math.radians(
        force_direction - lunar_module.travel_direction
    )

    # New components of lunar module velocity
    tangential += step * math.cos(angle)
    normal += step * math.sin(angle)

    direction_change = math.degrees(
        math.atan2(normal, tangential)
    )
    lunar_module.travel_direction += direction_change

    lunar_module.travel_speed = math.sqrt(
        normal ** 2 + tangential ** 2
    )

# Check for successful landing
def check_landing():
    if (
        abs(lunar_module.xcor() - module_landing_position[0])
        < landing_pos_tolerance_x
        and abs(lunar_module.ycor() - module_landing_position[1])
        < landing_pos_tolerance_y
    ):
        if (
            abs(lunar_module.heading() - landing_orientation)
            < landing_orientation_tolerance
        ):
            lunar_module.setposition(module_landing_position)
            lunar_module.setheading(landing_orientation)
            draw_lunar_module()
            burning_fuel.clear()
            return True
        else:
            burning_fuel.clear()
            return False  # Crash on landing pad - wrong angle
    if lunar_module.ycor() < -height / 2:
        burning_fuel.clear()
        return False  # Crash below moon surface
    return None  # No successful or unsuccessful landing yet

while True:
    burning_fuel.clear()
    # Apply thrust if both thrusters are on
    if (
        lunar_module.clockwise_thruster
        and lunar_module.anticlockwise_thruster
    ):
        apply_force("thrusters")
    # Change rotational speed of lunar module
    if lunar_module.clockwise_thruster:
        draw_burning_fuel("clockwise")
        lunar_module.rotation -= rotation_step
    if lunar_module.anticlockwise_thruster:
        draw_burning_fuel("anticlockwise")
        lunar_module.rotation += rotation_step
    # Rotate lunar module
    lunar_module.left(lunar_module.rotation)

    # Apply effect of gravity
    apply_force("gravity")

    # Translate lunar module
    x = lunar_module.travel_speed * math.cos(
        math.radians(lunar_module.travel_direction)
    )
    y = lunar_module.travel_speed * math.sin(
        math.radians(lunar_module.travel_direction)
    )
    lunar_module.setx(lunar_module.xcor() + x)
    lunar_module.sety(lunar_module.ycor() + y)

    # Refresh image of lunar module
    draw_lunar_module()

    # Check for successful or unsuccessful landing
    successful_landing = check_landing()
    if successful_landing is not None:
        if successful_landing:
            window.title("Well Done! You've landed successfully")
        else:
            window.bgcolor("red")
            window.title("The lunar module crashed")
        break

    time.sleep(0.05)
    window.update()

turtle.done()
