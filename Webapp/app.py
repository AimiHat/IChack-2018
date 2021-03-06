#!/usr/bin/python
# ! -*- coding: utf-8 -*-

import os
import sys
from importlib import reload
import io
import requests
import json
import time
import base64
from chatbot import bot, hard_coded
from gtts import gTTS
import Analysis.Analyze, Analysis.ImageEmotion, Analysis.Transcribe, Analysis.TraitAnalysis


from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import (LoginManager, login_user, logout_user,
						 login_required, current_user)


from flask import Flask, request, session, g, redirect, url_for, abort, \
	render_template, flash, Markup, jsonify, make_response, send_from_directory

from werkzeug.contrib.profiler import ProfilerMiddleware
from xlsxwriter.utility import xl_rowcol_to_cell

# Intitialize and configure Flask app.
app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
	SECRET_KEY="#$dsfasdas943JHSs9dueidoijdf",  # secret key for signing sessions
))
app.config.from_envvar('APP_SETTINGS', silent=True)

chatbot = bot()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

def tts(response, session):
    path= "sessions/"+str(session)+"/tts.mp3"
    tts = gTTS(text=response, lang='en')
    if os.path.exists(path):
        os.remove(path)
        print('deleted existing tts')
    tts.save(path)
    return path

@app.before_request
def before_request():
	"""
	Connect to the database before each request
	"""
	with open('session_count.txt', 'r') as f:
		g.session = int([x for x in f.readlines()][0])
	g.version = 1 #Used for updating cached assets in templates

@app.after_request
def after_request(response):
	return response


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		'''
		try:
			user = models.Users.get(models.Users.username == request.form['username'])
		except models.DoesNotExist:
			flash('Your username and password do not match!')
		else:
			if check_password_hash(user.password, request.form['password']):
				login_user(user)
				if user.is_admin:  # Redirects admin user to management page
					return redirect(url_for('user_management'))
				return redirect(request.args.get("next") or url_for('index'))
			else:
				flash('Your username and password do not match!')
		'''
		return redirect(url_for('index'))
	return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out!', 'success')
	return redirect(url_for('index'))

@app.route('/save_image', methods=['POST'])
def save_image():
	#print(request.form['image'].split(',')[1].decode('base64'))
	img_data = base64.b64decode(request.form['image'].split(',')[1])#.split(',')[1])
	directory = 'sessions/'+str(g.session)
	if not os.path.exists(directory):
		os.makedirs(directory)

	i = 0
	while os.path.exists(directory+'/'+str(i)+'.png'):
		i += 1

	with open(directory+'/'+str(i)+'.png', "wb") as fh:
		fh.write(img_data)

	#call endpoint to process last photo
	Analysis.Analyze.processFrame(directory+'/', str(i)+'.png')
		
	return json.dumps(True)

@app.route('/audio_save', methods=['POST'])
def audio_save():
	#print(request.form['image'].split(',')[1].decode('base64'))

	text = request.form['message'];
	textDuration = request.form['duration'];

	Analysis.Transcribe.processText('sessions/'+str(g.session) + '/', text, textDuration);

	print("In audio_save, message = "+text)

	if not text.lower().strip().replace(",","").replace(".","") in hard_coded:
		r='http://www.cleverbot.com/getreply'
		d = {'key':'CC6wwsZu_c50FJ9mMPyRjXHbl7Q','input':text}
		r = requests.get(r,d).text
		response = json.loads(r)['output']
	else:
		response = hard_coded[text.lower()]
	#url = tts(response,g.session)
	print(response)
	return json.dumps({'text':text,'response':response})



@app.route('/analyze_api', methods=['GET'])
def analyze_api():
	#print(request.form['image'].split(',')[1].decode('base64'))
	# audio = base64.b64decode(request.form['audio'])#.split(',')[1])
	directory = 'sessions/'+str(g.session)+'/'
	# directory = 'sessions/31/'
	
	fillers = Analysis.TraitAnalysis.fillerWord(directory + 'results_speech.csv')
	intersestScoreSpeech = Analysis.TraitAnalysis.intersestScoreSpeech(directory + 'results_speech.csv')
	intersestScoreSpeech = round(intersestScoreSpeech,2)
	intersestScoreVideo = Analysis.TraitAnalysis.intersestScoreVideo(directory + 'results_image.csv')
	intersestScoreVideo = round(intersestScoreVideo,2)
	nervousnessScoreVideo = Analysis.TraitAnalysis.nervousnessScoreVideo(directory + 'results_image.csv')
	print('nervousnessScoreVideo',nervousnessScoreVideo)
	nervousnessScoreVideo = round(nervousnessScoreVideo,2)

	speedScore = Analysis.TraitAnalysis.getSpeedScore(directory)
	return json.dumps({'fillers':fillers,'intersestScoreSpeech':intersestScoreSpeech,'intersestScoreVideo':intersestScoreVideo,
						'nervousnessScoreVideo':nervousnessScoreVideo,'speedScore':speedScore})

@app.route('/analyze')
def analyze():
	return render_template('/analysis.html')

@app.route('/sessions/<int:sess>/<string:file_name>')
def serve_audio(sess, file_name):
	return send_from_directory('sessions/'+str(sess)+'/',file_name)


def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d


@app.route('/camera')
def camera():
	with open('session_count.txt', 'w') as f:
		f.write(str(g.session+1))
	return render_template('camera.html')

@app.route("/")
def index():
	return render_template('index.html')


if __name__ == '__main__':
	app.run(debug=True, host='localhost', port=8200)
