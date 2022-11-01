import streamlit as st
from speechkit import Session, ShortAudioRecognition, RecognitionLongAudio, SpeechSynthesis
from rev_ai import apiclient
import requests
import time

# examples
file_name_ru = 'data/NewYear1 (mp3cut.net).wav'
file_name_en = 'data/c_plus.mp3'

# rev ai speach to text
APIkeyREVAI = '02M4ifpxtVRxzZ3eUAEPlumovR6htX5bx7TaFu9G7N1TJFZi1c_5c7aQ8ZeulA9MmnAFvURZdqqTOQQ53FLJDCFGHyDm0'

# yandex voice kit
oauth_token = "y0_AgAAAABQ3UwxAATuwQAAAADRN7aBnbsd-FK3Ro-YRFPVG34yYsCy0xY"
catalog_id = "b1gije2etsfujf34tgvm"

# assemblyai
APIkeyAssemblyai = "bd1c2439243943489ee1e5a56c7d968c"


def read_file(file):
    with open(file, 'rb') as f:
        data = f.read()
    return data


def yandex_voice_kit():
    data = read_file(file_name_ru)
    session = Session.from_yandex_passport_oauth_token(oauth_token, catalog_id)
    recognizeShortAudio = ShortAudioRecognition(session)
    text = recognizeShortAudio.recognize(data, format='lpcm', sampleRateHertz='48000')
    return text


def getTextrevai():
    client = apiclient.RevAiAPIClient(APIkeyREVAI)
    job = client.submit_job_local_file(file_name_en)
    job_id = job.id
    while (job.status.name == 'IN_PROGRESS'):
        details = client.get_job_details(job_id)
        print("Job status: " + details.status.name)
        if (details.status.name == 'TRANSCRIBED'):
            data = client.get_transcript_text(job_id)
            return data
        if (details.status.name == 'FAILED'):
            print("Job failed: " + details.failure_detail)
            break
        time.sleep(30)


def getTextAssembyAI():
    UPLOAD_ENDPOINT = "https://api.assemblyai.com/v2/upload"
    TRANSCRIPTION_ENDPOINT = "https://api.assemblyai.com/v2/transcript"
    headers = {"authorization": APIkeyAssemblyai, "content-type": "application/json"}
    upload_response = requests.post(UPLOAD_ENDPOINT, headers=headers, data=read_file(file_name_en))
    audio_url = upload_response.json()["upload_url"]
    transcript_request = {'audio_url': audio_url}
    transcript_response = requests.post(TRANSCRIPTION_ENDPOINT, json=transcript_request, headers=headers)
    _id = transcript_response.json()["id"]
    while True:
        polling_response = requests.get(TRANSCRIPTION_ENDPOINT + "/" + _id, headers=headers)
        if polling_response.json()['status'] == 'completed':
            data = polling_response.json()['text']
            return data
            break
        elif polling_response.json()['status'] == 'error':
            raise Exception("Transcription failed. Make sure a valid API key has been used.")
        else:
            print("Transcription queued or processing ...")
        time.sleep(30)


st.markdown("# speach recognition")
option = st.selectbox(
    'choose methods', ('yandex voice kit', 'rev ai', 'AssembyAI'))

if st.button('do magic'):
    if option == 'yandex voice kit':
        st.write(yandex_voice_kit())
    elif option == 'rev ai':
        st.write(getTextrevai())
    elif option == 'AssembyAI':
        st.write(getTextAssembyAI())
