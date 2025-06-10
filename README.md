# Indian Sign Language Recognition Web App

A full-stack web application for real-time **Indian Sign Language (ISL)** gesture recognition using a webcam, with multilingual **text** and **audio** output. Users can sign gestures like "hello", "goodbye", "yes" and receive predictions in **English, Hindi, Gujarati, Tamil, Spanish or German**.

## Features

- Real-time webcam-based gesture recognition
- Teachable Machine-powered gesture model (`keras_model.h5`)
- User authentication (Login/Signup)
- Translate gesture output to multiple languages
- Choose between **text or audio output**
- Clean and intuitive UI 

## Tech Stack

| Layer         | Technology                                |
|---------------|--------------------------------------------|
| Frontend      | HTML, CSS, JavaScript                     |
| Backend       | Python, Flask, Flask-Login                |
| ML Model      | Keras (from Teachable Machine export)     |
| Gesture Logic | `cvzone`, `opencv-python`, `numpy`        |
| Translation   | `translate` library                       |
| Audio Output  | `gTTS` (Google Text-to-Speech)            |

## Supported Gestures

| Gesture            | Predicted Label |
|------------        |-----------------|
| Two finger salute  | `hello`         |
| Wave               | `goodbye`       |
| Fist               | `yes`           |




