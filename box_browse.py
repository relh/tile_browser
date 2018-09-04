from tkinter import *
from tkinter import simpledialog
from PIL import Image,ImageTk


class ExampleApp(Frame):
    def __init__(self,master):
        Frame.__init__(self,master=None)
        self.x = self.y = 0
        self.canvas = Canvas(master, width=1920, height=1080,  cursor="cross")

        self.sbarv=Scrollbar(self,orient=VERTICAL)
        self.sbarh=Scrollbar(self,orient=HORIZONTAL)
        self.sbarv.config(command=self.canvas.yview)
        self.sbarh.config(command=self.canvas.xview)

        self.canvas.config(yscrollcommand=self.sbarv.set)
        self.canvas.config(xscrollcommand=self.sbarh.set)

        self.canvas.grid(row=0,column=0,sticky=N+S+E+W)
        self.sbarv.grid(row=0,column=1,stick=N+S)
        self.sbarh.grid(row=1,column=0,sticky=E+W)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.rect = None

        self.start_x = None
        self.start_y = None


        self.im = Image.open("image.jpg")
        self.wazil,self.lard=self.im.size
        print(self.im.size)
        self.canvas.config(scrollregion=(0,0,self.wazil,self.lard))
        self.tk_im = ImageTk.PhotoImage(self.im)
        self.canvas.create_image(0,0,anchor="nw",image=self.tk_im)   


    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = event.x
        self.start_y = event.y

        # create rectangle if not yet exist
        #if not self.rect:
        self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, fill="")


    def on_move_press(self, event):
        curX, curY = (event.x, event.y)

        # expand rectangle as you drag the mouse
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)    
        self.curX = curX
        self.curY = curY


    def on_button_release(self, event):
        answer = simpledialog.askstring("Input", "Where do you want to go?",
                                parent=self)
        get_screenshot(answer)
        im = Image.open("screenshot.png")
        im = im.resize((self.curX-self.start_x, self.curY-self.start_y))
        tk_im = ImageTk.PhotoImage(im)
        self.canvas.create_image(self.start_x,self.start_y,anchor='nw',image=tk_im)   


def get_screenshot(where):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    import os

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")

    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', chrome_options=chrome_options)
    driver.get("http://"+where)

    driver.save_screenshot("screenshot.png")

    driver.close()


if __name__ == "__main__":
    root=Tk()
    root.geometry("1920x1080")

    app = ExampleApp(root)
    root.mainloop()
