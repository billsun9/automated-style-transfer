import os
from flask import Flask, request, redirect, render_template
from werkzeug.utils import secure_filename
from utils import purge, allowed_file, show_predictions
from style_transfer import style_transfer
import numpy as np
UPLOAD_FOLDER = 'static/user_imgs'
STYLE_FOLDER = 'static/style_imgs'
PREDICTION_FOLDER = 'static/preds'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    purge()
    return render_template('index.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    purge()
    if request.method == 'POST':
        style_path = request.form['style']
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        #if file.filename == '':
        #    flash('No selected file')
        #    return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            user_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(user_path)
            path = style_transfer(user_path, style_path)
            return render_template('results.html', path=path)
# %%
if __name__ == '__main__':
    app.run(debug=False)