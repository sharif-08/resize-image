from flask import Flask ,request,render_template,send_from_directory
from PIL import Image
import os
app = Flask(__name__)
UPLOAD_FOLDER ='uploads'
RESIZED_FOLDER ='resized'

os.makedirs(UPLOAD_FOLDER,exist_ok=True)
os.makedirs(RESIZED_FOLDER,exist_ok=True)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == "POST":
        file =request.files['image']
        scale =int(request.form['scale'])
        if file and scale > 0:
            filename =file.filename
            filepath = os.path.join(UPLOAD_FOLDER,filename)
            file.save(filepath)
            img = Image.open(filepath)
            new_size =(int(img.width * scale /100),int(img.height*scale/100))
            resized_img =img.resize(new_size)
            resized_path =os.path.join(RESIZED_FOLDER,filename)
            resized_img.save(resized_path, quality =100)
            return render_template('index.html',filename=filename)
    return render_template('index.html',filename=None)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(RESIZED_FOLDER,filename, as_attachment =True)

if __name__=="__main__":
    app.run(debug=True)

