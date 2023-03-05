import streamlit as st
# import whisper
from streamlit_extras.add_vertical_space import add_vertical_space
# from googletrans import Translator
# import torch
import os
import azure.cognitiveservices.speech as speechsdk
from audio_recorder_streamlit import audio_recorder
import openai
import whisper


model_names = {
    "Tiny (English only)": 'tiny.en', 
    "Tiny": 'tiny', 
    "Base (English only)":'base.en',
    "Base": 'base', 
    "Small (English only)":'small.en',
    "Small": 'small',
    "Medium (English only)":'medium.en',
    "Medium": 'medium',
    "Large": 'large'
}

selected_model = st.sidebar.selectbox("Select a Model (Larger models take longer but are more accurate)", ('Medium', 'Tiny (English only)', 'Tiny', 'Base (English only)', 'Base', 'Small (English only)', 'Small', 'Medium (English only)', 'Large'))


@st.cache_data(show_spinner=False)
def generate_subtitle(path):
    model = whisper.load_model(model_names[selected_model])
    res = model.transcribe(path)
    return res


st.write("<style>h1{text-align:center;}</style>", unsafe_allow_html=True)
st.title("🗣 AI English teacher")
add_vertical_space(3)

model_dict = {
    'English (Austrilia)Natasha (Female)': 'en-AU-NatashaNeural',
    'English (Austrilia)William (Male)': 'en-AU-WilliamNeural',
    'English (India)Neerja (Female)':'en-IN-NeerjaNeural',
    'English (India)Prabhat (Male)':'en-IN-PrabhatNeural',
    'English (United Kingdom)Hollie (Female)':'en-GB-HollieNeural',
    'English (United Kingdom)Ryan (Male)':'en-GB-RyanNeural',
    'English (United States)Jenny (Female)':'en-US-JennyNeural',
    'English (United States)Jason (Male)':'en-US-JasonNeural',
    'Chinese (Mandarin, Simplified)Xiaomeng (Female)-晓萌':'zh-CN-XiaomengNeural',
    'Chinese (Mandarin, Simplified)Yunhao (Male)-云浩':'zh-CN-YunhaoNeural',
    'Chinese (Northeastern Mandarin, Simplified)Xiaobei (Female)-晓蓓':'zh-CN-liaoning-XiaobeiNeural',
    'Chinese (Cantonese, Simplified)XiaoMin (Female)-晓敏':'yue-CN-XiaoMinNeural',
    'Chinese (Cantonese, Simplified)YunSong (Male)-云松':'yue-CN-YunSongNeural',
}

selected_language = st.sidebar.selectbox("Language", ('English (Austrilia)', 'English (India)', 'English (United States)', 'English (United Kingdom)'))
if selected_language == 'English (Austrilia)':
    selected_voice = st.sidebar.selectbox("Voice", ('Natasha (Female)', 'William (Male)'))
elif selected_language == 'English (India)':
    selected_voice = st.sidebar.selectbox("Voice", ('Neerja (Female)', 'Prabhat (Male)'))
elif selected_language == 'English (United Kingdom)':
    selected_voice = st.sidebar.selectbox("Voice", ('Hollie (Female)', 'Ryan (Male)'))
elif selected_language == 'English (United States)':
     selected_voice = st.sidebar.selectbox("Voice", ('Jenny (Female)', 'Jason (Male)'))
elif selected_language == 'Chinese (Mandarin, Simplified)':
     selected_voice = st.sidebar.selectbox("Voice", ('Xiaomeng (Female)-晓萌', 'Yunhao (Male)-云浩'))
elif selected_language == 'Chinese (Northeastern Mandarin, Simplified)':
     selected_voice = st.sidebar.selectbox("Voice", ('Xiaobei (Female)-晓蓓', ))
elif selected_language == 'Chinese (Cantonese, Simplified)':
     selected_voice = st.sidebar.selectbox("Voice", ('XiaoMin (Female)-晓敏', 'YunSong (Male)-云松'))
    
    
# # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
# speech_config = speechsdk.SpeechConfig(subscription="da388ea1b54e4fb398c3818f568db437", region="eastus")
# audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
# # The language of the voice that speaks.
# speech_config.speech_synthesis_voice_name=model_dict[selected_language+selected_voice]
# speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)


audio_bytes = audio_recorder()
if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")

text = generate_subtitle(audio_bytes)
st.write(text)
# Get text from the console and synthesize to the default speaker.
# text = st.text_input("Input", placeholder="Enter some text that you want to speak >", label_visibility="hidden")
# text = st.text_area("Input", placeholder="Enter some text that you want to speak >", label_visibility="hidden", height=150, max_chars=500)

# if text:
#     speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
#     # if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
#     #     st.write("Speech synthesized for text [{}]".format(text))
#     if speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
#         cancellation_details = speech_synthesis_result.cancellation_details
#         st.warning("Speech synthesis canceled: {}".format(cancellation_details.reason))
#         if cancellation_details.reason == speechsdk.CancellationReason.Error:
#             if cancellation_details.error_details:
#                 st.error("Error details: {}".format(cancellation_details.error_details))
#                 st.warning("Did you set the speech resource key and region values?")

#     filename = "downloads/result.wav"
#     with open(filename, "wb") as f:
#         f.write(speech_synthesis_result.audio_data)
    
#     st.audio(filename)

