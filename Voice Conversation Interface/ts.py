#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Speech API sample application using the streaming API.

NOTE: This module requires the additional dependency `pyaudio`. To install
using pip:

    pip install pyaudio

Example usage:
    python transcribe_streaming_mic.py
"""

# [START speech_transcribe_streaming_mic]

from __future__ import division

#mp3 파일을 재생
from pygame import mixer

import re
import sys
from time import sleep

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
from six.moves import queue

import os

import quickstart as tts #

import time

#show map
import tkinter
import os
print (os.path.dirname(os.path.realpath(__file__)) ) #소스코드 파일 경로 출력

#direction key
import map_

# stt용 key
credential_path =r"/home/pi/Desktop/stt_tts/STT_TTS_KEY.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


# Global 미미짱
# transfer = ""


# Audio recording parameters
DEVICE = 2
CHANNELS =1
RATE = 44100#16000
CHUNK = int(RATE / 10)  # 100ms


class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)


def listen_print_loop(responses):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = ' ' * (num_chars_printed - len(transcript))
       

        if not result.is_final: ###
            sys.stdout.write(transcript + overwrite_chars + '/')
            sys.stdout.flush()

            num_chars_printed = len(transcript)
        

        else:
            print(transcript + overwrite_chars)

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r'\b(exit|끝)\b', transcript, re.I):
                print('Exiting..')
                

            num_chars_printed = 0


    # for문 끝나고 최종으로 나온 문장
    if (transcript + overwrite_chars) != None: 
       
        # transfer = ""
       
        transfer = transcript + overwrite_chars # 현재 transfer에 안녕 들어있음
        # 여기에 tts 코드 넣기
        credential_path =r"/home/pi/Desktop/stt_tts/STT_TTS_KEY.json"
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
        sentence = tts.run_quickstart(transfer) #s값 반환
        print("----------------------------------------------------")
        #오디오 바로 실행코드
        mixer.init()
        os.chdir("/home/pi/Desktop/stt_tts")
        mixer.music.load(sentence+".mp3")
        mixer.music.play()
        #show map
        if sentence == "역사 장르는 2층 f6열에 위치하고 있어요, 저를 따라오세요.":
            map_.key()
        elif sentence == "혁신의 용광로 책은 추천 도서란에 위치하고 있습니다. 저를 따라오세요.":
            map_.key()
        elif sentence == "신간도서는 2층 메인 로비의 중앙에 위치합니다. 4번 위치로 제가 데려다드릴게요.":
            map_.key()
        
            


        
            
        
            
def Audio_main():
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    language_code = 'ko-KR'  # a BCP-47 language tag

    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)

        # Now, put the transcription responses to use.

    listen_print_loop(responses)





            


if __name__ == '__main__':
    i=0
    while(i<10):
        # stt용 key
        credential_path =r"/home/pi/Desktop/stt_tts/STT_TTS_KEY.json"
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
        Audio_main()
        print("time sleep 6sec")
        time.sleep(6) #기다려라
        print("try next order")
        i = i+1

        

# [END speech_transcribe_streaming_mic]
