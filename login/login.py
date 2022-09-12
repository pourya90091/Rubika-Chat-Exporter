from initialize import driver, login_data_dir, chat_box_xpath, folders_container_xpath, phone_number, chat_name, time_out
from selenium.webdriver.common.keys import Keys
from utils.utils import wastetime_counter, hash_key
from time import sleep


def login():
    auth = get_auth()
    profile = get_profile()

    if auth == "" or profile == "":
        manual_login()

        while True:
            if logged_in() is True:
                break
            sleep(time_out)

        save_login_data()
    else:
        driver.execute_script(f"localStorage.setItem('auth', '{auth}');")
        driver.execute_script(f"localStorage.setItem('profile', '{profile}');")

        if logged_in() is not True:
            with open(f"{login_data_dir}/auth.txt", "w") as file:
                file.write("")
            with open(f"{login_data_dir}/profile.txt", "w") as file:
                file.write("")

            login()

    print("\nLogged in")

    opened_chat = open_chat()
    if opened_chat:
        print("\nThe chat is opened")

        chat_id = driver.find_element("xpath", chat_box_xpath).get_attribute("data-chat-id")
        return chat_id
    else: 
        raise Exception("The chat doesn't open")


@wastetime_counter
def manual_login():
    try:
        phone_number_input = driver.find_element("xpath", "//*[@id='auth-pages']/div/div[2]/div[1]/div/div[3]/div[3]/input[1]")
        phone_number_input.send_keys(phone_number + Keys.ENTER)

        verification_code = input("\nEenter verification code: ")

        verification_code_input = driver.find_element("xpath", "//*[@id='auth-pages']/div/div[2]/div[2]/div/div[4]/div/input")
        verification_code_input.send_keys(verification_code + Keys.ENTER)
    except:
        raise Exception("Manual login failed")


def get_auth():
    try:
        with open(f"{login_data_dir}/auth.txt", "r") as file:
            auth = hash_key(file.read())
    except FileNotFoundError:
        with open(f"{login_data_dir}/auth.txt", "w") as file:
            file.write("")
            auth = ""
    finally:
        return auth


def get_profile():
    try:
        with open(f"{login_data_dir}/profile.txt", "r") as file:
            profile = hash_key(file.read())
    except FileNotFoundError:
        with open(f"{login_data_dir}/profile.txt", "w") as file:
            file.write("")
            profile = ""
    finally:
        return profile


def save_login_data():
    auth = driver.execute_script("return localStorage.getItem('auth');")
    profile = driver.execute_script("return localStorage.getItem('profile');")

    with open(f"{login_data_dir}/auth.txt", "w") as file:
        file.write(hash_key(auth))
    with open(f"{login_data_dir}/profile.txt", "w") as file:
        file.write(hash_key(profile))


def open_chat():

    def click():
        chat_name_titles = driver.find_elements("xpath", f"{folders_container_xpath}/li/div[@class='user-caption']//span[@class='peer-title']")
        for chat_name_title in chat_name_titles:
            if chat_name == chat_name_title.text:
                chat_icon = driver.find_element("xpath", f"{folders_container_xpath}/li/div[@class='user-caption']//span[@class='peer-title' and text()='{chat_name}']/ancestor::li[@rb-chat-item]")
                chat_icon.click()

                return True
        else:
            return False

    def load_folders():
        while True:
            last_folder = get_last_folder()

            scroll_down()

            sleep(time_out)

            new_last_folder = get_last_folder()

            if last_folder == new_last_folder:
                if last_folder is None and new_last_folder is None:
                    raise Exception("The folders container is not loaded or empty")

                return True
            elif click() is True:
                return "clicked"

    if click() is not True:
        load = load_folders()
        if load is True:
            if click() is not True:
                return False
        elif load == "clicked":
            pass

    return True


def logged_in():
    try:
        driver.find_elements("xpath", "//div[@id='page-chats' and not(@hidden)]")
    except:
        return False
    else:
        return True


def get_last_folder():
    try:
        last_folder = driver.find_element("xpath", f"{folders_container_xpath}/li[last()]")
    except:
        return None
    else:
        return last_folder


def scroll_down():
    try:
        driver.execute_script(f"document.evaluate(\"{folders_container_xpath}\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollIntoView(false);")
    except:
        raise Exception("The folders container is not loaded")
