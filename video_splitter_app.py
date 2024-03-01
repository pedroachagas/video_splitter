from moviepy.editor import VideoFileClip
import streamlit as st
import math
import os

# Use a unique session identifier if needed
session_id = st.session_state.get('session_id', None)
if session_id is None:
    import uuid
    session_id = str(uuid.uuid4())
    st.session_state['session_id'] = session_id

def cleanup_temp_files(prefix):
    """
    Delete temporary files starting with a specific prefix in the given directory.
    """
    for file in os.listdir():
        if file.startswith(prefix):
            os.remove(file)

@st.cache_data(persist=True, show_spinner=True)
def split_video(video_path, segment_length=59):
    prefix = f"temp_video_segment_{session_id}_"
    cleanup_temp_files(prefix)
    
    video = VideoFileClip(video_path)
    duration = video.duration
    total_segments = math.ceil(duration / segment_length)

    output_files = []
    
    for segment in range(total_segments):
        start_time = segment * segment_length
        end_time = min((segment + 1) * segment_length, duration)
        current_segment = video.subclip(start_time, end_time)
        output_filename = f"{prefix}{segment+1}.mp4"
        current_segment.write_videofile(output_filename, codec="libx264", audio_codec="aac")
        output_files.append(output_filename)
    
    return output_files

st.title('Video Splitter App')

uploaded_file = st.file_uploader("Choose a video file", type=['mp4'])

if uploaded_file is not None:
    video_path = f"temp_video_{session_id}.mp4"
    with open(video_path, "wb") as f:
        f.write(uploaded_file.getvalue())
    
    segment_length = st.number_input('Enter segment length in seconds', min_value=1, value=59)
    
    if st.button('Split Video'):
        output_files = split_video(video_path, segment_length)
        st.session_state['output_files'] = output_files

if 'output_files' in st.session_state:
    st.divider()
    st.subheader('Download Segments')
    for file_path in st.session_state['output_files']:
        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                st.download_button(label=f"Download {os.path.basename(file_path)}",
                                   data=file,
                                   file_name=os.path.basename(file_path),
                                   mime="video/mp4")
        else:
            st.error("File does not exist. Please try splitting the video again.")
