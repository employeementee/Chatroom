from uuid import uuid4
from nicegui import ui

messages = []

@ui.refreshable
def chat_messages(own_id):
    for user_id, avatar, text in messages:
        ui.chat_message(avatar=avatar, text=text, sent=user_id==own_id)

@ui.page('/')
def index():
    def send():
        messages.append((user, avatar, text.value))
        chat_messages.refresh()
        text.value = ''

    user = str(uuid4())
    avatar = f'https://robohash.org/{user}?bgset=bg2'
    with ui.column().classes('w-full items-stretch'):
        chat_messages(user)

    with ui.footer().classes('bg-white p-2'):
    with ui.row().classes('w-full items-center flex-wrap gap-2'):
        # Avatar
        with ui.avatar().classes('w-10 h-10'):
            ui.image(avatar).classes('w-full h-full object-cover rounded-full')
        # Message input
        text = ui.input(placeholder='Message…') \
            .props('rounded outlined') \
            .classes('flex-grow min-w-[150px]') \
            .on('keydown.enter', send)
        # Send button
        ui.button(icon='send') \
            .props('rounded') \
            .classes('w-10 h-10 shrink-0') \
            .on('click', lambda: send())

ui.run()
