import os
import time
import random
from pathlib import Path
from typing import Union

os.environ['OPENCV_FFMPEG_LOGLEVEL'] = '-8'  # Delete error messages from ffmpeg in the terminal

import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt 

import cv2
from ultralytics import YOLO

import threading

#Project files
import readConfiguration
from frameWrapper   import FrameWrapper
from frameQueue     import FrameQueue
from frameDispacher import FrameDispatcher

def randomVideo(folder_path, extensions=['.mp4', '.avi', '.mov']):
    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} does not exist or is not a directory.")
        return None

    # Get all files in the directory
    all_files = os.listdir(folder_path)
    
    # Filter valid extensions
    video_files = [f for f in all_files if any(f.lower().endswith(ext) for ext in extensions)]
    
    if not video_files:
        print(f"Error: No video files found in {folder_path} with extensions {extensions}.")
        return None

    # Select a random video file
    random.seed(time.time())   # Seed the random number generator with the current time
    selected_file = random.choice(video_files)
    video_path = os.path.join(folder_path, selected_file)
    
    print(f"Selected video: {selected_file}")
    return video_path

def saveFrame(ret, frame, output_dir):
    if not ret:
        print("Error: No frame to save.")
        return

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"frame_{time.strftime('%Y%m%d_%H%M%S')}.png")
    cv2.imwrite(output_path, frame)
    print(f"Frame saved successfully at: {output_path}")

def videoStats(video_path : Union[str,Path], output_dir : Union[str,Path]):

    if not os.path.isfile(video_path):
        print(f"Error: Video file '{video_path}' not found.")
        return
    
    if output_dir is None or output_dir == '':
        print("Error: Output directory is not specified.")
        return

    print(f"\n--- Reading: {Path(video_path).name} ---")

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Captura as propriedades do vídeo
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"Width x Height: **{frame_width} x {frame_height}** pixels")
    print(f"FPS: **{fps:.2f}**")
    print(f"Total Frames: {total_frames}")
    
    cap.read() #First frame should be avoided because it can be corrupted, so we read it and discard it.
    ret, frame = cap.read()
    
    saveFrame(ret, frame, output_dir)
    
    cap.release()

def isValidConfiguration(*args) -> bool:
    return all(arg is not None for arg in args)

if __name__ == "__main__":
    config_path = Path('configuration.yaml')
    config = readConfiguration.readConfig(config_path=config_path)
    
    video_folder = readConfiguration.getVideoFolder(config)
    output_frames_folder = readConfiguration.getOutputFramesFolder(config)
    max_queue_size = readConfiguration.getMaxQueueSize(config)

    if not isValidConfiguration(video_folder, output_frames_folder, max_queue_size):
        print("Error: Configuration is missing required fields. Please check the configuration file.")
        exit(1)

    #selected_video_path = randomVideo(video_folder)
    selected_video_path = './dataset/video/cctv052x2004080616x00054.avi' 
    videoStats(selected_video_path, output_frames_folder)

    queue     = FrameQueue(max_size=max_queue_size)
    wrapper   = FrameWrapper(video_path=selected_video_path, queue=queue)
    dispacher = FrameDispatcher(queue=queue)

    #Se inicia un paralelizado
    #Hilo 1: Lee el video y llena la cola de frames
    producer_thread = threading.Thread(target=wrapper.readVideo)
    #Hilo 2: Procesa los frames de la cola 
    consumer_thread = threading.Thread(target=dispacher.processFrames)

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()
    