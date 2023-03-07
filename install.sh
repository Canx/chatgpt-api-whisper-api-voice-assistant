#!/bin/bash
pip -r install requirements
tts --text "Hola" --model_name "tts_models/es/css10/vits"
sudo apt install sox
