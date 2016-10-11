#!/usr/bin/python
import shutil
import os
import os.path
import logging
from flask import Flask,request,abort,redirect,abort
import time


UPLOAD_FOLDER='/var/www/html/.uploader106/uploads/'

LOG_FILENAME = '/tmp/logging_.out'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)


try:


 app = Flask(__name__)
 app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


 @app.route("/",methods=['GET'])
 def check_test_chunk ():
	filename = request.args["resumableChunkSize"]+'.'+request.args['resumableIdentifier']+'.'+request.args['resumableChunkNumber']
        filesize = request.args["resumableCurrentChunkSize"]
        full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename).encode("utf-8")
	
	ex_file=os.path.join(UPLOAD_FOLDER,request.args["resumableChunkSize"]+'.'+request.args['resumableIdentifier']+".ex.txt").encode("utf-8")
        chunk_number=int(request.args['resumableChunkNumber'])

	if(os.path.isfile(ex_file)==False):
        	return "Not Found",404

	else:
               f = open(ex_file, "r")
               try:
                       ex=f.read()
                       if(ex[chunk_number-1]=='1'):
                               return "OK",200
                       else:
                               return "Not Found",404
               finally:
                       f.close()

 @app.route("/",methods=['POST'])
 def store_recieved_chunk ():

 	filename = request.form['resumableChunkSize']+'.'+request.form['resumableIdentifier']+'.'+request.form['resumableChunkNumber']
 	filesize = request.form["resumableCurrentChunkSize"]
	full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename).encode("utf-8")
	chunks= int( float(request.form['resumableTotalSize']) / float(request.form['resumableChunkSize']))+1

	ex_file=os.path.join(UPLOAD_FOLDER,request.form['resumableChunkSize']+'.'+request.form['resumableIdentifier']+".ex.txt").encode("utf-8")
	final_file=os.path.join(UPLOAD_FOLDER,request.form['resumableChunkSize']+'.'+request.form['resumableIdentifier']).encode("utf-8")

 	chunk_number=int(request.form['resumableChunkNumber'])

	if(os.path.isfile(ex_file)==False):
                f = open(ex_file, "w+")
                for i in range (0,chunks):
                        f.write('0')
                f.close()
		f = open(final_file, "w+") #creates file		
                f.close()
	
        file = request.files['file']

	with open(final_file, "rb+") as f:
		f.seek((chunk_number-1)*float(request.form["resumableChunkSize"]))
                while True:
                        packet=file.read(1000)
                        if not packet:
                                break
                        f.write(str(packet))

        f = open(ex_file, "r+")
        f.seek(chunk_number-1)
        f.write('1')
        f.close()

        return "OK",200



 @app.route("/merge",methods=['POST','GET'])
 def merge_chunks ():
	filename= request.args["chunk_size"]+'.'+request.args["filename"]
	chunks_num=request.args["chunks_num"]
	chunk_size=request.args["chunk_size"]
	full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename).encode("utf-8")

	os.remove(full_path+".ex.txt")
	return chunks_num+":"+chunk_size,200


except:
        logging.exception('Got exception on main handler')
        raise
