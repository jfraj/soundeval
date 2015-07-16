from flask import Flask
from flask import render_template
from flask_wtf import Form
from wtforms.fields import RadioField, StringField, SubmitField
from wtforms.validators import Required

import player_recording

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'


class RecordInfoQuestionsForm(Form):
    player_name = RadioField('Your answer', choices=[('jfraj', 'jfraj'),
                                                     ('marina', 'marina'),
                                                     ('unknown', 'Unknown')])
    play_type = RadioField('Your answer', choices=[('longbow', 'longbow'),
                                                   ('halfbow', 'halfbow')])

    max_length = StringField('Max recording length', validators=[Required()])
    submit = SubmitField('Record')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recording/')
def record_player(player_name='noname', max_length=1):
    basename = '{}_flasktest'.format(player_name)
    audio_fname = player_recording.record_playing(countdown=1,
                                                  max_length=max_length,
                                                  wait4enter=False,
                                                  basename=basename,
                                                  save_dir='/Users/jean-francoisrajotte/projects/soundeval/test/')
    #return 'finished recording and saved in {}'.format(fname)
    return render_template('recording_result.html', audio_fname=audio_fname)


@app.route('/record_info/', methods=['GET', 'POST'])
def record_info():
    form = RecordInfoQuestionsForm(player_name='marina',
                                   play_type='longbow',
                                   max_length=5)
    if form.validate_on_submit():
        return record_player(form.player_name.data, int(form.max_length.data))
        #return record_player(form.player_name.data, 50)
    return render_template('record_info.html', form=form)


@app.route('/test/')
def test_page():
    return 'This is a test page'


@app.route('/<name>/')
def name_page(name):
    return 'Hello, {name}'.format(name=name)


if __name__ == '__main__':
    app.run(debug=True)
