import os
UPLOAD_FOLDER = 'static/user_imgs'
STYLE_FOLDER = 'static/style_imgs'
PREDICTION_FOLDER = 'static/preds'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def purge():
    data = [UPLOAD_FOLDER, PREDICTION_FOLDER]
    for folder in data:
        for file in os.listdir(folder):
            os.remove(folder+"/"+file)
    # remove the zip files
    #for item in os.listdir('static/download/'):
    #    os.remove('static/download/'+item)
    #for file in os.listdir('static/preds/'):
    #   os.remove('static/preds/'+file)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def show_predictions(dir):
    filelist = os.listdir(dir)
    to_show = []
    for file in filelist:
        saved_loc = os.path.join(dir, file)
        to_show.append(saved_loc)
    return to_show