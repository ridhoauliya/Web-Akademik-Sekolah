from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Ganti dengan kunci rahasia yang aman

# Koneksi ke MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='Akun',
    autocommit=True  # Set autocommit ke True
)
cursor = conn.cursor()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Ambil data dari form
        username = request.form['username']
        password = request.form['password']

        # Simpan data ke database
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Logika untuk menangani permintaan POST saat pengguna mengirimkan formulir login
        username = request.form['username']
        password = request.form['password']

        # Cek data di database
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        
        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

# Rute untuk halaman guru
# ...

@app.route('/guru')
def guru_list():
    # Ambil daftar guru dari database
    cursor.execute("SELECT * FROM guru")
    guru_list = cursor.fetchall()
    return render_template('guru.html', guru_list=guru_list)

@app.route('/list')
def list():
    # Ambil daftar guru dari database
    cursor.execute("SELECT * FROM guru")
    guru_list = cursor.fetchall()
    return render_template('guru.html', guru_list=guru_list)

@app.route('/guru/add', methods=['GET', 'POST'])
def add_guru():
    if request.method == 'POST':
        # Ambil data dari form
        nama = request.form['nama']
        mata_pelajaran = request.form['mata_pelajaran']
        jabatan = request.form['jabatan']

        # Simpan data ke database
        cursor.execute("INSERT INTO guru (Nama, Mata_pelajaran, Jabatan) VALUES (%s, %s, %s)",
                       (nama, mata_pelajaran, jabatan))
        conn.commit()

        return redirect(url_for('guru_list'))

    return render_template('add_guru.html')

@app.route('/guru/edit/<int:id>', methods=['GET', 'POST'])
def edit_guru(id):
    cursor.execute("SELECT * FROM guru WHERE id = %s", (id,))
    guru = cursor.fetchone()

    if request.method == 'POST':
        # Ambil data dari form
        nama = request.form['nama']
        mata_pelajaran = request.form['mata_pelajaran']
        jabatan = request.form['jabatan']

        # Update data ke database
        cursor.execute("UPDATE guru SET Nama=%s, Mata_pelajaran=%s, Jabatan=%s WHERE id=%s",
                       (nama, mata_pelajaran, jabatan, id))
        conn.commit()

        return redirect(url_for('guru_list'))

    return render_template('edit_guru.html', guru=guru)

@app.route('/guru/delete/<int:id>')
def delete_guru(id):
    # Hapus data dari database
    cursor.execute("DELETE FROM guru WHERE id = %s", (id,))
    conn.commit()

    return redirect(url_for('guru_list'))

# ...


# Rute untuk halaman fasilitas
@app.route('/fasilitas')
def fasilitas():
    if 'username' in session:
        return render_template('fasilitas.html', username=session['username'])
    else:
        return "You are not logged in."

# Rute untuk halaman jadwal
@app.route('/jadwal')
def jadwal():
    if 'username' in session:
        return render_template('jadwal.html', username=session['username'])
    else:
        return "You are not logged in."

# Rute untuk halaman rank
@app.route('/rank')
def rank():
    if 'username' in session:
        return render_template('rank.html', username=session['username'])
    else:
        return "You are not logged in."
    

if __name__ == '__main__':
    app.run(debug=True)
