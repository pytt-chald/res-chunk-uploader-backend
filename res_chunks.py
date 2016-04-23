#!/usr/bin/python
import shutil
import os
import os.path
import logging
from flask import Flask,request,abort,redirect,abort



UPLOAD_FOLDER='/var/www/html/.uploader106/uploads/'

LOG_FILENAME = '/tmp/logging_.out'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)


try:


 app = Flask(__name__)
 app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


 @app.route("/",methods=['GET'])
 def check_test_chunk ():

	filename = request.args['resumableIdentifier']+'.'+request.args['resumableChunkNumber']
        filesize = request.args["resumableCurrentChunkSize"]
        full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)


	if (os.path.isfile(full_path) and int(os.path.getsize(full_path))==int(filesize)):
		return "OK",200
	else:
		return "Not Found",404

 @app.route("/",methods=['POST'])
 def store_recieved_chunk ():

 	filename = request.form['resumableIdentifier']+'.'+request.form['resumableChunkNumber']
 	filesize = request.form["resumableCurrentChunkSize"]
 	full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

       	file = request.files['file']
        file.save( os.path.join(app.config['UPLOAD_FOLDER'], filename) )

        return "OK",200



 @app.route("/merge",methods=['POST','GET'])
 def merge_chunks ():

	filename=str(request.args["filename"])
	chunks_num=request.args["chunks_num"]

	with open(app.config['UPLOAD_FOLDER']+filename,"wb") as wf:
        	for i in range(1,int(chunks_num)+1):
                	with open(app.config['UPLOAD_FOLDER']+filename+"."+str(i),"rb") as chunk:
                        	for line in chunk:
                                	wf.write(line)
                	os.remove(app.config['UPLOAD_FOLDER']+filename+"."+str(i))

	return "OK",200


except:
        logging.exception('Got exception on main handler')
        raise
