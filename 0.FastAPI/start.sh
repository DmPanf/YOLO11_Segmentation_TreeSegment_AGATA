#@title start.sh
pip3 install -q fastapi
pip3 install -q uvicorn
pip3 install -q python-multipart
pip3 install -q opencv-python
pip3 install -q Pillow numpy

mkdir 0_fastapi && cd 0_fastapi/
nano app.py

nohup uvicorn app:app --host 0.0.0.0 --port 8001 --reload &
