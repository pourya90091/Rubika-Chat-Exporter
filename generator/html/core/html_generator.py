from initialize import base_dir
from generator.html.core.variables import message_body, relpy_box
from utils.utils import log_progress
from os import mkdir, listdir
from os.path import isdir
from shutil import copy
from textwrap import shorten
from re import sub, MULTILINE
from json import load


def generate_html(location):
    global chat_history

    html_export_dir = f"{location}/html"
    css_export_dir = f"{html_export_dir}/css"

    if not isdir(html_export_dir):
        mkdir(html_export_dir)

    if not isdir(css_export_dir):
        mkdir(css_export_dir)

    file_paths = listdir(location)
    for file_path in file_paths:
        if file_path == "html":
            continue

        with open(f"{base_dir}/generator/html/template.html", "r") as file:
            html = file.read()

        with open(f"{location}/{file_path}", "r", encoding="utf-8") as file:
            chat_history = load(file)

        total_indexes = len(chat_history["messages"]) - 1
        conatiners = ""
        for message in chat_history["messages"]:
            conatiners += bind_message(message)
            log_progress(chat_history["messages"].index(message), total_indexes, prefix="Progress:", suffix="Complete", decimals=2, auto_size=True)

        html = sub(r'(<ul id="messages">)(</ul>)', rf'\g<1>{conatiners}\g<2>', html)

        current_location = f"{html_export_dir}/chat_history_{file_paths.index(file_path) + 1}.html"
        with open(current_location, "w", encoding="utf-8") as file:
            file.write(html)

    copy(f"{base_dir}/generator/html/styles.css", f"{css_export_dir}/styles.css")


def bind_message(message: dict) -> str:
    try: message["id"]
    except: message["id"] = None

    try: message["date"]
    except: message["date"] = None

    try: message["clock"]
    except: message["clock"] = None

    try: message["sender"]
    except: message["sender"] = None

    try: message["reply_to_message_id"]
    except: message["reply_to_message_id"] = None

    try: message["text"]
    except: message["text"] = None

    current_message_body = ""

    current_message_body = sub(r'(<li class="message" id=")(">)', rf'\g<1>{message["id"]}\g<2>', message_body)
    # current_message_body = 
    current_message_body = sub(r'(<p class="message-time">)(</p>)', rf'\g<1>{message["clock"]}\g<2>', current_message_body)
    current_message_body = sub(r'(<p class="message-uname">)(</p>)', rf'\g<1>{message["sender"]}\g<2>', current_message_body)

    if message["sender"] == "you":
        current_message_body = sub(r'(<div class="message-body)(">)', r'\g<1> message-right\g<2>', current_message_body)
    else:
        current_message_body = sub(r'(<div class="message-body)(">)', r'\g<1> message-left\g<2>', current_message_body)

    if message["reply_to_message_id"]:
        pattern = r"""(^      <li class="message" id=".*">
        <div class="message-body (message-right|message-left)">
          <p class="message-uname">.*</p>\n)(\n.+\n.+\n.+\n.+$)"""

        current_relpy_box = sub(r'(<div class="reply-box" href="#)(">)', rf'\g<1>{message["reply_to_message_id"]}\g<2>', relpy_box)
        current_relpy_box = sub(r'(<a href="#)(">)', rf'\g<1>{message["reply_to_message_id"]}\g<2>', current_relpy_box)

        for msg in chat_history["messages"]:
            try:
                if msg["id"] == message["reply_to_message_id"]:
                    current_relpy_box = sub(r'(<p class="reply-box-uname">)(</p>)', rf'\g<1>{msg["sender"]}\g<2>', current_relpy_box)
                    break
            except:
                continue
        else:
            current_relpy_box = sub(r'(<p class="reply-box-uname">)(</p>)', rf'\g<1>Unknown\g<2>', current_relpy_box)

        for msg in chat_history["messages"]:
            try:
                if msg["id"] == message["reply_to_message_id"]:
                    msg["text"] = shorten(msg["text"], width=50, placeholder="...")

                    current_relpy_box = sub(r'(<p class="reply-box-text">)(</p>)', rf'\g<1>{msg["text"]}\g<2>', current_relpy_box)
                    break
            except:
                continue
        else:
            current_relpy_box = sub(r'(<p class="reply-box-text">)(</p>)', rf'\g<1>...\g<2>', current_relpy_box)

        current_message_body = sub(pattern, rf'\g<1>{current_relpy_box}\g<3>', current_message_body, flags=MULTILINE)

    current_message_body = sub(r'(<p class="message-text">)(</p>)', rf'\g<1>{message["text"]}\g<2>', current_message_body)

    return current_message_body
