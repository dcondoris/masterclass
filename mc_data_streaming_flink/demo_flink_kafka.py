import logging
import sys
import json
import re

from pyflink.common import Types,SimpleStringSchema,WatermarkStrategy, Time, Encoder
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaSink,KafkaOffsetsInitializer,KafkaRecordSerializationSchema
from pyflink.datastream.connectors import StreamingFileSink
from pyflink.datastream.connectors.file_system import FileSink, OutputFileConfig
from pyflink.table import Row
from pyflink.datastream.formats.csv import CsvRowSerializationSchema
from pyflink.datastream.formats.json import JsonRowDeserializationSchema,JsonRowSerializationSchema

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def load_tweet(json_string):
    data = json.loads(json_string)
    return ([data['user']['name'],
        data['user']['id'],
     data["created_at"],
      data['user']['location'],
       sentiment_analyzer.polarity_scores(data['text'])["compound"],
       len(data['text'])])

def read_from_kafka(env,P_ADDRESS):
    deserialization_schema = JsonRowDeserializationSchema.Builder() \
        .type_info(Types.ROW([Types.INT(), Types.STRING()])) \
        .build()

    source = KafkaSource.builder() \
    .set_bootstrap_servers('{IP_ADDRESS}:9093') \
    .set_topics("Twitter") \
    .set_group_id("my-group") \
    .set_starting_offsets(KafkaOffsetsInitializer.earliest()) \
    .set_value_only_deserializer(SimpleStringSchema()) \
    .build()

    ds = env.from_source(source, WatermarkStrategy.no_watermarks(), "Kafka Source")
    return ds

def retweet(liste):
    """
    s'il y a un retweet dans le corps du texte => on prend le premier
    si pas de retweet => no retweet
    """
    n= len(liste)
    return liste[0] if n>0 else "no retweet"


def load_tweet(json_string):
    """
    On transforme le dictionnaire en type Row (de l'API Table)
    pour écrire ensuite dans un topic Kafka
    """
    data = json.loads(json_string)
    return Row( 
    data['user']['name'],
    len(data['text']),
    len(set(data['text'].split())),
    retweet(re.findall(r"\@[a-zA-z0-9\é\à\ù]+",data['text']) ),
    sentiment_analyzer.polarity_scores(data['text'])["compound"],
  
       )

def write_stream_to_kafka(env, datastream,type_info):
    """
    Le port 9092 ou 9093 du broker kafka peut changer selon le docker-compose
    Vérifiez sur l'onglet broker de Kafka UI
    """
    serialization_schema = CsvRowSerializationSchema.Builder(type_info).build()
    
    sink = KafkaSink.builder() \
    .set_bootstrap_servers(f'{IP_ADDRESS}:9093') \
    .set_record_serializer(
        KafkaRecordSerializationSchema.builder()
            .set_topic("Consumer")
            .set_value_serialization_schema(serialization_schema)
            .build()
    ) \
    .build()
    
    # send the datastream to KafkaSink
    datastream.sink_to(sink)

if __name__ == '__main__':
    #message en sortie de console
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")

    env = StreamExecutionEnvironment.get_execution_environment()
    ##Il faut créer un environnement virtuel, ajouter l'extension jar à cet endroit et ajouter cette ligne sinon ça ne marche pas
    env.add_jars("file:////home/ubuntu/flink/flink_env/lib/python3.8/site-packages/pyflink/lib/flink-sql-connector-kafka-1.16.0.jar")
    IP_ADDRESS= '63.34.168.100'
    
    print("start reading data from kafka")
    tweets_datastream= read_from_kafka(env,IP_ADDRESS)
    ##Pour vérifi qu'on lit bien les sorties :
    #  tweets_datastream.print()
    #On calcule score sentiment analysis à la volée
    sentiment_analyzer = SentimentIntensityAnalyzer()
    type_info = Types.ROW([Types.STRING(),Types.INT(),Types.INT(),
   Types.STRING(),
    Types.FLOAT()])

    #On ajoute des infos comme les retweets, nombres de mots, score ...
    datastream_score= tweets_datastream.map( load_tweet , output_type= type_info) 

    print("start writing data to kafka")
    write_stream_to_kafka(env, datastream_score,type_info)

    # define the KafkaSink with the serialization schema
    output_path = '/home/ubuntu/flink/MC_Kafka/Datasink/'
    file_sink = FileSink \
        .for_row_format(output_path, Encoder.simple_string_encoder()) \
        .build()
    datastream_score.sink_to(file_sink)

    env.execute()
#Pour lancer le conteneur avec Kafka
#docker-compose up --scale kafka=3 -d


