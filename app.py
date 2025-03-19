import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from PIL import Image
import base64
from io import BytesIO

class MotorImageryDataset:
    def __init__(self, dataset='A01T.npz'):
        if not dataset.endswith('.npz'):
            dataset += '.npz'

        self.data = np.load(dataset)
        self.Fs = 250  # 250Hz from original paper
        self.raw = self.data['s'].T
        self.events_type = self.data['etyp'].T
        self.events_position = self.data['epos'].T
        self.events_duration = self.data['edur'].T
        self.artifacts = self.data['artifacts'].T

        # Types of motor imagery
        self.mi_types = {769: 'left', 770: 'right',
                        771: 'foot', 772: 'tongue', 783: 'unknown'}

    def get_trials_from_channel(self, channel=7):
        startrial_code = 768
        starttrial_events = self.events_type == startrial_code
        idxs = [i for i, x in enumerate(starttrial_events[0]) if x]

        trials = []
        classes = []

        for index in idxs:
            try:
                type_e = self.events_type[0, index+1]
                class_e = self.mi_types[type_e]
                classes.append(class_e)

                start = self.events_position[0, index]
                stop = start + self.events_duration[0, index]
                trial = self.raw[channel, start:stop]
                trial = trial.reshape((1, -1))
                trials.append(trial)

            except:
                continue

        return trials, classes

    def get_trials_from_channels(self, channels=[7, 9, 11]):
        trials_c = []
        classes_c = []
        for c in channels:
            t, c = self.get_trials_from_channel(channel=c)
            tt = np.concatenate(t, axis=0)
            trials_c.append(tt)
            classes_c.append(c)

        return trials_c, classes_c


st.set_page_config(page_title="BCI", layout="wide")


st.markdown("<h1 style='text-align: center;'>Brain Computer Interection (BCI)</h1>", unsafe_allow_html=True)

st.sidebar.title("Control Panel")
subject = st.sidebar.selectbox(
    "Choose test subject",
    [f"A0{i}T" for i in range(1, 10)]
)

with open(f"{subject}.npz", "rb") as file:
    btn = st.sidebar.download_button(
        label="Download",
        data=file,
        file_name=f"{subject}.npz",
        mime="application/x-npz",
        type="primary"
    )


st.sidebar.divider()
st.sidebar.markdown("""More Projects on [GitHub](https://github.com/rounakdey2003)""")

with st.container(border=True):
    st.markdown("""
    ### Note
    - LEFT hand     (C4)
    - RIGHT hand    (C3)
    - FOOT & TONGUE (Cz)

    """)


dataset = MotorImageryDataset(subject)
trials, classes = dataset.get_trials_from_channels([7, 9, 11])

tab1, tab2, tab3 = st.tabs(["Brain Activity Map", "Brain Signals Explorer", "Readme"])

with tab1:
    with st.container(border=True):
        st.markdown("""
        ### Explaination
        - :red[**Red colors**]: Brain is very active
        - :blue[**Blue colors**]: Brain is resting

        - **Brain Part**:
            - **C3**: Left side of the brain (helps control right side of body)
            - **Cz**: Middle of the brain (helps with foot and tongue movements)
            - **C4**: Right side of the brain (helps control left side of body)
        """)
    with st.container(border=True):
        fig = make_subplots(rows=3, cols=1, 
                            subplot_titles=('Left Brain (C3)', 'Middle Brain (Cz)', 'Right Brain (C4)'),
                            vertical_spacing=0.15)

        for i, (trial, title) in enumerate(zip(trials, ['C3', 'Cz', 'C4'])):
            fig.add_trace(
                go.Heatmap(
                    z=trial,
                    showscale=(i == 0),
                    colorscale='RdBu',
                    name=title
                ),
                row=i+1, col=1
            )

        fig.update_layout(
            height=900,
            width=800,
            title_text=f"Activity Monitor",
            showlegend=False,
            font=dict(size=14)
        )

        st.plotly_chart(fig, use_container_width=True)

