CÀI ANACONDA trước khi clone
tải file yolov3.weights vào thư mục gốc project "https://drive.google.com/file/d/1N1s6Xv2H6vph3vi76mU3JJvydnqTqshx/view?usp=sharing"

làm 2 bước sau (bắt buộc):
	kích hoạt môi trường : 'conda activate ./env'
	ktra: 'conda info --envs'

hướng dẫ thêm:
	cài mt từ file environment: 'conda env create -f environment.yml'
	tạo môi trường trong folder: 'conda create --prefix ./env python=3.10'
	tạo môi trường mặc định (trong anaconda): 'conda create --name myenv python=3.10'
	tạo mới file environment: 'conda env export > environment.yml'
	ghi đè: 'conda env export -p ./env > environment.yml'



app.py là stream video lên web

app(arduino).py là chạy local, điều khiển Servo

oldapp.py là code bản cũ (kệ)

creatdb là scrpit chạy 1 lần để tạo database (không chạy lại)