import gtts
from pydub import AudioSegment
import speech_recognition as sr

def ogg2wav(ofn):
    wfn = ofn.replace('.off', '.wav')
    segment = AudioSegment.from_file(ofn)
    segment.export(wfn, format='wav')

def speech_to_text(audio_file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language="ru-RU")
        return text

