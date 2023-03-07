import gradio as gr
import openai, config, subprocess
openai.api_key = config.OPENAI_API_KEY



def transcribe(audio, rol):
    messages = [{"role": "system", "content": rol}]
    audio_file = open(audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    messages.append({"role": "user", "content": transcript["text"]})

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    system_message = response["choices"][0]["message"]
    print(system_message)
    messages.append(system_message)

    #engine = pyttsx3.init()
    #voices = engine.getProperty('voices')
    #engine.setProperty('voice', 'spanish')
    #engine.say(system_message['content'].replace("\n", ""))
    #engine.runAndWait()

    #  tts --text "Ya ha venido Marcos!" --model_name "tts_models/es/css10/vits"
    subprocess.call(["tts","--text", system_message['content'], "--model_name", "tts_models/es/css10/vits"])
    # Falta reproducir con vlc
    subprocess.call(["play", "tts_output.wav"])
    #subprocess.call(["spd-say", "-t", "female3", "-l", "es", "\"" + system_message['content'] + "\""])

    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

    return chat_transcript

ui = gr.Interface(fn=transcribe, inputs=
    [ 
      gr.Audio(source="microphone", type="filepath"),
      gr.Textbox(label="Rol", 
                 info="Initial text",
                 lines=1,
                 value="Eres un profesor de secundaria. Intenta responder con 100 palabras o menos.")
    ]
    , outputs="text").launch()
ui.launch()
