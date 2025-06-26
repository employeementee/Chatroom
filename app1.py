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

    with ui.element('div').classes('chat-wrapper w-full h-screen flex flex-col'):

        # Header
        with ui.header().classes('bg-white bg-opacity-80 text-black p-4 shadow-md'):
            ui.label('Pepsu Gang Chatroom').classes('text-xl font-semibold')

        # Chat messages area
        with ui.column().classes('flex-grow w-full overflow-auto px-2 py-4'):
            chat_messages(user)

        # Footer with input
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
ui.add_body_html('''
<style>
  body {
    margin: 0;
    font-family: sans-serif;
  }
  .chat-wrapper {
    position: relative;
    background-image: url("https://ik.imagekit.io/hvgic7qdf/Image.jpg?updatedAt=1750919438721");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
  }
  .chat-wrapper::before {
    content: "";
    position: absolute;
    inset: 0;
    background: rgba(255, 255, 255, 0.6); /* semi-transparent white overlay */
    z-index: 0;
  }
  .chat-wrapper > * {
    position: relative;
    z-index: 1; /* push actual content above overlay */
  }
</style>
''')



ui.run()
