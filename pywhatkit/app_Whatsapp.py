import os
import time
import webbrowser as web
from datetime import datetime
from re import fullmatch
from typing import List
from urllib.parse import quote
import paperclip
import pyautogui as pg
import pyperclip
import keyboard
from pywhatkit.core import core, exceptions, log
from typing import Union
import streamlit as st
pg.FAILSAFE = False

core.check_connection()



def sendwhatmsg_instantly(
        phone_no: str,
        message: str,
        wait_time: int = 0,
        tab_close: bool = False,
        close_time: int = 3,
) -> None:
    """Send WhatsApp Message Instantly"""

    if not core.check_number(number=phone_no):
        raise exceptions.CountryCodeException("Country Code Missing in Phone Number!")

    phone_no = phone_no.replace(" ", "")
    if not fullmatch(r"^\+?[0-9]{2,4}\s?[0-9]{9,15}", phone_no):
        raise exceptions.InvalidPhoneNumber("Invalid Phone Number.")

    web.open(f"https://web.whatsapp.com/send?phone={phone_no}&text={quote(message)}")
    time.sleep(wait_time)
    index = 0
    message ="..........................................................."
    length = len(message)
    while index < length:
        letter = message[index]
        pg.write(letter)
        if letter == ":":
            index += 1
            while index < length:
                letter = message[index]
                if letter == ":":

                    pg.press("enter")
                    break
                pg.write(letter)
                index += 1
        index += 1
    pg.press("enter")
    log.log_message(_time=time.localtime(), receiver=phone_no, message=message)
    if tab_close:
        core.close_tab(wait_time=close_time)


def sendimg_or_video_immediately(
        phone_no: str,
        path: str,
        wait_time: int = 0,
        tab_close: bool = False,
        close_time: int = 3,
) -> None:
    """Send WhatsApp Message Instantly"""

    if not core.check_number(number=phone_no):
        raise exceptions.CountryCodeException("Country Code Missing in Phone Number!")

    phone_no = phone_no.replace(" ", "")
    if not fullmatch(r"^\+?[0-9]{2,4}\s?[0-9]{9,15}", phone_no):
        raise exceptions.InvalidPhoneNumber("Invalid Phone Number.")

    web.open(f"https://web.whatsapp.com/send?phone={phone_no}")
    time.sleep(wait_time)
    core.find_link()
    time.sleep(1)
    core.find_photo_or_video()

    pyperclip.copy(os.path.abspath(path))
    print("Copied")
    time.sleep(1)
    keyboard.press("ctrl")
    keyboard.press("v")
    keyboard.release("v")
    keyboard.release("ctrl")
    time.sleep(1)
    keyboard.press("enter")
    keyboard.release("enter")
    time.sleep(1)
    keyboard.press("enter")
    keyboard.release("enter")
    if tab_close:
        core.close_tab(wait_time=close_time)


# def sendwhatdoc_immediately(
#         phone_no: str,
#         path: str,
#         wait_time: int = 15,
#         tab_close: bool = True,
#         close_time: int = 3,
# ) -> None:
#     """Send WhatsApp Message Instantly"""

#     if not core.check_number(number=phone_no):
#         raise exceptions.CountryCodeException("Country Code Missing in Phone Number!")

#     phone_no = phone_no.replace(" ", "")
#     if not fullmatch(r"^\+?[0-9]{2,4}\s?[0-9]{9,15}", phone_no):
#         raise exceptions.InvalidPhoneNumber("Invalid Phone Number.")

#     web.open(f"https://web.whatsapp.com/send?phone={phone_no}")
#     time.sleep(wait_time)
#     core.find_link()
#     time.sleep(1)
#     core.find_document()
#     pyperclip.copy(os.path.abspath(path))
#     print("Copied")
#     time.sleep(1)
#     keyboard.press("ctrl")
#     keyboard.press("v")
#     keyboard.release("v")
#     keyboard.release("ctrl")
#     time.sleep(1)
#     keyboard.press("enter")
#     keyboard.release("enter")
#     time.sleep(1)
#     keyboard.press("enter")
#     keyboard.release("enter")
#     if tab_close:
#         core.close_tab(wait_time=close_time)


