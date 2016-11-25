#import relevant libraries: glob for searching for files, os for manipulating files, sys for getting the arguments, ast for converting string to dictionary
import glob
import os
import sys
import ast
import tkinter as tk
from tkinter import ttk

class MainApplication:
	def __init__(self, master):
		self.master = master

		

		#functions:
		#setting up the workspace
		download_dir = ""
		global original_dir
		original_dir = os.getcwd()
		file_dict = {}
		
		default_extensions = {
			"document_extensions":[".txt", ".pdf", ".docx", ".md"],
			"program_extensions":[".exe", ".msi"],
			"compressed_extensions":[".zip", ".7z", ".tar", ".cab", ".bz2", ".rar", ".xz"],
			"sound_extensions":[".mp3", ".wav", ".aac", ".flac"],
			"image_extensions":[".jpg", ".jpeg", ".JPEG", ".JPG", ".png", ".gif", ".tiff", ".ico"],
			"dskimg_extensions":[".iso", ".img", ".esd"],
		}
		default_configuration = {
			"first_time": "no",
			"download_dir": ""
		}
		
		
		help_text = "This program sorts your downloads. Use these arguments to choose what to sort:\n\t-docs\t\tsorts your documents\n\t-progs\t\tsorts your programs\n\t-compressed\tsorts your compressed files\n\t-sound\t\tsorts your sound files\n\t-image\t\tsorts your image files\n\t-dskimg\t\tsorts your disk image files\n\t-misc\t\tsorts your miscellaneous files\n\t-all\t\tsorts all file types\n\t-custom\t\tcustomisable file sort\n\t-chgdir\t\tchanges the downloads folder\n\t-help\t\tshows this help text"
		
		global extensions
		extensions = {}
		configuration = {}
		
		def save_config(items):
			global extensions
			global configuration
			if items == "default_exts":
				with open(original_dir + "\extensions.txt", mode="w") as config:
					#contents = "".join(contents)
					config.write(str(default_extensions))
			elif items == "edited_exts":
				with open(original_dir + "\extensions.txt", mode="w") as config:
					config.write(str(extensions))
			elif items == "config":
				with open(original_dir + "\config.txt", mode="w") as config:
					print("save config" + str(configuration))
					config.write(str(configuration))
			elif items == "default_config":
				with open(original_dir + "\config.txt", mode="w") as config:
					config.write(str(default_configuration))
		
		def load_config():
			global extensions
			global configuration
			try:
				with open(original_dir + "\extensions.txt", mode="r") as config:
					extensions = config.read()
			except FileNotFoundError:
				file = open("config.txt", mode="w")
				file.close()
				save_config("default_config")
			try:
				with open(original_dir + "\config.txt", mode="r") as config:
					configuration = config.read()
			except FileNotFoundError:
				file = open("extensions.txt", mode="w")
				save_config("default_exts")
				file.close()
			print("load"+configuration)
			print("load"+extensions)
		
		def edit_extensions(task):
			if task == "add":
				global extensions
				load_config()
				extensions = ast.literal_eval(extensions)
				print("Extension groups:")
				for key in extensions.keys():
					print("\t" + key)
				group = input("Edit which group of extensions? ")
				extension = input("Add which extension? ")
				edit = extensions[group]
				edit.append(extension)
				extensions[group] = edit
				print("This is your edit: \n\t" + str(extensions))
				if input("Save your edit? (y/n) ").lower() == "y":
					save_config("edited_exts")
			elif task == "remove":
				load_config()
				extensions = ast.literal_eval(extensions)
				print("Extension groups:")
				for key in extensions.keys():
					print("\t" + key)
				group = input("Edit which group of extensions? ")
				extension = input("Remove which extension? ")
				try:
					edit = extensions[group]
				except KeyError:
					print("Can't remove {0} from {1} because {1} is not a group of extensions.".format(extension, group))
					return
				try:
					edit.remove(extension)
				except ValueError:
					print("Can't remove {0} from {1} because {0} is not an extension in the group.".format(extension, group))
					return
				extensions[group] = edit
				print("This is your edit: \n\t" + str(extensions))
				if input("Save your edit? (y/n) ").lower() == "y":
					save_config("edited_exts")
		
		def edit_config(key, value):
			global configuration
			load_config()
			if bool(configuration) == False or key == "download_dir":
				save_config("default_config")
				load_config()
				print("bool" + str(configuration))
				configuration = ast.literal_eval(configuration)
				print(value)
				configuration[key] = os.path.normpath(value)
				print("normpath" + str(configuration))
				save_config("config")
			else:
				'''
				try:
					configuration = ast.literal_eval(configuration)
				except SyntaxError:
					save_config("default_config")
				'''
				try:
					edit = configuration[key]
				except KeyError:
					print("Can't set {0} to {1} because {0} is not an editable setting.".format(key, value))
					return
				except TypeError:
					load_config()
					print("TypeError" + str(configuration))
					configuration = ast.literal_eval(configuration)
					edit = configuration[key]
					return
				configuration[key] = value
				if key == "download_dir":
					normalpath = os.path.normpath(configuration[key])
					#print("normalpath is " + normalpath)
					#print("what I was given" + value)
					configuration[key] = normalpath
					#print("what to write" + configuration[key])
				else:
					edit = value
				print("Editing {0} to {1}...".format(key, value))
				save_config("config")
			
		#this function changes to your downloads directory and keeps it in the config file
		def change_dir(change):
			global download_dir
			global configuration
			#if it's the first time or a change has been requested
			load_config()
			print("changedir"+configuration)
			#ast.literal_eval(configuration)
			if change == True or bool(configuration) == False:
				download_input = input("Please enter the full path to a folder where your downloads are currently kept: ")
				edit_config("first_time", "no")
				edit_config("download_dir", download_input)
				'''
				configuration = ""
				configuration += "first_time=no"
				download_dir = input("Please enter the full path to a folder where your downloads are currently kept: ")
				configuration += "\n" + "download_dir=" + download_dir
				download_dir = configuration.split("download_dir=", 1)[1]
				'''
				try:
					load_config()
					print(configuration)
					configuration = ast.literal_eval(configuration)
					os.chdir(configuration["download_dir"])
				except FileNotFoundError:
						print("{0} was not found, creating now...".format(download_dir))
						os.makedirs(download_dir)
						os.chdir(download_dir)
				save_config("config")
				
				
				print("Folder to sort is {0}.".format(os.getcwd()))
			
			else:
				if "download_dir" in configuration:
					configuration = ast.literal_eval(configuration)
					try:
						os.chdir(configuration["download_dir"])
					except FileNotFoundError:
						print("{0} was not found, creating now...".format(configuration["download_dir"]))
						os.makedirs(configuration["download_dir"])
						os.chdir(configuration["download_dir"])
						
				print("Folder to sort is {0}.".format(os.getcwd()))
				print("after to sort is" + str(configuration))
		
		
		#this function takes in the directory to move the files to, the extensions to move, and a the category of the files so the output looks nice
		def sort_custom(directory, extensions, type):
			global custom_files
			custom_files = []
			for x in file_dict:
				if file_dict[x] in extensions:
					custom_files.append(x)
			if not os.path.exists(directory):
				os.makedirs(directory)
			#check if it can't be copied
			for x in custom_files:
				try:
					os.rename(x, directory+os.path.basename(x))
					print("Moving {0} to {1}".format(x, directory+os.path.basename(x)))
				except FileExistsError:
					print("Can't move {0} to {1}. The file already exists...".format(x, directory+os.path.basename(x)))
					custom_files.remove(x)
				except PermissionError:
					print("Can't move {0} to {1}. The file is currently in use...".format(x, directory+os.path.basename(x)))
					custom_files.remove(x)
			print("Moved {0}{1} files.".format(str(len(custom_files)), type))
		
		#miscellaneous sorting is slightly different
		def sort_misc(directory):
			all_extensions = extensions["document_extensions"] + extensions["program_extensions"] + extensions["compressed_extensions"] + extensions["sound_extensions"] + extensions["image_extensions"] + extensions["dskimg_extensions"]
			global misc_files
			misc_files = []
			#only gets files not in the extension lists
			for x in file_dict:
				if file_dict[x] not in all_extensions and not file_dict[x] == ".ini":
					misc_files.append(x)
			if not os.path.exists(directory):
				os.makedirs(directory)
			for x in misc_files:
				try:
					os.rename(x, directory+os.path.basename(x))
					print("Moving {0} to {1}".format(x, directory+os.path.basename(x)))
				except FileExistsError:
					print("Can't move {0} to {1}. The file already exists...".format(x, directory+os.path.basename(x)))
					misc_files.remove(x)
				except PermissionError:
					print("Can't move {0} to {1}. The file is currently in use...".format(x, directory+os.path.basename(x)))
					misc_files.remove(x)
			print("Moved {0} miscellaneous files.".format(str(len(misc_files))))
		
		def startup():
			global file_dict
			global configuration
			
			if bool(extensions) == False:
				save_config("default_exts")
			check = 0
			while os.path.isfile("config.txt") == False or os.path.isfile("extensions.txt") == False:
				if os.path.isfile("config.txt") == False:
					file = open("config.txt", mode="w")
					file.close()
					change_dir(True)
					check += 1
					print("Config doesn't exist, creating it")
				elif os.path.isfile("extensions.txt") == False:
					file = open("extensions.txt", mode="w")
					save_config("default_exts")
					file.close()
					check += 1
					print("Extensions doesn't exist, creating it")
				else:
					change_dir("normal")
					print("all files exist, continue")
				if check == 2:
					print("all files exist, continue")
					break
			change_dir("normal")
			print("about to load")
			load_config()
			print("finished loading")
			#extensions = ast.literal_eval()
			print("afterchangedir:configuration:" + str(configuration))
			#gets wiped out here?????!!?!?
			print("after change_dir:extensions:"+str(extensions))
			#{path:extension}
			file_dict = {os.path.realpath(f):os.path.splitext(f)[1] for f in glob.glob("*.*")}

		def button_command():
			global configuration
			global extensions
			
			if type(configuration) == str:
				configuration = ast.literal_eval(configuration)
			if type(extensions) == str:
				extensions = ast.literal_eval(extensions)
			
			value = taskmenu.get()
			if value == "Documents":
				sort_custom(configuration["download_dir"] + "/Documents/", extensions["document_extensions"], " document")
				
				"""
				sort_custom(configuration["download_dir"] + "/Programs/", extensions["program_extensions"], " program")
				sort_custom(configuration["download_dir"] + "/Compressed/", extensions["compressed_extensions"], " compressed")
				sort_custom(configuration["download_dir"] + "/Sounds/", extensions["sound_extensions"], " sound")
				sort_custom(configuration["download_dir"] + "/Images/", extensions["image_extensions"], " image")
				sort_custom(configuration["download_dir"] + "/Disk images/", extensions["dskimg_extensions"], " disk image")
				sort_misc(configuration["download_dir"] + "/Miscellaneous/")
				custom_extensions_input = input("Enter the extensions to move separated by commas: ").split(",")
				custom_directory_input = configuration["download_dir"] + input("Enter a subdirectory name (such as /ISOs/): ")
				sort_custom(custom_directory_input, custom_extensions_input, "")
				"""
				
			else:
				print(value) 
				
		#start it up
		startup()
		
		#styling
		master.title("Downloads Sorter")
		master.geometry("814x477")
		master.wm_iconbitmap(original_dir + os.path.normpath("/sorter.ico"))

		self.frame = tk.Frame(self.master)

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

		#adding elements
		label1 = ttk.Label(self.frame, text="Select a task:")
		label1.pack(side="left")
		taskmenu = ttk.Combobox(self.frame, state="readonly")
		taskmenu["values"] = ["Documents", "Programs/Installers", "Compressed files", "Sounds/Music files", "Images", "Disk Images", "Miscellaneous files", "Custom sort"]
		taskmenu.pack(side="left")
		button1 = ttk.Button(self.frame, text="Run", command=button_command)
		button1.pack(side="left")
		self.frame.pack()


class About:
	def __init__(self, master):
		self.master = master
		master.geometry("282x109")
		#master.wm_iconbitmap("D:\Coding\Python\Downloads Sorter\img\info.ico")
		#master.wm_iconbitmap(os.path.dirname(os.path.abspath("info.ico")))
		master.wm_iconbitmap(original_dir + os.path.normpath("/info.ico"))
		self.frame = tk.Frame(self.master)
		self.quitButton = ttk.Button(self.frame, text = "Close", width = 25, command = self.close_windows)
		self.aboutlbl = ttk.Label(self.frame, text = "This was made by tech189", width = 25)
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