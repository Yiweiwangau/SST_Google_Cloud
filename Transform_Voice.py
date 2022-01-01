# use Google Speech-to-Text API to transform data in Google Cloud
def Speech_to_Text(filename):

    from google.cloud import speech
    from google.cloud import storage
    speech_client = speech.SpeechClient()

    # define audio file location
    uri = 'gs://weldclass/'
    media_uri = uri+filename

    long_audi_wav = speech.RecognitionAudio(uri=media_uri)
    # define audio file configaration
    config_wav = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        enable_automatic_punctuation=True,
        language_code='en-US'
    )  

    operation = speech_client.long_running_recognize(
        config=config_wav,
        audio=long_audi_wav
    )
    response = operation.result(timeout=20000)
    
    for result in response.results:
        print(result.alternatives[0].transcript) # print the result
        print(result.alternatives[0].confidence) # confidence score
    ## create a text file to store the result
    client = storage.Client()
    bucket = client.get_bucket('weldclass')
    blob = bucket.blob(filename.replace('.','_')+'.txt') 
    # 
    with blob.open(mode='w') as f:
        for result in response.results:
            f.write(result.alternatives[0].transcript)
    # with open('C:\Users\ty536\Desktop'+filename+'.txt', 'w') as f:
    #     f.write(result.alternatives[0].transcript)
    

Speech_to_Text("sample.wav")