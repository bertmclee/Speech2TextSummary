# importing libraries 
import speech_recognition as sr 
import os   
from pydub import AudioSegment
from pydub.silence import split_on_silence 
  
# a function that splits the audio file into chunks 
# and applies speech recognition 
def silence_based_conversion(path, min_sil_len, sil_thresh, sil_duration, chunk_expand): 
  
    # open the audio file stored in 
    # the local system as a wav file. 
    song = AudioSegment.from_wav(path) 
  
    # open a file where we will concatenate   
    # and store the recognized text 
    fh = open("output_"+str(min_sil_len)+"_"+str(sil_thresh)+"_"+str(sil_duration)+"_"+str(chunk_expand)+".txt","w") 
          
    # split track where silence is 0.5 seconds  
    # or more and get chunks 

    chunks = split_on_silence(song, 
        min_silence_len = min_sil_len, 
        silence_thresh = sil_thresh,
        chunk_expansion = chunk_expand
    ) 
  
    # create a directory to store the audio chunks. 
    try: 
        os.mkdir('audio_chunks') 
    except(FileExistsError): 
        pass
  
    # move into the directory to 
    # store the audio files. 
    os.chdir('audio_chunks') 
  
    i = 0
    # process each chunk 
    for chunk in chunks: 
              
        # Create 0.5 seconds silence chunk 
        chunk_silent = AudioSegment.silent(duration = sil_duration) 
  
        # add 0.5 sec silence to beginning and  
        # end of audio chunk. This is done so that 
        # it doesn't seem abruptly sliced. 
        audio_chunk = chunk_silent + chunk + chunk_silent 
  
        # export audio chunk and save it in  
        # the current directory. 
        print("saving chunk{0}.wav".format(i)) 
        # specify the bitrate to be 192 k 
        audio_chunk.export("./chunk{0}.wav".format(i), bitrate ='192k', format ="wav") 
  
        # the name of the newly created chunk 
        filename = 'chunk'+str(i)+'.wav'
  
        print("Processing chunk "+str(i)) 
  
        # get the name of the newly created chunk 
        # in the AUDIO_FILE variable for later use. 
        file = filename 
  
        # create a speech recognition object 
        r = sr.Recognizer() 
  
        # recognize the chunk 
        with sr.AudioFile(file) as source: 
            # remove this if it is not working 
            # correctly. 
            r.adjust_for_ambient_noise(source) 
            audio_listened = r.listen(source) 
  
        try: 
            # try converting it to text 
            rec = r.recognize_google(audio_listened, language = 'zh-tw') 
            print("Text: "+rec+'\n')
            # write the output to the file. 
            fh.write(rec+". \n") 
  
        # catch any errors. 
        except sr.UnknownValueError: 
            print("Could not understand audio") 
  
        except sr.RequestError as e: 
            print("Could not request results. check your internet connection") 
        i += 1

    os.chdir('..') 
  
  
if __name__ == '__main__': 
    print('Enter the audio file path') 
    path = input() 

    # must be silent for at least 0.5 seconds 
    # or 500 ms. adjust this value based on user 
    # requirement. if the speaker stays silent for  
    # longer, increase this value. else, decrease it. 
    min_sil_len = 1200
    # consider it silent if quieter than -16 dBFS 
    # adjust this per requirement    
    sil_thresh = -42
    # add silence to beginning and  
    # end of audio chunk. This is done so that 
    # it doesn't seem abruptly sliced. 
    sil_duration =  0
    # expand the audio chunk    
    chunk_expand = 1000

    silence_based_conversion(path, min_sil_len, sil_thresh, sil_duration, chunk_expand)

      