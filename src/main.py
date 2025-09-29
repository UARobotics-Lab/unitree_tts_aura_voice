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
from tempfile import NamedTemporaryFile
from pydub import AudioSegment

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


    combined = AudioSegment.empty()
    if os.path.exists('initial_audio.mp3'):
        os.remove('initial_audio.mp3')

    i = 0
    for segment in text_segments:
        tts = gTTS(segment, lang='es')
        
        with NamedTemporaryFile(delete=True, suffix=".mp3") as f:
            tts.save(f.name)
            audio = AudioSegment.from_file(f.name)
            print(f"*** {segment} ... {i} __ {len(text_segments)}")
            print("Time --- ",pause_ms[i])
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
    if os.path.exists('converted_audio.wav'):
        os.remove('converted_audio.wav')

    os.system('ffmpeg -i initial_audio.mp3 -ar 16000 -ac 1 converted_audio.wav')
    time.sleep(3)
    os.system(f"""ffmpeg -i converted_audio.wav -af "atempo=1.2" {outputfile}""")
    time.sleep(3)
    with taglib.File(f"{outputfile}", save_on_exit=True) as song:
        song.tags['ARTIST'] = "AXA" # Professor
        song.tags['EVENT NAME'] = "AXA" # Class name
        song.tags['SCHEDULE'] = "day one week two" # day of the class week 
        song.tags['TYPE'] = 'Class' # event 
        song.tags['TRACKNUMBER'] = '1/1'
        song.tags['DATE'] = '11082025' 
        song.tags['LYRICS'] = " ".join(text)
    time.sleep(3)

def main(inputfile, outputwav):
    df = pd.read_csv(inputfile, sep='\t', encoding='utf-8')

    print(f"{df['Delay']}  ---  {df['Text']} ")
    if os.path.exists(outputwav):
        while True:
            delete_verification = input("Would you like to replace the existing file? (Y/N)").lower()
            if delete_verification == "y":
                os.remove(outputwav)
                audio_generation(df['Text'], df['Delay'], outputwav)
                break
            if delete_verification not in ['y', 'n']:
                print("Invalid character!")
    else:                
        audio_generation(df['Text'], df['Delay'], outputwav)



main_path = os.getcwd()
print(main_path + '/../input/')
input_folder_path = os.path.join(main_path, '..', 'input/')
output_folder_path = os.path.join(main_path, '..', 'output/')
# audio_files_path = '/home/achury/Documents/AURA/unitree_tts_aura_voice/input/ICYA/'

try:
    os.path.exists(input_folder_path)
    folder_name = input("Enter the name of the folder containing the text files to be converted into audio... ")
    text_folder_path = os.path.join(input_folder_path, folder_name)
    audio_folder_path = os.path.join(output_folder_path, folder_name)
    os.makedirs(audio_folder_path, exist_ok=True)
    file_list = list_csv_files_in_directory(text_folder_path)
    input(f"{file_list}")
    for inputfile in file_list:
        input_file_path = os.path.join(text_folder_path, inputfile)
        output_file_path = os.path.join(audio_folder_path, inputfile[:-3] + "wav")
        print(f"¡¡¡ {inputfile}")
        # df = pd.read_csv(input_file_path, encoding='latin1')
        
        main(input_file_path, output_file_path)
        if os.path.exists('initial_audio.mp3'):
            os.remove('initial_audio.mp3')
        if os.path.exists('converted_audio.wav'):
            os.remove('converted_audio.wav')
    # inputfile = '/home/achury/Documents/AURA/unitree_tts_aura_voice/input/a_CBU_11082025_02-10.txt'


except:
    print("Check that the execution location exist and that the input folder exists!")
