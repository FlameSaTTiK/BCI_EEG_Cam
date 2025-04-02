# Brain Computer Interface (BCI) Visualization

This project provides an interactive visualization platform for Brain-Computer Interface (BCI) data using the BCI Competition IV Dataset 2a. It allows users to explore and analyze motor imagery signals through an intuitive web interface built with Streamlit.

## Features

- **Brain Activity Map**: Visualize brain activity across different regions (C3, Cz, C4) using interactive heatmaps
- **Brain Signals Explorer**: Analyze individual brain wave patterns for different motor imagery tasks
- **Multiple Subject Analysis**: Support for data from 9 different test subjects
- **Real-time Signal Visualization**: Interactive plots powered by Plotly

## Installation

1. Clone the repository or download the project files
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
2. Open your web browser and navigate to the provided local URL
3. Use the sidebar to select different test subjects
4. Explore different visualizations through the available tabs:
   - Brain Activity Map
   - Brain Signals Explorer
   - Documentation

## Dataset Information

The BCI Competition IV Dataset 2a consists of EEG data from 9 subjects performing four different motor imagery tasks:
- Left hand movement
- Right hand movement
- Both feet movement
- Tongue movement

Key dataset characteristics:
- 22 EEG channels
- 3 EOG channels
- 288 trials per subject
- 250Hz sampling rate

### Channel Information

- **C3**: Left hemisphere (right body control)
- **Cz**: Central area (feet and tongue movement)
- **C4**: Right hemisphere (left body control)

## Implementation Details

The application is built using:
- **Streamlit**: Web interface and interactive components
- **NumPy**: Data processing and manipulation
- **Plotly**: Interactive visualizations and heatmaps
- **PIL**: Image handling

## File Structure

```
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── bciIV2a.zip        # Dataset archive
├── desc_2a.pdf        # Dataset description
├── event_table.png    # Event code reference
├── mi_paradigm.png    # Motor imagery paradigm
└── A0[1-9][T/E].npz  # Subject data files
```

## Data Processing

The application processes the .npz files which contain:
- Raw EEG signals
- Event types and positions
- Event durations
- Artifact information

Event codes:
- 768: Trial Start
- 769: Left Hand
- 770: Right Hand
- 771: Foot
- 772: Tongue
