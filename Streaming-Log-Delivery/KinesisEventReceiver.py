import base64
import gzip
import json
import logging

# Setup logging configuration
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def unpack_kinesis_stream_records(event):

    # decode and decompress each base64 encoded data element
    return [gzip.decompress(base64.b64decode(k["kinesis"]["data"])).decode('utf-8') for k in event["Records"]]

def decode_raw_cloud_trail_events(cloudTrailEventDataList):

    #Convert Raw Event Data List
    eventList =  [json.loads(e) for e in cloudTrailEventDataList]

    #Filter out-non DATA_MESSAGES
    filteredEvents = [e for e in eventList if e["messageType"] == 'DATA_MESSAGE']

    #Covert each indidual log Event Message
    events = []
    for f in filteredEvents:
        for e in f["logEvents"]:
            events.append(json.loads(e["message"]))

    logger.info("{0} Event Logs Decoded".format(len(events)))
    return events

def handle_request(event, context):

    #Log Raw Kinesis Stream Records
    logger.debug(json.dumps(event, indent=4))

    # Unpack Kinesis Stream Records
    kinesisData = unpack_kinesis_stream_records(event)
    [logger.debug(k) for k in kinesisData]

    # Decode and filter events
    events = decode_raw_cloud_trail_events(kinesisData)

    ####### INTEGRATION CODE GOES HERE #########

    return f"Successfully processed {len(events)} records."

def lambda_handler(event, context):
    return handle_request(event, context)

