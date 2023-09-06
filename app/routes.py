from app import app, db
from app.forms import LoginForm, DaftarForm
from app.models import User
from flask import request, render_template, url_for, Response, redirect, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse


from app.opencvHandle import OPENCV
from app.dbHandle import DB
import os


# @app.route('/mendaftar')
# def mendaftar():
#     form = DaftarForm()
#     return render_template('mendaftar.html', form=form)

opencv = None

# @app.before_request
# def before_request():
#     if current_user.is_authenticated:
#         global opencv
#         opencv = OPENCV({'id':current_user.id, 'nama': current_user.username}, app)


@app.route('/login', methods=['GET', 'POST'])
def login():
    title = 'Masuk'
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Nama Anggota atau Password Salah')
            return redirect(url_for('login'))
        flash("Selamat anda berhasil login")
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login2.html', title=title, form=form)


@app.route('/login2')
def login2():
    return render_template('login2.html')




@app.route('/mendaftar', methods=['GET','POST'])
def mendaftar():
    title = "Mendaftar"
    if current_user.is_authenticated:
        return redirect('index')
    form = DaftarForm()
    if request.method == 'POST':
        if form.username.data == '':
            flash("Anda tidak mengisi Nama Anggota")
        if form.email.data == '':
            flash('Anda tidak mengisi email')
        if form.password.data == '':
            flash('Anda tidak mengisi password')
        if form.password2.data == '':
            flash('Anda tidak mengisi ulang password')
        print(form.username.data == '')
        print('User click submit')
    if form.validate_on_submit():
        print('submit on click')
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Selamat anda berhasil mendaftar')
        return redirect('login')
    return render_template('mendaftar2.html', form=form, title=title)


@app.route('/')
@app.route('/index')
@login_required
def index():
    title = "Beranda"
    global opencv
    opencv = OPENCV({'id':current_user.id, 'nama': current_user.username}, app)
    
    print(opencv.prediksi,"From prediksi")
    # print(current_user.face_prediksi)
    if current_user.face_prediksi == 0:
        pass

    return render_template('index.html', title=title)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/user_dataset')
def user_dataset():
    title = "user_dataset"
    return render_template('user_dataset.html', title=title)


@app.route('/get_location', methods=['GET'])
def get_location():
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))
    
    # Di sini Anda dapat melakukan apa pun dengan koordinat yang Anda terima,
    # seperti mencari lokasi atau menghitung jarak, dan kemudian mengembalikan
    # hasil sebagai respons JSON.
    
    
    result = f"Latitude: {lat}, Longitude: {lon}"
    
    return jsonify({"result": result})


@app.route("/daftar", methods=['GET', 'POST'])
def daftar():
    title = "Mendaftar"
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = DaftarForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Selamat anda telah berhasil mendaftar!')
        return redirect(url_for('login'))
    return render_template('daftar.html', title=title, form=form)
    

@app.route('/dataset')
def dataset():
    return render_template('addsample.html')

# db = DB()
# opencv = OPENCV(db.getByName('uki'))

@app.route('/set_sample_image')
def set_sample_image():
    return Response(opencv.generate_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/latih_')

# untuk produksi
# opencv = OPENCV(db.getByName(current_user.username))






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


# @app.route('/upload', methods=['POST'])
# def upload_video():
#     db = DB()
#     video_file = request.files['video']
#     if video_file:
#         # Handle the uploaded video (e.g., save it to a folder)
#         video_file.save('vidio/recorded.mp4')
#     if len(os.listdir('vidio')) > 0:
#         OPENCV().setDariRekam(db.getByName('uki'))
#         return 'Video uploaded successfully'
#     return "Ada yang Benar"


# @app.route('/base')
# def base():
#     return render_template('base.html')

# @app.route('/tes')
# def tes():
#     return render_template('deteksi.html')


@app.route("/deteksi")
def deteksi():
    global opencv
    return Response(opencv.deteksi_dengan_vidio(), mimetype='multipart/x-mixed-replace; boundary=frame')


# @app.route('/add')
# def addData():
#     return render_template('addsample.html')


@app.route('/video_feed')
def video_feed():
    return Response(opencv.generate_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/tutup_camera')
def tutup_camera():
    opencv.tutup_camera()
    # opencv.add_dataset_img()
    # opencv.training()
    # opencv.latih_sampleimg()
    return redirect(url_for('index'))