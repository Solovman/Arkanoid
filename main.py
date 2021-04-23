from tkinter import *
from random import *

size_w = 600
size_h = 600
ball_x, ball_y = size_w // 2, size_h // 2
ball_vx, ball_vy = -10, -10
radius = 20

carriage_x = size_w // 2
carriage_w = 200
carriage_h = 20
carriage_stop = True

interval = 30
points = 0
root = Tk()
root.title('Arkanoid')
root.wm_attributes('-topmost', 1)
root.resizable(0, 0)

string, column = 2, 3
bricks_zone = 0.2

canvas = Canvas(root, width=size_w, height=size_h, bg='black')
canvas.focus_set()
canvas.pack()

ball = canvas.create_oval(ball_x - radius, ball_y - radius, ball_x + radius, ball_y + radius, fill='white')

carriage = canvas.create_rectangle(carriage_x - carriage_w // 2, size_h,
                                   carriage_x + carriage_w // 2, size_h - carriage_h, fill='white')

scorer = canvas.create_text(ball_x, ball_y + 80, text='0', font=('Arial', 40, 'bold'), fill='white')

rectangle1 = canvas.create_rectangle(70, 300, 230, 350, fill='white')

rectangle2 = canvas.create_rectangle(420, 340, 520, 400, fill='white')

brick_w, brick_h = size_w / column, size_h * bricks_zone / string
bricks = []

for i in range(string):
    for j in range(column):
        brick_x, brick_y = j * brick_w, i * brick_h
        colors = choice(['red', 'orange',  'yellow', 'green', 'blue', 'aqua', 'violet'])
        bricks.append(canvas.create_rectangle(brick_x, brick_y, brick_x + brick_w, brick_y + brick_h, fill=colors))


def ball_movement():
    global ball_x, ball_y, ball_vx, ball_vy, carriage_stop, points
    ball_x, ball_y = ball_x + ball_vx, ball_y + ball_vy
    canvas.coords(ball, ball_x - radius, ball_y - radius, ball_x + radius, ball_y + radius)
    if ball_y <= radius:
        ball_vy = abs(ball_vy)
    if ball_x <= radius or ball_x >= size_w - radius:
        ball_vx = -ball_vx
    if carriage_x - carriage_w // 2 <= ball_x <= carriage_x + carriage_w // 2 and \
            ball_y == size_h - (radius + carriage_h):
        ball_vy = -ball_vy
        update_point()

    if 70 < ball_x < 230 and 300 < ball_y < 350:
        ball_vy = -ball_vy

    if 420 < ball_x < 520 and 340 < ball_y < 400:
        ball_vy = -ball_vy

    brick = crash_a_brick()
    if brick:
        ball_vy = -ball_vy
        canvas.delete(brick)
        bricks.pop(bricks.index(brick))
        update_point()
    root.update()
    if ball_y < (size_h - radius):
        root.after(interval, ball_movement)
    else:
        canvas.create_text(size_w // 2, size_h // 2, text='GAME OVER', fill='red', font=(None, 50))
        carriage_stop = False


def control(event):
    global carriage_x
    if event.keysym == 'Left' and carriage_x > 100:
        carriage_x -= 50
    if event.keysym == 'Right' and carriage_x < 600 - 100:
        carriage_x += 50
    if carriage_stop:
        canvas.coords(carriage, carriage_x - carriage_w // 2, size_h, carriage_x + carriage_w // 2, size_h - carriage_h)


def crash_a_brick():
    for brick in bricks:
        brick_x1, brick_y1, brick_x2, brick_y2 = canvas.coords(brick)
        if brick_x1 < ball_x < brick_x2 and brick_y1 < ball_y < brick_y2:
            return brick


def update_point():
    global points
    points += 1
    canvas.itemconfig(scorer, text=str(points))


ball_movement()
canvas.bind('<Key>', control)
root.mainloop()
