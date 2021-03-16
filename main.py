from flask import Flask
from data_objects import save_info_person_1, save_info_person_2, save_info_person_3, save_info_company_1, \
    save_info_company_2, save_info_company_3, user_validation
from flask import request, session, render_template, g, url_for
from werkzeug.utils import secure_filename
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# ---------------------------------------------------------------------->

# ---------------------------------------------------------------------->
# (Using flask as the designated Module for Web, and Flask-SQLAlchemy for Database Configuration)
app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/maxwellhollins/Desktop/naos_site/database.db'
app.config['IMAGE_UPLOADS'] = '/Users/maxwellhollins/Desktop/naos_site/static/upload_folder'
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PDF", "PNG", "GIF"]
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
# ---------------------------------------------------------------------->
db = SQLAlchemy(app)

# ---------------------------------------------------------------------->
# (Dictionary for User Registration)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))


# ---------------------------------------------------------------------->
@app.route('/form_login', methods=['POST', 'GET'])
def login():
    email = request.form['email']
    pwd = request.form['password']
    if request.method == 'POST':
        session.pop('user', None)
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, pwd):
                session['user'] = request.form['email']
                return render_template('home_es.html', name=email)
            else:
                return render_template('login.html',
                                       info_es='Contraseña no válida: vuelva a ingresar su contraseña correcta o registre una cuenta.',
                                       info_en='Invalid Password: Please re-enter your correct Password or register an account.')

        else:
            return render_template('login.html',
                                   info_es='Correo electrónico no válido: vuelva a ingresar '
                                           'su correo electrónico o registre una cuenta.',
                                   info_en='Invalid email: Please re-enter your email or register an account.')


@app.route('/form_register', methods=['POST', 'GET'])
def register():
    email = request.form['email']
    pwd = request.form['password']
    user = User.query.filter_by(email=email).first()
    if not user:
        hashed_password = generate_password_hash(pwd, method='sha256')
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return render_template('login.html',
                               info_es='Cuenta creada correctamente: continúe iniciando sesión.',
                               info_en='User Created! Please continue by logging in.')
    else:
        if user:
            return render_template('register.html',
                                   info_es='Este correo electrónico está actualmente en uso: '
                                           'utilice un correo electrónico diferente para esta cuenta.',
                                   info_en='This email is currently in use: Please use a different email for this account.')


@app.route('/form_login_en', methods=['POST', 'GET'])
def login_en():
    email = request.form['email']
    pwd = request.form['password']
    if request.method == 'POST':
        session.pop('user', None)
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, pwd):
                session['user'] = request.form['email']
                return render_template('home_es.html', name=email)
            else:
                return render_template('login_en.html',
                                       info_en='Invalid Password: Please re-enter your correct Password or register an account.')

        else:
            return render_template('login_en.html',
                                   info_en='Invalid email: Please re-enter your email or register an account.')


@app.route('/form_register_en', methods=['POST', 'GET'])
def register_en():
    email = request.form['email']
    pwd = request.form['password']
    user = User.query.filter_by(email=email).first()
    if not user:
        hashed_password = generate_password_hash(pwd, method='sha256')
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return render_template('login_en.html',
                               info_en='User Created! Please continue by logging in.')
    else:
        if user:
            return render_template('register_en.html',
                                   info_en='This email is currently in use: Please use a different email for this account.')


def allowed_image(filename):
    # We only want files with a . in the filename
    if not "." in filename:
        return False

    # Split the extension from the filename
    ext = filename.rsplit(".", 1)[1]

    # Check if the extension is in ALLOWED_IMAGE_EXTENSIONS
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


