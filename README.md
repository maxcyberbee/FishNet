# FishNet
FishNet is a deep learning project designed to identify invasive fish species in the Mediterranean Sea using video data. This project utilizes a YOLO model trained on a custom dataset created from video footage.
Table of Contents
Project Overview
Features
Installation
Usage
Dataset
Model Training
Real-Time Detection
Contributing
License
Acknowledgements
Project Overview
FishNet aims to assist in the early detection and monitoring of invasive fish species. The application processes video frames in real-time, identifies different fish species, and alerts relevant stakeholders when invasive species are detected.

Features
Real-time fish species detection
Alerts and notifications for invasive species
Data logging for further analysis
User-friendly interface for fishermen and researchers
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/FishNet.git
cd FishNet
Create a virtual environment:

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
Download the pre-trained YOLO model weights and place them in the weights directory.

Usage
Running the Application
Start the application:

bash
Copy code
python app.py
Access the application via your web browser at http://localhost:5000.

Processing Video Data
Place your video files in the data/videos directory.

Run the video processing script:

bash
Copy code
python process_videos.py
The results will be saved in the output directory, with logs and detected species.

Dataset
The dataset used for training the model consists of frames extracted from video footage, annotated with bounding boxes for different fish species. The dataset is divided into training, validation, and test sets.

Model Training
To train the YOLO model, follow these steps:

Prepare your dataset and ensure it is correctly formatted for YOLO.

Modify the configuration files as needed.

Train the model:

bash
Copy code
python train.py --data data.yaml --cfg yolov5.yaml --weights yolov5s.pt
Monitor the training process and adjust hyperparameters if necessary.

Real-Time Detection
To enable real-time detection, the application processes video streams frame by frame, using the trained YOLO model to identify fish species. Alerts are generated when invasive species are detected.

Contributing
Contributions are welcome! Please follow these steps to contribute:

Fork the repository.
Create a new branch (git checkout -b feature/your-feature-name).
Make your changes.
Commit your changes (git commit -m 'Add your feature').
Push to the branch (git push origin feature/your-feature-name).
Create a new Pull Request.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgements
Special thanks to the School of Zoology for providing the video data.
Thanks to the open-source community for tools and resources.
