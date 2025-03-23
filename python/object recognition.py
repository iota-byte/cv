import tensorflow as tf
from tensorflow.python.keras import layers, models
import cv2
import numpy as np
from vgg import vgg_16 as VGG16

# Load the pre-trained VGG16 model without the fully connected layers
base_model = VGG16( include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False

# Add custom fully connected layers
model = models.Sequential([
    base_model,
    layers.Flatten(),
    layers.Dense(512, activation='relu'),
    layers.Dense(256, activation='relu'),
    layers.Dense(10, activation='softmax')  # Assuming 10 classes
])

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Load your trained model weights (if applicable)
# model.load_weights('path_to_your_trained_model.h5')  # Uncomment this if you have pre-trained weights

# Create a dictionary of class labels (update with your own labels)
class_labels = ['Class1', 'Class2', 'Class3', 'Class4', 'Class5', 'Class6', 'Class7', 'Class8', 'Class9', 'Class10']

# Initialize webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # Preprocess the image to fit the input format of VGG16
    image_resized = cv2.resize(frame, (224, 224))  # Resize to 224x224
    image_normalized = image_resized / 255.0  # Normalize pixel values to [0, 1]
    image_expanded = np.expand_dims(image_normalized, axis=0)  # Add batch dimension
    
    # Predict using the model
    predictions = model.predict(image_expanded)
    
    # Get the class with the highest probability
    predicted_class = np.argmax(predictions, axis=1)[0]
    predicted_label = class_labels[predicted_class]
    
    # Display the result on the frame
    cv2.putText(frame, f'Predicted: {predicted_label}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Live Image Classifier', frame)
    
    # Exit loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