@app.route('/submit_page_one', methods=['POST', 'GET'])
def submit_page_one():
    if not g.user:
        return render_template('/login.html')
    else:
        if request.method == 'POST':
            fiscal_code = request.files["fiscal_code"]
            CURP_code = request.files["CURP_code"]
            passport = request.files["passport"]
            if request.files:
                if fiscal_code:
                    if allowed_image(fiscal_code.filename):
                        filename = secure_filename(fiscal_code.filename)
                        fiscal_code.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    else:
                        return render_template('/form_1_es.html',
                                               info_en='Something went wrong... please re-enter your information. (Please submit only file types of the following format: PDF, JPG, or PNG)',
                                               info_es='Ha ocurrido un error ... Vuelva a ingresar su información. (Por favor, asegurese de subir los archivos en los siguientes formatos: PDF, JPG, o PNG)')
                if CURP_code:
                    if allowed_image(CURP_code.filename):
                        filename = secure_filename(CURP_code.filename)
                        CURP_code.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    else:
                        return render_template('/form_1_es.html',
                                               info_en='Something went wrong... please re-enter your information. (Please submit only file types of the following format: PDF, JPG, or PNG)',
                                               info_es='Ha ocurrido un error ... Vuelva a ingresar su información. (Por favor, asegurese de subir los archivos en los siguientes formatos: PDF, JPG, o PNG)')
                if passport:
                    if allowed_image(passport.filename):
                        filename = secure_filename(passport.filename)
                        passport.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    else:
                        render_template('/form_1_es.html',
                                        info_en='Something went wrong... please re-enter your information. (Please submit only file types of the following format: PDF, JPG, or PNG)',
                                        info_es='Ha ocurrido un error ... Vuelva a ingresar su información. (Por favor, asegurese de subir los archivos en los siguientes formatos: PDF, JPG, o PNG)')

            data = request.form.to_dict()
            save_info_person_1(data)
            return render_template('/form_2_es.html',
                                   info_es='¡Página uno enviada con éxito! Continúe con la página dos.')
        else:
            return render_template('/form_1_es.html',
                                   info_en='Something went wrong... please re-enter your information. (Please submit only file types of the following format: PDF, JPG, or PNG)',
                                   info_es='Ha ocurrido un error ... Vuelva a ingresar su información. (Por favor, asegurese de subir los archivos en los siguientes formatos: PDF, JPG, o PNG)')


@app.route('/submit_page_two', methods=['POST', 'GET'])
def submit_page_two():
    if not g.user:
        return render_template('/login.html')
    else:
        if request.method == 'POST':
            proof_of_location = request.files["proof_of_location"]
            if request.files:
                if proof_of_location:
                    if allowed_image(proof_of_location.filename):
                        filename = secure_filename(proof_of_location.filename)
                        proof_of_location.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    else:
                        return render_template('/form_2_es.html',
                                               info_en='Something went wrong... please re-enter your information. (Please submit only file types of the following format: PDF, JPG, or PNG)',
                                               info_es='Ha ocurrido un error ... Vuelva a ingresar su información. (Por favor, asegurese de subir los archivos en los siguientes formatos: PDF, JPG, o PNG)')
            data = request.form.to_dict()
            save_info_person_2(data)
            return render_template('/form_3_es.html',
                                   info_es='Página dos enviada con éxito! Continúe con la página tres.')
        else:
            return render_template('/form_2_es.html',
                                   info_en='Something went wrong... please re-enter your information. (Please submit only file types of the following format: PDF, JPG, or PNG)',
                                   info_es='Ha ocurrido un error ... Vuelva a ingresar su información. (Por favor, asegurese de subir los archivos en los siguientes formatos: PDF, JPG, o PNG)')


