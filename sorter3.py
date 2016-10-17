#import relevant libraries: glob for searching for files, os for manipulating files, sys for getting the arguments
import glob
import os
import sys
from functions import *


#working out if this is your first time using it (creates config file if it doesn't exist)
if not os.path.exists("config") or os.stat("config").st_size == 0:
    with open("config", mode="w") as config:
        config.write("first_time=yes")

load_config()

#change to the directory that's written in the config file
change_dir(False)

#{path:extension}
file_dict = {os.path.realpath(f):os.path.splitext(f)[1] for f in glob.glob("*.*")}
help_text = "This program sorts your downloads. Use these arguments to choose what to sort:\n\t-docs\t\tsorts your documents\n\t-progs\t\tsorts your programs\n\t-compressed\tsorts your compressed files\n\t-sound\t\tsorts your sound files\n\t-image\t\tsorts your image files\n\t-dskimg\t\tsorts your disk image files\n\t-misc\t\tsorts your miscellaneous files\n\t-all\t\tsorts all file types\n\t-custom\t\tcustomisable file sort\n\t-chgdir\t\tchanges the downloads folder\n\t-help\t\tshows this help text"

#TODO: Make the extensions lists editable
#TODO: Save the extensions dictionary as a txt file
#TODO: Make these extensions not case sensitive
document_extensions = [".txt", ".pdf", ".docx", ".md"]
program_extensions = [".exe", ".msi"]
compressed_extensions = [".zip", ".7z", ".tar", ".cab", ".bz2", ".rar", ".xz"]
sound_extensions = [".mp3", ".wav", ".aac", ".flac"]
image_extensions = [".jpg", ".jpeg", ".JPEG", ".JPG", ".png", ".gif", ".tiff", ".ico"]
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