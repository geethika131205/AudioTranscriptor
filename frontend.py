import streamlit as st
import requests

st.title("🎤 Audio Transcription App")
st.write("Upload an audio file and get the transcribed text.")

uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/mp3")

    if st.button("Transcribe"):
        # Fix: Correct format for sending files in requests.post
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}

        try:
            response = requests.post("http://127.0.0.1:5000/transcribe", files=files)

            if response.status_code == 200:
                transcription = response.json().get("transcription", "")
                st.subheader("Transcription:")
                st.write(transcription)
                st.markdown(
                    f'<a href="http://127.0.0.1:5000/download_transcription" download="transcription.txt">'
                    f'<button style="padding:10px; font-size:16px;">📥 Download Transcription</button></a>',
                    unsafe_allow_html=True
                )
            else:
                st.error(f"Error: {response.json().get('error', 'Unknown error')}")
        except requests.exceptions.ConnectionError:
            st.error("❌ Could not connect to the backend. Make sure Flask is running on port 5000.")