@app.route('/submit_page_three', methods=['POST', 'GET'])
def submit_page_three():
    if not g.user:
        return render_template('/login.html')
    else:
        if request.method == 'POST':
            official_id_3 = request.files["official_id_3"]
            if request.files:
                if official_id_3:
                    if allowed_image(official_id_3.filename):
                        filename = secure_filename(official_id_3.filename)
                        official_id_3.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    else:
                        return render_template('/form_3_es.html',
                                               info_en='Something went wrong... please re-enter your information. (Please submit only file types of the following format: PDF, JPG, or PNG)',
                                               info_es='Ha ocurrido un error ... Vuelva a ingresar su información. (Por favor, asegurese de subir los archivos en los siguientes formatos: PDF, JPG, o PNG)')
            data = request.form.to_dict()
            save_info_person_3(data)
            return render_template('/finish_es.html')
        else:
            return render_template('/form_3_es.html',
                                   info_en='Something went wrong... please re-enter your information. (Please submit only file types of the following format: PDF, JPG, or PNG)',
                                   info_es='Ha ocurrido un error ... Vuelva a ingresar su información. (Por favor, asegurese de subir los archivos en los siguientes formatos: PDF, JPG, o PNG)')


@app.route('/submit_page_one_morales', methods=['POST', 'GET'])
def submit_page_one_morales():
    if not g.user:
        return render_template('/login.html')
    else:
        if request.method == 'POST':
            bank_account_statement = request.files["bank_account_statement"]
            incorporation_act = request.files["incorporation_act"]
            legal_rep_faculties = request.files["legal_rep_faculties"]
            legal_rep_id = request.files["legal_rep_id"]

            if request.files:
                if bank_account_statement:
                    if allowed_image(bank_account_statement.filename):
                        filename = secure_filename(bank_account_statement.filename)
                        bank_account_statement.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    else:
                        return render_template('/form_1_morales_es.html',
                                               info_en='Something went wrong... please re-enter your information. (Please submit only file types of the following format: PDF, JPG, or PNG)',
                                               info_es='Ha ocurrido un error ... Vuelva a ingresar su información. (Por favor, asegurese de subir los archivos en los siguientes formatos: PDF, JPG, o PNG)')
                    incorporation_act = request.files["incorporation_act"]
                if incorporation_act:
                    if allowed_image(incorporation_act.filename):
                        filename = secure_filename(incorporation_act.filename)
                        incorporation_act.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    else:
                        return render_template('/form_1_morales_es.html',
                                               info_en='Something went wrong... please re-enter your information. (Please submit only file types of the following format: PDF, JPG, or PNG)',
                                               info_es='Ha ocurrido un error ... Vuelva a ingresar su información. (Por favor, asegurese de subir los archivos en los siguientes formatos: PDF, JPG, o PNG)')
                if legal_rep_faculties:
                    if allowed_image(legal_rep_faculties.filename):
                        filename = secure_filename(legal_rep_faculties.filename)
                        legal_rep_faculties.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    else:
                        return render_template('/form_1_morales_es.html',
                                               info_en='Something went wrong... please re-enter your information. (Please submit only file types of the following format: PDF, JPG, or PNG)',
                                               info_es='Ha ocurrido un error ... Vuelva a ingresar su información. (Por favor, asegurese de subir los archivos en los siguientes formatos: PDF, JPG, o PNG)')
                if legal_rep_id:
                    if allowed_image(legal_rep_id.filename):
                        filename = secure_filename(legal_rep_id.filename)
                        legal_rep_id.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    else:
                        return render_template('/form_1_morales_es.html',
                                               info_en='Something went wrong... please re-enter your information. (Please submit only file types of the following format: PDF, JPG, or PNG)',
                                               info_es='Ha ocurrido un error ... Vuelva a ingresar su información. (Por favor, asegurese de subir los archivos en los siguientes formatos: PDF, JPG, o PNG)')
            data = request.form.to_dict()
            save_info_company_1(data)
            return render_template('/form_2_morales_es.html',
                                   info_es='¡Página uno enviada con éxito! Continúe con la página dos.')
        else:
            return render_template('/form_1_morales_es.html',
                                   info_en='Something went wrong... please re-enter your information. (Please submit only file types of the following format: PDF, JPG, or PNG)',
                                   info_es='Ha ocurrido un error ... Vuelva a ingresar su información. (Por favor, asegurese de subir los archivos en los siguientes formatos: PDF, JPG, o PNG)')


