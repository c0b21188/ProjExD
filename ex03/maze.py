import tkinter as tk
import random
import maze_maker as mm

def key_down(event): #key_downの関数
    global key
    key = event.keysym

def key_up(event): #key_upの関数
    global key
    key = ""

def main_proc():
    global cx, cy, mx, my
    UP, DOWN, LEFT, RIGHT = range(4)
    KEY_DIC = {"w":UP, "s":DOWN, "a":LEFT, "d":RIGHT}
    delta = { #押されているキーkey/値:移動幅リスト[x,y]
        "w":[0, -1],
        "s":[0, +1],
        "a":[-1, 0],
        "d":[+1,0],
        }
    try:
        if maze_bg[my+delta[key][1]][mx+delta[key][0]] == 0:
            my,mx = my+delta[key][1], mx+delta[key][0]
    except:
        pass



    cx,cy = mx*100+50,my*100+50
    canvas.coords("tori", cx, cy)
    root.after(100, main_proc)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("迷えるこうかとん")

    canvas = tk.Canvas(root, width=700, height=500, bg="black")
    canvas.pack()
    maze_bg = mm.make_maze(7, 5)
    mm.show_maze(canvas, maze_bg)
    #print(maze_bg)

    tori = tk.PhotoImage(file="fig/8.png")
    #box = tk.PhotoImage(file = "fig/hako.png ")
    #start = tk.PhotoImage(file = "fig/hata1.png ")
    mx, my = 1, 1
    cx,cy = mx*100+50,my*100+50
    #sx, sy = 150,150
    #bx, by = 1150, 550
    canvas.create_image(cx, cy, image = tori, tag = "tori")
    #canvas.create_image(sx, sy, image = start, tag = "start")
    #canvas.create_image(bx, by, image = box, tag = "box")
    #canvas.create_image(cx,cy,image=tori,tag="tori")

    key = ""
    root.bind("<KeyPress>", key_down)
    root.bind("<KeyRelease>", key_up)



    main_proc()

    root.mainloop()

