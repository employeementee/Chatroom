from uuid import uuid4
from nicegui import ui

messages = []

@ui.page('/')
def index():
    user_id = str(uuid4())
    avatar = f'https://robohash.org/{user_id}?bgset=bg2'

    def send():
        if text.value.strip():
            # Simulate one of your own messages
            messages.append((user_id, avatar, text.value.strip()))

            # Simulate another user reply (for testing)
            other_id = 'user-other'
            other_avatar = f'https://robohash.org/{other_id}?bgset=bg2'
            messages.append((other_id, other_avatar, f"Reply to: {text.value.strip()}"))

            chat_messages.refresh()
            text.value = ''

    @ui.refreshable
    def chat_messages():
        with ui.column().classes('w-full px-4 py-2 gap-2 flex-grow overflow-auto').props('id=chat-area'):
            for msg_user_id, msg_avatar, msg_text in messages:
                ui.chat_message(
                    avatar=msg_avatar,
                    text=msg_text,
                    sent=(msg_user_id != user_id)  # ✅ Yours → left, others → right
                )
        # Auto-scroll
        ui.run_javascript('''
            const chatArea = document.getElementById('chat-area');
            if (chatArea) {
                chatArea.scrollTop = chatArea.scrollHeight;
            }
        ''')

    # Background + light overlay
    ui.add_body_html('''
    <style>
        body {
            margin: 0;
            font-family: sans-serif;
        }
        #bg-image {
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
        }
        #bg-image::after {
            content: "";
            position: absolute;
            inset: 0;
            background-color: rgba(255, 255, 255, 0.6);
        }
    </style>
    <div id="bg-image"></div>
    ''')

    # Main Layout
    with ui.column().classes('w-full h-screen justify-between'):
        with ui.row().classes('w-full bg-white bg-opacity-80 p-4 shadow-md'):
            ui.label('Pepsu Gang Chatroom').classes('text-xl font-semibold text-black')

        chat_messages()

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
