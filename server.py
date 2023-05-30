import flask
from werkzeug.utils import secure_filename
import os
import socket


server = flask.Flask(__name__ , template_folder="templates" , static_folder="staticFiles")

@server.route("/")
def homePage():
    return flask.render_template("homePage.html")

# @server.before_request
# def limit_remote_addr():
#     if flask.request.remote_addr == '192.168.1.26':
#         flask.abort(403)  # Forbidden

@server.route('/' , methods=['POST' , 'GET'])
def uploadFiles():
    if flask.request.method == "POST":
        files = flask.request.files.getlist("files[]")
        for file in files:
            file.save(os.path.join(server.config["UPLOAD_FOLDER"] , secure_filename(file.filename)))
        return flask.render_template("homePage.html")
    
@server.route("/download/<filename>")
def downloadFile(filename):
    return flask.send_file(os.path.join(os.path.join(os.getcwd() , "F") , filename),as_attachment=True)

@server.route("/delete/<filename>")
def deleteFile(filename):
    os.remove(os.path.join(server.config["UPLOAD_FOLDER"],filename))
    return server.redirect("/files")
    
@server.route("/files")
def files():
    def max_len(file):
        if len(str(file)) > 3:
            return float(str(file)[0:4])
        
    files = os.listdir(os.path.join(os.getcwd() , "F"))
    links_dict = {}
    for file in files:
        file_size = os.stat(os.path.join(os.getcwd() , f"F/{file}")).st_size / (1024 * 1024)
        file_size = max_len(file_size)
        downloadfile = flask.url_for("downloadFile" , filename=file)
        links_dict[downloadfile] = [f"{file_size}MB" , flask.url_for("deleteFile" , filename=file)]
    return flask.render_template("files.html" , links_dict=links_dict)

if __name__ == "__main__":
    uploadFolder = os.path.join(os.getcwd() , "F")
    deviceName = socket.gethostname()
    ip_address = socket.gethostbyname(deviceName)
    server.config['UPLOAD_FOLDER'] = uploadFolder
    server.run(host=ip_address , port=5000 , debug=True)
