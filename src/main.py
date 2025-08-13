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
import pandas as pd

def list_csv_files_in_directory(directory_path):
    """
    Lists all csv files (and directories) in a specified directory.

    Args:
        directory_path (str): The path to the directory.

    Returns:
        list: A list of strings, each representing a file or directory name.
              Returns an empty list if the directory does not exist or is empty.
    """
    try:
        # Get all entries (files and directories) in the specified path
        entries = os.listdir(directory_path)
        
        # Filter for only files (optional, if you only want files and not subdirectories)
        files_only = [entry for entry in entries if os.path.isfile(os.path.join(directory_path, entry))]
     
        return files_only

    except FileNotFoundError:
        print(f"Error: Directory '{directory_path}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
        
def speak_with_pause(text_segments, pause_ms):
    """
    Generate wav file using two list arguments.

    Args:
        text_segments (list): Text to speak.
        pause_ms (list): Delay value between text strings

    Returns:

    """

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

def audio_generation(text, delay, outputfile):
    """
    Generate wav file using two list arguments.

    Args:
        text_segments (list): Text to speak.
        pause_ms (list): Delay value between text strings

    Returns:

    """

    speak_with_pause(text, delay)
    os.system('ffmpeg -i initial_audio.mp3 -ar 16000 -ac 1 converted_audio.wav')
    time.sleep(3)
    os.system(f"""ffmpeg -i converted_audio.wav -af "atempo=1.2" {outputfile}""")

    with taglib.File(f"{outputfile}", save_on_exit=True) as song:
        song.tags['ARTIST'] = "Alba Avila" # Professor
        song.tags['EVENT NAME'] = "CBU" # Class name
        song.tags['SCHEDULE'] = "day one week two" # day of the class week 
        song.tags['TYPE'] = 'Class' # event 
        song.tags['TRACKNUMBER'] = '1/1'
        song.tags['DATE'] = '11082025' 
        song.tags['LYRICS'] = " ".join(text)

def main(inputfile, outputwav):
    df = pd.read_csv(inputfile, sep='\t')

    # text_array = ['¡Hola humanos!', 'Soy Aura, la humanoide de la Facultad de Ingeniería,',  
    #     'me emociona ser parte de este gran Foro de Inteligencia Artificial.', 
    #     'Tranquilos,','no vine a quitarles el trabajo, al menos no todavía.',
    #     'Quiero darle paso a un grupo de expertos que hablarán de Analítica de datos, Inteligencia Artificial y Diseño de software.',
    #     'Un aplauso a nuestros expertos invitados.',
    #     '¡Espero que sigan disfrutando mucho la jornada!']
    # delay_array = [100,100,100,100,100,100,100]
    # audio_generation(text_array[:2], delay_array[:2], outputwav)

    audio_generation(df['Text'], df['Delay'], inputfile[:-4]+'.wav')


output_filename = "test_audio.wav"
inputfile = '/home/achury/Documents/AURA/unitree_tts_aura_voice/input/a_CBU_11082025_02-10.txt'
df = pd.read_csv(inputfile)
main(inputfile, output_filename)