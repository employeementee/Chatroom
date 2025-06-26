from uuid import uuid4
from nicegui import ui

messages = []

@ui.refreshable
def chat_messages(own_id):
    with ui.column().classes('w-full px-4 py-2 gap-2 flex-grow overflow-auto').props('id=chat-area'):
        for user_id, avatar, text in messages:
            ui.chat_message(avatar=avatar, text=text, sent=user_id==own_id)
    ui.run_javascript('''
            const chatArea = document.getElementById('chat-area');
            if (chatArea) {
                chatArea.scrollTop = chatArea.scrollHeight;
            }
        ''')
    ui.add_body_html(f'''
    <style>
        body {{
            margin: 0;
            font-family: sans-serif;
        }}
        #bg-image {{
            position: fixed;
            top: 0;
            left: 0;
            height: 100vh;
            width: 100vw;
            background-image: url("https://ik.imagekit.io/hvgic7qdf/Image.jpg?updatedAt=1750919438721");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            z-index: -1;
        }}
        #bg-image::after {{
            content: "";
            position: absolute;
            inset: 0;
            background-color: rgba(255, 255, 255, 0.6);
        }}
    </style>
    <div id="bg-image"></div>
    ''')

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

    with ui.footer().classes('bg-white'):
        with ui.row().classes('w-full items-center'):
            with ui.avatar():
                ui.image(avatar)
            text = ui.input(placeholder='message') \
                .props('rounded outlined').classes('flex-grow') \
                .on('keydown.enter', send)

ui.run()
