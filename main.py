import tkinter as tk
from tkinter import Canvas
import random


class Snake:
    def __init__(self):
        self.w = tk.Tk()
        self.w.attributes('-fullscreen', True)
        self.fullScreenState = False
        self.w.title("snake")
        self.snakeBodies = []
        self.xMOVEMENT = 10
        self.yMOVEMENT = 0
        self.width, self.height = self.w.winfo_screenwidth(), self.w.winfo_screenheight()
        self.margin = 125
        self.spawnMargin = 40
        self.LEFT_BORDER = self.margin
        self.RIGHT_BORDER = self.width - self.margin
        self.TOP_BORDER = self.margin
        self.BOTTOM_BORDER = self.height - self.margin
        self.w.geometry("%dx%d" % (self.width, self.height))
        self.w.configure(bg='black')
        self.canvas = Canvas(self.w, width=self.width, height=self.height)
        self.canvas.configure(bg="black")
        self.canvas.pack()
        self.bindAll()
        self.alive = True
        self.ate = False
        self.paused = False
        self.score = 0
        self.direction = "Right"
        self.drawBorders()
        self.initSnake()
        self.generateFood()
        self.w.after(75, self.performActions)
        self.w.mainloop()

    def bindAll(self):
        self.w.bind("<F11>", self.toggleFullScreen)
        self.w.bind("<Escape>", self.quitFullScreen)
        self.w.bind("<Return>", self.quit)
        self.w.bind("<Left>", self.left)
        self.w.bind("<Right>", self.right)
        self.w.bind("<Up>", self.up)
        self.w.bind("<Down>", self.down)
        self.w.bind("p", self.pause)

    def quit(self, event):
        print("Closed")
        self.w.destroy()

    def drawBorders(self):
        self.canvas.create_line(self.margin, self.margin, self.width-self.margin, self.margin, width=5, fill="white")
        self.canvas.create_line(self.margin, self.margin, self.margin, self.height - self.margin, width=5, fill="white")
        self.canvas.create_line(self.margin, self.height - self.margin, self.width - self.margin, self.height-self.margin, width=5, fill="white")
        self.canvas.create_line(self.width-self.margin, self.height - self.margin, self.width - self.margin, self.margin, width=5, fill="white")
        self.canvas.create_rectangle(0, 0, self.width, self.margin, fill="#368583", outline="")
        self.canvas.create_rectangle(0, self.height-self.margin, self.width, self.height, fill="#368583", outline="")
        self.canvas.create_rectangle(0, 0, self.margin, self.height, fill="#368583", outline="")
        self.canvas.create_rectangle(self.width-self.margin, 0, self.width, self.height, fill="#368583", outline="")

    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.w.attributes("-fullscreen", self.fullScreenState)

    def quitFullScreen(self, event):
        self.fullScreenState = False
        self.w.attributes("-fullscreen", self.fullScreenState)

    def initSnake(self):
        x1, y1 = random.randint(self.LEFT_BORDER + self.spawnMargin, self.RIGHT_BORDER - self.spawnMargin), \
                 random.randint(self.TOP_BORDER + self.spawnMargin, self.BOTTOM_BORDER - self.spawnMargin)
        x2, y2 = x1 + 15, y1 + 15
        for i in range(4):
            self.snakeBodies.append(self.canvas.create_rectangle(x1, y1, x2, y2, outline="white", fill="blue"))

    def moveSnake(self):
        if self.alive == False or self.paused:
            print(self.score)
            return
        head = self.snakeBodies[0]
        self.canvas.move(head, self.xMOVEMENT, self.yMOVEMENT)
        newHeadX1, newHeadY1, newHeadX2, newHeadY2 = self.canvas.coords(head)
        self.canvas.delete(self.snakeBodies[-1])
        self.snakeBodies = [self.canvas.create_rectangle(newHeadX1, newHeadY1, newHeadX2, newHeadY2, outline="white", fill="blue")] + self.snakeBodies[:-1]

    def growSnake(self):
        self.snakeBodies.append(self.snakeBodies[-1])

    def performActions(self):
        self.moveSnake()
        self.w.after(75, self.performActions)
        self.checkCollisions()
        if self.ate:
            self.generateFood()
            self.ate = False

    def generateFood(self):
        x1, y1 = random.randint(self.LEFT_BORDER + self.spawnMargin, self.RIGHT_BORDER - self.spawnMargin), \
                 random.randint(self.TOP_BORDER + self.spawnMargin, self.BOTTOM_BORDER - self.spawnMargin)
        x2, y2 = x1 + 10, y1 + 10
        self.food = self.canvas.create_rectangle(x1, y1, x2, y2, outline="white", fill="red")

    def checkCollisions(self):
        headX1, headY1, headX2, headY2 = self.canvas.coords(self.snakeBodies[0])
        foodX1, foodY1, foodX2, foodY2 = self.canvas.coords(self.food)
        snakeBodyPos = []
        for i in range(2, len(self.snakeBodies)-1):
            snakeBodyPos.append((self.canvas.coords(self.snakeBodies[i])[0], self.canvas.coords(self.snakeBodies[i])[1]))
        if (headX2 > self.RIGHT_BORDER or
            headY1 < self.TOP_BORDER or
            headX1 < self.LEFT_BORDER or
            headY2 > self.BOTTOM_BORDER):
                self.alive = False
        if (headX1, headY1) in snakeBodyPos:
            self.alive = False
        if self.snakeBodies[0] in self.canvas.find_overlapping(foodX1, foodY1, foodX2, foodY2):
            self.ate = True
            self.score += 1
            self.growSnake()
            self.canvas.delete(self.food)

    def pause(self, event):
        if self.paused:
            self.paused = False
        else:
            self.paused = True

    def left(self, event):
        if self.direction == "Up":
            self.direction = "Left"
            self.xMOVEMENT = -20
            self.yMOVEMENT = 0
        elif self.direction == "Down":
            self.direction = "Left"
            self.xMOVEMENT = -20
            self.yMOVEMENT = 0

    def right(self, event):
        if self.direction == "Up":
            self.direction = "Right"
            self.xMOVEMENT = 20
            self.yMOVEMENT = 0
        elif self.direction == "Down":
            self.direction = "Right"
            self.xMOVEMENT = 20
            self.yMOVEMENT = 0

    def up(self, event):
        if self.direction == "Right":
            self.direction = "Up"
            self.xMOVEMENT = 0
            self.yMOVEMENT = -20
        elif self.direction == "Left":
            self.direction = "Up"
            self.xMOVEMENT = 0
            self.yMOVEMENT = -20

    def down(self, event):
        if self.direction == "Right":
            self.direction = "Down"
            self.xMOVEMENT = 0
            self.yMOVEMENT = 20
        elif self.direction == "Left":
            self.direction = "Down"
            self.xMOVEMENT = 0
            self.yMOVEMENT = 20


if __name__ == '__main__':
    app = Snake()