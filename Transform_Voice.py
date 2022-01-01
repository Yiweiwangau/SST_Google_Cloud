# use Google Speech-to-Text API to transform data in Google Cloud
def Speech_to_Text(filename):
    
    # Define the location using imported os.
    import os
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="D:\Onedrive\work\Interview\Weldclass\speech-to-text-336805-17456073e2b9.json"
    # Import Google cloud speech and storage service initialize the speech-to-text API
    from google.cloud import speech
    from google.cloud import storage
    speech_client = speech.SpeechClient()

    # define audio file location
    uri = 'gs://weldclass/Audio/'
    media_uri = uri+filename

    long_audi_wav = speech.RecognitionAudio(uri=media_uri)
    # define audio file configaration
    config_wav = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        enable_automatic_punctuation=True,
        language_code='en-US'
    )  
    # define the operation
    operation = speech_client.long_running_recognize(
        config=config_wav,
        audio=long_audi_wav
    )
    response = operation.result(timeout=20000)
    # print results in terminal
    for result in response.results:
        print(result.alternatives[0].transcript) # print the result
        print(result.alternatives[0].confidence) # confidence score
    ## define the name and location of text file saved
    client = storage.Client()
    bucket = client.get_bucket('weldclass')
    blob = bucket.blob('Transcript/'+filename.replace('.','_')+'.txt') 
    # save the result to a text file
    with blob.open(mode='w') as f:
        for result in response.results:
            f.write(result.alternatives[0].transcript+'\n')


Speech_to_Text("1.wav")