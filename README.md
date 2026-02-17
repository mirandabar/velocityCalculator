# velocityCalculator

1) Crear entorno virtual \
`
python3 -m venv .venv
`

2) Activar entorno virtual en Linux \
`
source .venv/bin/activate
`

3) Instalar dependencias necesarias \
`
pip install -r requirements.txt
`

4) Librerías linux\
`
sudo apt-get update && sudo apt-get install -y libgl1-mesa-glx libglib2.0-0` \
`
sudo apt-get install -y libsm6 libxext6 libxrender-dev libgomp1
`

5) Ejecutar proyecto
`
python3 trafficDetection.py 
`