def sendwhatmsg(
        phone_no: str,
        message: Union[list, str],
        time_hour: int,
        time_min: int,
        wait_time: int = 0,
        tab_close: bool = False,
        close_time: int = 3,
) -> None:
    """Send a WhatsApp Message at a Certain Time"""
    if not core.check_number(number=phone_no):
        raise exceptions.CountryCodeException("Country Code Missing in Phone Number!")

    phone_no = phone_no.replace(" ", "")
    if not fullmatch(r'^\+?[0-9]{2,4}\s?[0-9]{9,15}', phone_no):
        raise exceptions.InvalidPhoneNumber("Invalid Phone Number.")

    if time_hour not in range(25) or time_min not in range(60):
        raise Warning("Invalid Time Format!")

    current_time = time.localtime()
    left_time = datetime.strptime(
        f"{time_hour}:{time_min}:0", "%H:%M:%S"
    ) - datetime.strptime(
        f"{current_time.tm_hour}:{current_time.tm_min}:{current_time.tm_sec}",
        "%H:%M:%S",
    )

    if left_time.seconds < wait_time:
        raise exceptions.CallTimeException(
            "Call Time must be Greater than Wait Time as WhatsApp Web takes some Time to Load!"
        )

    sleep_time = left_time.seconds - wait_time
    print(
        f"In {sleep_time} Seconds WhatsApp will open and after {wait_time} Seconds Message will be Delivered!"
    )
    time.sleep(sleep_time)
    if isinstance(message, list):
        core.send_message_list(message=message, receiver=phone_no, wait_time=wait_time)
    else:
        core.send_message(message=message, receiver=phone_no, wait_time=wait_time)
        log.log_message(_time=current_time, receiver=phone_no, message=message)

    if tab_close:
        core.close_tab(wait_time=close_time)


def sendwhatmsg_to_group(
        group_id: str,
        message: str,
        time_hour: int,
        time_min: int,
        wait_time: int = 0,
        tab_close: bool = False,
        close_time: int = 3,
) -> None:
    """Send WhatsApp Message to a Group at a Certain Time"""

    if time_hour not in range(25) or time_min not in range(60):
        raise Warning("Invalid Time Format!")

    current_time = time.localtime()
    left_time = datetime.strptime(
        f"{time_hour}:{time_min}:0", "%H:%M:%S"
    ) - datetime.strptime(
        f"{current_time.tm_hour}:{current_time.tm_min}:{current_time.tm_sec}",
        "%H:%M:%S",
    )

    if left_time.seconds < wait_time:
        raise exceptions.CallTimeException(
            "Call Time must be Greater than Wait Time as WhatsApp Web takes some Time to Load!"
        )

    sleep_time = left_time.seconds - wait_time
    print(
        f"In {sleep_time} Seconds WhatsApp will open and after {wait_time} Seconds Message will be Delivered!"
    )
    time.sleep(sleep_time)
    core.send_message(message=message, receiver=group_id, wait_time=wait_time)
    log.log_message(_time=current_time, receiver=group_id, message=message)
    if tab_close:
        core.close_tab(wait_time=close_time)


def sendwhatmsg_to_group_instantly(
        group_id: str,
        message: str,
        wait_time: int = 0,
        tab_close: bool = False,
        close_time: int = 3,
) -> None:
    """Send WhatsApp Message to a Group Instantly"""

    current_time = time.localtime()
    time.sleep(4)
    core.send_message(message=message, receiver=group_id, wait_time=wait_time)
    log.log_message(_time=current_time, receiver=group_id, message=message)
    if tab_close:
        core.close_tab(wait_time=close_time)


def sendwhatsmsg_to_all(
        phone_nos: List[str],
        message: str,
        time_hour: int,
        time_min: int,
        wait_time: int = 0,
        tab_close: bool = False,
        close_time: int = 3,
):
    for phone_no in phone_nos:
        sendwhatmsg(
            phone_no, message, time_hour, time_min, wait_time, tab_close, close_time
        )


