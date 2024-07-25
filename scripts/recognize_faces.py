from tensorflow.keras.models import load_model
import numpy as np
import cv2
import dlib
from sklearn.metrics.pairwise import cosine_similarity
import sys

# Load FaceNet model
facenet_model = load_model('facenet_keras.h5')

# Load Dlib's face detector and shape predictor
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def preprocess_image(image):
    image = cv2.resize(image, (160, 160))
    image = image.astype('float32')
    mean, std = image.mean(), image.std()
    image = (image - mean) / std
    return image

def get_face_embedding(model, face):
    face = preprocess_image(face)
    face = np.expand_dims(face, axis=0)
    embedding = model.predict(face)
    return embedding

def recognize_faces(image, known_face_embeddings, known_face_names, model):
    faces = detector(image, 1)
    face_embeddings = []

    for face in faces:
        shape = sp(image, face)
        face_chip = dlib.get_face_chip(image, shape, size=160)
        face_embedding = get_face_embedding(model, face_chip)
        face_embeddings.append(face_embedding)

    face_names = []
    for embedding in face_embeddings:
        similarities = cosine_similarity(known_face_embeddings, embedding)
        name = "Unknown"
        if np.max(similarities) > 0.7:  # Similarity threshold
            best_match_index = np.argmax(similarities)
            name = known_face_names[best_match_index]
        face_names.append(name)

    return face_names

if __name__ == "__main__":
    # Load known face embeddings and their corresponding names
    known_face_embeddings = np.load('known_face_embeddings.npy')  # Example file path
    known_face_names = np.load('known_face_names.npy').tolist()  # Example file path

    # Load an image for recognition
    image_path = sys.argv[1]  # Update with a frame image path
    image = cv2.imread(image_path)

    # Recognize faces in the image
    face_names = recognize_faces(image, known_face_embeddings, known_face_names, facenet_model)
    print(face_names)
