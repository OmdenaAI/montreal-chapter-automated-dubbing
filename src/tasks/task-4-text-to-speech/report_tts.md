## Task 4 - text-to-speech
The scope of this task is to convert the translated text to speech based on timestamp and voice type(male/female). 
 

| Team       |           |
| ------------- |-------------|
| Lead       | Divya Muthu Krishnan          |
| Co-lead | Sherya Kommuri|
| Collaborators |Vishnu Vardhan, Benito Martin, Winston   | 

Our collaborators researched various libraries/APIs. One of our collaborators, Winston summarized its advantages and disadvatages of the following models. 
1. Tacotron2 / HiFIGAN
2. Fastspeech / MelGAN
3. speech T5 model

The document can be found in notion folder. https://www.notion.so/Task-04-Text-to-Speech-33827e93ec9f42348751a344a02d825f

Benito Martin, Vishnu Vardhan, Winston, Shreya Kommuri explored various models from different libraries and uploaded the code in the examples folder under our task folder. https://github.com/OmdenaAI/montreal-chapter-automated-dubbing/tree/main/src/tasks/task-4-text-to-speech/Examples

There are many approaches that can be used to convert the text to speech. We focused on the approach of converting the text to  Mel Spectrogram and then to speech (Vocoder). Since there are many pretrained models available for generating spectrogram and voice we used the existing models instead of training from scratch.

Below are the frameworks that are experimented by our collaborators.
| Collaborator        | Framework/API           |
| ------------- |-------------|
| Vishnu Vardhan|Speechbrain, Meta-MMS   | 
| Benito Martin | SileroTTS, Couqui_ai_tts, pyttsx3      | 
| Sherya Kommuri | Speech T5      | 
| Winston | pyttsx3      |
| Divya Muthu Krishnan|edge-tts | 

We tried different models from the above frameworks and we agreed to work on Tacotron model for mel-spectrogram generation and HiFIGAN as vocoder to generate the audio from the mel-spectrogram. But there were few issues. 
- The model is not multi speaker model. The voice generated was good for female voice. But for converting it to a male voice, we had to change the sample rate which compromises the quality. 
- Since we use 3 languages(English, french, spanish) in our dubbing app we need to use 3 models for generating mel spectrogram and atleast 1 model for vocoder(1 in case of waveglow and 3 in case of GAN model)

Considering the storagespace and the processing speed we switched to the edge-tts API since it has below advantages. 
- edge-tts API supports many languages. 
- Since it is an API, it is very fast and there is no need of storage space to save the models. 
- We tested the quality of the speech in English, Arabic and Tamil. The generated speech quality was very good for both male and female voice.

The only issue is edge-tts is not released by microsoft itself. So far the API is working fine but it could break down if  there are any updates in microsoft service in the future and the API is not updated accordingly.

While concatenating the generated audio segments based on the time stamp we faced an issue. The audio generated sometimes overlapped because of the difference in speaking rate of the original audio and the generated audio. Vishnu Vardhan implemented a solution by changing the speed of the speech generated so that the speech generated would fit into the time stamp. That worked well and fit properly in the time stamp. However, in some audio segments, the generated audio was very slow and was not clear so there was some inconsistency. Based on the suggestion by Mohammed Kandil, translation team used llms to summarise the text translated to fit in the time stamp so that we simply generated the speech from the text and concatenated it based on the timestamps.