def sendwhats_image(
        receiver: str,
        img_path: str,
        time_hour: int,
        time_min: int,
        caption: str = "",
        wait_time: int = 0,
        tab_close: bool = False,
        close_time: int = 3,
) -> None:
    """Send Image to a WhatsApp Contact or Group at a Certain Time"""

    if (not receiver.isalnum()) and (not core.check_number(number=receiver)):
        raise exceptions.CountryCodeException("Country Code Missing in Phone Number!")

    current_time = time.localtime()
    left_time = datetime.strptime(
        f"{time_hour}:{time_min}:0", "%H:%M:%S"
    ) - datetime.strptime(
        f"{current_time.tm_hour}:{current_time.tm_min}:{current_time.tm_sec}",
        "%H:%M:%S",
    )

    if left_time.seconds < wait_time:
        raise exceptions.CallTimeException(
            "Call Time must be Greater than Wait Time as WhatsApp Web takes some Time to Load!"
        )

    sleep_time = left_time.seconds - wait_time
    print(
        f"In {sleep_time} Seconds WhatsApp will open and after {wait_time} Seconds Image will be Delivered!"
    )
    time.sleep(sleep_time)
    core.send_image(
        path=img_path, caption=caption, receiver=receiver, wait_time=wait_time
    )
    log.log_image(_time=current_time, path=img_path, receiver=receiver, caption=caption)
    if tab_close:
        core.close_tab(wait_time=close_time)


def open_web() -> bool:
    """Opens WhatsApp Web"""

    try:
        web.open("https://web.whatsapp.com")
    except web.Error:
        return False
    else:
        return True
    
massage ='''
Greetings of the day,

I hope this message finds you well! 😊

I wanted to introduce you to Dmaax Real Estate, where we're passionate about helping you find your dream property. Whether you're looking for a new home, an investment opportunity, or a place that suits your lifestyle, we've got you covered.

At Dmaxx, we believe in making your property search a breeze, offering:

🏡 A diverse range of properties to match your preferences.
💼 Expert guidance on the real estate market.
📈 Investment insights for those looking to grow their portfolios.
🤝 Personalized service tailored to your needs.

If you're open to exploring the exciting world of real estate, I'd love to connect with you and discuss how we can assist you in achieving your property goals.

Feel free to reply to this message, and we can schedule a time for a quick chat or meeting at your convenience.
'''

import csv