with tab2:
    with st.container(border=True):
        st.markdown("""
        ### Explaination
        - Each bump in the line means brain sending a tiny electrical signal
        - When the line goes up and down a lot, means brain is very active
        - When the line is flatter, means brain is more relaxed
        """)
    with st.container(border=True):
        selected_channel = st.selectbox(
            "Choose brain part",
            ["Left Brain (C3)", "Middle Brain (Cz)", "Right Brain (C4)"]
        )
        
        channel_idx = {'Left Brain (C3)': 0, 'Middle Brain (Cz)': 1, 'Right Brain (C4)': 2}
        

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            y=trials[channel_idx[selected_channel]][0],
            mode='lines',
            name='Brain Signal',
            line=dict(color='#2E86C1', width=2)
        ))
        
        fig2.update_layout(
            title=f"Brain Waves from {selected_channel}",
            yaxis_title="Signal Strength",
            xaxis_title="Time",
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    
with tab3:
    st.markdown("""
    ### BCI Competition Dataset IV 2a
        This is a repository for BCI Competition 2008 dataset IV 2a fixed and optimized for python and numpy. 
        This dataset is related with motor imagery. That is only a "port" of the original dataset, 
        Used the original GDF files and extract the signals and events.
    """)

    st.markdown("""<h3 style='text-align: center;'>Research Paper</h3>""", unsafe_allow_html=True)
    
   
    with st.container():
       
        st.markdown(
            """
            <style>
                .pdf-container {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    width: 100%;
                }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        pdf_file_path = "desc_2a.pdf"
        
        try:
            with open(pdf_file_path, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            
            pdf_display = f"""
            <div class="pdf-container">
                <iframe 
                    src="data:application/pdf;base64,{base64_pdf}" 
                    width="700" 
                    height="700" 
                    style="border:none; margin:auto;"
                ></iframe>
            </div>
            """
            st.markdown(pdf_display, unsafe_allow_html=True)
            
        except FileNotFoundError:
            st.error("PDF file not found. Please check if the file exists in the correct location.")
        except Exception as e:
            st.error(f"Error displaying PDF: {str(e)}")


    st.write("##")       
    
    with st.container(border=True):  
        st.markdown("""

        ## How to use

        In that paper the authors explain the adquisition process. 
        The dataset contain data about motor imagery of four different motor imagery tasks, 
        namely the imagination of movement of the left hand (class 1),right hand (class 2), both feet (class 3), and tongue (class 4).

        The form of each motor imagery task is like the figure below.
        """)

    
        try:
            image = Image.open("mi_paradigm.png")
            st.image(image, caption="Motor Imagery Paradigm")
        except FileNotFoundError:
            st.error("Image 'mi_paradigm.png' not found. Please check if the file exists.")
        except Exception as e:
            st.error(f"Error displaying image: {str(e)}")


        st.markdown("""
        Exist 9 subjects and for each subject one run that consists of 48 trials (12 for each of the four possible classes), yielding a total of 288 trials per session.

        Each event (e.g. Start of Trial) is coded using the below table.
        """)

        try:
            image = Image.open("event_table.png")
            st.image(image, caption="Event Code Table", width=700)
        except FileNotFoundError:
            st.error("Image 'event_table.png' not found. Please check if the file exists.")
        except Exception as e:
            st.error(f"Error displaying image: {str(e)}")


        st.markdown("""

        ### About this work

        The current fileformat of these files are ".npz". Below you can see an example.

        ```python
        import numpy as np
        data = np.load('A01T.npz')  # to load the data of the subject 1
        ```

        The names convention used for each datafile:

        -   's': contains all the raw data in a numpy array format.
        -   'etyp': have all the events and its determinated type.
        -   'epos': contains all the events position and its index is related with etyp and edur.
        -   'edur': contains all the events duration.


        ```python
        from matplotlib import pyplot as plt
        import numpy as np
        data = np.load('A01T.npz')  # contains the data of the subject 1
        signal = data['s']
        # The index 7 represent the channel C3, for the info of each channel read the original paper.
        channelC3 = signal[:, 7]

        x = 7  # this is the event number

        # Extract the type of the event 7, in this case the type is 768 (in the table this is a Start of a trial event).
        etype = data['etyp'].T[0, x]
        # This is the position of the event in the raw signal
        epos = data['epos'].T[0, x]
        edur = data['edur'].T[0, x]  # And this is the duration of this event

        # Then extract the signal related the event selected.
        trial = channelC3[epos:epos+edur]

        # The selected event type is 768 (Start of a trial) , see the array of event types ('etype')
        # observe the next event is 772 (Cue onset tongue) with that deduce the class of
        # this trial: Tongue Imagery Task.

        # Then for the class of this trial (7), need to read the type of the inmediate next event
        trial_type = data['etyp'].T[0, x+1]

        # For the order of this events, see the data['etyp'] array.

        # plot this event with matplotlib (or plotly to make interactive)
        plt.plot(trial)
        plt.show()
        ```

        The result of this code is the plot of the one trial.

        ### Complex example

        Create a class with a method for extract all trials of one subject (AT01 in the example). Note that try catch is here because some trial have a reject event, then with this try/catch, select only valid trials.

        ```python
        class MotorImageryDataset:
            def __init__(self, dataset='A01T.npz'):
                if not dataset.endswith('.npz'):
                    dataset += '.npz'

                self.data = np.load('A01T.npz')

                self.Fs = 250 # 250Hz from original paper

                # keys of data ['s', 'etyp', 'epos', 'edur', 'artifacts']

                self.raw = self.data['s'].T
                self.events_type = self.data['etyp'].T
                self.events_position = self.data['epos'].T
                self.events_duration = self.data['edur'].T
                self.artifacts = self.data['artifacts'].T

                # Types of motor imagery
                self.mi_types = {769: 'left', 770: 'right', 771: 'foot', 772: 'tongue', 783: 'unknown'}

            def get_trials_from_channel(self, channel=7):

                # Channel default is C3

                startrial_code = 768
                starttrial_events = self.events_type == startrial_code
                idxs = [i for i, x in enumerate(starttrial_events[0]) if x]

                trials = []
                classes = []
                for index in idxs:
                    try:
                        type_e = self.events_type[0, index+1]
                        class_e = self.mi_types[type_e]
                        classes.append(class_e)

                        start = self.events_position[0, index]
                        stop = start + self.events_duration[0, index]
                        trial = self.raw[channel, start:stop]
                        trials.append(trial)

                    except:
                        continue

                return trials, classes

        datasetA1 = MotorImageryDataset()
        trials, classes = datasetA1.get_trials_from_channel()
        # trials contains the N valid trials, and clases its related class.
        ```
        """)
