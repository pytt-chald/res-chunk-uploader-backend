# res-chunk-uploader-backend
python backend for res-chunk-uploader, using flask
res-chunk-uploader: https://github.com/pytt-chald/res-chunk-uploader


#Apache configuration

##add to apache.conf:

WSGIScriptAlias /upload/target/url /path/to/wsgi/file/res_chunks.wsgi
WSGIPythonPath /path/to/wsgi/file/

  <Directory /path/to/wsgi/file/>
        <Files res_chunks.wsgi>
                Require all granted
        </Files>
  </Directory>



##example:

WSGIScriptAlias /.uploader106/upload /var/www/html/flask/res_chunks.wsgi
WSGIPythonPath /var/www/html/flask

  <Directory /var/www/html/flask/>
        <Files res_chunks.wsgi>
                Require all granted
        </Files>
  </Directory>

