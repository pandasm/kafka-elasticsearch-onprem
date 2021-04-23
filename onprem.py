from socket import timeout
from time import sleep
from json import dumps, loads
import requests
import base64
import json
from kafka import KafkaProducer
import kafka
from kafka.consumer import group
from requests.api import head
import sys


def producer():
    print('i am in producer')
    producer = kafka.KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer= lambda x: dumps(x).encode('utf-8'))
    #data = {"test_id":"test-1", "description":"POC elasticsearch sink connector with kafka connect"}
    for i in range(20):
        data = {"test_id":"test-"+str(i), "description":"POC elasticsearch sink connector with kafka connect"}
        producer.send('test-topic',value=data)
        sleep(2)
    print('i am in producer -- end')

def consumer():
    print("i am in consumer")
    consumer = kafka.KafkaConsumer('test-topic',bootstrap_servers=['localhost:9092'],auto_offset_reset='earliest',enable_auto_commit=True,group_id='connect-test-connector',value_deserializer=lambda x: loads(x.decode('utf-8')))
    for message in consumer:
        print(message.value)

def producer_rest():
    url = "http://localhost:8082/topics/rest-topic"
    headers={
        "Accept": "application/vnd.kafka.v2+json",
        "Content-Type" : "application/vnd.kafka.json.v2+json"
    }

    for i in range(10):
        payload = dumps({"records":[{"value":{"test_id":"test-"+str(i), "description":"POC elasticsearch sink connector with kafka connect"}}]})
        res = requests.post(url,data=payload,headers=headers)
        if res.status_code!=200:
            print("Status Code: " + str(res.status_code))
            print(res.text) 
        sleep(2)
    print('end of producer rest function')

def consumer_rest():
    
    #Assuming that the consumer and the subscription are all in place

    #http://localhost:8082/consumers/resttestgroup/instances/rest-topic-test-consumer/records
    
    consumer_group = "resttestgroup"
    instance_name = "rest-topic-test-consumer"
    
    url = "http://localhost:8082/consumers/resttestgroup/instances/rest-topic-test-consumer/records"
    headers={
            "Accept": "application/vnd.kafka.json.v2+json",
            "Content-Type" : "application/vnd.kafka.json.v2+json"
        }

    res = requests.get(url,headers=headers)
    if res.status_code != 200:
        print("Status Code: " + str(res.status_code))
        print(res.text)
        sys.exit("Error thrown while getting message")
    
    print(res.text)

consumer_rest()