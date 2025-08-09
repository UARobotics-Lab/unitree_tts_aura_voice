"""
@file main.py
@author Alvaro Achury - Uniandes - UARoboticsLab
@date 2025-08-209
@version 1.1
@brief TTs a partir de archivo csv en formato wav compatible con robot AURA-UnitreeG1.

"""

from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import os
import time
import taglib

output_filename = "test_audio.wav"
def speak_with_pause(text_segments, pause_ms):
    from tempfile import NamedTemporaryFile
    from pydub import AudioSegment
    combined = AudioSegment.empty()
    i = 0
    for segment in text_segments:
        tts = gTTS(segment, lang='es')
        
        with NamedTemporaryFile(delete=True, suffix=".mp3") as f:
            tts.save(f.name)
            audio = AudioSegment.from_file(f.name)
            print(f"*** {segment} ... {i} __ {len(text_segments)}")
            if (i+1) < len(text_segments):
                combined += audio + AudioSegment.silent(duration=pause_ms[i])
            else:
                combined += audio + AudioSegment.silent(duration=0)
            i += 1

    combined.export("initial_audio.mp3", format="mp3")

text_array = ['¡Hola humanos!', 'Soy Aura, la humanoide de la Facultad de Ingeniería,',  
    'me emociona ser parte de este gran Foro de Inteligencia Artificial.', 
    'Tranquilos,','no vine a quitarles el trabajo, al menos no todavía.',
    'Quiero darle paso a un grupo de expertos que hablarán de Analítica de datos, Inteligencia Artificial y Diseño de software.',
    'Un aplauso a nuestros expertos invitados.',
    '¡Espero que sigan disfrutando mucho la jornada!']
delay_array = [100,100,100,100,100,100,100]

speak_with_pause(text_array[:2], delay_array[:2])

os.system('ffmpeg -i initial_audio.mp3 -ar 16000 -ac 1 converted_audio.wav')
time.sleep(3)
os.system(f"""ffmpeg -i converted_audio.wav -af "atempo=1.2" {output_filename}""")

  
with taglib.File(f"/home/achury/Documents/AURA/unitree_tts_aura_voice/{output_filename}", save_on_exit=True) as song:
    song.tags['ARTIST'] = "Alba Avila" # Professor
    song.tags['ALBUM'] = "CBU" # Class name
    song.tags['TITLE'] = "day one week two" # day of the class week 
    song.tags['GENRE'] = 'Class' # event 
    song.tags['TRACKNUMBER'] = '1/1'
    song.tags['DATE'] = '11082025' 
    song.tags['LYRICS'] = " ".join(text_array)