@app.route('/submit_page_two_morales', methods=['POST', 'GET'])
def submit_page_two_morales():
    if not g.user:
        return render_template('/login.html')
    else:
        if request.method == 'POST':
            proof_of_location = request.files["proof_of_location"]
            legal_rep_address = request.files["legal_rep_address"]

            if request.files:
                if proof_of_location:
                    if allowed_image(proof_of_location.filename):
                        filename = secure_filename(proof_of_location.filename)
                        proof_of_location.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    else:
                        return render_template('/form_2_morales_es.html',
                                               info_en='Something went wrong... please re-enter your information. (Please submit only file types of the following format: PDF, JPG, or PNG)',
                                               info_es='Ha ocurrido un error ... Vuelva a ingresar su información. (Por favor, asegurese de subir los archivos en los siguientes formatos: PDF, JPG, o PNG)')
                if legal_rep_address:
                    if allowed_image(legal_rep_address.filename):
                        filename = secure_filename(legal_rep_address.filename)
                        legal_rep_address.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    else:
                        return render_template('/form_2_morales_es.html',
                                               info_en='Something went wrong... please re-enter your information. (Please submit only file types of the following format: PDF, JPG, or PNG)',
                                               info_es='Ha ocurrido un error ... Vuelva a ingresar su información. (Por favor, asegurese de subir los archivos en los siguientes formatos: PDF, JPG, o PNG)')
            data = request.form.to_dict()
            save_info_company_2(data)
            return render_template('/form_3_morales_es.html',
                                   info_es='Página dos enviada con éxito! Continúe con la página tres.')
        else:
            return render_template('/form_2_morales_es.html',
                                   info_en='Something went wrong... please re-enter your information. (Please submit only file types of the following format: PDF, JPG, or PNG)',
                                   info_es='Ha ocurrido un error ... Vuelva a ingresar su información. (Por favor, asegurese de subir los archivos en los siguientes formatos: PDF, JPG, o PNG)')


@app.route('/submit_page_three_morales', methods=['POST', 'GET'])
def submit_page_three_morales():
    if not g.user:
        return render_template('/login.html')
    else:
        if request.method == 'POST':
            official_id_3 = request.files["official_id_3"]
            organization_chart = request.files["organization_chart"]

            if request.files:
                if official_id_3:
                    if allowed_image(official_id_3.filename):
                        filename = secure_filename(official_id_3.filename)
                        official_id_3.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    else:
                        return render_template('/form_3_morales_es.html',
                                               info_en='Something went wrong... please re-enter your information. (Please submit only file types of the following format: PDF, JPG, or PNG)',
                                               info_es='Ha ocurrido un error ... Vuelva a ingresar su información. (Por favor, asegurese de subir los archivos en los siguientes formatos: PDF, JPG, o PNG)')
                if organization_chart:
                    if allowed_image(organization_chart.filename):
                        filename = secure_filename(organization_chart.filename)

                        organization_chart.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    else:
                        return render_template('/form_3_morales_es.html',
                                               info_en='Something went wrong... please re-enter your information.',
                                               info_es='Ha ocurrido un error ... Vuelva a ingresar su información. (Por favor, asegurese de subir los archivos en los siguientes formatos: PDF, JPG, o PNG)')
            data = request.form.to_dict()
            save_info_company_3(data)
            return render_template('/finish_es.html')
        else:
            return render_template('/form_3_morales_es.html',
                                   info_en='Something went wrong... please re-enter your information.',
                                   info_es='Ha ocurrido un error ... Vuelva a ingresar su información. (Por favor, asegurese de subir los archivos en los siguientes formatos: PDF, JPG, o PNG)')


