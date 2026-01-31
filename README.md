🔍 TRUESIGHT AI – Suspicious Object Detection System

TRUESIGHT AI is a computer vision–based security system that detects suspicious objects and activities in real time using YOLOv8.
The project combines Artificial Intelligence and Cybersecurity concepts to analyze live camera feeds and identify potential threats such as weapons, unattended luggage, suspects, and victims.

🚀 Features

		Real-time webcam detection
	
		Multi-model YOLOv8 architecture
		
		Detection of:
	  
		  Suspicious luggage
		  
		  Weapons
		  
		  Victims
		  
		  Suspects
			
	  Confidence threshold filtering
		
	  FPS optimization
		
	  Color-coded bounding boxes
		
	  Overlapping box merging (NMS)

🧠 System Architecture

    Webcam Input
         ↓
    YOLOv8 Model
         ↓
    Confidence Filtering
         ↓
    Non-Maximum Suppression
         ↓
    Detection Output

⚙️ Installation

1️⃣ Clone the repository

git clone https://github.com/ALOITH-exe/TRUESIGHT-AI.git
cd TRUESIGHT-AI

2️⃣ Create virtual environment

python3 -m venv venv
source venv/bin/activate

3️⃣ Install dependencies

pip install -r requirements.txt

▶️ Usage

cd gui
python main.py

Press q to quit the webcam feed.

🧪 Models

Two Trained Models are included.

📊 Technologies Used
  
	  Python
	  
	  YOLOv8 (Ultralytics)
	  
	  OpenCV
	  
	  NumPy
	  
	  Kaggle Notebook (Model Training)
	  
	  Roboflow (Dataset Preparation)

🎓 Academic Context

This project was developed as a semester project for the Artificial Intelligence course, focusing on applying deep learning techniques to real-world cybersecurity surveillance scenarios.

🔮 Future Enhancements

	  Video file detection
	  
	  Alert system (email/SMS)
	  
	  Cloud deployment
	  
	  Model fusion into a single unified model
	  
	  Threat severity scoring

👤 Author

ALOITH

Cyber Security Student

Artificial Intelligence & Security Enthusiast
