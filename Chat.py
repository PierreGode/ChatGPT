import openai
import speech_recognition as sr
from gtts import gTTS
import time

# initialize the API client with your API key
openai.api_key = "YOUR API KEY HERE"

# initialize the speech recognition engine
r = sr.Recognizer()

# function to convert voice commands to text
def transcribe_speech_to_text():
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except Exception as e:
        print("Error transcribing speech: ", e)
        return None

# function to generate audio from text
def generate_audio_from_text(text):
    tts = gTTS(text)
    tts.save("response.mp3")

# main loop to continuously listen for voice
# commands and generate audio responses
start_time = time.time()
questions_asked = 0
while True:
    elapsed_time = time.time() - start_time
    if elapsed_time >= 300:
        print("Time limit reached, waiting for the trigger word...")
        questions_asked = 0
        start_time = time.time()

    # transcribe voice command to text
    voice_command = transcribe_speech_to_text()
    if voice_command and "elsa" in voice_command.lower():
        # send text request to OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=voice_command,
            max_tokens=1024, n=1, stop=None,
            temperature=0.5,
        )
        # extract response text from API response
        response_text = response["choices"][0]["text"]
        print("Response: ", response_text)
        # generate audio from response text
        generate_audio_from_text(response_text)
        # play the audio file
        from os import system
        system("mpg321 response.mp3")

        questions_asked += 1
        if questions_asked >= 5:
            print("5 questions limit reached, waiting for the trigger word...")
            questions_asked = 0
    elif voice_command and "tell me more" in voice_command.lower():
        response_text = "I'm sorry, I'm not able to answer that right now. Can I help you with something else?"
        print("Response: ", response_text)
        # generate audio from response text
        generate_audio_from_text(response_text)
        # play the audio file
        from os import system
        system("mpg321 response.mp3")
