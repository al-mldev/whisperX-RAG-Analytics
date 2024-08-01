<p style="text-align: center; font-size: 25px; font-weight: bold;  color: #FFFFFF;">Whisper-x Metrics </p>


 Metrics project is designed to evaluate the performance of the speech to text process using a pretrained whisper faster model with [Whisper-X](https://github.com/m-bain/whisperX) pipeline developed by [@m-bain](https://github.com/m-bain/) to generate the transcription and diarization of the audio conversation. The objective is to provide a framework for process the audio files as a batch load, generate the transcription, retrieve the diarization objects, and store them in a non-rel database, then evaluate the performance metrics of the transcription process within the loaded model. The module metrics can calculate the real time factor (RTF) for the audio file and if reference data is available the word error rate (WER) and character error rate (CER) can be calculated and stored into the database. The utils module allows to load whisper models that can be downloaded from huggingface, or manually copy into `models/` directory, and then transform it into whisper faster format. It can run transcriptions with mutiple models to the same audio and evaluate their individual performance based on the metrics. This speech to text process can be implemented into a ETL cycle for a large audio batch, generate new transcriptions, correct them and use as tagged audios for feed the training datasets for your models. 
 


<p style="text-align: center; font-size: 25px; font-weight: bold;  color: #FFFFFF;">Architecture</p>


![Pipeline](images\Architecture.png)



<p style="text-align: center; font-size: 25px; font-weight: bold;  color: #FFFFFF;">Instructions</p>

<p style="text-align: left; font-size: 20px; font-weight: bold;  color: #FFFFFF;">Previous settings:</p>


<p style="text-align: left; font-size: 16px; font-weight: bold;  color: #FFFFFF;">1) Set local environment</p>

This version runs in a standalone windows local machine, but could run into a virtual environment.The needed dependencies are in requirements.txt, this specific code runs with whisperx 3.1.2, python 3.8. and CUDA 11.8. and the latest version of ffmpeg. 

`pip install -r requirements.txt`

<p style="text-align: left; font-size: 16px; font-weight: bold;  color: #FFFFFF;">2) Set Mongo DB</p>

Install mongodb and mongo compass, create the database `'whisperx'` then set the localhost uri (make sure to match with the one set in the connections of the project) and then run create_collections.py for insert the collections schema into the created database. 

<p style="text-align: left; font-size: 20px; font-weight: bold;  color: #FFFFFF;">Menu:</p>

Once you have your local environment and the connection to mongodb with the created collections make sure to prepare correctly the settings by checking the following steps. 

<p style="text-align: left; font-size: 16px; font-weight: bold;  color: #FFFFFF;">1) Load models</p>

On main.py set `hf_token` with your huggingface token, and `model_name` the huggingface uri of yout desired pretrained model available in their site, the current model set for download is whisper tiny english once selectedz both run main.py then select the option 1 in menu to download the whisper model, and then convert to whisper faster format. You can also load manually in models directory. 

<p style="text-align: left; font-size: 16px; font-weight: bold;  color: #FFFFFF;">2) Load audios</p>

Copy your audios in `local_input_batch/audio_batch/`, make sure to use mp3 format. Then select option 2 in menu, you should see the new audio files in the database, in the `audio_files` collection. 

INSERT AUDIO FILES PICTURE 

<p style="text-align: left; font-size: 16px; font-weight: bold;  color: #FFFFFF;">3) Load references</p>

This is an optional step, you have manually corrected transcriptions, for the audio, copy your referene files into `local_input_batch/reference_batch/`, make sure to name `R-<audioname>.txt`. Select the option 3 in menu, provide the `audio_id` generated in the database for the asociated mp3 file previously loaded, then you should see the reference in `references` collection.    


<p style="text-align: left; font-size: 16px; font-weight: bold;  color: #FFFFFF;">4) Run transcriptions</p>

Once all setup, select option 4 in menu then run the transcription. If references are not available, word and character error rate wont be calculated. 

Note: The ouput_text returns the not aligned text used as a reference format, you can check an example on `local_input_batch/reference_batch/R-audioexample.txt`, so if the model generate a 'visually consistent' transcription this new text can be used as a base to make a manual reference then calculate the wer and cer to the transcription asociated to the specific downloaded model. 




