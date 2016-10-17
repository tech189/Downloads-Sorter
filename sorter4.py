#import relevant libraries: glob for searching for files, os for manipulating files, sys for getting the arguments, ast for converting string to dictionary
import glob
import os
import sys
import ast

#setting up the workspace
download_dir = ""
original_dir = os.getcwd()

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

#{path:extension}
file_dict = {os.path.realpath(f):os.path.splitext(f)[1] for f in glob.glob("*.*")}
help_text = "This program sorts your downloads. Use these arguments to choose what to sort:\n\t-docs\t\tsorts your documents\n\t-progs\t\tsorts your programs\n\t-compressed\tsorts your compressed files\n\t-sound\t\tsorts your sound files\n\t-image\t\tsorts your image files\n\t-dskimg\t\tsorts your disk image files\n\t-misc\t\tsorts your miscellaneous files\n\t-all\t\tsorts all file types\n\t-custom\t\tcustomisable file sort\n\t-chgdir\t\tchanges the downloads folder\n\t-help\t\tshows this help text"


extensions = {}
configuration = {}

def load_config():
    global extensions
    global configuration
    with open(original_dir + "\extensions.txt", mode="r") as config:
        extensions = config.read()
    with open(original_dir + "\config.txt", mode="r") as config:
        configuration = config.read()

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
    #ast.literal_eval(configuration)
    if "first_time=yes" in configuration or change == True or configuration == {}:
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
        
        
        print("Downloads folder changed to {0}.".format(os.getcwd()))
    
    else:
        if "download_dir" in configuration:
            configuration = ast.literal_eval(configuration)
            try:
                os.chdir(configuration["download_dir"])
            except FileNotFoundError:
                print("{0} was not found, creating now...".format(configuration["download_dir"]))
                os.makedirs(configuration["download_dir"])
                os.chdir(configuration["download_dir"])
                
        print("Downloads folder changed to {0}.".format(os.getcwd()))


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


while os.path.isfile("config.txt") == False or os.path.isfile("extensions.txt") == False:
    if os.path.isfile("config.txt") == False:
        file = open("config.txt", mode="w")
        file.close()
    elif os.path.isfile("extensions.txt") == False:
        file = open("extensions.txt", mode="w")
        save_config("default_exts")
        file.close()
    else:
        break
        
if bool(extensions) == False:
    save_config("default_exts")

change_dir("normal")


extensions = ast.literal_eval(extensions)

#get the arguments and act on them
if len(sys.argv) < 2:
    print(help_text)
else:
    if sys.argv[1] == "-docs":
        sort_custom(configuration["download_dir"] + "Documents/", document_extensions, " document")
    elif sys.argv[1] == "-progs":
        sort_custom(configuration["download_dir"] + "Programs/", program_extensions, " program")
    elif sys.argv[1] == "-compressed":
        sort_custom(configuration["download_dir"] + "Compressed/", compressed_extensions, " compressed")
    elif sys.argv[1] == "-sound":
        sort_custom(configuration["download_dir"] + "Sounds/", sound_extensions, " sound")
    elif sys.argv[1] == "-image":
        sort_custom(configuration["download_dir"] + "Images/", image_extensions, " image")
    elif sys.argv[1] == "-dskimg":
        sort_custom(configuration["download_dir"] + "Disk images/", dskimg_extensions, " disk image")
    elif sys.argv[1] == "-misc":
        sort_misc(configuration["download_dir"] + "Miscellaneous/")
    elif sys.argv[1] == "-all":
        sort_custom(configuration["download_dir"] + "Documents/", document_extensions, " document")
        sort_custom(configuration["download_dir"] + "Programs/", program_extensions, " program")
        sort_custom(configuration["download_dir"] + "Compressed/", compressed_extensions, " compressed")
        sort_custom(configuration["download_dir"] + "Sounds/", sound_extensions, " sound")
        sort_custom(configuration["download_dir"] + "Images/", image_extensions, " image")
        sort_custom(configuration["download_dir"] + "Disk images/", dskimg_extensions, " disk image")
        sort_misc(configuration["download_dir"] + "Miscellaneous/")
    elif sys.argv[1] == "-custom":
        custom_extensions_input = input("Enter the extensions to move separated by commas: ").split(",")
        custom_directory_input = configuration["download_dir"] + input("Enter a subdirectory name (such as ISOs/): ")
        sort_custom(custom_directory_input, custom_extensions_input, "")
    elif sys.argv[1] == "-chgdir":
        change_dir(True)
    elif sys.argv[1] == "-help":
        print(help_text)
    else:
        print(help_text)