
import flet import *
import string
import random
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import routeros_api

# Characters for password generation
characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")


# Function to generate a random password
def generate_random_password(length=8):
    random.shuffle(characters)
    password = [random.choice(characters) for _ in range(length)]
    random.shuffle(password)
    return "".join(password)


# Function to create a user card image
def create_card(username, password, output_path="cardEdited.png"):
    img = Image.open('card.jpg')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('font/DINNextLTArabic-Medium-4.ttf', 30)
    draw.text((220, 190), username, font=font, fill=(90, 90, 90))
    draw.text((125, 250), password, font=font, fill=(90, 90, 90))
    img.save(output_path)


# Main function to generate users and add to MikroTik
def start_generation(username_list, add_to_mikrotik, host, profile, mikrotik_username, mikrotik_password, status_label):
    try:
        api = None
        if add_to_mikrotik:
            connection = routeros_api.RouterOsApiPool(host, username=mikrotik_username, password=mikrotik_password, plaintext_login=True)
            api = connection.get_api()
            if not api.get_resource('ip/hotspot/user/profile').get(name=profile):
                status_label.value = "ط®ط·ط£ ظپظٹ ط§ط³ظ… ط§ظ„ط¨ط±ظˆظپط§ظٹظ„"
                return

        for username in username_list:
            password = generate_random_password()
            if add_to_mikrotik:
                api.get_resource('ip/hotspot/user').add(name=username, password=password, profile=profile)
            create_card(username, password)
            status_label.value = f"طھظ… ط¥ظ†ط´ط§ط، ط§ظ„ط¨ط·ط§ظ‚ط© ظ„ظ„ظ…ط³طھط®ط¯ظ… {username}"
            status_label.update()

        status_label.value = "طھظ… ط§ظ„ط§ظ†طھظ‡ط§ط، ط¨ظ†ط¬ط§ط­"
    except Exception as e:
        status_label.value = f"ط­ط¯ط« ط®ط·ط£: {str(e)}"


# UI function with Flet
def main(page: ft.Page):
    page.title = "SADA PM - ط¥ظ†ط´ط§ط، ط¨ط·ط§ظ‚ط§طھ ط§ظ„ظ…ط³طھط®ط¯ظ…ظٹظ†"
    page.scroll = "auto"

    # UI Elements
    mikrotik_host = ft.TextField(label="IP ط¬ظ‡ط§ط² ط§ظ„ظ…ط§ظٹظƒط±ظˆطھظٹظƒ", width=300)
    mikrotik_username = ft.TextField(label="ط§ط³ظ… ط§ظ„ظ…ط³طھط®ط¯ظ…", width=300)
    mikrotik_password = ft.TextField(label="ظƒظ„ظ…ط© ط§ظ„ظ…ط±ظˆط±", password=True, width=300)
    profile = ft.TextField(label="ط§ط³ظ… ط§ظ„ط¨ط±ظˆظپط§ظٹظ„", width=300)
    add_to_mikrotik = ft.Checkbox(label="ط¥ط¶ط§ظپط© ط§ظ„ظ…ط³طھط®ط¯ظ…ظٹظ† ط¥ظ„ظ‰ ظ…ط§ظٹظƒط±ظˆطھظٹظƒ")
    status_label = ft.Text("")
    username_file = ft.FilePicker(on_result=lambda e: None)
    file_button = ft.ElevatedButton("ط§ط®طھط± ظ…ظ„ظپ ط§ظ„ظ…ط³طھط®ط¯ظ…ظٹظ†", on_click=lambda e: username_file.pick_files())

    # Start generation button
    def start_button_click(e):
        try:
            username_list = pd.read_excel(username_file.result.files[0].path, index_col=0).index.tolist()
            start_generation(
                username_list,
                add_to_mikrotik.value,
                mikrotik_host.value,
                profile.value,
                mikrotik_username.value,
                mikrotik_password.value,
                status_label
            )
        except Exception as ex:
            status_label.value = f"ط­ط¯ط« ط®ط·ط£ ط£ط«ظ†ط§ط، ط§ظ„ظ‚ط±ط§ط،ط©: {ex}"
            status_label.update()

    start_button = ft.ElevatedButton("ط¨ط¯ط، ط§ظ„ط¹ظ…ظ„ظٹط©", on_click=start_button_click)

    # Adding elements to the page
    page.add(
        mikrotik_host,
        mikrotik_username,
        mikrotik_password,
        profile,
        add_to_mikrotik,
        file_button,
        start_button,
        status_label
    )


# Run the Flet app
app(main)
