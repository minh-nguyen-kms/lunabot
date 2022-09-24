# Python program to translate
# speech to text and text to speech


import speech_recognition as sr
import pyttsx3

# Initialize the recognizer
r = sr.Recognizer()

# Initialize the text to speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', 'english+f3')
rate = engine.getProperty('rate')
volume = engine.getProperty('volume')
engine.setProperty('volume', volume + 0.25)
engine.setProperty('rate', rate - 40)

# Function to convert text to
# speech
def SpeakText(command):
    engine.say(command)
    engine.runAndWait()

# Loop infinitely for user to
# speak

while(1):
    
    # Exception handling to handle
    # exceptions at the runtime
    try:
        
        # use the microphone as source for input.
        with sr.Microphone() as source2:
            
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source2, duration=0.2)
            
            #listens for the user's input
            audio2 = r.listen(source2)
            print("I'm thinking")
            
            # Using google to recognize audio
            MyText = r.recognize_google(audio2) 
            # MyText = r.recognize_sphinx(audio2) //too bad
            MyText = MyText.lower()

            print("Did you say "+MyText)
            SpeakText(MyText)
            
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        
    except sr.UnknownValueError:
        print("I don't understand. Please repeat your question")
