from flask import render_template
from app import app
from forms import AccoutForm


@app.route('/', methods=['GET', 'POST'])
def index():
    form = AccoutForm()
    return render_template('index.html', form=form)


# @app.route('/')
# def register(username):
# 	return render_template('user.html', name=username)