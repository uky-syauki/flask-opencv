from app import app
from flask import request, render_template
from app.opencvHandle import OPENCV
from app.dbHandle import DB
import os


@app.route('/')
@app.route('/index')
def index():
    return render_template('vidio.html')


# @app.route('/upload', methods=['GET', 'POST'])
# def upload_photo():
#     if 'photo' not in request.files:
#         return "Tidak ada foto yang diunggah"
    
#     photo_file = request.files['photo']
#     nama = request.form['nama']
    
#     if photo_file.filename == '':
#         return "tidak ada photo yang dipilih"
    

#     photo_file.save(f'dataset/{nama}.jpg')
#     return "Berhasil mengunggah photo"


@app.route('/upload', methods=['POST'])
def upload_video():
    db = DB()
    video_file = request.files['video']
    if video_file:
        # Handle the uploaded video (e.g., save it to a folder)
        video_file.save('vidio/recorded.mp4')
    if len(os.listdir('vidio')) > 0:
        OPENCV().setDariRekam(db.getByName('uki'))
        return 'Video uploaded successfully'
    return "Ada yang Benar"