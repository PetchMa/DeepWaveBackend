#our web app framework!
#Generating HTML from within Python is not fun, and actually pretty cumbersome because you have to do the
from os.path import join, dirname, realpath
from flask import request, redirect, url_for, render_template, flash, send_from_directory
#from werkzeug.utils import secure_filename
from PIL import Image
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import h5py
from werkzeug.utils import secure_filename

from flask import Flask, render_template,request
#scientific computing library for saving, reading, and resizing images
from scipy.misc import imsave, imread, imresize
#for matrix math
import numpy as np
#for importing our keras model
import keras.models
#for regular expressions, saves time dealing with string data
import re
#system level operations (like loading files)
import sys 
#for reading operating system data
import cv2
import os
import base64
import io
from keras.preprocessing.image import img_to_array
#tell our app where our saved model is
sys.path.append(os.path.abspath("./model"))
from load import * 
#initalize our flask app
app = Flask(__name__)
#global vars for easy reusability
global model, graph
#initialize these variables
model, graph = init()

#decoding an image from base64 into raw representation

# def convertImage(imgData1): 
# 	imgstr = re.search(b'base64,(.*)',imgData1).group(1) #print(imgstr) 
# 	with open('output.png','wb') as output: 
# 		output.write(base64.b64decode(imgstr))	
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static\\uploads\\')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# HTML_TEMPLATE = Template('/DeepGalaxyDemo.html')



@app.route('/')
def index():
	#initModel()
	#render out pre-built HTML file right on the index page
	return render_template("index.html")
@app.route('/learn.html')
def learn():
	#initModel()
	#render out pre-built HTML file right on the index page
	return render_template("learn.html")
@app.route('/DeepGalaxy.html')
def DeepGalaxy():
	#initModel()
	#render out pre-built HTML file right on the index page
	return render_template("DeepGalaxy.html")
@app.route('/DeepGalaxyDemo.html')
def DeepGalaxyDemo(filename="", cleaned_path="", error=""):
	#initModel()
	#render out pre-built HTML file right on the index page
	return render_template('DeepGalaxyDemo.html', filename=filename, cleaned_path=cleaned_path, error=error)
@app.route('/research.html')
def research():
	#initModel()
	#render out pre-built HTML file right on the index page
	return render_template("research.html")
@app.route('/team.html')
def team():
	#initModel()
	#render out pre-built HTML file right on the index page
	return render_template("team.html")
@app.route('/index.html')
def home():
	#initModel()
	#render out pre-built HTML file right on the index page
	return render_template("index.html")
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html")




@app.route('/denoise/learn.html')
def denoiselearn():
	
	return redirect(url_for('learn'))
@app.route('/denoise/DeepGalaxy.html')
def denoiseDeepGalaxy():
	
	#render out pre-built HTML file right on the index page
	return redirect(url_for('DeepGalaxy'))
@app.route('/denoise/DeepGalaxyDemo.html')
def denoiseDeepGalaxyDemo(filename="", cleaned_path="", error=""):
	
	#render out pre-built HTML file right on the index page
	return redirect(url_for('DeepGalaxyDemo'))
@app.route('/denoise/research.html')
def denoiseresearch():
	
	#render out pre-built HTML file right on the index page
	return redirect(url_for('research'))
@app.route('/denoise/team.html')
def denoiseteam():
	
	#render out pre-built HTML file right on the index page
	return redirect(url_for('team'))
@app.route('/denoise/index.html')
def denoisehome():
	
	#render out pre-built HTML file right on the index page
	return redirect(url_for('home'))


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		try:
			f = request.files['file']
			
			# f = base64.b64decode(f)
			
			f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
			return render_template('DeepGalaxyDemo.html', filename=f.filename)
		except Exception as e:
			return render_template('DeepGalaxyDemo.html', error=e)
	return redirect(url_for('DeepGalaxyDemo'))

# @app.route('/upload_file', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         try:
#             f = request.files['file']
# 			f = base64.b64decode(f)
# 			print('1')
# 			f = secure_filename(f.filename)
# 			print('a')
#             f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
#             return render_template('DeepGalaxyDemo.html', filename=f.filename)
#         except Exception as e:
#             return render_template('DeepGalaxyDemo.html', error=e)
#     return redirect(url_for('hello'))


@app.route('/uploads/<filename>')
def view_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
@app.route('/return_file/<filename>')
def return_file(filename):
	try:
		return send_from_directory(UPLOAD_FOLDER, filename, as_attachment = True)
	except Exception as e:
		return render_template('DeepGalaxyDemo.html', error=e)
	return redirect(url_for('DeepGalaxyDemo'))

@app.route('/denoise',  defaults={'filename': 'defualt'})
@app.route('/denoise/<filename>')
def denoise(filename):
	try:	
		img = 0
		debug()
		
		debug()
		imgData = os.path.join(app.config['UPLOAD_FOLDER'], filename)
		
		debug()
		
		x = cv2.imread(imgData)
		
		x = cv2.resize(x,(25,25))
		debug()
		x = x.astype('float32')
		
		x /= 255
		
		x = np.expand_dims(x, axis=0)
		
		num = x[0,5,24,2]*10
		
		debug()
		with graph.as_default():
			img = model.predict(x)
			img = img [0, : , :, :]
			debug()

			cleaned_path = UPLOAD_FOLDER + 'cleaned-' + filename
			debug()
		
			img =(img * 255).astype(np.uint8)

			debug()

			Image.fromarray(img).save(cleaned_path)

			return render_template('DeepGalaxyDemo.html',  filename=filename, cleaned_path='cleaned-'+filename )
	except Exception as e:
		return render_template('DeepGalaxyDemo.html', error=e)
	return redirect(url_for('DeepGalaxyDemo'))

if __name__ == "__main__":
	#decide what port to run the app in
	port = int(os.environ.get('PORT', 5000))
	#run the app locally on the givn port
	app.run(host='0.0.0.0', port=port)
	#optional if we want to run in debugging mode
	app.run(debug=True)
