from initialize import driver, chat_box_xpath, replied_message_xpath, chat_name, chat_type, from_date, to_date, location, time_out, overload
from core.variables import present, removed_to_date_useless_chats
from CDP.Domains import Network
from utils.utils import wastetime_counter, log_progress, log_loading
from json import dump
from time import sleep
from re import findall
from os import listdir


# --- Load Data ---

def load_all_chats():
    i = 1
    while True:
        first_chat = get_first_chat()

        scroll_up()

        sleep(time_out)

        if to_date != "present":
            set_present(get_dates())

        new_first_chat = get_first_chat()

        all_chats_length = get_all_chats_length()

        if first_chat == new_first_chat:
            if first_chat is None and new_first_chat is None:
                raise Exception("The chat box is not loaded or empty")

            first_chat = get_first_chat(head=True)
            date = get_date(first_chat)
            if date:
                verification_last_msg = verification_last_message(date)
                if verification_last_msg:
                    break
        i = log_loading(i, "Loading all chats", prefix=f"{all_chats_length} | ")

    return True


def load_limited_chats(from_date):
    FDEL = -1 # Final Date Elements Length

    check_from_date = True

    i = 1
    while True:
        scroll_up()

        sleep(time_out)

        dates = get_dates()

        set_present(dates)

        if check_from_date:
            if from_date in dates:
                check_from_date = False
                FDEL = len(dates[dates.index(from_date):])

        all_chats_length = get_all_chats_length()

        if all_chats_length == None:
            check_from_date = True

        if len(dates) > FDEL != -1:
            break
        i = log_loading(i, "Loading limited chats", prefix=f"{all_chats_length} | ")

    return False


def get_all_chats_length():

    def get_current_chat_history(all_chats):
        if removed_to_date_useless_chats:
            all_chats = driver.find_elements("xpath", f"{chat_box_xpath}/div[@rb-observer]") # New all_chats

        chat_history = get_chat_history(all_chats[1:])
        save_chats(chat_history)

    def overload_checks():
        if to_date != "present":
            if to_date == present:
                if not removed_to_date_useless_chats:
                    remove_to_date_useless_chats()

                get_current_chat_history(all_chats)
            else:
                remove_all_useless_chats(all_chats[1:])
        else:
            get_current_chat_history(all_chats)

    all_chats = driver.find_elements("xpath", f"{chat_box_xpath}/div[@rb-observer]")

    all_chats_length = len(all_chats)
    if all_chats_length >= overload:
        print("\nOverloaded")

        if Network.canClearBrowserCache():
            Network.clearBrowserCache()
            print("\nBrowser cache cleared")

        overload_checks()

        return None
    else:
        return all_chats_length


def remove_all_useless_chats(useless_chats):
    i = 1
    for chat in useless_chats:
        remove_element(f"{chat_box_xpath}/div[@rb-observer and @data-msg-id='{chat.get_attribute('data-msg-id')}']")
        i = log_loading(i, "Removing all useless chats")
    else:
        print("\nAll useless chats removed")


def remove_to_date_useless_chats():
    global removed_to_date_useless_chats

    if to_date == present:
        useless_chats = driver.find_elements("xpath", f"{chat_box_xpath}/div[@rb-observer]/div[@class='bubble service is-date']//span[substring-after(text(), '، ') = '{to_date}']/ancestor::div[@rb-observer]/following-sibling::div")

        i = 1
        for chat in useless_chats:
            remove_element(f"{chat_box_xpath}/div[@rb-observer and @data-msg-id='{chat.get_attribute('data-msg-id')}']")
            i = log_loading(i, "Removing to date useless chats")
        else:
            removed_to_date_useless_chats = True
            print("\nTo date useless chats removed")


def set_present(dates):
    global present

    if not removed_to_date_useless_chats:
        if len(dates) > 1:
            if to_date in dates[1:]:
                present = to_date


def get_first_chat(head=False):
    try:
        if head:
            first_chat = driver.find_element("xpath", f"{chat_box_xpath}/div[1]")
        else:
            first_chat = driver.find_element("xpath", f"({chat_box_xpath}/div[@rb-observer]/div[@class='bubble service is-date']/..)[1]/following-sibling::div[1]")
    except:
        return None
    else:
        return first_chat


def get_date(chat):
    all_chat_elements = chat.find_elements("xpath", "./div")
    if len(all_chat_elements) >= 2:
        try:
            date = chat.find_element("xpath", "./div[@class='bubble service is-date']//span")
            date = findall(r"^.*، (.*)$", date.text)[0]
        except:
            return None
        else:
            return date
    else:
        return None


def get_dates():
    date_elements = driver.find_elements("xpath", f"{chat_box_xpath}/div[@rb-observer]/div[@class='bubble service is-date']//span")
    if not date_elements:
        raise Exception("The chat box is not loaded or empty")

    dates = []
    for date_element in date_elements:
        date = findall(r"^.*، (.*)$", date_element.text)[0]
        dates.append(date)
    else:
        return dates


@wastetime_counter
def verification_last_message(date):
    print("\n\n" + date)

    verification_last_msg = input("\nAre you verify last message? (y/N): ")

    verifications = ["y", "Y", "yes", "YES", "Yes", "yea", "yeah"]
    if verification_last_msg in verifications:
        return True
    else:
        return False