# Define a function to format phone numbers
def format_phone_number(country, mobile):
    if country == 'QAT':
        mobile = mobile.replace('00974', '+974').lstrip('0')
    elif country == 'Finland':
        mobile = mobile.replace('00358', '+358').lstrip('0')
    elif country == 'Norway':
        mobile = mobile.replace('0047', '+47').lstrip('0')
    elif country == 'UAE':
        mobile = '+971' + mobile.replace('00971', '').lstrip('0')
    elif country == 'Croatia':
        mobile = mobile.replace('00385', '+385').lstrip('0')
    elif country == 'Jordan':
        mobile = mobile.replace('00962', '+962').lstrip('0')
    elif country == 'Azerbaijan':
        mobile = mobile.replace('00994', '+994').lstrip('0')
    elif country == 'Malta':
        mobile = mobile.replace('00356', '+356').lstrip('0')
    elif country == 'Pakistan':
        mobile = mobile.replace('0092', '+92').lstrip('0')
    elif country == 'Oman':
        mobile = mobile.replace('00968', '+968').lstrip('0')
    elif country == 'Poland':
        mobile = mobile.replace('0048', '+48').lstrip('0')
    elif country == 'Bangladesh':
        mobile = mobile.replace('00880', '+880').lstrip('0')
    elif country == 'Afghanistan':
        mobile = mobile.replace('0093', '+93').lstrip('0')
    elif country == 'AUS':
        mobile = mobile.replace('0061', '+61').lstrip('0')
    elif country == 'UK & UAE':
        mobile = mobile.replace('0044', '+44').replace('00971', '+971').lstrip('0')
    elif country == 'Kuwait':
        mobile = mobile.replace('00965', '+965').lstrip('0')
    elif country == 'Iraq':
        mobile = mobile.replace('00964', '+964').lstrip('0')
    elif country == 'United Kingdom':
        mobile = mobile.replace('0044', '+44').lstrip('0')
    elif country == 'Kazakhstan':
        mobile = mobile.replace('0007', '+7').lstrip('0')
    elif country == 'Luxembourg':
        mobile = mobile.replace('00352', '+352').lstrip('0')
    elif country == 'Nigeria':
        mobile = mobile.replace('00234', '+234').lstrip('0')
    elif country == 'Iceland':
        mobile = mobile.replace('00354', '+354').lstrip('0')
    elif country == 'Armenia':
        mobile = mobile.replace('00374', '+374').lstrip('0')
    elif country == 'Tanzania, United Republic of':
        mobile = mobile.replace('00255', '+255').lstrip('0')
    elif country == 'USA':
        mobile = mobile.replace('0001', '+1').lstrip('0')
    elif country == 'Spain':
        mobile = mobile.replace('0034', '+34').lstrip('0')
    elif country == 'Lebanon':
        mobile = mobile.replace('00961', '+961').lstrip('0')
    elif country == 'Tunisia':
        mobile = mobile.replace('00216', '+216').lstrip('0')
    elif country == 'Monaco':
        mobile = mobile.replace('00377', '+377').lstrip('0')
    elif country == 'LEB':
        mobile = mobile.replace('00961', '+961').lstrip('0')
    elif country == 'FRA':
        mobile = mobile.replace('0033', '+33').lstrip('0')
    elif country == 'Australia':
        mobile = mobile.replace('0061', '+61').lstrip('0')
    elif country == 'SW':
        mobile = mobile.replace('0046', '+46').lstrip('0')
    elif country == 'Singapore':
        mobile = mobile.replace('0065', '+65').lstrip('0')
    elif country == 'KUW':
        mobile = mobile.replace('00965', '+965').lstrip('0')
    elif country == 'Zimbabwe':
        mobile = mobile.replace('00263', '+263').lstrip('0')
    elif country == 'India':
        mobile = mobile.replace('0091', '+91').lstrip('0')
    elif country == 'Italy':
        mobile = mobile.replace('0039', '+39').lstrip('0')
    elif country == 'Mauritius':
        mobile = mobile.replace('00230', '+230').lstrip('0')
    elif country == 'Uzbekistan':
        mobile = mobile.replace('00998', '+998').lstrip('0')
    elif country == 'Kenya':
        mobile = mobile.replace('00254', '+254').lstrip('0')
    elif country == 'Bulgaria':
        mobile = mobile.replace('00359', '+359').lstrip('0')
    elif country == 'Japan':
        mobile = mobile.replace('0081', '+81').lstrip('0')
    elif country == 'Saudi Arabia':
        mobile = mobile.replace('00966', '+966').lstrip('0')
    elif country == 'Denmark':
        mobile = mobile.replace('0045', '+45').lstrip('0')
    elif country == 'Algeria':
        mobile = mobile.replace('00213', '+213').lstrip('0')
    elif country == 'Nepal':
        mobile = mobile.replace('00977', '+977').lstrip('0')
    elif country == 'Switzerland':
        mobile = mobile.replace('0041', '+41').lstrip('0')
    elif country == 'Canada':
        mobile = mobile.replace('0001', '+1').lstrip('0')
    elif country == 'Bahrain':
        mobile = mobile.replace('00973', '+973').lstrip('0')
    elif country == 'Ireland':
        mobile = mobile.replace('00353', '+353').lstrip('0')
    elif country == 'Russian Federation':
        mobile = mobile.replace('0007', '+7').lstrip('0')
    elif country == 'Slovakia':
        mobile = mobile.replace('00421', '+421').lstrip('0')
    elif country == 'Maldives':
        mobile = mobile.replace('00960', '+960').lstrip('0')
    elif country == 'United States':
        mobile = mobile.replace('0001', '+1').lstrip('0')
    elif country == 'Kyrgyzstan':
        mobile = mobile.replace('00996', '+996').lstrip('0')
    elif country == 'Greece':
        mobile = mobile.replace('0030', '+30').lstrip('0')
    elif country == 'GER':
        mobile = mobile.replace('0049', '+49').lstrip('0')
    elif country == 'Germany':
        mobile = mobile.replace('0049', '+49').lstrip('0')
    elif country == 'Thailand':
        mobile = mobile.replace('0066', '+66').lstrip('0')
    elif country == 'Belarus':
        mobile = mobile.replace('00375', '+375').lstrip('0')
    elif country == 'UAE & BELGIUM':
        mobile = mobile.replace('00971', '+971').lstrip('0')
    elif country == 'Country':
        mobile = mobile  # No change for 'Country'
    elif country == 'Albania':
        mobile = mobile.replace('00355', '+355').lstrip('0')
    elif country == 'United Arab Emirates':
        mobile = mobile.replace('00971', '+971').lstrip('0')
    elif country == 'Iran':
        mobile = mobile.replace('0098', '+98').lstrip('0')
    elif country == 'Turkey':
        mobile = mobile.replace('0090', '+90').lstrip('0')
    elif country == 'Qatar':
        mobile = mobile.replace('00974', '+974').lstrip('0')
    elif country == 'Hong Kong':
        mobile = mobile.replace('00852', '+852').lstrip('0')
    elif country == 'Latvia':
        mobile = mobile.replace('00371', '+371').lstrip('0')
    elif country == 'Netherlands':
        mobile = mobile.replace('0031', '+31').lstrip('0')
    elif country == 'Portugal':
        mobile = mobile.replace('00351', '+351').lstrip('0')
    elif country == 'KSA':
        mobile = mobile.replace('00966', '+966').lstrip('0')
    elif country == 'Belgium':
        mobile = mobile.replace('0032', '+32').lstrip('0')
    elif country == 'Egypt':
        mobile = mobile.replace('0020', '+20').lstrip('0')
    elif country == 'Cyprus':
        mobile = mobile.replace('00357', '+357').lstrip('0')
    elif country == 'Sri Lanka':
        mobile = mobile.replace('0094', '+94').lstrip('0')
    elif country == 'Hungary':
        mobile = mobile.replace('0036', '+36').lstrip('0')
    elif country == 'Sweden':
        mobile = mobile.replace('0046', '+46').lstrip('0')
    elif country == 'South Africa':
        mobile = mobile.replace('0027', '+27').lstrip('0')
    elif country == 'Gibraltar':
        mobile = mobile.replace('00350', '+350').lstrip('0')
    elif country == 'RUS':
        mobile = mobile.replace('0007', '+7').lstrip('0')
    elif country == 'Malaysia':
        mobile = mobile.replace('0060', '+60').lstrip('0')
    elif country == 'Yemen':
        mobile = mobile.replace('00967', '+967').lstrip('0')
    elif country == 'UK':
        mobile = mobile.replace('0044', '+44').lstrip('0')
    elif country == 'Austria':
        mobile = mobile.replace('0043', '+43').lstrip('0')
    elif country == 'France':
        mobile = mobile.replace('0033', '+33').lstrip('0')
    elif country == 'Syrian Arab Republic':
        mobile = mobile.replace('00963', '+963').lstrip('0')


    
    return mobile
