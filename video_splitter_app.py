import streamlit as st
import math
import os
from moviepy.editor import VideoFileClip

def cleanup_temp_files():
    """
    Delete temporary files starting with a specific prefix in the given directory.
    """
    for file in os.listdir():
        if file.startswith("temp_video_segment"):
            os.remove(file)

def split_video(video_path, segment_length=59):
    # Cleanup any previous temporary files
    cleanup_temp_files()
    
    # Use moviepy to get the duration of the video
    video = VideoFileClip(video_path)
    duration = video.duration
    total_segments = math.ceil(duration / segment_length)

    output_files = []
    
    st.write(f"Number of segments: {total_segments}")
    progress_bar = st.progress(0)
    
    for segment in range(total_segments):
        start_time = segment * segment_length
        end_time = min((segment + 1) * segment_length, duration)
        current_segment = video.subclip(start_time, end_time)
        output_filename = f"temp_video_segment_{segment+1}.mp4"
        current_segment.write_videofile(output_filename, codec="libx264", audio_codec="aac")
        output_files.append(output_filename)
        
        progress_bar.progress((segment + 1) / total_segments)
    
    return output_files

st.title('Video Splitter App')

uploaded_file = st.file_uploader("Choose a video file", type=['mp4'])

if uploaded_file is not None:
    video_path = "temp_video.mp4"
    with open(video_path, "wb") as f:
        f.write(uploaded_file.getvalue())  # Use getvalue() for Streamlit's UploadedFile
    
    segment_length = st.number_input('Enter segment length in seconds', min_value=1, value=59)
    
    if st.button('Split Video'):
        output_files = split_video(video_path, segment_length)
        st.session_state.output_files = output_files  # Store output files in session state

# Check if there are any output files stored in session state and create download buttons for them
if 'output_files' in st.session_state:
    for file_path in st.session_state.output_files:
        with open(file_path, "rb") as file:
            st.download_button(label=f"Download {os.path.basename(file_path)}",
                               data=file,
                               file_name=os.path.basename(file_path),
                               mime="video/mp4")
