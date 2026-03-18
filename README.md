# Audio Para Texto

---

O presente repositório tem como objetivo aplicar o Faster Whisper para transcrever conversação de audio para texto. A conversação esta presente apenas em um channel de conversa, então não houve a necessidade de tracsrever mais canais de comunicação e demais pre-processamento de audio com libs como librosa.

Além da tradução do audio, neste repositório existe a implementação de transcrição utilizando o Spark para paralelizar o processo de transcrição em ambientes de big data, unindo o poder de uma engine distribuida com o Faster Whisper. 
