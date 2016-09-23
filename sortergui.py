import tkinter as tk

class MainApplication:
    def __init__(self, master):
        self.master = master

        #styling
        master.title("Downloads Sorter")
        master.geometry("1100x600")
        #TODO Downloads icon from metro pack
		#master.wm_iconbitmap("android.ico")

        #self.frame = tk.Frame(self.master)

        #functions for the menu
        def about_window():
            self.newWindow = tk.Toplevel(self.master)
            self.app = About(self.newWindow)

		#creating the menu:
        menubar = tk.Menu(master)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=master.quit)
        menubar.add_cascade(label="Window", menu=filemenu)

        #editmenu = tk.Menu(menubar, tearoff=0)
        #editmenu.add_command(label="Copy result to clipboard", command=copy_text)

        #menubar.add_cascade(label="Edit", menu=editmenu)
        helpmenu = tk.Menu(menubar, tearoff=0)
        #helpmenu.add_command(label="Help...", command=help_window)
        helpmenu.add_command(label="About...", command=about_window)
        menubar.add_cascade(label="Help", menu=helpmenu)

        master.config(menu=menubar)

        #self.frame.pack()


class About:
	def __init__(self, master):
		self.master = master
		self.frame = tk.Frame(self.master)
		self.quitButton = tk.Button(self.frame, text = "Close", width = 25, command = self.close_windows)
		self.aboutlbl = tk.Label(self.frame, text = "This was made by tech189", width = 25)
		self.aboutlbl.pack()
		self.quitButton.pack()
		self.frame.pack()
		master.after(10, lambda: master.focus_force())
	def close_windows(self):
		self.master.destroy()

def main():
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()

if __name__ == '__main__':
    main()
