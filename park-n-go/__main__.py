import os, platform

if platform.system() == "Windows":
    os.system("winget install wkhtmltopdf")
elif platform.system() == "Linux":
    os.system("sudo apt install wkhtmltopdf")
else:
    print("Your distribution is not supported at the moment, try on Windows or Linux, or open up an issue")
    exit()

os.chdir("park-n-go")
os.system("python main.py")