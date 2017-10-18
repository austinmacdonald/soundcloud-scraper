from flask import Flask, render_template, session, redirect, url_for, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import scraper

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


class SearchForm(FlaskForm):
    search = StringField('Artist/Title')
    submit = SubmitField('Search')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        search_string = form.search.data
        return redirect("/search/"+search_string)
    return render_template('index.html', form=form, name=session.get('name'))


@app.route('/search/<search_string>', methods=['GET'])
def search(search_string):
    return render_template('search.html', songs=scraper.search(search_string))


@app.route('/song/<song_id>', methods=['GET'])
def song(song_id):
    return render_template('song.html', songs=scraper.get_songs(song_id)[1], playlists_found=scraper.get_songs(song_id)[0])

if __name__ == '__main__':
    manager.run()
