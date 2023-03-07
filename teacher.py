import gradio as gr
import openai, config, subprocess
openai.api_key = config.OPENAI_API_KEY



def transcribe(audio, rol):
    estilo = " Intenta responder con 100 palabras o menos. Si indicas números escríbelos como texto, por ejemplo: uno, dos, tres,..."
             
    messages = [{"role": "system", "content": rol + estilo}]
    audio_file = open(audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    messages.append({"role": "user", "content": transcript["text"]})

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    system_message = response["choices"][0]["message"]
    messages.append(system_message)

    subprocess.call(["tts","--text", system_message['content'], "--model_name", "tts_models/es/css10/vits"])
    subprocess.call(["play", "tts_output.wav"])

    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

    return chat_transcript

ui = gr.Interface(fn=transcribe, inputs=
    [ 
      gr.Audio(source="microphone", type="filepath"),
      gr.Dropdown(
            ["Eres un profesor de secundaria.",
             "Eres un médico.",
             "Eres un psicólogo."
            ], label="Rol", info="Indica el rol que tomará el asistente"
        )
    ], outputs="text").launch()
ui.launch()
