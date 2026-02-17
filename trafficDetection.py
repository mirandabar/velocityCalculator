import cv2
import numpy as np
import os
import random
from pathlib import Path
import csv
import pandas as pd
import matplotlib.pyplot as plt 
import time
from ultralytics import YOLO

VIDEO_FOLDER = './dataset/video' 

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
    seconds = time.time()  # Get current time in seconds
    random.seed(seconds)   # Seed the random number generator with the current time
    selected_file = random.choice(video_files)
    video_path = os.path.join(folder_path, selected_file)
    
    print(f"Selected video: {selected_file}")
    return video_path

def videoStats(video_path):
    
    if video_path is None:
        return

    print(f"\n--- Verificando o arquivo: {Path(video_path).name} ---")

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("❌ ERRO: Não foi possível abrir o vídeo (verifique o formato/codec).")
        return

    # Captura as propriedades do vídeo
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"Dimensões (Largura x Altura): **{frame_width} x {frame_height}** pixels")
    print(f"FPS (Frames por Segundo): **{fps:.2f}**")
    print(f"Total de Quadros: {total_frames}")
    
    # Leitura do primeiro quadro
    ret, frame = cap.read()
    
    # Leitura do segundo quadro
    ret, second_frame = cap.read()

    ret, third_frame = cap.read()
    if ret:
        print(f"✅ Primeiro quadro lido com sucesso! Formato: {frame.shape}")
        
        # Cria a pasta de saída e define o caminho do arquivo
        output_dir = "frames_de_teste"
        os.makedirs(output_dir, exist_ok=True)
        
        video_name = Path(video_path).stem
        output_path = os.path.join(output_dir, f"{video_name}_primeiro_quadro.png")
        
        # Salva o frame
        cv2.imwrite(output_path, second_frame)
        print(f"🖼️ Quadro salvo com sucesso em: **{output_path}**")

    else:
        print("❌ ERRO: Não foi possível ler o primeiro quadro do vídeo.")
    
    cap.release()
    print("------------------------------------------------")


if __name__ == "__main__":
    #selected_video_path = randomVideo(VIDEO_FOLDER)
    selected_video_path = './dataset/video/cctv052x2004080616x00054.avi'  # Caminho fixo para teste
    videoStats(selected_video_path)