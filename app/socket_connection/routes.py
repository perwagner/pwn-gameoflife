from . import socketio


@socketio.on('message')
def handle_message(message):
    print("XXXXXXXXXXXXXXXXXX")
    print('received message: ' + message)

@socketio.on('my event')
def handle_my_custom_event(json):
    print(f"Message is now: {json['data']}")
