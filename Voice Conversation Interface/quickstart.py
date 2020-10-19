# -*- coding: utf-8 -*-

#!/usr/bin/env python

# Copyright 2018 Google Inc. All Rights Reserved.
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

"""Google Cloud Text-To-Speech API sample application .
Example usage:
    python quickstart.py
"""





def run_quickstart(transfer):
    # [START tts_quickstart]
    """Synthesizes speech from the input string of text or ssml.
    Note: ssml must be well-formed according to:
        https://www.w3.org/TR/speech-synthesis/
    """
    from google.cloud import texttospeech

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()


    print("-",transfer,"-","전달받은 파라미터")
    
    #s = transfer ###
    if transfer == '안녕':
        s = "어서오세요, 박태준 도서관에 오신 것을 환영합니다."
        
    elif transfer == '혁신':
        s = "혁신의 용광로 책은 추천 도서란에 위치하고 있습니다. 저를 따라오세요."
    elif transfer == '혁신의':
        s = "혁신의 용광로 책은 추천 도서란에 위치하고 있습니다. 저를 따라오세요."
    elif transfer == '신간':
        s = "신간도서는 2층 메인 로비의 중앙에 위치합니다. 4번 위치로 제가 데려다드릴게요."
    elif transfer == '신가':
        s = "신간도서는 2층 메인 로비의 중앙에 위치합니다. 4번 위치로 제가 데려다드릴게요."
    elif transfer == '고마워':
        s = "별 말씀을요, 위치가 궁굼하다면 언제든지 제게 물어보세요!"

    elif transfer == '역사':
        s = "역사 장르는 2층 f6열에 위치하고 있어요, 저를 따라오세요."
    elif transfer == '해리 포터':
        s = "해리포터 책을 찾으시는군요,"
    elif transfer == '위치':
        s = "현재 위치는 2층 입구 앞입니다."
    elif transfer == '시간':
        s = "도서관 운영시간은 오전7시부터 밤12시까지입니다."
    else:
        s = "죄송하지만 알아듣지 못했어요."

    print(s)
    
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=s)
    
    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # OUTPUT = input("output.mp3")  #apple.mp3

    
    # The response's audio_content is binary.
    with open(s+".mp3", "wb") as out:
        
        # wb : binary 형태를 읽어주는 w는 이미 있는 파일 삭제하고 새로 실행

        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')

    return s
    # [END tts_quickstart]


"""if __name__ == "__main__":
    run_quickstart(transfer)
"""
