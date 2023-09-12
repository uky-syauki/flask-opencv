from app import app, db
from app.forms import LoginForm, DaftarForm
from app.models import User, Admin
from flask import request, render_template, url_for, Response, redirect, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse


from app.opencvHandle import OPENCV
import os

opencv = None

# @app.before_request
# def before_request():
#     if current_user.is_authenticated:
#         global opencv
#         opencv = OPENCV(current_user.username, app)


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     title = 'Masuk'
#     if current_user.is_authenticated:
#         return redirect(url_for("index"))
#     form = LoginForm()
#     if form.validate_on_submit():
#         print('Username: ',form.username.data)
#         print('Password: ',form.password.data)
#         admin = Admin.query.filter_by(username=form.username.data).first()
#         if admin is None or not admin.check_password(form.password.data):
#             flash('Nama Anggota atau Password Salah')
#             print("Gagal Login")
#             return redirect(url_for('login'))
#         # flash("Selamat anda berhasil login")
#         login_user(admin, remember=form.remember_me.data)
#         print("Login success")
#         next_page = request.args.get('next')
#         if not next_page or url_parse(next_page).netloc != '':
#             next_page = url_for('index')
#         return redirect(url_for('index'))
#     return render_template('login.html', title=title, form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    title = 'Masuk'
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = Admin.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Nama Anggota atau Password Salah')
            return redirect(url_for('login'))
        flash("Selamat anda berhasil login")
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title=title, form=form)


# @app.route('/login2')
# def login2():
#     return render_template('login2.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/mendaftar', methods=['GET','POST'])
@login_required
def mendaftar():
    title = "Mendaftar"
    # if current_user.is_authenticated:
    #     return redirect('index')
    form = DaftarForm()
    if request.method == 'POST':
        if form.username.data == '':
            flash("Anda tidak mengisi Nama Anggota")
        if form.email.data == '':
            flash('Anda tidak mengisi email')
        print('User click submit')
    if form.validate_on_submit():
        print('submit on click')
        user = User(username=form.username.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash('Selamat anda berhasil mendaftar')
        return redirect('login')
    return render_template('register.html', form=form, title=title)


@app.route('/dasboard')
@login_required
def dasboard():
    # filtered_data = {k: v for k, v in data.items() if v > 5}
    title = "Beranda"
    # user = .query.filter_by(username=current_user.username).first()
    allUser = User.query.all()

    # print(user.face_prediksi, 'from index')
    return render_template('dasboard.html', title=title, allUser=allUser)



@app.route('/')
@app.route('/index')
@login_required
def index():
    title = "Beranda"
    # user = User.query.filter_by(username=current_user.username).first()
    # allUser = User.query.all()
    # print(user.face_prediksi, 'from index')
    return render_template('index.html', title=title)


@app.route('/tambahkan_wajah/<username>', methods=['GET'])
def tambahkan(username):
    title = "add Face"
    global opencv
    user = User.query.filter_by(username=username).first()
    opencv = OPENCV(user.username, app)
    return render_template('tambahkan_wajah.html', title=title, user=user)


@app.route('/pengenalan')
def pengenalan():
    title = "Pengenalan"
    return render_template('pengenalan.html', title=title)


@app.route("/galery")
def galery():
    print(os.getcwd())
    imgpath = {}
    for isi in os.listdir('sampleimg/'):
        imgpath[f'sampleimg/{isi}'] = []
        for isi2 in os.listdir(f'sampleimg/{isi}'):
            imgpath[f'sampleimg/{isi}'].append(isi2)
    print(imgpath)
    return render_template('samplegalery.html', imgpath=imgpath)

# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('login'))


@app.route('/user_dataset')
@login_required
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


@app.route('/daftarkan_wajah')
def daftarkan():
    title = "Daftarkan Wajah"
    return render_template('daftarkan_wajah.html', title=title)


@app.route('/set_sample_image')
def set_sample_image():
    return Response(opencv.generate_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/deteksi2')
def deteksi2():
    print(opencv.camera_aktif, "INFO CAMERA")
    return render_template('deteksi2.html', cam=url_for('deteksi'))


@app.route("/deteksi")
@login_required
def deteksi():
    user = Admin.query.filter_by(username=current_user.username).first()
    user.face_prediksi = 0
    db.session.add(user)
    db.session.commit()
    print(user.face_prediksi, "from deteksi")
    def redd():
        return redirect(url_for('index'))
    return Response(opencv.deteksi_dengan_vidio(redd), mimetype='multipart/x-mixed-replace; boundary=frame')


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





# @app.route('/latih_')

# untuk produksi
# opencv = OPENCV(db.getByName(current_user.username))




# @app.route('/add')
# def addData():
#     return render_template('addsample.html')



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

# @app.route('/ftes')
# def ftes():
#     return render_template('testing.html')


# @app.route("/testing")
# def deteksi3():
#     return Response(opencv.deteksi_dengan_vidio2(), mimetype='multipart/x-mixed-replace; boundary=frame')

