import gradio as gr
import openai, config, subprocess
import re
from num2words import num2words
openai.api_key = config.OPENAI_API_KEY

def _conv_num(match):
    return num2words(match.group(), lang='es')

def numbers_to_words(text):
    return re.sub(r'\b\d+\b', _conv_num, text)

def test_transcribe(audio, rol, palabras):
    texto = "Esto es 12, 24, 260"

    return numbers_to_words(texto)

def transcribe(audio, rol, palabras):
    estilo = "Intenta responder con " + str(palabras) + " palabras o menos."
             
    messages = [{"role": "system", "content": rol + ". " + estilo}]
    audio_file = open(audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    messages.append({"role": "user", "content": transcript["text"]})

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    system_message = response["choices"][0]["message"]
    messages.append(system_message)

    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

    
    subprocess.call(["tts","--text", numbers_to_words(system_message['content']), "--model_name", "tts_models/es/css10/vits"])
    subprocess.call(["play", "tts_output.wav"])
    
    return chat_transcript

ui = gr.Interface(fn=transcribe, inputs=
    [ 
      gr.Audio(source="microphone", type="filepath"),
      gr.Dropdown(
            ["Eres un profesor de secundaria",
             "Eres un programador",
             "Eres un médico",
             "Eres un psicólogo",
             "Eres un abogado",
             "Eres un preparador de oposiciones de informática",
             "Eres un preparador físico",
             "Eres mi mejor amigo"
            ], label="Rol", value="Eres un profesor de secundaria", info="Indica el rol que tomará el asistente"
        ),
      gr.Number(100, label="Límite de palabras en la respuesta")
    ], outputs="text").launch()
ui.launch()
