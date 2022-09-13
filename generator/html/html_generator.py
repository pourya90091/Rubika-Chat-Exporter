def new_message (username, text, time, messageID):
    side = "left"
    if username.lower() == "you" : side = "right"

    return f"""<li class="message">
    <div class="message-body message-{side}" id="{messageID}">
      <p class="message-uname">{username}</p>
      <p class="message-text">{text}</p>
      <p class="message-time">{time}</p>
    </div>
  </li>"""