
import streamlit as st
from moviepy.editor import VideoFileClip
import math
import os

def split_video(video_path, segment_length=59):
    video = VideoFileClip(video_path)
    duration = video.duration
    total_segments = math.ceil(duration / segment_length)
    output_files = []
    
    for segment in range(total_segments):
        start_time = segment * segment_length
        end_time = min((segment + 1) * segment_length, duration)
        current_segment = video.subclip(start_time, end_time)
        output_filename = f"temp_video_segment_{segment+1}.mp4"
        current_segment.write_videofile(output_filename, codec="libx264", audio_codec="aac")
        output_files.append(output_filename)
    
    return output_files

st.title('Video Splitter App')

uploaded_file = st.file_uploader("Choose a video file", type=['mp4'])

if uploaded_file is not None:
    file_details = {"FileName":uploaded_file.name, "FileType":uploaded_file.type}
    with open("temp_video.mp4", "wb") as f:
        f.write(uploaded_file.read())
    if st.button('Split Video'):
        output_files = split_video("temp_video.mp4")
        segment_options = {f"Segment {i+1}": filename for i, filename in enumerate(output_files)}
        selected_segment = st.selectbox("Select a video segment to download", options=list(segment_options.keys()))
        download_filename = segment_options[selected_segment]
        
        with open(download_filename, "rb") as file:
            btn = st.download_button(
                label="Download Video Segment",
                data=file,
                file_name=download_filename,
                mime="video/mp4"
            )
        
        # Clean up after downloading
        for file_name in output_files:
            os.remove(file_name)  # Clean up the segment file
        os.remove("temp_video.mp4")  # Clean up the uploaded temporary file
