#!/usr/bin/env python

import sys
import speech
import CoreNLP
import assistantdb

def Integrate(optional_message = None):
    if optional_message:
        sentence = optional_message
        print "Text input provided: '" + optional_message + "'"
    else:
        speech.speak('What can I help you with?', True)
        (success, sentence) = speech.listen()
        if not success:
            speech.speak(sentence, True)
            exit()
    sentence = sentence.replace("Start", "start").replace("open", "Open").replace("Show", "show").replace("Please", "").replace("please", "")
    (verb, verb_object, noun2, verb2, preposition) = CoreNLP.Parse(sentence)
    if preposition:
        verb = "%s %s" % (verb, preposition)
        verb_object = noun2
    print(verb, verb_object, verb2)
    assistantdb.parse(verb.lower(), verb_object.lower(), noun2.lower(), verb2.lower())

if __name__ == "__main__":
    if len(sys.argv) > 1:
        Integrate(" ".join(sys.argv[1:]))
    else:
        Integrate()
