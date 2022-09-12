from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
from os import mkdir
from os.path import isdir
from time import sleep


base_dir = Path(__file__).parent.resolve()
base_url = "https://web.rubika.ir"

chat_exports_dir = f"{base_dir}/exports"
login_data_dir = f"{base_dir}/login/data"

chat_box_xpath = "//div[contains(@class, 'bubbles-inner')]"
folders_container_xpath = "//div[@anim-tab='all_chats']/ul[@class='chatlist']"
replied_message_xpath = f"{chat_box_xpath}/div[@rb-observer]/div[contains(@class, 'is-highlighted')]"

# Headless mode must be turned off to perform this function
def chrome_configure_experimental_flags():
    global driver

    # Browser config javascript commands (need to be launched from chrome://flags)
    enable_quic_command = "chrome.send('enableExperimentalFeature', ['enable-quic', 'true'])"

    driver.get("chrome://flags")

    sleep(time_out)

    try:
        driver.execute_script(enable_quic_command)
    except:
        print("\nFailed to configure chrome experimental features")
    else:
        # Close and re-build driver with same options (and so same profile, so experimental flags will be kept)
        driver.close()
        driver = webdriver.Chrome(service=service, options=options)

        print("\nChrome experimental features configured")

try:
    phone_number = input("Set phone number: ")
    chat_name = input("Set chat name (required): ")
    chat_type = input("Set chat type (by default = \"personal_chat\"): ")
    from_date = input("Set from date (by default = \"the oldest message\"): ")
    to_date = input("Set to date (by default = \"present\"): ")
    location = input("Set directory for chat export(s) (by default = \"./exports\"): ")
    time_out = input("Set time out (by default = 0.5): ")
    overload = input("Set overload (by default = 1000): ")

    if isdir(chat_exports_dir) is not True:
        mkdir(chat_exports_dir)

    if isdir(login_data_dir) is not True:
        mkdir(login_data_dir)

    if not phone_number:
        phone_number = None
    elif phone_number[0] == "0":
        phone_number = phone_number[1:]

    if not chat_name:
        raise Exception("\"chat_name\" is required")

    if not chat_type:
        chat_type = "personal_chat"

    if not from_date:
        from_date = "the oldest message"

    if not to_date:
        to_date = "present"

    if not location:
        location = chat_exports_dir

    if not time_out:
        time_out = 0.5
    else:
        time_out = float(time_out)

    if not overload:
        overload = 1000
    elif int(overload) < 100:
        raise Exception("\"overload\" can't be less than 100")
    else:
        overload = int(overload)
except (Exception, KeyboardInterrupt) as err:
    if type(err) is KeyboardInterrupt:
        err = "Interrupted"
    print("\nError:", err)
    exit()
else:
    print("\nPreparing the WebDriver")

    service = Service(executable_path=ChromeDriverManager().install())

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920, 1080")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--dns-prefetch-disable")
    options.add_argument("--disk-cache-size=1")
    options.add_argument("--media-cache-size=1")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    # options.add_experimental_option("prefs", {"download.default_directory": rf"{base_dir}\download"})

    driver = webdriver.Chrome(service=service, options=options)
    # chrome_configure_experimental_flags()
    driver.implicitly_wait(time_out)
