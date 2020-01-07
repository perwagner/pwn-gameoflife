import os

from application import create_app, socketio

ENV = os.getenv("ENV", "local")
app = create_app(env=ENV)

if __name__ == "__main__":
    socketio.run(app, debug=True)