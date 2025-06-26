from uuid import uuid4
from nicegui import ui

messages = []

@ui.refreshable
def chat_messages(own_id):
    with ui.column().classes('w-full px-4 py-2 gap-2 overflow-auto flex-grow'):
        for user_id, avatar_url, msg in messages:
            ui.chat_message(avatar=avatar_url, text=msg, sent=(user_id == own_id))

@ui.page('/')
def index():
    def send():
        if text.value.strip():
            messages.append((user_id, avatar, text.value.strip()))
            chat_messages.refresh()
            text.value = ''

    user_id = str(uuid4())
    avatar = f'https://robohash.org/{user_id}?bgset=bg2'

    # Main app container with background
    with ui.column().classes('w-full h-screen justify-between').style(
        'background-image: url("https://ik.imagekit.io/hvgic7qdf/Image.jpg?updatedAt=1750919438721");'
        'background-size: cover; background-position: center; background-repeat: no-repeat;'):

        # HEADER
        with ui.row().classes('w-full bg-white bg-opacity-80 p-4 shadow-md'):
            ui.label('Pepsu Gang Chatroom').classes('text-xl font-semibold text-black')

        # CHAT BODY (scrollable)
        chat_messages(user_id)

        # FOOTER
        with ui.row().classes('w-full bg-white bg-opacity-90 p-2 items-center gap-2'):
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

ui.run()
