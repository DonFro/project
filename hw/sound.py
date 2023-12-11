import librosa
import soundfile as sf
import os
def convert_wav(file_path):
    # Check the file format
    _, file_extension = os.path.splitext(file_path)

    if file_extension.lower() == '.wav':
        print("File is already in WAV format.")
        return file_path

    if file_extension.lower() in ['.mp3', '.aac']:
        print(f"Converting {file_path} to WAV...")
        # Load audio using LibROSA
        audio, sr = librosa.load(file_path, sr=None)

        # Create a new file path for the WAV file
        wav_file_path = os.path.splitext(file_path)[0] + ".wav"

        # Save the audio in WAV format using soundfile library
        sf.write(wav_file_path, audio, sr)
        print(f"File converted to WAV: {wav_file_path}")

        return wav_file_path
    else:
        print("Unsupported file format. Please provide a .wav, .mp3, or .aac file")
        return None


# Replace 'file_path' with the path to your audio file
file_path = input("")  # Replace this with your file path

converted_file_path = convert_wav(file_path)
