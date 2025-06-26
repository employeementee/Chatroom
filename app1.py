from uuid import uuid4
from nicegui import ui

messages = []

@ui.refreshable
def chat_messages(own_id):
    for user_id, avatar, text in messages:
        ui.chat_message(avatar=avatar, text=text, sent=user_id == own_id)

@ui.page('/')
def index():
    def send():
        if text.value.strip():
            messages.append((user, avatar, text.value.strip()))
            chat_messages.refresh()
            text.value = ''

    user = str(uuid4())
    avatar = f'https://robohash.org/{user}?bgset=bg2'

    # HEADER must be top-level
    with ui.header().classes('bg-white bg-opacity-80 text-black p-4 shadow-md'):
        ui.label('Pepsu Gang Chatroom').classes('text-xl font-semibold')

    # Chat area
    with ui.column().classes('w-full flex-grow overflow-auto px-2 py-4'):
        chat_messages(user)

    # FOOTER must be top-level
    with ui.footer().classes('bg-white bg-opacity-90 p-2'):
        with ui.row().classes('w-full items-center flex-wrap gap-2'):
            with ui.avatar().classes('w-10 h-10'):
                ui.image(avatar).classes('w-full h-full object-cover rounded-full')
            text = ui.input(placeholder='Message…') \
                .props('rounded outlined') \
                .classes('flex-grow min-w-[150px]') \
                .on('keydown.enter', send)
            ui.button(icon='send') \
                .props('rounded') \
                .classes('w-10 h-10 shrink-0') \
                .on('click', send)

# ✅ Apply background image + light overlay to the full page
ui.add_body_html('''
<style>
  body {
    margin: 0;
    font-family: sans-serif;
    background-image: url("https://ik.imagekit.io/hvgic7qdf/Image.jpg?updatedAt=1750919438721");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    position: relative;
  }

  /* Light overlay */
  body::before {
    content: "";
    position: fixed;
    inset: 0;
    background-color: rgba(255, 255, 255, 0.6);
    z-index: -1;
  }
</style>
''')

ui.run()
