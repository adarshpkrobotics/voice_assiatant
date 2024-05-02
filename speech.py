import speech_recognition as sr
import datetime
import pyttsx3
import os
from pydub import AudioSegment
from pydub.playback import play
# Initialize the recognizer
recognizer = sr.Recognizer()

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to play a beep sound
def play_activation_sound():
    activation_sound = AudioSegment.from_file("examples_audio_activation.wav")
    play(activation_sound)

# Function to get the current time
def get_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak("The current time is " + current_time)

# Function to greet
def greet():
    speak("Hello! How can I assist you?")

# Function to handle unrecognized commands
def unrecognized():
    speak("I'm sorry, I didn't catch that.")

# Function to listen for the wake word
def listen_for_wake_word():
    with sr.Microphone() as source:
        print("Adjusting noise for wake word detection...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        while True:
            print("Listening for wake word...")
            audio = recognizer.listen(source)
            try:
                print("Recognizing wake word...")
                wake_word = recognizer.recognize_google(audio).lower()

                if "roya" in wake_word:  # Adjust the wake word as needed
                    print("Wake word detected!")
                    play_activation_sound()  # Play activation sound
                    listen_for_commands()  # Start listening for commands
                    break
                
            except sr.UnknownValueError:
                print("Sorry, I couldn't understand what you said.")
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))

# Main function to listen for commands
def listen_for_commands():
    with sr.Microphone() as source:
        print("Adjusting noise for command detection...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        
        if "time" in command:
            get_time()
        elif "hello" in command:
            greet()
        elif "hai" in command:  # Assuming "hai" is a greeting
            greet()
        else:
            unrecognized()
    
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        unrecognized()

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

# Call the function to start listening for the wake word
listen_for_wake_word()
