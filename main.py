
from unicodedata import name
import pandas as pd
import string
import random
# Importing the PIL library
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import tkinter as tk
from tkinter import Button, filedialog
import routeros_api


## characters to generate password from
characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")




 
# Open an Image

def createCard(username, password):
	img = Image.open('card.jpg')
	
	# Call draw Method to add 2D graphics in an image
	I1 = ImageDraw.Draw(img)
	
	# Custom font style and font size
	myFont = ImageFont.truetype('font\DINNextLTArabic-Medium-4.ttf', 30)
	
	# Add Text to an image
	I1.text((220, 190), username, font=myFont, fill =(90, 90, 90))
	I1.text((125, 250), password, font=myFont, fill =(90, 90, 90))
	
	# Display edited image
	
	# Save the edited image
	img.save("cardEdited.png")

is_select_folder_path = False
def pastImg(loopsCounter, loopEndCounter):
	folder_path ="output/"
 
	if is_select_folder_path:
		folder_path = file_path + "/"
	CardListName = 'cardList'+ str(loopEndCounter) +'.png'
	im1 = Image.open('empty.png')
	if loopsCounter > 0:	
		im1 = Image.open(folder_path + CardListName)
	im2 = Image.open('cardEdited.png')

	position = {
		0: (25, 25),
  		1: (600, 25),
    	2: (25, 380),
     	3: (600, 380),
		4: (25, 740),
		5: (600, 740),
		6: (25, 1100),
		7: (600, 1100),
		8: (25, 1430),
  		9:(600, 1430)
	}

	im2 = im2.resize((500, 300))
	back_im = im1.copy()
	back_im.paste(im2, position[loopsCounter])
	back_im.save(folder_path + CardListName, quality=100)

def generate_random_password():
	## length of password from the user
	length = 8

	## shuffling the characters
	random.shuffle(characters)
	
	## picking random characters from the list
	password = []
	for i in range(length):
		password.append(random.choice(characters))

	## shuffling the resultant password
	random.shuffle(password)

	## converting the list to string
	## printing the list
	return "".join(password)



def getExcel():
    df = pd.read_excel (r'excel.xlsx', index_col=0)
    return df.index

usernameList = getExcel()

def startGen(is_add_to_mikrotik=0, host="", profile="", my_label=None, mikrotik_username="", mikrotik_password=""):
	from routeros_api.exceptions import RouterOsApiCommunicationError, RouterOsApiConnectionError
	loopsCounter = 0
	loopEndCounter = 0
 	
	api = None
	if is_add_to_mikrotik:
		try:
			connection = routeros_api.RouterOsApiPool(host, username=mikrotik_username, password=mikrotik_password, plaintext_login=True)
			api = connection.get_api()
		except RouterOsApiCommunicationError:
			my_label.config(text = "خطاء في اسم المستخدم وكلمة المرور")
			return
		except RouterOsApiConnectionError:
			my_label.config(text = "لا يمكن الاتصال بجهاز الميكروتيك")
			return
	for i in usernameList:
		username = i
		password = generate_random_password()
		if isinstance(i, (float)):
			continue
		if is_add_to_mikrotik:
			if not api.get_resource('ip/hotspot/user/profile').get(name=profile):
				my_label.config(text = "هناك خطاء في في اسم البروفايل")
				return

			try:
				api.get_resource('ip/hotspot/user').add(name=username, password=password, profile=profile)
			except:
				pass
		createCard(username, password)
		pastImg(loopsCounter, loopEndCounter)
		print("username: " + username, "  password: " + password, "Done")
		loopsCounter += 1
		if loopsCounter >= 10:
			loopsCounter = 0
			loopEndCounter +=1
	my_label.config(text = "تم الانتهاء بنجاح")

def get_file_path():
    global file_path
    # Open and return file path
    file_path= filedialog.askdirectory()
    global is_select_folder_path
    is_select_folder_path = True
    

root = tk.Tk()
check_1 = tk.IntVar()
root.title("SADA PM")
root.geometry("400x400")
label = tk.Label(root, text="SADA PM استخراج البطاقات")
label.pack()



add_to_mikrotik = tk.Checkbutton(root, text="اضافة المستخدمين الى مايكروتيك", onvalue = 1, offvalue = 0, variable=check_1)
add_to_mikrotik.pack()

tk.Label(root, text="ايبي المايكروتيك").pack()
mikrotik_host = tk.Entry(root)
mikrotik_host.pack()

tk.Label(root, text="اسم المستخدم للمايكروتيك").pack()
mikrotik_username = tk.Entry(root)
mikrotik_username.pack()

tk.Label(root, text="كلمة المرور للمايكروتيك").pack()
mikrotik_password = tk.Entry(root)
mikrotik_password.pack()


tk.Label(root, text="بروفايل المستخدمين").pack()
profile = tk.Entry(root)
profile.pack()


tk.Label(root, text = "عند البدء يرجى الانتظار وعدم اغلاق النافذا").pack()
def getvalue():
	is_add_to_mikrotik = check_1.get()

	startGen(is_add_to_mikrotik,mikrotik_host.get(), profile.get(), my_label, mikrotik_username.get() ,mikrotik_password.get())

b1 = tk.Button(root, text = "مكان حفظ الصور", command = get_file_path).pack()

tk.Button(root, text="بدء", command=getvalue).pack()
my_label = tk.Label(root, text = "")
my_label.pack()
root.mainloop()