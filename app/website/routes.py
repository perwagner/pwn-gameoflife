import os

from flask import render_template


from . import website



@website.route('/')
def index():
    return render_template("index.html", title="HOME", user="PER")
