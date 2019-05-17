import json
import logging
import logging.handlers

import paho.mqtt.client as mqtt

from speech.action_parser import ActionParser

# Mqtt settings
MQTT_SERVER = '39.96.4.124'
MQTT_PORT = 1883
SUB_TOPIC_HW = '/speech/A001'  # 环卫
PUB_TOPIC_HW = '/speech/A002'

SUB_TOPIC_JX = '/speech/A003'  # 基线
PUB_TOPIC_JX = '/speech/A004'

SUB_TOPIC_ZF = '/speech/A005'  # 政府
PUB_TOPIC_ZF = '/speech/A006'

# Action dict path
VERBS_PATH = 'config/verbs.conf'
# DICT_PATH = 'config/dict.conf'


# mqtt callback
def on_connect(client, userdata, flags, rc):
    global main_logger

    main_logger.info('Connection with result code: %d', rc)
    # client.subscribe("$SYS/#")
    client.subscribe(SUB_TOPIC_JX)
    client.subscribe(SUB_TOPIC_HW)
    client.subscribe(SUB_TOPIC_ZF)


# mqtt callback
def on_message(client, userdata, msg):
    global main_logger
    global action_parser

    if msg.topic == SUB_TOPIC_HW \
            or msg.topic == SUB_TOPIC_JX \
            or msg.topic == SUB_TOPIC_ZF:
        action_string = msg.payload.decode('utf8')
        # action_string = msg.payload.decode('gb2312')
        main_logger.info('Received from [%s]: %s', msg.topic, action_string)
        # action_param = actionparser.get_action_parameter(action_string)
        action_param = action_parser.get_action_param(action_string)
        # if action_param:
        if action_param.action:
            dest_topic = msg.topic[:-1] + str(int(msg.topic[-1]) + 1)
            main_logger.info('Send to mqtt topic [%s]: %s', dest_topic, action_param)
            # client.publish(TOPIC_PUB, json.dumps(action_param).encode('utf-8'))
            client.publish(dest_topic, json.dumps(action_param._asdict()).encode('utf-8'))


# init config
def init_logger():
    logging.basicConfig(filename='log/speech.log',
                        format='[ %(asctime)s - %(levelname)s - %(name)s ] %(message)s',
                        level=logging.INFO)
    # fh = logging.handlers.RotatingFileHandler(
    #     'log/speech.log',
    #     maxBytes=1024 * 1024,
    #     backupCount=5,
    #     encoding='utf8'
    # )
    # fh.setLevel(logging.INFO)
    # fhfmt = logging.Formatter('[ %(asctime)s - %(levelname)s - %(name)s ] %(message)s')
    # fh.setFormatter(fhfmt)
    # logging.getLogger('').addHandler(fh)
    #
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


if __name__ == '__main__':
    init_logger()

    # global main_logger
    main_logger = logging.getLogger(__name__)

    # global action_parser
    action_parser = ActionParser(VERBS_PATH)

    mqtt_client = mqtt.Client()

    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_SERVER, MQTT_PORT, 60)
    mqtt_client.loop_forever()
