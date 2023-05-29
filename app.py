import streamlit as st
import os
import time
import glob
import os
import subprocess
import whisper
from whisper.utils import write_vtt
import openai

#from gtts import gTTS
from gtts import *
from googletrans import Translator

try:
    os.mkdir("temp")
except:
    pass

st.markdown('<h3 style="text-align:center;text-decoration: lightblue underline;font-size:60px;color:red">Nairo24 <span style="color:#4f9bce;font-weight:bolder;font-size:60px;"> News</span></h3>',unsafe_allow_html=True)

st.title("Text to speech")
translator = Translator()

# Add an image
image = "Nairo24.png"
st.image(image, caption="", use_column_width=True)

text = st.text_area("Enter text", value="", height=200)
in_lang = st.selectbox(
    "Select your input language",
    ("English", "Hindi", "Bengali", "korean", "Chinese", "Japanese"),
)
if in_lang == "English":
    input_language = "en"
elif in_lang == "Hindi":
    input_language = "hi"
elif in_lang == "Bengali":
    input_language = "bn"
elif in_lang == "korean":
    input_language = "ko"
elif in_lang == "Chinese":
    input_language = "zh-cn"
elif in_lang == "Japanese":
    input_language = "ja"

out_lang = st.selectbox(
    "Select your output language",
    ("English", "Hindi", "Bengali", "korean", "Chinese", "Japanese"),
)
if out_lang == "English":
    output_language = "en"
elif out_lang == "Hindi":
    output_language = "hi"
elif out_lang == "Bengali":
    output_language = "bn"
elif out_lang == "korean":
    output_language = "ko"
elif out_lang == "Chinese":
    output_language = "zh-cn"
elif out_lang == "Japanese":
    output_language = "ja"

english_accent = st.selectbox(
    "Select your english accent",
    (
        "Default",
        "India",
        "United Kingdom",
        "United States",
        "Canada",
        "Australia",
        "Ireland",
        "South Africa",
    ),
)

if english_accent == "Default":
    tld = "ca"
elif english_accent == "India":
    tld = "co.in"

elif english_accent == "United Kingdom":
    tld = "co.uk"
elif english_accent == "United States":
    tld = "com"
elif english_accent == "Canada":
    tld = "ca"
elif english_accent == "Australia":
    tld = "com.au"
elif english_accent == "Ireland":
    tld = "ie"
elif english_accent == "South Africa":
    tld = "co.za"


def text_to_speech(input_language, output_language, text, tld):
    translation = translator.translate(text, src=input_language, dest=output_language)
    trans_text = translation.text
    tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, trans_text


display_output_text = st.checkbox("Display output text")

if st.button("convert"):
    result, output_text = text_to_speech(input_language, output_language, text, tld)
    audio_file = open(f"temp/{result}.mp3", "rb")
    audio_bytes = audio_file.read()
    st.markdown(f"## Your audio:")
    st.audio(audio_bytes, format="audio/mp3", start_time=0)

    if display_output_text:
        st.markdown(f"## Output text:")
        st.write(f" {output_text}")

    # Add download button for the generated MP3 file
    st.download_button("Download MP3", data=audio_bytes, file_name=f"{result}.mp3")


def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)
                
remove_files(7)



###MULTILINGUAL AI. FOR ADDING CAPTIONS TO VIDEOS###

#Download the model
#model = whisper.load_model("medium")




openai.api_key = "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"

models = openai.Model.list()
model = None

for model in models:
    if model["model_name"] == "whisper":
        model = model
        break

if model is None:
    raise ValueError("Model not found in the list of available models.")
    
def video2mp3(video_file, output_ext="mp3"):
    filename, ext = os.path.splitext(video_file)
    subprocess.call(["ffmpeg", "-y", "-i", video_file, f"{filename}.{output_ext}"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)
    return f"{filename}.{output_ext}"


def translate(input_video):
    audio_file = video2mp3(input_video)

    options = dict(beam_size=5, best_of=5)
    translate_options = dict(task="translate", **options)
    result = model.transcribe(audio_file, **translate_options)

    output_dir = '/content/'
    audio_path = audio_file.split(".")[0]

    with open(os.path.join(output_dir, audio_path + ".vtt"), "w") as vtt:
        write_vtt(result["segments"], file=vtt)

    subtitle = audio_path + ".vtt"
    output_video = audio_path + "_subtitled.mp4"

    os.system(f"ffmpeg -i {input_video} -vf subtitles={subtitle} {output_video}")

    return output_video


st.title("MultiLingual AI: Add Caption to Videos")

uploaded_file = st.file_uploader("Upload your video", type=["mp4"])

if uploaded_file is not None:
    st.video(uploaded_file)
    if st.button("Generate Subtitle Video"):
        # Save uploaded file to a temporary location
        with open("temp_video.mp4", "wb") as f:
            f.write(uploaded_file.read())

        output_video = translate("temp_video.mp4")

        # Display the output video
        st.video(output_video)

        # Remove temporary files
        os.remove("temp_video.mp4")

st.markdown(
    '''
    <style>
    .footer {
        font-size: 12px;
        color: #888888;
        text-align: center;
    }
    </style>
    <div class="footer">
        <p>Powered by <a href="https://openai.com/" style="text-decoration: underline;" target="_blank">OpenAI</a> - Developer Tel: <a style="text-decoration: underline;" target="_blank">+254704205553</a>
                    </p>
    </div>
    ''',
    unsafe_allow_html=True
)
   