# ---------------------------------------------------------------------->
# (English copies of paths
# ---------------------------------------------------------------------->
@app.route('/submit_page_one_en', methods=['POST', 'GET'])
def submit_page_one_en():
    if not g.user:
        return render_template('/login.html')
    else:
        if request.method == 'POST':
            fiscal_code = request.files["fiscal_code"]
            CURP_code = request.files["CURP_code"]
            passport = request.files["passport"]
            if request.files:
                if fiscal_code:
                    if allowed_image(fiscal_code.filename):
                        filename = secure_filename(fiscal_code.filename)
                        fiscal_code.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    else:
                        return render_template('/form_1.html',
                                               info_en='Something went wrong... please re-enter your information. (Please submit only file types of the following format: PDF, JPG, or PNG)')
                if CURP_code:
                    if allowed_image(CURP_code.filename):
                        filename = secure_filename(CURP_code.filename)
                        CURP_code.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    else:
                        return render_template('/form_1.html',
                                               info_en='Something went wrong... please re-enter your information. (Please submit only file types of the following format: PDF, JPG, or PNG)',
                                               )
                if passport:
                    if allowed_image(passport.filename):
                        filename = secure_filename(passport.filename)
                        passport.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    else:
                        render_template('/form_1.html',
                                        info_en='Something went wrong... please re-enter your information. (Please submit only file types of the following format: PDF, JPG, or PNG)',
                                        )

            data = request.form.to_dict()
            save_info_person_1(data)
            return render_template('/form_2.html',
                                   info_en='Page one successfully submitted! Please continue to page two.')
        else:
            return render_template('/form_1.html',
                                   info_en='Something went wrong... please re-enter your information. (Please submit only file types of the following format: PDF, JPG, or PNG)',
                                   )


@app.route('/submit_page_two_en', methods=['POST', 'GET'])
def submit_page_two_en():
    if not g.user:
        return render_template('/login.html')
    else:
        if request.method == 'POST':
            proof_of_location = request.files["proof_of_location"]
            if request.files:
                if proof_of_location:
                    if allowed_image(proof_of_location.filename):
                        filename = secure_filename(proof_of_location.filename)
                        proof_of_location.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    else:
                        return render_template('/form_2.html',
                                               info_en='Something went wrong... please re-enter your information. (Please submit only file types of the following format: PDF, JPG, or PNG)',
                                               )
            data = request.form.to_dict()
            save_info_person_2(data)
            return render_template('/form_3.html',
                                   info_en='Page two successfully submitted! Please continue to page three.')
        else:
            return render_template('/form_2.html',
                                   info_en='Something went wrong... please re-enter your information. (Please submit only file types of the following format: PDF, JPG, or PNG)',
                                   )


@app.route('/submit_page_three_en', methods=['POST', 'GET'])
def submit_page_three_en():
    if not g.user:
        return render_template('/login.html')
    else:
        if request.method == 'POST':
            if request.files:
                official_id_3 = request.files["official_id_3"]
                if allowed_image(official_id_3.filename):
                    filename = secure_filename(official_id_3.filename)
                    official_id_3.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                else:
                    return render_template('/form_3.html',
                                           info_en='Something went wrong... please re-enter your information. (Please submit only file types of the following format: PDF, JPG, or PNG)',
                                           )
            data = request.form.to_dict()
            save_info_person_3(data)
            return render_template('/finish_es.html')
        else:
            return render_template('/form_3.html',
                                   info_en='Something went wrong... please re-enter your information. (Please submit only file types of the following format: PDF, JPG, or PNG)',
                                   )


