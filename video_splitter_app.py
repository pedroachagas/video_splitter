import streamlit as st
import math
import os
import subprocess

def cleanup_temp_files():
    """
    Delete temporary files starting with a specific prefix in the given directory.
    """
    for file in os.listdir():
        if file.startswith("temp_video") or file.startswith("temp_video_segment"):
                os.remove(file)

def split_video(video_path, segment_length=59):
    # Use ffmpeg to get the duration of the video
    cmd = ['ffprobe', '-v', 'error', '-show_entries', 
           'format=duration', '-of', 
           'default=noprint_wrappers=1:nokey=1', video_path]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    duration = float(result.stdout)
    total_segments = math.ceil(duration / segment_length)

    output_files = []
    
    st.write(f"Number of segments: {total_segments}")
    progress_bar = st.progress(0)
    
    for segment in range(total_segments):
        start_time = segment * segment_length
        output_filename = f"temp_video_segment_{segment+1}.mp4"
        # Construct ffmpeg command for splitting the video
        cmd = ['ffmpeg', '-y', '-i', video_path, '-ss', str(start_time), '-t', str(segment_length), 
               '-c:v', 'libx264', '-c:a', 'aac', '-strict', '-2', output_filename]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
        
        # Display links or download buttons for the output files
        for file_path in output_files:
            with open(file_path, "rb") as file:
                st.download_button(label=f"Download {os.path.basename(file_path)}",
                                   data=file,
                                   file_name=os.path.basename(file_path),
                                   mime="video/mp4")
