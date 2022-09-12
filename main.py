from initialize import driver, base_url
from CDP.initialize import CDP_initialize
from core.core import get_all_chats, get_chat_history, save_chats
from login.login import login
from utils.utils import runtime_counter


@runtime_counter
def main():
    driver.get(base_url)

    chat_id = login()
    all_chats = get_all_chats(chat_id)
    chat_history = get_chat_history(all_chats)

    save_chats(chat_history)

if __name__ == "__main__":
    try:
        CDP_initialize()
        main()
    except (Exception, KeyboardInterrupt) as err:
        if type(err) is KeyboardInterrupt:
            err = "Interrupted"
        print("\nError:", err)
        exit()
    finally:
        print("\nWait for the WebDriver to quit")
        driver.quit()
