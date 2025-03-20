# import streamlit as st
# import requests
# from PIL import Image
# import io

# # FastAPI endpoint
# API_URL = "http://127.0.0.1:8000/detect-faces/"

# # Streamlit app UI
# st.title("Face Detection App using MTCNN (facenet-pytorch)")
# st.write("Upload an image, and the system will detect faces via FastAPI backend.")

# uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# if uploaded_file is not None:
#     # Display uploaded image
#     image = Image.open(uploaded_file)
#     # st.image(image, caption="Uploaded Image", use_column_width=True)

#     # Convert image to bytes
#     img_bytes = io.BytesIO()
#     image.save(img_bytes, format='JPEG')
#     img_bytes.seek(0)

#     # API call button
#     if st.button("Detect Faces"):
#         # Send image to FastAPI
#         files = {'file': (uploaded_file.name, img_bytes, uploaded_file.type)}
#         response = requests.post(API_URL, files=files)

#         if response.status_code == 200:
#             result = response.json()
#             st.success(f"Faces Detected: {result['faces_detected']}")
#             if result['faces_detected'] > 0:
#                 st.write("**Details of Detected Faces:**")
#                 for face in result['details']:
#                     st.write(f"Face ID: {face['face_id']}, "
#                              f"Box Coordinates: {face['box_coordinates']}, "
#                              f"Confidence: {face['confidence']:.4f}")
#             else:
#                 st.warning("No faces detected in the image.")
#         else:
#             st.error("Error in processing the image. Please try again.")
















# import streamlit as st
# import requests
# from PIL import Image
# import io
# import numpy as np
# import cv2

# # FastAPI endpoint
# API_URL = "http://127.0.0.1:8000/detect-faces/"

# # Streamlit app UI
# st.title("Face Detection App using MTCNN (facenet-pytorch)")
# st.write("Upload an image, and the system will detect faces via FastAPI backend.")

# uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# if uploaded_file is not None:
#     # Display uploaded image
#     image = Image.open(uploaded_file)
#     st.image(image, caption="Uploaded Image", use_column_width=True)

#     # Convert PIL Image to bytes
#     img_bytes = io.BytesIO()
#     image.save(img_bytes, format='JPEG')
#     img_bytes.seek(0)

#     # Convert PIL Image to OpenCV format
#     image_cv = np.array(image)  # Convert PIL image to NumPy array (RGB)
#     image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGB2BGR)  # Convert to BGR for OpenCV

#     # API call button
#     if st.button("Detect Faces"):
#         # Send image to FastAPI
#         files = {'file': (uploaded_file.name, img_bytes, uploaded_file.type)}
#         response = requests.post(API_URL, files=files)

#         if response.status_code == 200:
#             result = response.json()
#             st.success(f"Faces Detected: {result['faces_detected']}")

#             if result['faces_detected'] > 0:
#                 st.write("**Details of Detected Faces:**")
#                 for face in result['details']:
#                     x, y, w, h = face['box_coordinates']
                    
#                     # Draw rectangle around face
#                     cv2.rectangle(image_cv, (x, y), (w, h), (0, 255, 0), 2)

#                     st.write(f"Face ID: {face['face_id']}, "
#                              f"Box Coordinates: {face['box_coordinates']}, "
#                              f"Confidence: {face['confidence']:.4f}")

#                 # Convert back to RGB for displaying in Streamlit
#                 image_cv_rgb = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)
#                 st.image(image_cv_rgb, caption="Detected Face", use_column_width=True)

#             else:
#                 st.warning("No faces detected in the image.")
#         else:
#             st.error("Error in processing the image. Please try again.")






























# import streamlit as st
# import requests
# import cv2
# import numpy as np
# import tempfile

# # FastAPI endpoint
# API_URL = "http://127.0.0.1:8000/detect-faces/"

# st.title("Real-Time Face Detection using MTCNN (FastAPI)")

# # Start the webcam
# st.write("Click 'Start Webcam' to begin real-time face detection.")

# # Button to start webcam stream
# if st.button("Start Webcam"):
#     cap = cv2.VideoCapture(0)  # Open webcam
#     stframe = st.empty()  # Create an empty Streamlit frame

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             st.error("Failed to capture frame from webcam.")
#             break

#         # Convert frame to bytes for API request
#         frame = cv2.flip(frame,1)
#         _, img_encoded = cv2.imencode('.jpg', frame)
#         img_bytes = img_encoded.tobytes()

#         # Send frame to FastAPI for face detection
#         files = {'file': ('frame.jpg', img_bytes, 'image/jpeg')}
#         response = requests.post(API_URL, files=files)

#         if response.status_code == 200:
#             result = response.json()

#             # Draw bounding boxes if faces are detected
#             for face in result['details']:
#                 x, y, w, h = face['box_coordinates']
#                 cv2.rectangle(frame, (x, y), (w, h), (0, 255, 0), 2)

#         # Convert frame to RGB (for Streamlit display)
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         stframe.image(frame, channels="RGB", use_container_width=True)

#     cap.release()  # Release webcam when done

































import streamlit as st
import requests
import cv2
import numpy as np

# FastAPI endpoint
API_URL = "http://127.0.0.1:8000/detect-faces/"

st.title("Real-Time Face Detection using MTCNN (FastAPI)")

# Webcam control state
if "run_webcam" not in st.session_state:
    st.session_state.run_webcam = False

# Start webcam button
if st.button("Start Webcam"):
    st.session_state.run_webcam = True

# Stop webcam button
if st.button("Stop Webcam"):
    st.session_state.run_webcam = False

if st.session_state.run_webcam:
    cap = cv2.VideoCapture(0)
    stframe = st.empty()

    while st.session_state.run_webcam:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to capture frame from webcam.")
            break

        frame = cv2.flip(frame, 1)

        # Convert frame to bytes for API request
        _, img_encoded = cv2.imencode('.jpg', frame)
        img_bytes = img_encoded.tobytes()

        # Send frame to FastAPI for face detection
        files = {'file': ('frame.jpg', img_bytes, 'image/jpeg')}
        response = requests.post(API_URL, files=files)

        if response.status_code == 200:
            result = response.json()

            # Draw bounding boxes if faces are detected
            for face in result['details']:
                x, y, w, h = face['box_coordinates']
                cv2.rectangle(frame, (x, y), (w, h), (0, 255, 0), 2)

        # Convert frame to RGB for Streamlit display
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame, channels="RGB", use_container_width=True)

    cap.release()
