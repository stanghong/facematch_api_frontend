import streamlit as st
import requests
from PIL import Image as PILImage
from io import BytesIO
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables
_ = load_dotenv(find_dotenv())
API_URL = os.getenv('API_URL', 'http://facematchapi-production.up.railway.app/api/face_match_api/')

def main():
    # Streamlit UI components
    st.title("Face Match: Your Pixar-Style Avatar")

    # Initialize session state for the API response data
    if 'input_image_url' not in st.session_state:
        st.session_state['input_image_url'] = None
    if 'output_image_url' not in st.session_state:
        st.session_state['output_image_url'] = None
    if 'description' not in st.session_state:
        st.session_state['description'] = ""
    if 'chinese_description' not in st.session_state:
        st.session_state['chinese_description'] = ""

    # Image uploader
    uploaded_image = st.file_uploader("Upload your photo", type=["jpg", "jpeg", "png"])

    # Check if an image has been uploaded
    if uploaded_image:
        # Display the uploaded image
        image = PILImage.open(uploaded_image)
        st.image(image, caption='Your Photo')

        # Button to send the image to the API
        if st.button("Generate Pixar Avatar"):
            try:
                # Convert the image to RGB format
                image = image.convert('RGB')

                # Resize the image if needed
                max_size = (2048, 2048)
                image.thumbnail(max_size)

                # Save the image to a BytesIO object
                buffer = BytesIO()
                image.save(buffer, format="JPEG")
                buffer.seek(0)

                # Prepare the file for the API request
                files = {'image': (uploaded_image.name, buffer, 'image/jpeg')}
                
                # Send the request to the API
                response = requests.post(API_URL, files=files)

                # Check the status and process the response
                if response.status_code == 200:
                    data = response.json()
                    st.session_state['input_image_url'] = data.get('image_url', 'No URL available')
                    st.session_state['output_image_url'] = data.get('output_image_url', 'No URL available')
                    st.session_state['description'] = data.get('description', 'No description available')
                    st.session_state['chinese_description'] = data.get('chinese_description', 'No translation available')
                    st.success("Image processed successfully!")
                else:
                    st.error(f"Server returned an error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Failed to process image: {str(e)}")

    # Display the results if available
    if st.session_state['description']:
        st.markdown("### Description")
        st.write(st.session_state['description'])
        
    if st.session_state['chinese_description']:
        st.markdown("### Chinese Translation")
        st.write(st.session_state['chinese_description'])

    if st.session_state['output_image_url']:
        st.markdown("### Your Pixar Avatar")
        # Display the generated image directly
        try:
            response = requests.get(st.session_state['output_image_url'])
            if response.status_code == 200:
                output_image = PILImage.open(BytesIO(response.content))
                st.image(output_image, caption='Generated Pixar Avatar')
            else:
                st.error(f"Failed to load generated image: {response.status_code}")
        except Exception as e:
            st.error(f"Error displaying generated image: {str(e)}")

if __name__ == "__main__":
    main()
