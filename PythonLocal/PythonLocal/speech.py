﻿#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr

def Listen():
	# obtain audio from the microphone
	r = sr.Recognizer()
	ret = ""

    # For Windows, add zero as parameter
	with sr.Microphone(0) as source:
		print("Say something!")
		audio = r.listen(source)

	# recognize speech using Google Speech Recognition
	try:
		# for testing purposes, we're just using the default API key
		# to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
		# instead of `r.recognize_google(audio)`
		sentence = r.recognize_google(audio)
		print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
		return True, sentence
	except sr.UnknownValueError:
		ret = "Google Speech Recognition could not understand audio"
	except sr.RequestError:
		ret = "Could not request results from Google Speech Recognition service"
	return False, ret


if __name__ == '__main__':
	(success, error) = Listen()
	if not success:
		print(error)
