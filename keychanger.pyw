'''
Russell Dranch
Python keychanger
Install under pyinstaller: pyinstaller keychanger.pyw --onefile
'''
# Basic imports for program to run successfully
import time, random, subprocess, ctypes


# Dict Language associated with windows language ID 
keys = {
	"Arabic":"401",
	"Chinese":"804",
	"English":"409",
	"Greek":"408",
	"Hindi":"439",
	"Italian":"410",
	"Korean":"412",
	"Portuguese":"816"
}

# Dict Language associated with windows string ID
short = {
	"Arabic":"ar-SA",
	"Chinese":"zh-CN",
	"English":"en-US",
	"Greek":"el-GR",
	"Hindi":"hi-IN",
	"Italian":"it-IT",
	"Korean":"ko-KR",
	"Portuguese":"pt-PT"
}

# List of messagebox popup's
# Format: Title Flags Message
lst = [
	"Warning 0x00000014 Are you sure you want to delete C:\\Windows\\System32\\?",
	"Warning 0x00000035 Please confirm you'd like to restart your computer.",
	"WindowsVirusScan 0x00000014 Found infected file 'Microsoft Windows'\nRemove it?",
	"ERROR 0x00000040 ERROR! A system failure has occurred 0x00032A1C. Please contact customer support.",
	"ERROR 0x00000015 An error has occurred while resetting your machine. Do you want to continue?",
	"DiskCleaner 0x00000056 You've run out of space. Would you like to clear up space from C:\\Windows\\System32\\?",
	"RandomError 0x00000030 You haven't gotten any error messages recently so here is one just to make sure you know we haven't started caring yet.",
	"Catastrophic 0x00000041 Catastrophic error failed successfully. Do you wish to continue?"
]

# List of messagebox popup's reply
# Format: Title Flags Message
lst_rep = [
	"Windows10 0x00000040 Warning! Task failed successfully.",
	"KeyboardError 0x00004030 Keyboard not responding. Press any key to continue.",
	"Warning 0x00000036 Are you sure you want to resend 'Recycle Bin' to the Recycle Bin?",
	"Done 0x00000030 \n\nERROR!\nTo print this window click OK.",
	"Error 0x00000010 An error has occurred while creating an error report.",
	"ErrorError 0x00000035 An error has occured while displaying the previous error."
]

'''
Main function of program - Will infinitely run until computer restarts
1) Choses random language
2) Changes keyboard language based on whatever was picked. This is done over powershell and utilizes subprocess
3) Choses random message and error reply
4) Parses through the random message and error reply to create a popup box with some message
5) Function sleeps for 10 seconds then repeats to annoy users
'''
def main():

	while True:
		rand = random.choice(list(keys.keys()))

		#print("Changed to " + rand + " " + short[rand])
		subprocess.Popen('powershell.exe Set-WinUserLanguageList -LanguageList ' + short[rand] + ' -Force')

		msg_one = random.choice(lst).split(" ", 2)[2]
		error_one = ctypes.c_ulong(int(random.choice(lst).split(" ", 2)[1], 16))
		title_one = random.choice(lst).split(" ", 2)[0]

		msg_two = random.choice(lst_rep).split(" ", 2)[2]
		error_two = ctypes.c_ulong(int(random.choice(lst_rep).split(" ", 2)[1], 16))
		title_two = random.choice(lst_rep).split(" ", 2)[0]

		ctypes.windll.user32.MessageBoxW(0, msg_one, title_one, error_one)
		ctypes.windll.user32.MessageBoxW(0, msg_two, title_two, error_two)

		time.sleep(10)

main()