import socket
from glob import glob
from time import sleep
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql import functions as pf
from faster_whisper import WhisperModel

model = None

def get_model():
    from faster_whisper import WhisperModel
    global model
    
    if model is None:
        model = WhisperModel(
            "/tmp/model/",
            device="cpu",
            compute_type="int8"
        )

    return model

def transcribe_audio(file_path):
    model = get_model()

    segments, _ = model.transcribe(
        file_path,
        language="pt",
        #vad_filter=True,
        condition_on_previous_text=False,
    )

    full_text = " ".join([segment.text for segment in segments])

    return full_text

def process_partition(iterator):
    hostname = socket.gethostname()

    for row in iterator:
        file_path = row.file_path
        
        try:
            transcription = transcribe_audio(file_path)
            dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            yield (
                file_path,
                hostname,
                transcription,
                dt
            )

        except Exception as e:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            yield (
                file_path,
                hostname,
                f"ERRO: {str(e)}",
                dt
            )


if __name__ == "__main__":
    spark = SparkSession.builder.appName("MyApp") \
    .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.AnonymousAWSCredentialsProvider") \
    .config("spark.sql.execution.pyspark.udf.faulthandler.enabled", "true") \
    .getOrCreate()

    wav_files = glob("/tmp/sample-audios/*.wav")
    df = spark.createDataFrame([(f,) for f in wav_files], ["file_path"])

    print("Number of partitions: ", df.rdd.getNumPartitions())
    df = df.repartition(4)

    df = spark.createDataFrame(
        df.rdd.mapPartitions(process_partition),
        ["file_path", "hostname", "transcription", "datetime"]
    )

    df.select(
        "file_path",
        "hostname",
        "datetime",
        "transcription"
    ).orderBy(
        "datetime"
    ).show(truncate=True)