@app.route('/submit_page_one_morales_en', methods=['POST', 'GET'])
def submit_page_one_morales_en():
    if not g.user:
        return render_template('/login.html')
    else:
        if request.method == 'POST':
            bank_account_statement = request.files["bank_account_statement"]
            incorporation_act = request.files["incorporation_act"]
            legal_rep_faculties = request.files["legal_rep_faculties"]
            legal_rep_id = request.files["legal_rep_id"]

            if request.files:
                if bank_account_statement:
                    if allowed_image(bank_account_statement.filename):
                        filename = secure_filename(bank_account_statement.filename)
                        bank_account_statement.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    else:
                        return render_template('/form_1_morales_es.html',
                                               info_en='Something went wrong... please re-enter your information. (Please submit only file types of the following format: PDF, JPG, or PNG)',
                                               )
                    incorporation_act = request.files["incorporation_act"]
                if incorporation_act:
                    if allowed_image(incorporation_act.filename):
                        filename = secure_filename(incorporation_act.filename)
                        incorporation_act.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    else:
                        return render_template('/form_1_morales_es.html',
                                               info_en='Something went wrong... please re-enter your information. (Please submit only file types of the following format: PDF, JPG, or PNG)'
                                               )
                if legal_rep_faculties:
                    if allowed_image(legal_rep_faculties.filename):
                        filename = secure_filename(legal_rep_faculties.filename)
                        legal_rep_faculties.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    else:
                        return render_template('/form_1_morales_es.html',
                                               info_en='Something went wrong... please re-enter your information. (Please submit only file types of the following format: PDF, JPG, or PNG)'
                                               )
                if legal_rep_id:
                    if allowed_image(legal_rep_id.filename):
                        filename = secure_filename(legal_rep_id.filename)
                        legal_rep_id.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    else:
                        return render_template('/form_1_morales_es.html',
                                               info_en='Something went wrong... please re-enter your information. (Please submit only file types of the following format: PDF, JPG, or PNG)'
                                               )
            data = request.form.to_dict()
            save_info_company_1(data)
            return render_template('/form_2_morales_es.html',
                                   info_es='¡Página uno enviada con éxito! Continúe con la página dos.')
        else:
            return render_template('/form_1_morales_es.html',
                                   info_en='Something went wrong... please re-enter your information. (Please submit only file types of the following format: PDF, JPG, or PNG)',
                                   info_es='Ha ocurrido un error ... Vuelva a ingresar su información. (Por favor, asegurese de subir los archivos en los siguientes formatos: PDF, JPG, o PNG)')


@app.route('/submit_page_two_morales_en', methods=['POST', 'GET'])
def submit_page_two_morales_en():
    if not g.user:
        return render_template('/login.html')
    else:
        if request.method == 'POST':
            proof_of_location = request.files["proof_of_location"]
            legal_rep_address = request.files["legal_rep_address"]

            if request.files:
                if proof_of_location:
                    if allowed_image(proof_of_location.filename):
                        filename = secure_filename(proof_of_location.filename)
                        proof_of_location.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    else:
                        return render_template('/form_2_morales_es.html',
                                               info_en='Something went wrong... please re-enter your information. (Please submit only file types of the following format: PDF, JPG, or PNG)',
                                               info_es='Ha ocurrido un error ... Vuelva a ingresar su información. (Por favor, asegurese de subir los archivos en los siguientes formatos: PDF, JPG, o PNG)')
                if legal_rep_address:
                    if allowed_image(legal_rep_address.filename):
                        filename = secure_filename(legal_rep_address.filename)
                        legal_rep_address.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    else:
                        return render_template('/form_2_morales_es.html',
                                               info_en='Something went wrong... please re-enter your information. (Please submit only file types of the following format: PDF, JPG, or PNG)',
                                               info_es='Ha ocurrido un error ... Vuelva a ingresar su información. (Por favor, asegurese de subir los archivos en los siguientes formatos: PDF, JPG, o PNG)')
            data = request.form.to_dict()
            save_info_company_2(data)
            return render_template('/form_3_morales_es.html',
                                   info_es='Página dos enviada con éxito! Continúe con la página tres.')
        else:
            return render_template('/form_2_morales_es.html',
                                   info_en='Something went wrong... please re-enter your information. (Please submit only file types of the following format: PDF, JPG, or PNG)',
                                   info_es='Ha ocurrido un error ... Vuelva a ingresar su información. (Por favor, asegurese de subir los archivos en los siguientes formatos: PDF, JPG, o PNG)')


