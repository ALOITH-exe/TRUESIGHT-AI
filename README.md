🔍 TRUESIGHT AI – Suspicious Object Detection System

TRUESIGHT AI is a computer vision–based security system that detects suspicious objects and activities in real time using YOLOv8.
The project combines Artificial Intelligence and Cybersecurity concepts to analyze live camera feeds and identify potential threats such as weapons, unattended luggage, suspects, and victims.

Features

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
  
  Modular and scalable design

🧠 System Architecture
      Webcam Input
           ↓
      Multiple YOLOv8 Models
           ↓
      Confidence Filtering
           ↓
      Non-Maximum Suppression
           ↓
      Unified Detection Output

📁 Project Structure
TRUESIGHT_AI/
├── src/                 # Detection scripts
├── data/                # Sample test images
├── models/              # Trained YOLOv8 models (not included)
├── results/             # Output results
├── requirements.txt
└── README.md

⚙️ Installation
1️⃣ Clone the repository
git clone https://github.com/YOUR_USERNAME/TRUESIGHT-AI.git
cd TRUESIGHT-AI

2️⃣ Create virtual environment
python3 -m venv venv
source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

▶️ Usage
Live Webcam Detection (Optimized Multi-Model)
cd src
python detect_webcam_multi_opt_nms.py

Press q to quit the webcam feed.

🧪 Models

Trained YOLOv8 models are not included due to size constraints.
Place your trained .pt files inside the models/ directory.

📊 Technologies Used

  Python
  
  YOLOv8 (Ultralytics)
  
  OpenCV
  
  NumPy
  
  Google Colab (Model Training)
  
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
