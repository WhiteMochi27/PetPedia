import streamlit as st
import cv2
import numpy as np
import PIL.Image
import google.generativeai as genai
import base64
import os
from io import BytesIO

genai.configure(api_key=st.secrets["GeminiAI_API_Key"])

def decode_image(data):
    binary = base64.b64decode(data.split(',')[1])
    img = np.array(PIL.Image.open(BytesIO(binary)))
    return img

def take_photo():
    st.info("Click the button below to take a photo.")
    img_file_buffer = st.camera_input("Take a picture")

    if img_file_buffer is not None:
        image = np.array(PIL.Image.open(img_file_buffer))
        return image

def animal_identification(image):
    model = genai.GenerativeModel(
        "gemini-1.5-flash",
        system_instruction="""
        You are an animal expert that is able to identify the breed and the species of the given image.
        You are also able to give a brief description of the animal. The output must be in the below format:
        Breed: <breed>
        Species: <species>
        Characteristics: <characteristics>
        Diet: <diet>
        Lifespan: <lifespan>
        Habitat: <habitat>
        Description: <description>
        """
    )
    response = model.generate_content(["Identify the breed and the species     of the given image.", image])

    st.image(image, caption="Uploaded Image")
    st.write(response.text)

def main():
    st.title("Animal Identification System")

    st.sidebar.title("Options")
    user_choice = st.sidebar.selectbox("Choose an option", ["Take Photo", "Upload Photo", "Exit"])

    if user_choice == "Take Photo":
        photo = take_photo()
        if photo is not None:
            st.image(photo, caption="Captured Image")
            
            if st.button("Analyze Photo"):
                animal_identification(photo)
            elif st.button("Retake Photo"):
                st.experimental_rerun()
                
    elif user_choice == "Upload Photo":
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
        
        if uploaded_file is not None:
            image = np.array(PIL.Image.open(uploaded_file))
            st.image(image, caption="Uploaded Image")
            
            if st.button("Analyze Uploaded Photo"):
                animal_identification(image)
                
    elif user_choice == "Exit":
        st.write("Exiting...")

if __name__ == "__main__":
    main()
