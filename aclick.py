#import threading
import time
from pynput.keyboard import KeyCode, Listener, Key
from pynput.mouse import Controller, Button
from win32api import GetSystemMetrics
import tkinter as tk
import queue
import random

delay = random.uniform(6.5, 8.4)
toPress = Button.right
switchKey = KeyCode(char='s')
exitKey = KeyCode(char='e')
mouse = Controller()
screen_width = GetSystemMetrics(0)
app_width = 1100
app_height = 200
    
class AutoClick:
    def __init__(self, delay, button):
        self.delay = delay
        self.button = button
        self.running = True
        self.clicking = False
        
    def startAutoClicking(self):
        self.clicking = True
        
    def stopAutoClicking(self):
        self.clicking = False
        
    def exit(self):
        self.stopAutoClicking()
        self.running = False
    
    def rand_delay(self):
        self.delay = random.uniform(6.5, 8.4)
        
class StatWindow:
    def __init__(self, clicker, app_width, app_height, screen_width):
        self.callbackID = None
        self.eventqueue = queue.Queue()
        
        self.clicker = clicker
        self.app_width = app_width
        self.app_height = app_height
        self.screen_width = screen_width
        self.res = str(self.app_width) + "x" + str(self.app_height) + "+" + str(round((self.screen_width / 2) - (self.app_width / 2))) + "+0" 
        
        self.root = tk.Tk()
        self.root.overrideredirect(1)
        self.root.attributes("-alpha", 1.0)
        self.root.lift()
        self.root.attributes("-topmost", True)
        self.root.geometry(self.res)
        self.root.config(bg='white')
        
        self.var = tk.StringVar()
        
        self.label = tk.Label(self.root, textvariable=self.var, bg='white', width=900, font='Courier 40 bold')
        
        self.root.attributes("-transparentcolor", "white")
        
        self.label.pack()
        self.label.config(fg="red")
        self.var.set("Script is running!\nThe autoclicker is currently OFF")
        
        self.listener_thread()
        self.root.after(0, self.update)
        
    def changeToGreen(self):
        self.label.config(fg="green")
        self.var.set("Script is running!\nThe autoclicker is currently ON\nCurrent delay: " + "{:.2f}".format(self.clicker.delay) + "s")
        
    def changeToRed(self):
        self.label.config(fg="red")
        self.var.set("Script is running!\nThe autoclicker is currently OFF")
        
    def updt(self):
        self.root.update()
        self.root.update_idletasks()
        self.root.lift()
        
    def close(self):
        time.sleep(0.5)
        self.root.quit()
        self.root.destroy()
   
    def click_update(self):
        if self.clicker.clicking:
            mouse.click(self.clicker.button)
            self.clicker.rand_delay()
            
            self.var.set("Script is running!\nThe autoclicker is currently ON\nCurrent delay: " + "{:.2f}".format(self.clicker.delay) + "s")
            
            self.callbackID = self.root.after(round(self.clicker.delay * 1000), self.click_update)
        else:
            self.callbackID = None
        
    def process_key(self, key):
        if key == switchKey:
            if self.clicker.clicking:
                self.clicker.stopAutoClicking()
                self.changeToRed()
                if self.callbackID:
                    self.root.after_cancel(self.callbackID)
                    self.callbackID = None
            else:
                self.clicker.startAutoClicking()
                self.click_update()
                self.changeToGreen()  
                
        elif key == exitKey:
            self.clicker.exit()
            self.close()
    
    def update(self):
        try:
            while True:
                key = self.eventqueue.get_nowait()
                self.process_key(key)
        except queue.Empty:
            pass
        self.root.after(100, self.update)
    
    def listener_thread(self):
        def on_press(key):
            if key == switchKey or key == exitKey:
                self.eventqueue.put_nowait(key)

        listener = Listener(on_press=on_press)
        listener.start()
        
def main():
    
    clicker = AutoClick(delay, toPress)
    root = StatWindow(clicker, app_width, app_height, screen_width)
    
    root.root.mainloop()
    
    
if __name__ == "__main__":
    main()