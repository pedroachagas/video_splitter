import streamlit as st
from moviepy.editor import VideoFileClip
import math
import os

def split_video(video_path, segment_length=59):
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
        # Save the uploaded file temporarily
        with open("temp_video.mp4", "wb") as f:
                f.write(uploaded_file.read())

        segment_length = st.number_input('Enter segment length in seconds', min_value=1, value=59)
        if st.button('Split Video'):
                output_files = split_video("temp_video.mp4", segment_length)
                
                # Store the list of output files in a session state to preserve it across runs
                st.session_state['output_files'] = output_files
                segment_options = [f"Segment {i+1}" for i in range(len(output_files))]
                st.session_state['selected_segment'] = st.selectbox("Select a video segment to download", options=segment_options)

# This part is moved to the end, after the Cleanup button, to ensure logical flow and clarity
if 'output_files' in st.session_state:
    # Ensures the dropdown is only created if there are output files
    segment_options = [f"Segment {i+1}" for i in range(len(st.session_state['output_files']))]
    # Use a unique key for the dropdown to avoid DuplicateWidgetID error
    selected_segment = st.selectbox("Select a video segment to download", options=segment_options, key='unique_segment_selector')

    if 'selected_segment' in st.session_state:
        # Dropdown for selecting segment to download - This line is redundant and removed to avoid confusion
        # selected_segment = st.session_state['selected_segment']
        output_files = st.session_state['output_files']
        download_filename = output_files[int(selected_segment.split()[-1]) - 1]
        
        with open(download_filename, "rb") as file:
            st.download_button(
                label="Download Video Segment",
                data=file,
                file_name=download_filename,
                mime="video/mp4"
            )