def scroll_up():
    try:
        driver.execute_script(f"document.evaluate(\"{chat_box_xpath}\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollIntoView(true);")
    except:
        raise Exception("The chat box is not loaded")


def clear_console():
    try:
        driver.execute_script(f"console.clear()")
    except:
        print(f"\nTakes error on clearing console")


# --- Save Data ---

def get_all_chats(ID):
    global chat_id; chat_id = ID
    global loaded_all_chats

    all_chats = []
    if from_date == "the oldest message":
        loaded_all_chats = load_all_chats()
        all_chats = driver.find_elements("xpath", f"{chat_box_xpath}/div[@rb-observer]")
    
        if not removed_to_date_useless_chats: # It also means "if not overloaded"
            if to_date != "present":
                to_date_all_chats = driver.find_elements("xpath", f"{chat_box_xpath}/div[@rb-observer]/div[@class='bubble service is-date']//span[substring-after(text(), '، ') = '{to_date}']/ancestor::div[@rb-observer]/preceding-sibling::div")
                all_chats = to_date_all_chats
    else:
        loaded_all_chats = load_limited_chats(from_date)
        from_date_all_chats = driver.find_elements("xpath", f"{chat_box_xpath}/div[@rb-observer]/div[@class='bubble service is-date']//span[substring-after(text(), '، ') = '{from_date}']/ancestor::div[@rb-observer]/preceding-sibling::div[1]/following-sibling::div")

        if not removed_to_date_useless_chats:
            if to_date == present:
                to_date_all_chats = driver.find_elements("xpath", f"{chat_box_xpath}/div[@rb-observer]/div[@class='bubble service is-date']//span[substring-after(text(), '، ') = '{to_date}']/ancestor::div[@rb-observer]/preceding-sibling::div")

                i = 1
                for chat in from_date_all_chats:
                    if chat in to_date_all_chats:
                        all_chats.append(chat)
                    i = log_loading(i, "Sorting limited chats")
            else:
                all_chats = from_date_all_chats
        else:
            all_chats = from_date_all_chats

    return all_chats


def get_chat_history(all_chats):
    total_indexes = len(all_chats) - 1
    chat_history = []
    for chat in all_chats[::-1]:
        try:
            chat_data = chat.find_element("xpath", "./div[contains(@class, 'is-in') or contains(@class, 'is-out')]")
        except:
            continue
        else:
            current_message = bind_message(chat, chat_data)
            chat_history.append(current_message)
        finally:
            current_index = all_chats.index(chat)

            remove_element(f"{chat_box_xpath}/div[@rb-observer and @data-msg-id='{chat.get_attribute('data-msg-id')}']")

            log_progress(total_indexes - current_index, total_indexes, prefix="Progress:", suffix="Complete", decimals=2, auto_size=True)

    chat_history = {
        "name": chat_name,
        "type": chat_type,
        "id": chat_id,
        "messages": chat_history[::-1]
    }

    return chat_history


def bind_message(chat, chat_data):
    global sender_name

    try: message_id = chat.get_attribute("data-msg-id")
    except: message_id = None

    try: date = get_date(chat)
    except: date = None

    try: clock = chat_data.find_element("xpath", ".//span[contains(@class, 'time rbico') and @title]").text
    except: clock = None

    try:
        classes = chat_data.get_attribute("class")
        if chat_type == "group":
            if "is-group-first" in classes:
                sender_name = chat_data.find_element("xpath", ".//a[contains(@class, 'name')]").text
        else:
            sender_name = chat_name
    except: classes = None

    try:
        if loaded_all_chats:
            all_chat_content_elements = chat_data.find_elements("xpath", ".//div[@class='bubble-content']/div")
            if len(all_chat_content_elements) >= 3:
                replied_message = chat_data.find_element("xpath", ".//div[@class='bubble-content']/div[contains(@class, 'reply')]")
                replied_message.click()

                reply_to_message_id = driver.find_element("xpath", f"{replied_message_xpath}/parent::div[@rb-observer]").get_attribute("data-msg-id")

                remove_class(replied_message_xpath, "is-highlighted")
            else:
                raise Exception()
        else:
            raise Exception()
    except: replied_message = None

    try: text = chat_data.find_element("xpath", ".//div[@class='bubble-content']/div[contains(@class, 'message')]/descendant::div[@dir or (not(@*) and position() = 1) or contains(@class, 'document-message')]").text
    except: text = None

    current_message = {}

    if message_id: current_message["id"] = int(message_id)
    if date: current_message["date"] = date
    if clock: current_message["clock"] = clock
    if classes: current_message["sender"] = sender_name if "is-in" in classes else "you"
    if replied_message: current_message["reply_to_message_id"] = int(reply_to_message_id)
    if text: current_message["text"] = text

    return current_message


def remove_class(xpath, class_name):
    try:
        driver.execute_script(f"document.evaluate(\"{xpath}\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.classList.remove(\"{class_name}\");")
    except:
        print(f"\nTakes error on removing \"{class_name}\" class")
        return Exception()()


def remove_element(xpath):
    try:
        driver.execute_script(f"document.evaluate(\"{xpath}\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.remove();")
    except:
        print(f"\nTakes error on removing element")


def file_scan():
    """next update"""


def save_chats(chat_history):
    file_paths = listdir(location)
    number = len(file_paths) + 1
    current_location = f"{location}/chat_history_{number}.json"

    with open(current_location, "w") as file:
        dump(chat_history, file, indent=1)
