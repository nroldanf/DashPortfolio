import base64
# import librosa
# import librosa.display
import numpy as np
# import matplotlib.pyplot as plt

def parse_contents(contents):
    _, content_string = contents.split(',')
    decoded = base64.b64decode(content_string).decode('ascii')
    return decoded


# def load_audio(audio_filename):
#     v_signal, fs = librosa.load(audio_filename, sr=None)
#     t = np.arange(0.0,len(v_signal)/fs,(1/fs))

#     return t, v_signal, fs

# def stft_save_image(signal, n_fft, fs, filename):
#     fft = librosa.stft(signal, n_fft=n_fft)  # STFT of y
#     S_db = librosa.amplitude_to_db(np.abs(fft), ref=np.max)

#     plt.figure(figsize=(20,4))
#     img = librosa.display.specshow(S_db, x_axis='time', y_axis='linear', sr=fs, hop_length=n_fft // 4)
#     plt.savefig("{}.png".format(filename), format='png', bbox_inches="tight", pad_inches=0)
#     plt.close()

#     with open("{}.png".format(filename), "rb") as f:
#         encoded_image = base64.b64encode(f.read()).decode('ascii')

#     return encoded_image