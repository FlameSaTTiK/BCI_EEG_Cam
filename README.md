# Brain Computer Interface (BCI) Visualization Tool

## Overview
This project is a Streamlit-based application that visualizes brain activity data from the BCI Dataset. It provides an interactive interface to explore brain signals related to motor imagery tasks (imagining movements of left hand, right hand, foot, and tongue) and includes a real-time camera-based movement detection system that shows which parts of the brain would be active during physical movements.

## Features
- **Brain Activity Map**: Visualize brain activity across different regions (C3, Cz, C4) using heatmaps
- **Brain Signals Explorer**: Examine detailed brain wave patterns from specific brain regions
- **Movement Detection**: Real-time camera-based detection of body movements with corresponding brain activity visualization
- **Dataset Selection**: Choose from 9 different test subjects' data

## Prerequisites
- Python 3.8 or higher
- Webcam (for Movement Detection feature)
- The dataset files (A01T.npz through A09T.npz) included in the repository

## Project Structure

```
bciIV2a/
 A01T.npz                # Subject 1 training data
 A01E.npz                # Subject 1 evaluation data
 A02T.npz                # Subject 2 training data
 A02E.npz                # Subject 2 evaluation data
 ... (repeated for subjects 3-9)
 app.py                  # Main Streamlit application
 camera_utils.py         # Webcam motion detection logic
 requirements.txt        # Python dependencies
 README.md               # Project documentation
```

Note: Contains 18 dataset files (9 subjects × 2 files each) following naming pattern:
- `A[subject #]T.npz` for training data
- `A[subject #]E.npz` for evaluation data

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/rounakdey2003/CollegeProject.git
   cd CollegeProject/bciIV2a
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Start the Streamlit application:
   ```
   streamlit run app.py
   ```

2. The application will open in your default web browser at `http://localhost:8501`

### Brain Activity Map Tab
This tab displays heatmaps showing brain activity across three key regions:
- **C3** (Left Brain): Controls right side of the body
- **Cz** (Middle Brain): Controls foot and tongue movements
- **C4** (Right Brain): Controls left side of the body

Red colors indicate high brain activity, while blue colors indicate resting state.

### Brain Signals Explorer Tab
This tab allows you to view detailed brain wave patterns from specific brain regions:
1. Select a brain region from the dropdown menu
2. Observe the corresponding brain signal visualization
3. Each bump in the line represents a tiny electrical signal from the brain

### Movement Detection Tab
This tab uses your webcam to detect body movements and shows which parts of your brain would be active during these movements:

1. Click the "Start Camera" button to activate your webcam
2. Move different parts of your body to see real-time brain activity:
   - Left hand movement activates the right side of your brain (C4)
   - Right hand movement activates the left side of your brain (C3)
   - Head movement activates the middle of your brain (Cz)
   - Foot movement activates the middle of your brain (Cz)
3. Observe both the visual representation of brain activity and the corresponding brain signals
4. Click "Stop Camera" when finished

## Dataset Information

This application uses the BCI Dataset, which contains EEG recordings from 9 subjects performing motor imagery tasks. Each subject performed four different motor imagery tasks:
- Imagination of left hand movement
- Imagination of right hand movement
- Imagination of foot movement
- Imagination of tongue movement

The dataset files (A01T.npz through A09T.npz) contain the following data:
- Raw EEG signals
- Event types and positions
- Event durations
- Artifact information

## Technical Details

### Brain Regions
- **C3**: Located on the left side of the brain, primarily controls movement on the right side of the body
- **Cz**: Located in the middle of the brain, involved in foot and tongue movements
- **C4**: Located on the right side of the brain, primarily controls movement on the left side of the body

### Motion Detection
The application uses OpenCV to detect motion through your webcam. It divides the camera view into regions corresponding to different body parts:
- Left side of the screen: Left hand region
- Right side of the screen: Right hand region
- Top center: Head region
- Bottom center: Foot region

When movement is detected in these regions, the application shows which parts of the brain would be active during these movements.

## Troubleshooting

- **Camera not working**: Ensure your webcam is properly connected and not being used by another application
- **Missing dataset files**: Verify that all .npz files are in the project directory
- **Dependency issues**: Make sure all required packages are installed with the correct versions as specified in requirements.txt

## System Architecture

### Application Workflow
```text
Start --> Load Dataset --> [Files Loaded Successfully?]
    Yes --> Process Data --> Select Subject --> Choose Visualization
        |--> Brain Activity Map --> Generate Heatmap --> Display Visualization
        |--> Brain Signals Explorer --> Generate Signal Plot --> Display Visualization
    Display Visualization --> [Change Subject or Visualization?]
        Yes --> Select Subject
        No --> End
    No --> Error --> End

          +-------+
          | Start |
          +-------+
              |
              v
    +-------------------+
    | Load Dataset      |
    | (.npz files)     |
    +-------------------+
              |
              v
    +-------------------+
    | Files Loaded?    |----No----> +-------+
    +-------------------+           | Error |
              | Yes                 +-------+
              v                        |
    +-------------------+              v
    | Process Data      |          +-------+
    | (NumPy)           |--------->| End   |
    +-------------------+          +-------+
              |
              v
    +-------------------+
    | Select Subject    |
    | (1-9)            |
    +-------------------+
              |
              v
    +-------------------+
    | Choose Vis Type?  |----Brain Activity Map----> +-------------------+
    +-------------------+                            | Generate Heatmap  |
              |                                      | (Plotly)          |
              | Brain Signals Explorer               +-------------------+
              v                                                |
    +-------------------+                                      v
    | Generate Signal   |                            +-------------------+
    | Plot (Plotly)     |<---------------------------| Display Vis       |
    +-------------------+                            | (Streamlit)       |
              |                                      +-------------------+
              v                                                |
    +-------------------+                                      v
    | Change Subject/   |----Yes------------------> +-------------------+
    | Visualization?    |                           | Select Subject    |
    +-------------------+                           +-------------------+
              |
              No
              v
          +-------+
          | End   |
          +-------+
```

### System Block Diagram
```text
+--------------------------------+       +-----------------------------+       +-----------------------------+       +-----------------------------+       +-------+
| BCI Competition IV Dataset 2a  | ----> | Data Processing (NumPy)     | ----> | Visualization Engine (Plotly)| ----> | Streamlit Web Interface     | ----> | User  |
| - EEG Data (.npz files)        |       | - Process EEG Signals       |       | - Heatmaps & Signal Plots   |       | - Sidebar & Tabs            |       |       |
| - 9 Subjects, 22 Channels      |       | - Extract Events            |       | - Interactive Visuals       |       | - Brain Activity Map        |       |       |
+--------------------------------+       +-----------------------------+       +-----------------------------+       +-----------------------------+       +-------+
```

## Acknowledgments
- EEG for providing the dataset
- Streamlit for the web application framework
- Plotly for interactive visualizations

## License
This project is part of a college project by Rounak Dey.