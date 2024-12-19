# AI-Based Intrusion Detection System (IDS)

This project uses machine learning to build an Intrusion Detection System (IDS) using the NSL-KDD dataset.

## Directory Structure
AI_IDS_Project/
├── data/                   # Contains NSL-KDD dataset
│   ├── KDDTrain+.csv       # Converted ARFF to CSV
│   ├── KDDTest+.csv
├── scripts/                # Contains Python scripts
│   ├── ids_model.py        # Main IDS code
│   ├── preprocess.py       # Preprocessing code
├── README.md               # Project description
├── requirements.txt        # Python dependencies
└── LICENSE                 # License file


## Features
- Preprocessing NSL-KDD dataset
- Training and evaluating an Isolation Forest model
- Visualizing anomalies in network traffic

## Installation
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Convert ARFF files to CSV using `scripts/preprocess.py`.

## Usage
Run the IDS model:
```bash
python scripts/ids_model.py

