from Tkinter import *

#画圆~好多同心圆
if __name__ == '__main__':

    #设置画布，大小，背景颜色
    canvas = Canvas(width = 800, height = 600, bg = 'yellow')

    canvas.pack(expand = Yes, fill = BOTH)

     k = 1
     j = 1

     for i in range(0,26):
         canvas.create_oval(310 - k, 250 - k, 310 + k, 250 + k, width = 1)
         k += j
         j += 0.3

    mainloop()


#画直线
if __name__ == '__main__':
 
    canvas = Canvas(width=300, height=300, bg='green')   
    canvas.pack(expand=YES, fill=BOTH)                  
    x0 = 263
    y0 = 263
    y1 = 275
    x1 = 275
    for i in range(19):
        canvas.create_line(x0,y0,x0,y1, width=1, fill='red')
        x0 = x0 - 5
        y0 = y0 - 5
        x1 = x1 + 5
        y1 = y1 + 5
 
    x0 = 263
    y1 = 275
    y0 = 263
    for i in range(21):
        canvas.create_line(x0,y0,x0,y1,fill = 'red')
        x0 += 5
        y0 += 5
        y1 += 5
 
    mainloop()



#画同心方块
if __name__ == '__main__':

    root = Tk()
    root.title('Canvas')
    canvas = Canvas(root,width = 400,height = 400,bg = 'yellow')
    x0 = 263
    y0 = 263
    y1 = 275
    x1 = 275
    for i in range(19):
        canvas.create_rectangle(x0,y0,x1,y1)
        x0 -= 5
        y0 -= 5
        x1 += 5
        y1 += 5
        
    canvas.pack()
    root.mainloop()


#组合鬼画符1
if __name__  == '__main__':
    from Tkinter import *
    canvas = Canvas(width = 300,height = 300,bg = 'green')
    canvas.pack(expand = YES,fill = BOTH)
    x0 = 150
    y0 = 100
    canvas.create_oval(x0 - 10,y0 - 10,x0 + 10,y0 + 10)
    canvas.create_oval(x0 - 20,y0 - 20,x0 + 20,y0 + 20)
    canvas.create_oval(x0 - 50,y0 - 50,x0 + 50,y0 + 50)
    import math
    B = 0.809
    for i in range(16):
        a = 2 * math.pi / 16 * i
        x = math.ceil(x0 + 48 * math.cos(a))
        y = math.ceil(y0 + 48 * math.sin(a) * B)
        canvas.create_line(x0,y0,x,y,fill = 'red')
    canvas.create_oval(x0 - 60,y0 - 60,x0 + 60,y0 + 60)
    

    for k in range(501):
        for i in range(17):
            a = (2 * math.pi / 16) * i + (2 * math.pi / 180) * k
            x = math.ceil(x0 + 48 * math.cos(a))
            y = math.ceil(y0 + 48 + math.sin(a) * B)
            canvas.create_line(x0,y0,x,y,fill = 'red')
        for j in range(51):
            a = (2 * math.pi / 16) * i + (2* math.pi / 180) * k - 1
            x = math.ceil(x0 + 48 * math.cos(a))
            y = math.ceil(y0 + 48 * math.sin(a) * B)
            canvas.create_line(x0,y0,x,y,fill = 'red')
    mainloop()


#组合鬼画符2

if __name__ == '__main__':
    from Tkinter import *
    canvas = Canvas(width = 400,height = 600,bg = 'white')
    left = 20
    right = 50
    top = 50
    num = 15
    for i in range(num):
        canvas.create_oval(250 - right,250 - left,250 + right,250 + left)
        canvas.create_oval(250 - 20,250 - top,250 + 20,250 + top)
        canvas.create_rectangle(20 - 2 * i,20 - 2 * i,10 * (i + 2),10 * ( i + 2))
        right += 5
        left += 5
        top += 10

    canvas.pack()
    mainloop()
    

#画椭圆
if __name__ == '__main__':
    from Tkinter import *
    x = 360
    y = 160
    top = y - 30
    bottom = y - 30
    
    canvas = Canvas(width = 400,height = 600,bg = 'white')
    for i in range(20):
        canvas.create_oval(250 - top,250 - bottom,250 + top,250 + bottom)
        top -= 5
        bottom += 5
    canvas.pack()
    mainloop()

	
#一个优美的图形
import math
class PTS:
    def __init__(self):
        self.x = 0
        self.y = 0
points = []

def LineToDemo():
    from Tkinter import *
    screenx = 400
    screeny = 400
    canvas = Canvas(width = screenx,height = screeny,bg = 'white')

    AspectRatio = 0.85
    MAXPTS = 15
    h = screeny
    w = screenx
    xcenter = w / 2
    ycenter = h / 2
    radius = (h - 30) / (AspectRatio * 2) - 20
    step = 360 / MAXPTS
    angle = 0.0
    for i in range(MAXPTS):
        rads = angle * math.pi / 180.0
        p = PTS()
        p.x = xcenter + int(math.cos(rads) * radius)
        p.y = ycenter - int(math.sin(rads) * radius * AspectRatio)
        angle += step
        points.append(p)
    canvas.create_oval(xcenter - radius,ycenter - radius,
                       xcenter + radius,ycenter + radius)
    for i in range(MAXPTS):
        for j in range(i,MAXPTS):
            canvas.create_line(points[i].x,points[i].y,points[j].x,points[j].y)

    canvas.pack()
    mainloop()
if __name__ == '__main__':
    LineToDemo()
#一个优美的图形