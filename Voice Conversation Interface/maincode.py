import transcribe_streaming_mic2 as stt
import quickstart as tts

import os


credential_path =r"C:\Users\iwant\Desktop\SST_env\STT_key.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path



stt.Audio_main()









credential_path =r"C:\Users\iwant\Desktop\TTS_env\tts_key.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path



  
tts.run_quickstart()
