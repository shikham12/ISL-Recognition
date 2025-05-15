from flask import Flask, render_template, request, redirect, url_for, jsonify, flash,g
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from gesture_model import GestureRecognizer
import audio_handler
from translator import TRANSLATIONS,translate_gesture,speak_translation,LANGUAGE_CODES

from flask_sqlalchemy import SQLAlchemy
import numpy as np
import base64
import gtts
import cv2

import os

# --- Setup ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.secret_key = '8f3b2b10c9384d4e9a85c3dc9bbd22b0'


# Database setup
engine = create_engine(f'sqlite:///{os.path.join(BASE_DIR, "database.db")}')
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# User model

class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)
da = SessionLocal()
# Login manager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return da.query(User).get(int(user_id))

model_path = os.path.join(BASE_DIR, 'model/converted_keras/keras_model.h5')
labels_path = os.path.join(BASE_DIR, 'model/converted_keras/labels.txt')
labels_list = ["goodbye","hello","help","nice","yes"] # use keys from translations
recognizer = GestureRecognizer(model_path, labels_path, labels_list)

# --- Routes ---
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = da.query(User).filter_by(username=username).first()
        if existing_user:
            flash('Username already exists.')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        da.add(new_user)
        da.commit()
        flash('Account created successfully! Please log in.')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = da.query(User).filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('camera'))
        flash('Invalid username or password.')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/get_prediction')
@login_required
def get_prediction():
    prediction = recognizer.get_prediction()
    return jsonify({'prediction': prediction})

@app.route('/')
@login_required
def camera():
    return render_template('camera.html')

# Load gesture model once
@app.route('/predict', methods=['POST'])
@login_required
def predict():
    data = request.json
    img_data = data['image'].split(',')[1]  # Remove base64 header
    img_bytes = base64.b64decode(img_data)
    np_arr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    label = recognizer.predict_frame(img)
    return jsonify({'prediction': label})

@app.route('/speak', methods=['POST'])
@login_required
def speak():
    data = request.json
    gesture = data['text']
    lang = data['language']
    # Translate text
    translation = translate_gesture(gesture, lang)
    # Generate audio file
    code = LANGUAGE_CODES.get(lang, 'en')
    # Unique filename
    fname = f"audio_{gesture}_{lang}.mp3"
    out_path = os.path.join(BASE_DIR, 'static', 'audio', fname)
    speak_translation(translation, code, out_path)
    # Return translation and URL
    url = url_for('static', filename=f'audio/{fname}')
    return jsonify({'translation': translation, 'audio_url': url})


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
