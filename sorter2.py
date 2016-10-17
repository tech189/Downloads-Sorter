#import relevant libraries: glob for searching for files, os for manipulating files, sys for getting the arguments
import glob
import os
import sys

#setting up the workspace
download_dir = ""
original_dir = os.getcwd()

#working out if this is your first time using it (creates config file if it doesn't exist)
if not os.path.exists("config") or os.stat("config").st_size == 0:
    with open("config", mode="w") as config:
        config.write("first_time=yes")
    
#this function changes to your downloads directory and keeps it in the config file
def change_dir(change):
    global download_dir
    #if it's the first time or a change has been requested
    if "first_time=yes" in open(original_dir + "\config").read() or change == True:
        with open(original_dir + "\config", mode="w") as config:
            config.write("first_time=no")
            download_dir = input("Please enter the full path to a folder where your downloads are currently kept: ")
            download_dir = "\n" + "download_dir=" + download_dir
        with open(original_dir + "\config", mode="a") as config:
                config.write(download_dir)
        with open(original_dir + "\config") as config:
            download_dir = open(original_dir + "\config").read().split("download_dir=", 1)[1]
            try:
                os.chdir(download_dir)
            except FileNotFoundError:
                print("{0} was not found, creating now...".format(download_dir))
                os.makedirs(download_dir)
                os.chdir(download_dir)

        print("Downloads folder changed to {0}.".format(download_dir))
    else:
        if "download_dir" in open(original_dir + "\config").read():
            with open(original_dir + "\config") as config:
                download_dir = open(original_dir + "\config").read().split("download_dir=", 1)[1]
                try:
                    os.chdir(download_dir)
                except FileNotFoundError:
                    print("{0} was not found, creating now...".format(download_dir))
                    os.makedirs(download_dir)
                    os.chdir(download_dir)

#change to the directory that's written in the config file
change_dir(False)

#{path:extension}
file_dict = {os.path.realpath(f):os.path.splitext(f)[1] for f in glob.glob("*.*")}
help_text = "This program sorts your downloads. Use these arguments to choose what to sort:\n\t-docs\t\tsorts your documents\n\t-progs\t\tsorts your programs\n\t-compressed\tsorts your compressed files\n\t-sound\t\tsorts your sound files\n\t-image\t\tsorts your image files\n\t-dskimg\t\tsorts your disk image files\n\t-misc\t\tsorts your miscellaneous files\n\t-all\t\tsorts all file types\n\t-custom\t\tcustomisable file sort\n\t-chgdir\t\tchanges the downloads folder\n\t-help\t\tshows this help text"

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

def save_extensions(extension_var, extensions):
    contents = open(original_dir + "\config").read()
    if contents[contents.find("[")+1:contents.find("}")] == str(extensions):
        print("already added")
    elif extension_var in contents:
        print("already added")
    else:
        with open(original_dir + "\config", mode="r") as config:
            contents = config.readlines()
            contents.insert(1, extension_var + "[" + str(extensions) + "}\r")
        with open(original_dir + "\config", mode="w") as config:
            contents = "".join(contents)
            config.write(contents)
    #contents.close()

#TODO: Make the extensions lists editable
#TODO: Make these extensions not case sensitive
document_extensions = [".txt", ".pdf", ".docx", ".md"]
program_extensions = [".exe", ".msi"]
compressed_extensions = [".zip", ".7z", ".tar", ".cab", ".bz2", ".rar", ".xz"]
sound_extensions = [".mp3", ".wav", ".aac", ".flac"]
image_extensions = [".jpg", ".jpeg", ".JPEG", ".JPG", ".png", ".gif", ".tiff", ".ico"]
dskimg_extensions = [".iso", ".img", ".esd"]
all_extensions = document_extensions + program_extensions + compressed_extensions + sound_extensions + image_extensions + dskimg_extensions


'''
with open(original_dir + "\config", mode="r") as config:
    contents = config.readlines()
    contents.insert(1, "document_extensions=" + str(document_extensions) + "\r")
with open(original_dir + "\config", mode="w") as config:
    contents = "".join(contents)
    config.write(contents)
'''
#get the arguments and act on them
if len(sys.argv) < 2:
    print(help_text)
else:
    if sys.argv[1] == "-docs":
        sort_custom(download_dir + "Documents/", document_extensions, " document")
    elif sys.argv[1] == "-progs":
        sort_custom(download_dir + "Programs/", program_extensions, " program")
    elif sys.argv[1] == "-compressed":
        sort_custom(download_dir + "Compressed/", compressed_extensions, " compressed")
    elif sys.argv[1] == "-sound":
        sort_custom(download_dir + "Sounds/", sound_extensions, " sound")
    elif sys.argv[1] == "-image":
        sort_custom(download_dir + "Images/", image_extensions, " image")
    elif sys.argv[1] == "-dskimg":
        sort_custom(download_dir + "Disk images/", dskimg_extensions, " disk image")
    elif sys.argv[1] == "-misc":
        sort_misc(download_dir + "Miscellaneous/")
    elif sys.argv[1] == "-all":
        sort_custom(download_dir + "Documents/", document_extensions, " document")
        sort_custom(download_dir + "Programs/", program_extensions, " program")
        sort_custom(download_dir + "Compressed/", compressed_extensions, " compressed")
        sort_custom(download_dir + "Sounds/", sound_extensions, " sound")
        sort_custom(download_dir + "Images/", image_extensions, " image")
        sort_custom(download_dir + "Disk images/", dskimg_extensions, " disk image")
        sort_misc(download_dir + "Miscellaneous/")
    elif sys.argv[1] == "-custom":
        custom_extensions_input = input("Enter the extensions to move separated by commas: ").split(",")
        custom_directory_input = download_dir + input("Enter a subdirectory name (such as ISOs/): ")
        sort_custom(custom_directory_input, custom_extensions_input, "")
    elif sys.argv[1] == "-chgdir":
        change_dir(True)
    elif sys.argv[1] == "-saveext":
        if "first_time=yes" in open(original_dir + "\config").read():
            save_extensions("document_extensions=", document_extensions)
            save_extensions("program_extensions=", program_extensions)
            save_extensions("compressed_extensions=", compressed_extensions)
            save_extensions("sound_extensions=", sound_extensions)
            save_extensions("image_extensions=", image_extensions)
            save_extensions("dskimg_extensions=", dskimg_extensions)
    elif sys.argv[1] == "-help":
        print(help_text)
    else:
        print(help_text)