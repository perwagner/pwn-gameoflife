from . import website



@website.route('/')
def index():
    return "HELLO WORLD"
