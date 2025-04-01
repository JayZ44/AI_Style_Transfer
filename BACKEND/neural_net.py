import librosa
import librosa.display
import numpy as np
import os
import tensorflow as tf

DATASET_PATH = "/Users/jay/Downloads/Data/genres_original"  # Change this to the correct path
print(os.path.abspath("my_model.h5"))

def extract_features(file_path, max_pad_len=128):
    """Extracts MFCC features from an audio file."""
    try:
        audio, sample_rate = librosa.load(file_path, res_type='kaiser_fast')
        mfcc = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
        
        # Pad or truncate MFCC to ensure consistent input size
        if mfcc.shape[1] < max_pad_len:
            pad_width = max_pad_len - mfcc.shape[1]
            mfcc = np.pad(mfcc, pad_width=((0, 0), (0, pad_width)), mode='constant')
        else:
            mfcc = mfcc[:, :max_pad_len]

        return mfcc
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

# Initialize X and y outside the function
X, y = [], []
genres = os.listdir(DATASET_PATH)

for genre in genres:
    genre_path = os.path.join(DATASET_PATH, genre)
    if not os.path.isdir(genre_path):
        continue  # Skip if not a directory
    for file in os.listdir(genre_path):
        file_path = os.path.join(genre_path, file)
        features = extract_features(file_path)
        if features is not None:
            X.append(features)
            y.append(genre)

X = np.array(X)
y = np.array(y)

# Encode labels numerically
from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()
y = encoder.fit_transform(y)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.regularizers import l2

# Reshape X for CNN input
X = X[..., np.newaxis]  # Add channel dimension

# Define and compile the model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=X.shape[1:], kernel_regularizer=l2(0.0001)),
    MaxPooling2D(2, 2),
    Dropout(0.1),  # Reduced dropout rate
    Conv2D(64, (3, 3), activation='relu', kernel_regularizer=l2(0.01)),
    MaxPooling2D(2, 2),
    Dropout(0.2),  # Reduced dropout rate
    Flatten(),
    Dense(64, activation='relu', kernel_regularizer=l2(0.01)),
    Dropout(0.3),  # Reduced dropout rate
    Dense(len(genres), activation='softmax')  # Output layer with number of genres
])

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X, y, epochs=100, validation_split=0.2)

# Predict and print the label for each file
for genre in genres:
    genre_path = os.path.join(DATASET_PATH, genre)
    if not os.path.isdir(genre_path):
        continue  # Skip if not a directory
    for file in os.listdir(genre_path):
        file_path = os.path.join(genre_path, file)
        features = extract_features(file_path)
        if features is not None:
            features_reshaped = features[np.newaxis, ..., np.newaxis]  # Reshape for prediction
            prediction = model.predict(features_reshaped)
            predicted_label = encoder.inverse_transform([np.argmax(prediction)])
            
            # Print the file and its predicted label
            print(f"File: {file}, Predicted Label: {predicted_label[0]}")

model.save('my_model.keras')