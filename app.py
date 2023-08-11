import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
from PIL import Image
import requests
from pydub import AudioSegment
import numpy as np
from scipy.io.wavfile import write
from io import BytesIO
import pandas as pd
import openpyxl
import math
import streamlit_authenticator as stauth
from database import fetch_users

st.set_page_config(page_title="THE SOFT DRINK", page_icon=':computer:', layout= 'wide')

#---USER AUTHENTICATION---
users = fetch_users()
emails = [user['key'] for user in users]
usernames = [user['username'] for user in users]
passwords = [user['password'] for user in users]
ld, cd, rd = st.columns(3)
with cd:
    authenticator = stauth.Authenticate(emails, usernames, passwords, cookie_name="students", key="qwerty", cookie_expiry_days=1,)
    email, authentication_status, username = authenticator.login("THE SOFT DRINK STUDIOS 🎵", "main")


if username:

    if username in usernames:

        if authentication_status: 

            st.balloons()
            
            @st.cache_data   #Lottie Cache Setup
            def load_lottieurl(url):
                r = requests.get(url)
                if r.status_code != 200:
                    return  None
                return r.json()
            
            @st.cache_data   #Image Cache Setup
            def load_image(filename):
                l_img = Image.open(filename)
                return (l_img)

            @st.cache_data
            def generate_sound(frequency, duration, sample_rate):  #frequency sound geerator generator
                t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
                audio_data = np.sin(2 * np.pi * frequency * t)
                audio_data *= 32767 / np.max(np.abs(audio_data))
                audio_data = audio_data.astype(np.int16)

                # Create a BytesIO object to hold the audio data
                audio_stream = BytesIO()
                write(audio_stream, sample_rate, audio_data)

                # Reset the stream position to the beginning
                audio_stream.seek(0)

                # Create an AudioSegment from the in-memory audio data
                sound = AudioSegment.from_file(audio_stream, format="wav")
                return sound

            @st.cache_data
            def wavcal(fcq):
                wvl = 343/fcq 
                return wvl

            @st.cache_data
            def freqcal(w_l):
                f_l = 343/w_l
                return f_l

            @st.cache_data
            def ampcal(apt):
                apt0 = 20 # Reference amplitude in micropascals
                lvl = 20*math.log10(apt/apt0)
                return lvl

            lj,rj = st.columns((0.1,1))
            with rj:
                st.title('BASICS OF AUDIO ENGINEERING')
            lcl, rcl = st.columns((2,1))
            with rcl:
                st.write('***A course by Aakarshan Dutta***')


            with st.sidebar:
                c1,c2 = st.columns((0.5,2))
                with c1:
                    l_img = load_image("Images/logo.png")
                    st.image(l_img, width=65)
                with c2:
                    st.title("The Soft Drink Studios")
                h1,h2= st.columns((2,1))
                with h2:
                    authenticator.logout("👤Logout")
                with h1:
                    st.title("🎉 WELCOME 🎊")
                
                selected =  option_menu(
                    menu_title = f"{username} 🎧🎶🎤",
                    options = ["Introduction","Properties of Sound", "Acoustic Properties", "Equipments & Gears", "DAW"],
                    menu_icon = "cassette-fill"
                    )

            if selected == "Introduction":
                st.write("---")
                lcl, mcl, rcl = st.columns(3)
                with mcl:
                    st.header("INTRODUCTION")
                l_col, r_col = st.columns((2,1))
                with l_col:
                    with st.container():
                        st.write("##")
                        st.subheader("**What is Audio Engineering?**")
                        st.write("""
                        Audio Engineering is the art and science of recording, mixing, and manipulating sound. It encompasses the technical expertise required to capture and enhance audio quality in various media, including music, film, and broadcasting. Audio engineers utilize specialized equipment and techniques to create immersive and captivating sonic experiences.
                        """)
                        st.write('**Examples**')
                        st.write("""
                        1. Audio Recording
                        2. Dubbing for Film & Television
                        3. Audio Editing (Radio Edits, podcast,etc.)
                        4. Audio Post Production (Mixing & Mastering)
                        5. Music Production
                        6. Broadcasting
                        7. BGM (Background Music)
                        """)
                with r_col:
                    lottie1 = load_lottieurl('https://assets5.lottiefiles.com/packages/lf20_uv2O8HvO2x.json')
                    lottie2 = load_lottieurl('https://assets5.lottiefiles.com/packages/lf20_l8la4vrlSt.json')
                    st_lottie(lottie1, key= 'aud1')
                    st_lottie(lottie2, key= 'mic')
            
                st.write("##")
                st.subheader('SOUND/AUDIO')
                st.write("""
                        Sound or Audio can be defined as a form of energy that is transmitted through vibrations or waves in a medium, typically air. These vibrations create variations in pressure that our ears perceive as sound. Sound is characterized by properties such as frequency (pitch), amplitude (volume), and timbre (tone quality). It serves as a means of communication and plays a fundamental role in our daily lives, encompassing a wide range of audible phenomena, from music and speech to environmental noises."""
                        )
                st.write('**In Short:** Any object or material which vibrates and creates a difference in air pressure which can be heard or felt is called **SOUND**.')
                st.write("##")
                l_img = load_image("Images/Sound1.png")
                st.image(l_img)
                st.write("##")
                st.subheader("Audio Signal")
                st.write("""
                        An audio signal is a representation of sound in an electrical or digital form. It carries information about the changes in air pressure that create sound waves, and it can be processed, transmitted, and reproduced using electronic or digital devices.
                        """)
                st.write("**EXAMPLES**")
                st.write("""
                        1. **Acoustic Audio Signal:** An acoustic audio signal is the original, natural form of sound waves traveling through the air. It is the sound produced by musical instruments, human voices, or any sound source without any electronic or digital processing. For example, the sound of a guitar being played, a singer's voice, or the sound of clapping hands.

            2. **Analog Audio Signal:** An analog audio signal is represented by continuous electrical voltage fluctuations. It is the type of signal found in traditional audio equipment like vinyl record players, cassette players, and analog tape recorders. The voltage variations directly correspond to the changes in the sound wave. For example, the signal from a turntable playing a vinyl record.

            3. **Digital Audio Signal:** A digital audio signal is represented as a sequence of discrete numerical values. It is commonly used in modern audio devices like CDs, MP3 players, and streaming services. Sound waves are sampled at regular intervals, and each sample is assigned a numerical value, creating a digital representation of the audio. For example, the audio signal from a digital music file or the output from a digital audio workstation (DAW) on a computer.
                        """)
                st.write("***In addition to this, there are various formats of audio signals available.***")
                st.write("""
            1. **Mono (Monaural):**
            Mono, short for monaural, refers to a single-channel audio format where all audio signals are mixed together and played through a single speaker or audio channel. In a mono setup, there is no distinction between left and right channels; the sound is centered, making it appear to come from a single point. Mono audio is commonly used in older audio devices, telephones, and public address systems.

            2. **Stereo:**
            Stereo is a two-channel audio format that provides a more immersive and spatial audio experience compared to mono. In stereo, sound is distributed between two speakers or audio channels, with each channel containing slightly different audio information. This difference in audio signals creates a sense of direction and space in the sound, making it seem as if certain elements are coming from the left or right. Stereo is the standard audio format for most music recordings, audio systems, and headphones.

            3. **Surround Sound:**
            Surround sound is a multi-channel audio format that goes beyond the two channels of stereo to create a more immersive audio experience. It uses multiple speakers positioned around the listener to reproduce audio from different directions, simulating a three-dimensional sound environment. The most common surround sound formats are 5.1 and 7.1, which consist of five or seven main speakers and a subwoofer (the ".1" denotes the subwoofer channel for low-frequency effects).

                - 5.1 Surround Sound: It consists of five main speakers: front left, front center, front right, rear left, rear right, and one subwoofer. This format is commonly used in home theaters and movie theaters.

                - 7.1 Surround Sound: It adds two additional speakers to the 5.1 setup, creating a more immersive sound experience. In addition to the front and rear speakers, there are two side speakers. This format is often used in high-end home theaters and gaming setups.

            Surround sound is particularly effective in movies, video games, and other media that benefit from a more spatial and realistic audio presentation. It allows for sounds to move around the listener, enhancing the overall audio experience.
                        """)
                st.subheader('Wave Theory of Sound')
                st.write("""
                - **Sound as a Wave:** According to the wave theory of sound, sound is considered a mechanical wave that propagates through a medium, such as air or water.
            - **Longitudinal Waves:** Sound waves are classified as longitudinal waves. They involve the back-and-forth vibration of particles in the medium along the same direction as the wave travels.
            - **Compression and Rarefaction:** Sound waves consist of compressions (areas of increased particle density and higher pressure) and rarefactions (areas of decreased particle density and lower pressure) that move through the medium.
            - **Frequency and Pitch:** The frequency of a sound wave determines its pitch. Higher frequency waves have a higher pitch, while lower frequency waves have a lower pitch.
            - **Amplitude and Volume:** The amplitude of a sound wave corresponds to its intensity or volume. Higher amplitude waves create louder sounds, while lower amplitude waves create softer sounds.
            - **Reflection, Refraction, and Diffraction:** Sound waves can undergo reflection (bouncing off surfaces), refraction (bending when passing through mediums of different densities), and diffraction (spreading out when encountering obstacles or passing through small openings).
                """)
                l_img = load_image("Images/wts.jpg")
                st.image(l_img)
                st.subheader('Particle Theory of Sound')
                st.write("""
                - **Sound as a Particle Motion:** According to the particle theory of sound, sound is explained by the movement of individual particles or molecules in the medium.
            - **Collisions and Oscillations:** When an object or source vibrates or generates sound, it causes adjacent particles in the medium to collide with one another, transferring energy and motion.
            - **Particle Displacement:** The particles in the medium undergo back-and-forth oscillatory motion around their equilibrium positions, resulting in the transmission of sound energy.
            - **Rarefaction and Compression:** As particles oscillate, they form areas of rarefaction (particles spread apart) and compression (particles close together), creating regions of alternating density and pressure in the medium.
            - **Transfer of Energy:** Sound energy is transferred from particle to particle through a series of collisions and oscillations.
            - **Speed of Sound:** The speed of sound is determined by the average speed of particle motion within the medium.
            """)
                l_img = load_image("Images/pts.jpg")
                st.image(l_img)

                st.write("##")
                st.subheader('ACOUSTIC PHYSICS')
                st.write("""
            Acoustic physics is a branch of physics that deals with the study of sound, its properties, and its interactions with the environment. Here's a brief explanation of acoustic physics along with examples:

            - **Sound Waves:** Acoustic physics focuses on the characteristics and behavior of sound waves, including their generation, propagation, and reception. It explores concepts such as frequency, wavelength, amplitude, and speed of sound.
            - **Resonance:** Acoustic physics studies resonance phenomena, where objects or systems vibrate at their natural frequencies in response to an external sound wave. Examples include the resonance of a musical instrument or the resonance of a wine glass when a certain pitch is played.
            - **Reflection, Refraction, and Diffraction:** Acoustic physics examines how sound waves interact with different surfaces and objects. It investigates phenomena such as sound reflection (bouncing off surfaces), sound refraction (bending when passing through mediums of different densities), and sound diffraction (spreading out when encountering obstacles or passing through small openings).
            - **Acoustic Instruments:** Acoustic physics plays a crucial role in understanding the behavior and design of musical instruments. It explains how sound is produced, modified, and amplified in instruments such as guitars, pianos, flutes, and drums.
            - **Acoustic Imaging:** Acoustic physics is involved in techniques such as ultrasound imaging, which uses sound waves to create images of internal structures in the human body. This includes applications like medical ultrasound, sonar systems, and underwater imaging.
            - **Room Acoustics:** Acoustic physics examines the properties of sound within enclosed spaces. It studies how sound waves interact with walls, ceilings, and other surfaces, affecting factors like sound quality, echo, reverberation, and acoustics of concert halls, theaters, and recording studios.
            - **Acoustic Signal Processing:** Acoustic physics is essential in the field of signal processing, where it involves analyzing, modifying, and synthesizing sound signals. Examples include noise cancellation, audio compression algorithms, and speech recognition systems.
            - **Acoustic Measurement:** Acoustic physics provides techniques and tools for measuring sound, such as sound level meters, frequency analyzers, and microphone calibration. These measurements are crucial in various fields, including environmental noise monitoring, audio engineering, and research.

            Acoustic physics encompasses a wide range of phenomena and applications, contributing to fields like music, medicine, engineering, communication, and environmental science. By studying the principles of acoustic physics, we can better understand the behavior and manipulation of sound in various contexts.
            """)
                l_img = load_image("Images/img1.jpg")
                st.image(l_img, width= 700)
                st.write("##")
                st.subheader('PROPERTIES OF SOUND')
                st.write("""
                - **Frequency:** Frequency refers to the number of oscillations or cycles per second of a sound wave and is measured in Hertz (Hz). It determines the pitch of a sound. Higher frequency waves have a higher pitch, while lower frequency waves have a lower pitch.
                - **Amplitude:** Amplitude represents the magnitude or intensity of a sound wave. It is a measure of the energy carried by the wave and is perceived as the volume or loudness of the sound. Amplitude is typically measured in decibels (dB). Greater amplitude corresponds to a louder sound, while smaller amplitude corresponds to a softer sound.
                - **Wavelength:** Wavelength is the distance between two consecutive points of similar phase on a sound wave. It is inversely related to frequency, meaning that high-frequency waves have shorter wavelengths, while low-frequency waves have longer wavelengths.
                - **Speed of Sound:** The speed of sound refers to the rate at which sound waves propagate through a medium. It depends on the properties of the medium, such as temperature, density, and elasticity. In dry air at room temperature, sound travels at approximately 343 meters per second (m/s).
                - **Timbre:** Timbre refers to the unique quality or tone color of a sound. It allows us to distinguish between different musical instruments or voices producing the same pitch and loudness. Timbre is influenced by the harmonic content, envelope, and other characteristics of a sound wave.
                - **Phase:** Phase describes the relative position of a sound wave at a specific point in time. It indicates the point of the wave cycle that the wave has reached, such as the starting point or the peak. Phase relationships are important in phenomena such as interference and the perception of stereo sound.
                - **Reflection, Refraction, and Diffraction:** Sound waves can interact with surfaces, objects, and openings in the environment. Reflection occurs when sound waves bounce off a surface, refraction happens when sound waves bend as they pass through mediums of different densities, and diffraction occurs when sound waves spread out or bend around obstacles.
                """)
                st.write("---")

            if selected == 'Properties of Sound':
                st.write("---")
                lcl, rcl = st.columns((1,3))
                with rcl:
                    st.header("PROPERTIES OF SOUND")
                lcol, rcol = st.columns((2,1))
                with lcol:
                    st.write("##")
                    st.subheader("FREQUENCY")
                    st.write("""
                    Frequency in sound refers to the number of cycles or vibrations occurring in a sound wave per unit of time. It is a measure of how many times a sound wave repeats its pattern within a given timeframe. Frequency is commonly measured in ***Hertz (Hz)***, which represents the number of cycles per second.
                    """)
                with rcol:
                    lottie_f1 = load_lottieurl('https://assets7.lottiefiles.com/packages/lf20_uuqtvmhz.json')
                    lottie_f2 = load_lottieurl('https://assets7.lottiefiles.com/packages/lf20_1wolwueu.json')
                    st_lottie(lottie_f1, key= 'fr1')
                    st_lottie(lottie_f2, key= 'fr2')
                lc, mc, rc = st.columns((2.5,1,2))
                with mc:
                    st.write('**FREQUENCY**')
                l_img = load_image("Images/freq.png")
                st.image(l_img)
                st.write("##")
                st.write("""
                            In simpler terms, frequency determines the pitch of a sound. Higher frequencies result in higher-pitched sounds, while lower frequencies produce lower-pitched sounds. For example, a high-pitched whistle or the sound of a bird chirping has a higher frequency compared to a low-pitched rumble of thunder.
                        """)
                st. write("##")
                st.write("**FREQUENCY RANGE**")
                st.write("""
                The human hearing range is roughly ***20 Hz to 20,000 Hz***. It covers the spectrum of frequencies that most people can perceive. Lower frequencies are associated with deep sounds, while higher frequencies correspond to high-pitched sounds. Hearing ability can vary based on factors like age and exposure to loud noise.
                """)
                st.write("##")
                l_img = load_image("Images/freq_range.png")
                st.image(l_img)
                st.write('##')
                st.write("""
                Here's an example that demonstrates the sound of different frequencies. A slider ranging from 20 Hz to 20 kHz allows you to select any frequency within that range. By choosing a frequency and playing it, you can experience the sound characteristics unique to that particular frequency.
                """)
                l1, c1, r1, = st.columns((3))
                with c1:
                    st.write('**FREQUENCY SOUND GENERATOR**')
                frequency = st.slider("**Select Frequency (Hz)**", min_value = 20, max_value = 20000)   #frequency generator
                duration = 1 #in seconds
                sample_rate = 44100 #44.1 KHz
                generated_sound = generate_sound(frequency,duration, sample_rate)
                st.audio(generated_sound.export(format='wav').read(), format='audio/wav')

                st.write("##")
                st.write("""
                Similarly in music theory, each note is characterized by a unique frequency. By selecting a note from the dropdown menu (ranging from C to B), you can not only listen to its sound but also discover its corresponding frequency. This allows you to compare the generated frequency sound with the actual frequencies of different notes, enhancing your understanding of the relationship between musical notes and their pitch.
                """)
                l1, c1, r1, = st.columns((3))
                with c1:
                    st.write('**MUSICAL NOTE GENERATOR**')
                note = st.selectbox("**Select a Note**", ('C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B'))
                duration = 1

                notes_frequencies = {
                    'C': 261.63, 'C#/Db': 277.18, 'D': 293.66, 'D#/Eb': 311.13,
                    'E': 329.63, 'F': 349.23, 'F#/Gb': 369.99, 'G': 392.00, 
                    'G#/Ab': 415.30, 'A': 440.00, 'A#/Bb': 466.16, 'B': 493.88
                    }
                
                # Check if the note exists in the mapping
                if note in notes_frequencies:
                    frequency = notes_frequencies[note]
                    sample_rate = 44100

                    # Generate the note audio segment
                    note_audio = generate_sound(frequency, duration, sample_rate)

                    # Play the generated note
                    st.audio(note_audio.export(format="wav").read(), format="audio/wav")
                    st.write(f'The Frequency for this note is **{frequency} Hz**')
                st.write("##")
                l_img = load_image("Images/mf.png")
                st.image(l_img)
                st.write("##")
                st.subheader("WAVELENGTH")
                st.write("""
                    Wavelength refers to the distance between two consecutive points of identical phase in a sound wave. It is the physical length of one complete cycle of the wave, usually measured from crest to crest or trough to trough. 
            """)
                l_img = load_image("Images/frr.png")
                st.image(l_img)
                st.write("""
                    When a sound wave travels through a medium, such as air, it creates areas of compression and rarefaction. The wavelength is the distance from one compression to the next compression, or from one rarefaction to the next rarefaction.
                    """)
                lottie_w1 = load_lottieurl('https://assets3.lottiefiles.com/packages/lf20_chmcmntz.json')
                st_lottie(lottie_w1, key = 'wave')
                st.write("##")
                st.write("**RELATION BETWEEN FREQUENCY & WAVELENGTH**")
                st.write("""
                Wavelength is inversely related to the frequency of the sound wave. Higher frequencies have shorter wavelengths, while lower frequencies have longer wavelengths. This means that high-pitched sounds have shorter wavelengths, and low-pitched sounds have longer wavelengths.
                
            ***The relationship between frequency and wavelength of sound can be described by the formula:***

            *λ ∝ 1/f*

            Or we can also write the above equation as:

            *λ = c/f*

            Where **c** is a constant, which here denotes the speed of sound.
            Hence, the formula for determining the wavelength can be written as:
                
            *wavelength (**λ**) = speed of sound (**v**) / frequency (**f**)*

            Where:
            - Wavelength (**λ**) is measured in meters (**m**).
            - Speed of sound (**v**) is the speed at which sound waves travel through a medium, such as air. In dry air at room temperature, the approximate speed of sound is about **343 meters per second (m/s)**.
            - Frequency (**f**) is measured in hertz (**Hz**), which represents the number of cycles or vibrations per second.

            This formula shows that wavelength and frequency are inversely proportional to each other. As the frequency of a sound wave increases, its wavelength decreases, and vice versa. This means that higher frequency sounds have shorter wavelengths, while lower frequency sounds have longer wavelengths.

            For example, if the frequency of a sound wave is **1000 Hz (1 kHz)**, and the speed of sound is **343 m/s**, we can calculate the wavelength as follows:

            **wavelength (λ) = 343 (m/s) / 1000 (Hz) = 0.343 meters or 34.3 centimeters**

            This means that a sound wave with a frequency of **1000 Hz** has a wavelength of approximately **0.343 meters**.
                """)
                st.write("##")
                st.write("""
                Similarly we can caculate the wavelenght of different frequencies by using the following Wavelenght Calculator
                """)
                ll,cc,rr = st.columns(3)
                with cc:
                    st.write("**Wavelength Calculator**")
                fcq = st.number_input("Enter the frequency (in Hz):", min_value=0.1, max_value=20000.0, value=440.0, step=0.1)
                
                if st.button("Calculate Wavelength"):
                    wvl = wavcal(fcq)
                    st.write(f"The wavelength is **{wvl:.2f} m**.")
                st.write("##")
                st.write("""
                On the other hand, The relationship between wavelength and frequency of sound can be expressed vice versa using the following formula:

            **f = v / λ**

            Hence, if you are aware of the wavelength of a specific sound, you can determine its frequency using the above mentioned formula.

            For example, if the wavelength of a sound wave is **0.5 m**, and the speed of sound is **343 m/s**, we can calculate the frequency as follows:

            **frequency (f) = 343 (m/s) / 0.5 (m) = 686 Hz**

            This means that a sound wave with a wavelength of **0.5 m** has a wavelength of approximately **686 Hz**.
            """)
                ll,cc,rr = st.columns(3)
                with cc:
                    st.write("**Frequency Calculator**")
                w_l = st.number_input("Enter the wavelength (in m):", min_value=0.001, max_value=20000.0, value=1.0, step=0.1) 
                if st.button("Calculate Frequency"):
                    f_l = freqcal(w_l)
                    st.write(f"The frequency is **{f_l:.2f} Hz**.")
                st.write("##")
                st.write("""
                **You can find the frequencies and wavelengths of different musical notes of an octave in the table below:**
                """)
                ntble = {
                    'Note': ['C4', 'C#4/Db4', 'D4', 'D#4/Eb4', 'E4', 'F4', 'F#4/Gb4', 'G4', 'G#4/Ab4', 'A4', 'A#4/Bb4', 'B4'],
                    'Frequency (Hz)': [261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88],
                    'Wavelength (m)': [1.34, 1.27, 1.20, 1.13, 1.07, 1.01, 0.95, 0.89, 0.84, 0.79, 0.75, 0.71]
                }
                df = pd.DataFrame(ntble)
                st.table(df)
                st.write("##")
                st.subheader("AMPLITUDE")
                st.write("""
                Amplitude refers to the maximum displacement or distance that a particle or medium undergoes from its equilibrium position as a result of a sound wave. In the context of sound, it represents the magnitude or strength of the wave. It directly correlates with the loudness or volume of the sound, where larger amplitudes correspond to louder sounds and smaller amplitudes correspond to softer sounds. Amplitude is typically measured as the absolute value or peak value of the pressure variations caused by the sound wave. It plays a crucial role in our perception of sound intensity and can greatly influence the emotional impact and overall quality of the auditory experience.
                """)
                l2,r2 = st.columns(2)
                with l2:
                    l_img = load_image("Images/amp.png")
                    st.image(l_img)
                with r2:
                    l_img = load_image("Images/ampl.png")
                    st.image(l_img)
                st.write("##")
                st.write("**LEVEL OF SOUND**")
                st.write("""
                The level of sound refers to the measurement of sound intensity or loudness. It quantifies the perceived loudness of a sound wave and is typically expressed in decibels (**dB**), which is the SI unit for sound level.

            ***Relationship between the amplitude of sound and the level of sound:*** 

            The sound level in **dB** is logarithmically proportional to the square of the sound wave's amplitude.The equation to calculate the sound level (**L**) in dB based on the sound wave's amplitude (**A**) is:

            **L = 20 * log10(A/A0)**

            Where:
            - L is the sound level in decibels,
            - A is the sound wave's amplitude,
            - A0 is a reference amplitude (typically the threshold of human hearing, which is approximately 20 micropascals).
            """)
                apt = st.number_input("Enter the Amplitude of Sound Wave:", min_value=0.001)
                if st.button("Calculate Level"):
                    lvl = ampcal(apt)
                    st.write(f"The sound level is **{lvl:.2f} dB**")
                st.write("##")
                st.subheader("PITCH")
                st.write("""
                Pitch refers to the perceived frequency of a sound, determining whether it is perceived as high or low. It is one of the fundamental auditory sensations and is closely tied to the physical property of frequency. In music, pitch is a crucial element as it allows us to differentiate between different musical notes and forms the basis of melody, harmony, and musical structure.

            Musical examples can help illustrate the concept of pitch:

            1. **High Pitch:** The sound of a whistle, the chirping of a bird, or the upper keys of a piano all exhibit high pitch. These sounds have a higher frequency, resulting in a perception of higher pitch.

            2. **Low Pitch:** The rumble of thunder, the deep notes of a bass guitar, or the lower keys of a piano demonstrate low pitch. These sounds have a lower frequency, leading to a perception of lower pitch.

            3. **Melody:** A melody is a sequence of musical notes with varying pitches played in succession. Each note in a melody has a distinct pitch, allowing us to distinguish one note from another and recognize the melodic pattern.

            4. **Harmonies:** In harmonies, multiple pitches are played simultaneously, creating chords and chord progressions. The combination of different pitches produces unique tonal qualities and contributes to the richness and complexity of musical compositions.

            It is important to note that pitch perception can vary among individuals based on factors such as hearing ability, musical training, and cultural influences. Nonetheless, pitch remains a fundamental aspect of music and plays a significant role in our perception and enjoyment of musical sounds.
                """)
                st.write("##")
                st.subheader("PHASE")
                st.write("""
                Phase in sound refers to the relationship between two or more sound waves at a specific point in time. It describes the alignment or synchronization of the peaks and troughs of different waves. Understanding phase is essential in various aspects of audio engineering, acoustics, and music production.


            Phase is a measure of the position and timing of a sound wave at a given point in time, particularly in relation to other sound waves. It refers to the alignment or displacement of the peaks and troughs of different waves. The phase relationship between waves determines how they interact and combine when they are combined or played simultaneously.

            **Examples:**
            """)
                st.write("""
            1. **In-Phase:** When two or more sound waves have their peaks and troughs aligned, they are considered "in-phase." In this case, the waves reinforce each other, resulting in a stronger combined signal. For example, if two identical sine waves are perfectly in-phase and added together, the amplitude of the resulting wave is doubled.

            2. **Out-of-Phase:** When two or more sound waves have their peaks and troughs misaligned, they are considered "out-of-phase." In this case, the waves can partially or completely cancel each other out at certain frequencies or time intervals, resulting in a weakened or nullified combined signal. For instance, if two identical sine waves are completely out-of-phase, their combination results in complete cancellation, resulting in silence.

            3. **Phase Shift:** Phase shift refers to a change in the position or timing of a sound wave. It occurs when a waveform is delayed or advanced in time, causing a shift in the alignment of its peaks and troughs. Phase shifts can occur naturally due to reflections, refractions, or distance traveled by sound waves, or they can be intentionally introduced using audio processing techniques.

            4. **Stereo Imaging:** In stereo audio, phase differences are used to create a sense of spaciousness and location in the stereo field. By introducing controlled phase differences between the left and right channels, sound engineers can create stereo effects, such as panning, widening, or simulating three-dimensional spatial perception.

            Understanding phase and manipulating it correctly is crucial in audio recording, mixing, and mastering to avoid phase cancellation issues, achieve desired stereo imaging, and create unique sound effects.
            """)
                l_img = load_image("Images/Phase.png")
                st.image(l_img)
                st.write("---")

            if selected == 'Acoustic Properties':
                st.write("---")
                lcc,rcc = st.columns((0.5,2))
                with rcc:
                    st.header("ACOUSTIC PROPERTIES OF SOUND")
                st.write("##")
                st.subheader("REFLECTION OF SOUND")
                st.write("""
                The reflection of sound refers to the phenomenon where sound waves encounter a surface and bounce back, changing their direction. When sound waves strike a reflective surface, such as a wall or a hard floor, they undergo reflection, similar to how light waves reflect off a mirror.

            During reflection, the angle of incidence (the angle at which the sound wave strikes the surface) is equal to the angle of reflection (the angle at which the sound wave bounces off the surface). This principle is known as the law of reflection.

            Here are a few examples of sound reflection:

            1. **Echoes:** When you shout or clap your hands in a large, open space like a canyon or an empty room, you may hear the sound reflect off the surfaces and return to your ears as distinct repetitions, known as echoes.

            2. **Reverberation in concert halls:** In large concert halls or auditoriums, sound waves reflect off the walls, ceilings, and other surfaces, creating a prolonged decay of sound called reverberation. This phenomenon enhances the overall acoustic experience for the audience.

            3. **Sonar technology:** Sonar systems use sound waves to detect and locate objects underwater. A sound wave is emitted and then reflects off objects in the water, such as submarines or fish. By analyzing the time it takes for the reflected sound to return, the distance and location of the objects can be determined.

            4. **Sound reflection in everyday environments:** In everyday situations, sound waves reflect off various surfaces, such as buildings, furniture, or even people. This reflection affects the way we perceive sound in our surroundings, contributing to the overall acoustic environment.
                """)
                l_img = load_image("Images/reflection.png")
                st.image(l_img)
                st.write("##")
                st.subheader("REFRACTION OF SOUND")
                st.write("""
            Refraction of sound refers to the bending or change in direction of sound waves as they pass through a medium with varying acoustic properties. This change occurs due to the difference in the speed of sound waves in different mediums.

            When sound waves travel from one medium to another, such as air to water or air to a solid object, their speed changes due to the variation in the density and elasticity of the medium. As a result, the sound waves experience refraction, causing them to bend or change direction.

            Here are a few examples of refraction of sound:

            1. **Sound traveling through different layers of the atmosphere:** The Earth's atmosphere consists of multiple layers with varying properties. When sound waves propagate through these layers, they encounter changes in temperature, humidity, and pressure, which cause variations in the speed of sound. These variations in speed lead to refraction, and as a result, sound waves can bend and travel over long distances, such as in the case of distant thunder or sound heard from a faraway source.

            2. **Sound traveling from air to water:** When sound waves travel from air into water, they encounter a significant change in the density and elasticity of the medium. This change causes the sound waves to refract, bending them towards the normal (an imaginary line perpendicular to the interface between air and water). This phenomenon is commonly observed when you hear sounds underwater, such as a person speaking or the sound of a submerged object.

            3. **Sound traveling through a solid object:** When sound waves encounter a solid object, such as a wall or a building, they can refract as they pass through the object. This refraction can cause the sound to change direction and propagate in different ways within the structure. It is the basis for various techniques like acoustic imaging, where sound waves are used to create images or detect internal structures of objects.
                """)
                l_img = load_image("Images/refraction.png")
                st.image(l_img)
                ll,mm,rr = st.columns((2,1,2))
                with mm:
                    st.write("**Rerfaction of Sound**")
                st.write("##")
                st.subheader("DIFFUSION OF SOUND")
                st.write("""
            Diffusion of sound refers to the scattering or spreading out of sound waves in various directions when they encounter irregularities or obstacles in their path. It is a phenomenon where sound waves disperse and fill an environment uniformly.

            Here are a few examples of diffusion of sound:

            1. **Acoustic treatment in concert halls:** Concert halls and other performance venues often employ diffusive elements to enhance the listening experience. These elements, such as diffuser panels or architectural features, scatter sound waves in multiple directions, reducing the formation of echoes and creating a more balanced and enveloping sound. Diffusion helps to ensure that sound is evenly distributed throughout the hall, allowing the audience to perceive the performance clearly regardless of their seating location.

            2. **Acoustic diffusers in recording studios:** Recording studios often incorporate diffuser panels on the walls to minimize the negative effects of sound reflections. These diffusers scatter sound waves, preventing the formation of distinct echoes or standing waves that could interfere with the recording process. By diffusing the sound, the studio creates a more controlled and balanced acoustic environment.

            3. **Diffusion in open outdoor spaces:** When sound is emitted in open spaces, such as parks or open-air concert venues, it naturally undergoes diffusion as it encounters various objects, terrain features, and atmospheric conditions. These interactions cause the sound waves to scatter in multiple directions, allowing it to reach a wider audience and create a more immersive listening experience.

            4. **Diffusion in natural environments:** In nature, the irregularities of natural surfaces, such as trees, leaves, rocks, and foliage, contribute to the diffusion of sound. As sound waves encounter these surfaces, they are scattered in different directions, creating a more dispersed and ambient sound environment.

            Overall, diffusion of sound plays a significant role in shaping the way we perceive sound in various environments. By scattering sound waves in different directions, diffusion helps to create a more pleasant and immersive auditory experience while minimizing undesirable acoustic effects such as echoes or resonances.
            """)
                l_img = load_image("Images/diffusion.png")
                st.image(l_img)
                ll,mm,rr = st.columns((2,1,2))
                with mm:
                    st.write("**Diffusion of Sound**")
                st.write("##")
                st.subheader("DIFFRACTION OF SOUND")
                st.write("""
                Diffraction of sound refers to the bending or spreading out of sound waves as they encounter obstacles or pass through openings that are comparable in size to the wavelength of the sound waves. It is a phenomenon where sound waves change direction and propagate into regions that would otherwise be blocked.

            Here are a few examples of diffraction of sound:

            1. **Sound passing through a doorway:** When you hear sound coming from another room through an open doorway, the sound waves are diffracting around the edges of the doorway. The size of the doorway is comparable to the wavelength of the sound waves, allowing them to bend and spread out into the next room.

            2. **Sound around obstacles:** If you stand behind a large obstacle, such as a wall or a building, and someone on the other side speaks or produces sound, you can still hear them to some extent. This is because the sound waves diffract around the edges of the obstacle, reaching your ears even though the direct path is blocked.

            3. **Diffraction through small openings:** When sound waves pass through small openings, such as a narrow gap in a fence or the opening of a musical instrument, they diffract and spread out in different directions. This phenomenon is used in musical instruments like flutes and clarinets, where the small openings and air columns cause sound waves to diffract and produce specific tones and timbres.

            4. **Diffraction in outdoor environments:** In open outdoor spaces, sound waves can diffract around natural features like hills, trees, and buildings. This diffraction helps to carry sound over obstacles and allows it to reach listeners in different directions, contributing to the ambient and immersive nature of outdoor soundscapes.
                """)
                l_img = load_image("Images/diffraction.jpg")
                st.image(l_img)
                st.write("##")
                st.subheader("ABSORPTION OF SOUND")
                st.write("""
            Absorption of sound refers to the process by which sound waves are converted into other forms of energy, typically heat, when they interact with a material or surface. The absorbed sound energy is not reflected or transmitted but is instead dissipated within the material.


            Example: **A room with sound-absorbing panels**

            Imagine a room that is equipped with sound-absorbing panels on its walls, ceiling, and floor. These panels are made of materials designed to absorb sound energy rather than reflecting it. When sound waves propagate in the room, the sound-absorbing panels absorb a significant portion of the sound energy that reaches them.

            As a result of the sound absorption, the intensity and reverberation of the sound in the room decrease. The absorbed sound energy is converted into heat energy within the material of the panels. This leads to a reduction in echoes, reflections, and overall sound levels, resulting in a quieter and less reverberant environment.

            Materials used for sound absorption often have properties like porous or fibrous structures, which allow them to trap and dissipate sound energy effectively. Examples of sound-absorbing materials include acoustic foam, mineral wool, fiberglass insulation, and specialized acoustic ceiling tiles.

            In various settings, sound absorption is utilized to improve acoustic conditions. It finds applications in concert halls, recording studios, offices, theaters, and other spaces where reducing echoes, controlling reverberation, and enhancing sound quality are important factors.

            Overall, sound absorption plays a crucial role in managing sound levels and creating acoustically balanced environments by converting sound energy into heat within materials designed for this purpose.
            """)
                l_img = load_image("Images/absorption.png")
                st.image(l_img)
                ll,mm,rr = st.columns((2,1,2))
                with mm:
                    st.write("**Absorption of Sound**")
                st.write("##")
                st.subheader("RESONANCE OF SOUND")
                st.write("""
            Resonance of sound refers to the phenomenon that occurs when an object or a medium vibrates at its natural frequency in response to an external sound stimulus or an applied force. Resonance amplifies the sound waves and can result in increased sound intensity or sustained vibrations.

            Here are a few examples of resonance of sound:

            1. **Resonance in musical instruments:** Musical instruments, such as guitars, pianos, or wind instruments, rely on resonance to produce sound. When a string is plucked on a guitar or a key is struck on a piano, the instrument's body or soundboard resonates at specific frequencies that correspond to the natural resonant frequencies of the instrument. This resonance amplifies the sound produced, resulting in a rich and sustained tone.

            2. **Resonance in vocalization:** In the human voice, resonance plays a crucial role in sound production. The vocal cords generate sound waves, and these waves resonate in the vocal tract, including the throat, mouth, and nasal cavities. The resonance of these cavities amplifies specific frequencies and gives each individual their unique voice characteristics. Singers and public speakers often manipulate their vocal resonance to achieve different tones or project their voice effectively.

            3. **Resonance in architectural structures:** Large architectural structures, such as bridges or buildings, can be susceptible to resonance when exposed to sound waves or vibrations. If the frequency of the sound matches the natural frequency of the structure, resonance can occur, causing the structure to vibrate or even experience destructive oscillations. This phenomenon is particularly important in structural engineering to avoid resonance-related structural failures.

            4. **Resonance in musical acoustics:** Resonance is also observed in various acoustic phenomena, such as resonant cavities or resonant tubes. For example, in a pipe organ, air columns in the pipes resonate at specific frequencies when activated by the flow of air. The resonance amplifies the sound produced by the organ pipes.

            Resonance can have both desirable and undesirable effects depending on the context, and understanding and controlling it is important in various fields, including music, acoustics, and engineering.
            """)
                l_img = load_image("Images/resonance.jpg")
                st.image(l_img)
                st.write("##")
                st.subheader("ACOUSTIC TREATMENT")
                st.write("""
                Acoustic treatment of a room involves the strategic placement of materials and modifications to the room's surfaces to improve the sound quality and optimize the acoustic environment. This process is particularly important in recording, mixing, and mastering studios, where accurate sound reproduction and precise monitoring are essential. Here are some factors to consider and techniques to keep in mind while treating a room for these purposes:

            1. **Reflection control:** Excessive reflections can cause problems such as echoes, comb filtering, and unwanted coloration of the sound. To control reflections, consider using materials like acoustic panels, diffusers, and bass traps. Acoustic panels can absorb mid and high-frequency reflections, while diffusers scatter sound waves to create a more balanced sound field. Bass traps help control low-frequency reflections and resonances.

            2. **Frequency response and room modes:** Addressing room modes is crucial for achieving an even frequency response. Room modes are resonances that occur due to the dimensions and shape of the room, resulting in certain frequencies being emphasized or canceled. Bass traps and low-frequency absorption panels can help minimize the effects of room modes and create a more balanced bass response.

            3. **Reverberation time:** The reverberation time of a room is the duration it takes for sound to decay by 60 dB after the sound source stops. For recording, mixing, and mastering studios, it's important to have a controlled and predictable reverberation time. This can be achieved through the use of absorption panels, diffusers, and proper placement of furniture and other objects to help reduce the overall reverberation in the room.

            4. **Near-field monitoring:** When setting up a studio, consider using near-field monitors, which are designed to provide accurate sound representation at close listening distances. These monitors are typically placed on dedicated stands or speaker isolation pads to minimize coupling with the room and reduce unwanted resonances.

            5. **Room geometry and dimensions:** The dimensions and shape of the room can have a significant impact on its acoustics. Irregular room shapes with non-parallel surfaces can help minimize standing waves and reduce the prominence of room modes. If possible, design the room with appropriate proportions and avoid symmetrical dimensions.

            6. **Sound isolation:** In recording studios, sound isolation is crucial to prevent external noise from entering the recording space and to minimize sound leakage. This involves the use of soundproofing techniques such as acoustic insulation, resilient channels, and sealing gaps or air leaks.

            7. **Diffusion:** Incorporating diffusers into the room can help disperse sound waves, reduce flutter echoes, and create a more spacious and natural sound environment. Diffusers scatter sound in a controlled manner, enhancing the perception of depth and imaging.

            It's important to note that acoustic treatment should be tailored to the specific needs of the room and the desired sound characteristics. Consulting with acoustics professionals or acoustic consultants can provide valuable insights and help ensure the best possible acoustic environment for recording, mixing, and mastering activities.
            """)
                l_img = load_image("Images/act.jpg")
                st.image(l_img)
                st.write("##")
                st.write("---")

            if selected == 'Equipments & Gears':
                st.write("---")
                lcc,rcc = st.columns((0.5,2))
                with rcc:
                    st.header("AUDIO EQUIPMENTS & GEARS")
                st.write("##")
                st.subheader("MICROPHONES")
                st.write("""
                A microphone is an electronic device used to capture sound waves and convert them into an electrical signal. It is commonly used in various applications such as recording, broadcasting, live performances, communication systems, and more. The microphone consists of a diaphragm or a capsule that vibrates in response to sound waves. These vibrations are then converted into electrical signals through the use of various transducer technologies, such as dynamic, condenser, or ribbon. The electrical signal produced by the microphone can be amplified and processed further for recording, broadcasting, or other audio applications. Microphones come in different types, designs, and specifications to suit different needs and capture sound with varying levels of accuracy and sensitivity.
                """)
                st.write("**TYPES OF MICROPHONES**")
                st.write("""
                There are several types of microphones, each with its own characteristics, applications, and strengths. Here are some of the most common types of microphones:

            1. **Dynamic Microphones:** Dynamic microphones are robust and versatile, making them suitable for a wide range of applications. They work by using a diaphragm attached to a coil that moves within a magnetic field. They are known for their durability, ability to handle high sound pressure levels, and resistance to moisture and rough handling. Dynamic microphones are often used for live performances, broadcasting, instrument recording, and general-purpose audio capturing.
            """)
                l_img = load_image("Images/dynmic.png")
                st.image(l_img)
                st.write(""" 
            2. **Condenser Microphones:** Condenser microphones, also known as capacitor microphones, are more sensitive and accurate compared to dynamic microphones. They work based on the principle of capacitance, where a diaphragm vibrates next to a fixed backplate, forming a capacitor. Condenser microphones require power, either through batteries or phantom power from an audio interface or mixer. They offer extended frequency response, high sensitivity, and excellent transient response, making them suitable for studio recording, vocals, acoustic instruments, and capturing delicate sound details.
            """)
                l_img = load_image("Images/condmic.jpg")
                st.image(l_img)
                l3, c3, r3 = st.columns((1.3,1,1))
                with c3:
                    st.write("**CONDENSER MICROPHONES**")
                st.write("""
            3. **Ribbon Microphones:** Ribbon microphones utilize a thin metal ribbon suspended in a magnetic field. The ribbon acts as the diaphragm and generates the electrical signal as it vibrates with sound waves. Ribbon microphones are known for their smooth and warm sound character, natural high-frequency response, and ability to capture nuances and details. They are often used in studio recording for vocals, brass instruments, guitar amps, and string instruments. Ribbon microphones are delicate and require careful handling due to their fragile nature.
            """)
                l_img = load_image("Images/ribbonmic.jpg")
                st.image(l_img)
                l3, c3, r3 = st.columns((1.3,1,1))
                with c3:
                    st.write("**RIBBON MICROPHONES**")
                st.write("""
            4. **Lavalier and Lapel Microphones:** Lavalier or lapel microphones are small and discreet microphones that are commonly used in broadcast, presentations, interviews, and stage performances. They are designed to be clipped onto clothing, typically near the collar or lapel, allowing for hands-free operation. Lavalier microphones can be both dynamic or condenser types, depending on the specific application and desired audio quality.
            """)
                l_img = load_image("Images/lapel.jpg")
                st.image(l_img)
                l3, c3, r3 = st.columns((1.3,1,1))
                with c3:
                    st.write("**LAPEL MICROPHONES**")
                st.write("""
            5. **Shotgun Microphones:** Shotgun microphones are highly directional microphones with a long, narrow pickup pattern. They are commonly used in film, television, and outdoor recordings to capture sound from a specific direction while rejecting unwanted ambient noise. Shotgun microphones are often mounted on boom poles or camera mounts and are popular for capturing dialogue and sound effects in various audiovisual productions.
            """)
                l_img = load_image("Images/shotgunmic.jpg")
                st.image(l_img)
                l3, c3, r3 = st.columns((1.3,1,1))
                with c3:
                    st.write("**SHOTGUN MICROPHONES**")
                st.write("##")
                st.subheader("CABLES")
                with st.container():
                    st.write("""
                        Audio cables are electrical cables designed to transmit audio signals from one audio device to another. They are commonly used in various audio setups, such as connecting musical instruments to amplifiers, connecting speakers to audio sources, or linking audio equipment in recording studios.
                """)
                    lcl, rcl = st.columns(2)
                    with lcl:
                        st.write("""
                        The most common type of cables used in Audio World are:
                        1. XLR Cables
                        2. TS Cables (1/4-inch)
                        3. TRS Cables(1/4-inch)
                        4. MIDI Cables
                        5. 3.5 mm Stereo Audio Cables (1/8-inch)
                        """)       
                    with rcl:
                        lottie_cbl = load_lottieurl("https://lottie.host/1d64bbd0-2dd5-4fba-8d52-8cf545b94f2b/Xxfpe1BIST.json")
                        st_lottie(lottie_cbl, key = 'cbl', width = 300)
                st.write("##")
                st.write("**EXAMPLES**")
                st.write("""
                        1. **XLR Cables:** XLR cables are balanced audio cables with three pins in a circular connector. They excel in professional audio settings, connecting microphones to audio gear like mixers or interfaces. Their balanced design minimizes interference and noise, making them ideal for long cable runs. Widely used in studios, live events, and concerts, XLR cables ensure high-fidelity audio transmission, contributing to top-notch sound quality in recordings and performances.
                        In addition to microphones, XLR cables are also commonly employed to connect DI boxes and professional audio speakers, solidifying their status as a standard in the industry.
                            """)
                l_img = load_image("Images/xlr.png")
                st.image(l_img)
                st.write("""
                        2. **TS Cables:** TS cables are unbalanced audio cables with two pins in a circular connector. They are commonly used for instruments like electric guitars, keyboards, and synthesizers to connect to amplifiers, effects pedals, or audio interfaces. TS stands for "Tip" and "Sleeve," where the tip carries the audio signal, and the sleeve serves as the ground. Unlike XLR cables, TS cables are more susceptible to interference and signal loss over long cable runs. However, for short distances and in less demanding setups, they provide a simple and cost-effective solution for audio connections in various musical performances, home studios, and live events.
                        """)
                l_img = load_image("Images/ts.png")
                st.image(l_img)
                st.write("""
                        3. **TRS Cables:** TRS cables are balanced audio cables with three pins in a circular connector. TRS stands for "Tip," "Ring," and "Sleeve." They are used for various audio connections, such as headphones to audio sources, audio interfaces to studio monitors, and connecting certain instruments and effects pedals. The tip carries the left audio signal, the ring carries the right audio signal, and the sleeve serves as the common ground. TRS cables help minimize interference and noise, making them suitable for professional audio applications where high-fidelity sound transmission is essential.
                        """)
                l_img = load_image("Images/trs.jpg")
                st.image(l_img)
                st.write("""
                        ***Hence, the main difference between TS cables & TRS cables are:*** TS cables have two pins and are unbalanced, commonly used for instruments like guitars. TRS cables have three pins and are balanced, used for audio connections that require noise rejection, such as headphones, studio monitors, and professional audio equipment.
                        """)
                l_img = load_image("Images/tsvtrs.jpg")
                st.image(l_img)
                st.write("""
                        4. **MIDI Cables:** MIDI cables are digital data cables with 5-pin DIN connectors used for transmitting musical information between MIDI-compatible devices like keyboards, synthesizers, and computers. Enable precise control and synchronization for complex musical compositions and arrangements.
                        """)
                l_img = load_image("Images/midi.jpg")
                st.image(l_img)
                l3, c3, r3 = st.columns((1.3,1,1))
                with c3:
                    st.write("**MIDI CABLE**")
                st.write("""
                        5. **3.5mm Stereo Audio Cable:** The 3.5mm stereo audio cable (1/8-inch) is a popular audio cable with a small, cylindrical connector. It's commonly used to link audio sources like smartphones or MP3 players to speakers, headphones, or car stereos. The cable's versatile design and widespread availability make it a convenient choice for everyday audio connections, providing clear and reliable sound transmission in various setups.
                        """)
                l_img = load_image("Images/jack.jpg")
                st.image(l_img, width =800)
                l3, c3, r3 = st.columns((1.3,1,1))
                with c3:
                    st.write("**1/8-INCH CABLE**")
                st.write("""
                        In addition to these, the audio world incorporates various other cable types depicted in the image below.
                        """)
                l_img = load_image("Images/cabletype.jpg")
                st.image(l_img)
                st.write("##")
                st.subheader("AUDIO INTERFACE")
                st.write("""
                        An audio interface is an external device used to connect audio equipment, such as microphones, instruments, and speakers, to a computer or recording system. It serves as the bridge between analog audio signals and digital data, enabling users to record, process, and play back audio with high-quality results.

            Commonly used examples of audio interfaces include:

            1. **Focusrite Scarlett 2i2:** A popular USB audio interface for home studios, offering two inputs with preamps and MIDI connectivity.

            2. **Universal Audio Apollo Twin:** Known for its exceptional audio quality and real-time processing capabilities with onboard DSP.

            3. **PreSonus AudioBox USB:** A compact and affordable USB interface suitable for entry-level recording setups.

            4. **Behringer U-Phoria UMC204HD:** Provides multiple inputs and outputs, ideal for recording instruments and vocals simultaneously.

            5. **MOTU 828es:** A high-end audio interface with advanced connectivity options and extensive I/O for professional studios.

            Audio interfaces come in various configurations, catering to different recording needs, ranging from simple 2-channel interfaces for solo recordings to multi-channel interfaces for larger recording setups.
                            """)
                l_img = load_image("Images/aif.jpg")
                st.image(l_img)
                l3, c3, r3 = st.columns((1.3,1,1))
                with c3:
                    st.write("**AUDIO INTERFACES**")
                st.write("##")
                st.subheader("MIDI KEYBOARD")
                st.write("""
                        A MIDI (Musical Instrument Digital Interface) keyboard is a musical input device that uses the MIDI protocol to send digital musical information to MIDI-compatible devices, such as synthesizers, sound modules, and computers. It typically resembles a traditional piano keyboard and enables musicians, composers, and producers to control and play virtual instruments, record MIDI data, and create music digitally.

            Commonly used examples of MIDI keyboards include:

            1. **Akai MPK Mini MK3:** A compact and versatile MIDI keyboard with pads and knobs, ideal for music production on the go.

            2. **Novation Launchkey 49:** Offers a combination of a MIDI keyboard with pads and faders, suitable for both music production and live performances.

            3. **Arturia KeyLab Essential 61:** A feature-rich MIDI keyboard with a wide range of controls, designed for seamless integration with software instruments and DAWs.

            4. **M-Audio Keystation 88:** A full-sized, 88-key MIDI keyboard, suitable for piano players and professional studios requiring a larger keyboard range.

            5. **Native Instruments Komplete Kontrol S49:** A premium MIDI keyboard with touch-sensitive knobs and color displays, optimized for controlling Native Instruments software instruments and effects.

            MIDI keyboards come in various sizes, with different features and control options, catering to the needs of musicians and producers with varying preferences and workflows. They offer an essential tool for modern music production, making it easier to create, record, and manipulate music in digital environments.
                        """)
                l_img = load_image("Images/midikey.jpg")
                st.image(l_img)    
                l3, c3, r3 = st.columns((1.3,1,1))
                with c3:
                    st.write("**MIDI KEYBOARDS**")
                st.write("##")
                st.subheader("STUDIO MONITORS")
                st.write("""
                            Studio monitors are specialized speakers used in audio recording, mixing, and mastering environments. They provide accurate and transparent audio reproduction, allowing audio engineers and producers to hear precise details and nuances in their recordings.

            Commonly used examples of studio monitors include:

            1. **Yamaha HS5:** A popular choice for home studios and small recording spaces, known for their balanced sound and affordability.

            2. **KRK Rokit 5 G4:** Offers a balanced frequency response and is favored by many producers for its reliable performance.

            3. **Genelec 8030C:** High-quality monitors with excellent sound clarity and build quality, suitable for professional studios and critical listening.

            4. **Adam Audio T7V:** Known for their precise and detailed sound, making them suitable for both music production and post-production applications.

            5. **JBL 305P MkII:** Budget-friendly studio monitors with impressive sound quality and a compact design, ideal for small studios and home recording setups.

            Studio monitors come in different sizes and configurations, including two-way and three-way designs, with various driver sizes and materials. They are essential tools for audio professionals to accurately assess and fine-tune their audio recordings, ensuring that the final mix sounds as intended on various playback systems.
                            """)
                l_img = load_image("Images/monitor.jpg")
                st.image(l_img)    
                st.write("##")
                st.subheader("AUDIO MIXER")
                st.write("""
                        A studio mixer, also known as an audio mixer or mixing console, is a central hub for audio signal processing and blending in recording studios and live sound setups. It allows audio engineers to adjust and control multiple audio sources, achieving a balanced and polished sound mix.

            Commonly used examples of studio mixers include:

            1. **Behringer X32:** A digital mixer with extensive features and routing options, suitable for medium to large-scale recording and live events.

            2. **Yamaha MG10XU:** A compact analog mixer with built-in effects and USB connectivity, ideal for small home studios and live performances.

            3. **Allen & Heath QU-16:** A digital mixer with advanced processing capabilities, designed for both studio and live sound applications.

            4. **Soundcraft Signature 12MTK:** Analog mixer with multi-track recording via USB, making it useful for capturing individual channels separately.

            5. **Midas M32:** A premium digital mixer with excellent sound quality and a wide range of control options, favored in professional recording studios and concert venues.

            Studio mixers come in different sizes and configurations, offering various input and output options, as well as features like EQ, compression, effects, and routing capabilities. They play a crucial role in audio production, allowing engineers to craft and shape the audio signals from different sources, creating a cohesive and polished sound mix for various applications.
                        """)
                l_img = load_image("Images/mixer.jpg")
                st.image(l_img)   
                l3, c3, r3 = st.columns((2.5,1,2))
                with c3:
                    st.write("**MIXER**")
                st.write("##")
                st. write("""
                        *Likewise, studios incorporate numerous other equipment, such as musical instruments, amplifiers, cables, and audio processing gear, to name a few. Additional examples include synthesizers, drum machines, DI boxes, studio headphones, effects processors, equalizers, compressors, and audio interfaces. These tools collectively enhance the studio's capabilities, enabling musicians, producers, and audio engineers to create, record, and produce professional-quality music and audio content.*
                        """)
                l_img = load_image("Images/studio.jpeg")
                st.image(l_img)
                l3, c3, r3 = st.columns((1.3,1,1))
                with c3:
                    st.write("**RECORDING STUDIO**")
                st.write("---")
                
            if selected == 'DAW':
                st.write("---")
                ll,rr = st.columns((0.5,4))
                with rr:
                    st.header("DIGITAL AUDIO WORKSTATION (DAW)")
                st.write("##")
                st.write("""
                        DAW stands for Digital Audio Workstation. It is a software application used for recording, editing, producing, and arranging audio tracks and music. DAWs provide a comprehensive set of tools and features that enable musicians, producers, and audio engineers to create professional-grade music and audio projects.

            Some popular examples of DAWs include:

            1. **Ableton Live:** Known for its real-time performance capabilities and versatility, it is widely used for electronic music production, DJing, and live performances.
            [Check out this YouTube video to learn more.](https://www.youtube.com/watch?v=vCNASTnM6p4)""")
                l_img = load_image("Images/Ableton.jpg")
                st.image(l_img)
                st.write("##")
                st.markdown("""
            2. **Logic Pro X:** An Apple-exclusive DAW, favored by many musicians and producers for its intuitive interface and powerful editing tools.
            [Check out this YouTube video to learn more.](https://www.youtube.com/watch?v=xKWdaSf9y5U)""")
                l_img = load_image("Images/Logic.jpg")
                st.image(l_img)
                st.write("##")
                st.markdown("""
            3. **Pro Tools:** A widely used industry-standard DAW for professional audio recording, mixing, and editing, often used in recording studios and post-production facilities.
            [Check out this YouTube video to learn more.](https://www.youtube.com/watch?v=2PPihcAHhgU)""")
                l_img = load_image("Images/Protools.jpg")
                st.image(l_img)
                st.write("##")
                st.write("""
            4. **FL Studio (Fruity Loops):** Popular among electronic music producers and beatmakers, it offers a user-friendly interface and a wide range of virtual instruments and effects.
            [Check out this YouTube video to learn more.](https://www.youtube.com/watch?v=6ZuBg6bmkhk)""")
                l_img = load_image("Images/fl.jpg")
                st.image(l_img)
                st.write("##")
                st.write("""
            5. **Cubase:** A feature-rich DAW with advanced MIDI capabilities, commonly used in music production and sound design.
            [Check out this YouTube video to learn more.](https://www.youtube.com/watch?v=XLqT286Gbng)""")
                l_img = load_image("Images/cubase.jpg")
                st.image(l_img)
                st.write("##")
                st.write(""" 
            6. **Reaper:** A lightweight and affordable DAW known for its customizability and support for a wide range of audio plugins.
            [Check out this YouTube video to learn more.](https://www.youtube.com/watch?v=_shjd4GBILo&t=51s)""")
                l_img = load_image("Images/reaper.jpg")
                st.image(l_img)
                st.write("##")
                st.write(""" 
            7. **Studio One:** Valued for its straightforward workflow and seamless integration with PreSonus hardware.
            [Check out this YouTube video to learn more.](https://www.youtube.com/watch?v=iIg5ngjPp-g&t=76s)""")
                l_img = load_image("Images/studioone.jpg")
                st.image(l_img)
                st.write("##")
                st.write(""" 
            These are just a few examples, and there are many other DAWs available, each with its own unique features and strengths. Users often choose a DAW based on their specific needs, preferred workflow, and the type of music or audio projects they wish to create.
                        """)
                st.write("---")
    else:
        if authentication_status == False:
            lm,cm, rm = st.columns(3)
            with cm:
                st.error("Incorrect Username/Password!!")
else:
    if not authentication_status:
        lm,cm, rm = st.columns(3)
        with cm:
            st.warning("Please Enter Your Credentials!!")