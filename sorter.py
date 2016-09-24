import glob
import os
import sys

download_dir = ""
original_dir = os.getcwd()

def change_dir(change):
    global download_dir
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
change_dir(False)

#{path:extension}
file_dict = {os.path.realpath(f):os.path.splitext(f)[1] for f in glob.glob("*.*")}
help_text = "This program sorts your downloads. Use these arguments to choose what to sort:\n\t-docs\t\tsorts your documents\n\t-progs\t\tsorts your programs\n\t-compressed\tsorts your compressed files\n\t-sound\t\tsorts your sound files\n\t-image\t\tsorts your image files\n\t-dskimg\t\tsorts your disk image files\n\t-misc\t\tsorts your miscellaneous files\n\t-all\t\tsorts all file types\n\t-custom\t\tcustomisable file sort\n\t-chgdir\t\tchanges the downloads folder\n\t-help\t\tshows this help text"

def sort_custom(directory, extensions, type):
    global custom_files
    custom_files = []
    for x in file_dict:
        if file_dict[x] in extensions:
            custom_files.append(x)
    if not os.path.exists(directory):
        os.makedirs(directory)
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

def sort_misc(directory):
    global misc_files
    misc_files = []
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

#TODO: Make the extensions lists editable
document_extensions = [".txt", ".pdf", ".docx", ".md"]
program_extensions = [".exe", ".msi"]
compressed_extensions = [".zip", ".7z", ".tar", ".cab", ".bz2", ".rar", ".xz"]
sound_extensions = [".mp3", ".wav", ".aac", ".flac"]
image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".tiff", ".ico"]
dskimg_extensions = [".iso", ".img", ".esd"]
all_extensions = document_extensions + program_extensions + compressed_extensions + sound_extensions + image_extensions + dskimg_extensions

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
        custom_directory_input = download_dir + input("Enter a subdirectory name(such as ISOs/): ")
        sort_custom(custom_directory_input, custom_extensions_input, "")
    elif sys.argv[1] == "-chgdir":
        change_dir(True)
    elif sys.argv[1] == "-help":
        print(help_text)
    else:
        print(help_text)