import csv
formatted_numbers = []
a = ""
def process_phone_numbers(a):
    # Create an empty list to store the formatted phone numbers
    # Open the CSV file and process each line
    with open(a, 'r') as csvfile:
        reader = csv.reader(csvfile)
        #print(reader)
        for row in reader:
            print(row)
            if len(row) == 2:
                country, mobile = row
                print(1213)
                print(country, mobile)
                formatted_mobile = format_phone_number(country, mobile)
                print(formatted_mobile)
                if formatted_mobile:
                    formatted_numbers.append(formatted_mobile)

    # Your list of strings

    # Iterate through the list and add '+' if missing
    for i in range(len(formatted_numbers)):
        if not formatted_numbers[i].startswith('+'):
            formatted_numbers[i] = '+' + formatted_numbers[i]

    #formaformatted_numbers

    print(formatted_numbers)
    # Remove values that don't start with '+971'
    Uae_nos = [number for number in formatted_numbers if number.startswith('+971')]

    return Uae_nos  # Return the formatted numbers

def send_whatsapp_messages(numbers, massage):
    for i, n in enumerate(formatted_numbers):
        try:
            if i >= 127:  # Start after the 120th iteration
                sendwhatmsg_instantly(n, massage, 0, True, 3)
                print(f"Message sent to {n}")
        except Exception as e:
            print(f"Failed to send message to {n} with error: {str(e)}")
        print(i)

def main():
    st.title("WhatsApp Messaging App")

    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
    st.write(uploaded_file)
    print(uploaded_file)
    if uploaded_file is not None:
        st.write("File Uploaded!")
        a = r"/home/aisoftbuilders/Desktop/PyWhatKit/pywhatkit/ali - test campaign.csv"
        print(121)
        print(a)
        # Process the uploaded CSV file and extract phone numbers
        process_phone_numbers(a)
        # Display the formatted phone numbers
        st.subheader("Formatted Phone Numbers:")
        st.write(formatted_numbers)

        # Input field for custom message
        user_message = st.text_area("Custom Message (with spaces and indentation)", value=massage)

        # Send messages button
        if st.button("Send Messages"):
            if not user_message:
                st.warning("Please enter a message.")
            else:
                send_whatsapp_messages(formatted_numbers, user_message)

if __name__ == "__main__":
    main()