@app.route('/submit_page_three_morales_en', methods=['POST', 'GET'])
def submit_page_three_morales_en():
    if not g.user:
        return render_template('/login.html')
    else:
        if request.method == 'POST':
            official_id_3 = request.files["official_id_3"]
            organization_chart = request.files["organization_chart"]

            if request.files:
                if official_id_3:
                    if allowed_image(official_id_3.filename):
                        filename = secure_filename(official_id_3.filename)
                        official_id_3.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    else:
                        return render_template('/form_3_morales_es.html',
                                               info_en='Something went wrong... please re-enter your information. (Please submit only file types of the following format: PDF, JPG, or PNG)',
                                               )
                if organization_chart:
                    if allowed_image(organization_chart.filename):
                        filename = secure_filename(organization_chart.filename)

                        organization_chart.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    else:
                        return render_template('/form_3_morales_es.html',
                                               info_en='Something went wrong... please re-enter your information.',
                                               )
            data = request.form.to_dict()
            save_info_company_3(data)
            return render_template('/finish_es.html'
                                   )
        else:
            return render_template('/form_3_morales_es.html',
                                   info_en='Something went wrong... please re-enter your information.',
                                   )


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


@app.route("/logout")
def logout():
    session.pop('user', None)
    return render_template('/login.html')


@app.route('/')
def login_spanish():
    return render_template("login.html")


@app.route('/login_english')
def login_english():
    return render_template("login_en.html")


@app.route('/register')
def register_direct():
    return render_template("register.html")


@app.route('/register_english')
def register_english():
    return render_template("register_en.html")


@app.route("/home")
def my_home():
    if not g.user:
        return render_template('/login.html')
    else:
        return render_template("/home_es.html")


@app.route("/KYC_type_es")
def KYC_type_es():
    if not g.user:
        return render_template('/login.html')
    else:
        return render_template("/KYC_type_es.html")


@app.route("/KYC_type_en")
def KYC_type_en():
    if not g.user:
        return render_template('/login.html')
    else:
        return render_template("/KYC_type_en.html")


@app.route("/form_1")
def form_1():
    if not g.user:
        return render_template('/login.html')
    else:
        return render_template("/form_1.html")


@app.route("/form_1_es")
def form_1_es():
    if not g.user:
        return render_template('/login.html')
    else:
        return render_template("/form_1_es.html")


@app.route("/form_2")
def form_2():
    if not g.user:
        return render_template('/login.html')
    else:
        return render_template("/form_2.html")


@app.route("/form_2_es")
def form_2_es():
    if not g.user:
        return render_template('/login.html')
    else:
        return render_template("/form_2_es.html")


@app.route("/form_3")
def form_3():
    if not g.user:
        return render_template('/login.html')
    else:
        return render_template("/form_3.html")


@app.route("/form_3_es")
def form_3_es():
    if not g.user:
        return render_template('/login.html')
    else:
        return render_template("/form_3_es.html")


@app.route("/form_1_morales")
def form_1_morales():
    if not g.user:
        return render_template('/login.html')
    else:
        return render_template("/form_1_morales.html")


@app.route("/form_1_morales_es")
def form_1_morales_es():
    if not g.user:
        return render_template('/login.html')
    else:
        return render_template("/form_1_morales_es.html")


@app.route("/form_2_morales")
def form_2_morales():
    if not g.user:
        return render_template('/login.html')
    else:
        return render_template("/form_2_morales.html")


@app.route("/form_2_morales_es")
def form_2_morales_es():
    if not g.user:
        return render_template('/login.html')
    else:
        return render_template("/form_2_morales_es.html")


@app.route("/form_3_morales")
def form_3_morales():
    if not g.user:
        return render_template('/login.html')
    else:
        return render_template("/form_3_morales.html")


@app.route("/form_3_morales_es")
def form_3_morales_es():
    if not g.user:
        return render_template('/login.html')
    else:
        return render_template("/form_3_morales_es.html")
