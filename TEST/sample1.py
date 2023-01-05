from piano_transcription_inference import PianoTranscription, sample_rate, load_audio

# Load audio
inputpath=r'D:\standardizedPF\repositories\工作台\音乐库\tracks\G-DRAGON - 무제(无题) (Untitled, 2014) 2声道\accompaniment.wav'
(audio, _) = load_audio(inputpath, sr=sample_rate, mono=True)

# Transcriptor
transcriptor = PianoTranscription(device='cuda',checkpoint_path=r'D:\standardizedPF\repositories\piano_transcription\models\CRNN_note_F1=0.9677_pedal_F1=0.9186.pth')    # 'cuda' | 'cpu'

# Transcribe and write out to MIDI file
outputpath=r'D:\standardizedPF\repositories\工作台\音乐库\tracks\G-DRAGON - 무제(无题) (Untitled, 2014) 2声道\cut_liszt.mid'
transcribed_dict = transcriptor.transcribe(audio, outputpath)