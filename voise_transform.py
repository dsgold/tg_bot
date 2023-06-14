import whisper


def textFromVoice(path):
    model = 'medium'
    speech_model = whisper.load_model(model)
    result = speech_model.transcribe(path, fp16=False, language='russian')
    return result['text']

