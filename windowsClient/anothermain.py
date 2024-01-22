import speech_recognition as sr
import pyautogui as pyg
from audioplayer import AudioPlayer as adp
# Create a recognizer instance
Recognition = sr.Recognizer()

while True:
    print('Press CTRL+C to exit')
    try:
        with sr.Microphone() as Source:
            print('I am Ready to Listen')
            adp('windowsClient/audio/ting.mp3').play(block=True)
            print('I am Listening...')
            # listens for the user's input
            audio = Recognition.listen(Source)
            text = Recognition.recognize(audio)
            cmd = text.lower() # type: ignore
            if cmd == "exit":
                break
            else:
                pyg.write(text)
                print(text) 
    except LookupError:                                 # speech is unintelligible
        print("Could not understand audio")
        print('Exiting...')
        break   
   