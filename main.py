from flask import Flask, render_template, redirect, url_for, flash, request
from werkzeug.utils import secure_filename
from extract import Photo
import os

photo = Photo()

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ColourPaletteProject'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024

filename = None

#Establishes demo list of colors
file_image_source = 'static/uploads/sunflower.jpg'
photo.open_image_from_server(file_image_source)
photo.show_top_10()
colors = photo.color_dict

## Deletes files that is not used for the demo
files_folder = os.listdir('static/uploads')
for files in files_folder:
    if files !='sunflower.jpg':
        os.remove(f'static/uploads/{files}')

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_files():
    global file_image_source
    global colors
    global total_num_of_pixels
    global filename

    if request.method == 'POST':

        if 'num_color' in request.form:
            photo.NUM_CLUSTERS = int(request.form.get('num_color'))

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')

        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.

        if file.filename == '':
            flash('No selected file')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_image_source = f'static/uploads/{filename}'
            photo.open_image_from_server(file_image_source)
            photo.show_top_10()
            colors = photo.color_dict
            total_num_of_pixels = photo.num_pixels
            return redirect(url_for('upload_files', filename=filename, image=file_image_source, colors=colors))

    return render_template('index.html', filename=filename, image=file_image_source, colors=colors)

if __name__ == '__main__':
    app.run(debug=True)
