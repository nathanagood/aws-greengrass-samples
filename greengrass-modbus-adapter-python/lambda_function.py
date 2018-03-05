"""
Sample AWS Lambda Function that can be deployed to AWS Greengrass
as a long-running Lambda function to expose a modbus client that will
attach to a server and then forward the messages to the MQTT client.

See README.md to learn how to test.
"""

from __future__ import print_function
import logging
import json
import threading
import os

from pymodbus.client.sync import ModbusTcpClient

from modbus_client import ConcurrentClient

# pylint: disable=C0103
logger = logging.getLogger('modbus_adapter')
logger.setLevel(logging.INFO)

MODBUS_IP = os.environ.get('MODBUS_SERVER_IP', '127.0.0.1')
MODBUS_PORT = int(os.environ.get('MODBUS_SERVER_PORT', '5020'))


def client_factory():
    """
    Creates an instance of the Modbus client.
    """
    logger.debug("Creating client for: %s", threading.current_thread())
    client = ModbusTcpClient(MODBUS_IP, port=MODBUS_PORT)
    client.connect()
    return client


def function_handler(event, context):
    """
    Handler for the AWS Lambda function.
    :param event: AWS Lambda uses this parameter to pass in event data to the handler. This
    parameter is usually of the Python dict type. It can also be list, str, int, float, or
    NoneType type.
    :param context: The AWS Lambda event context. To learn more about what is included in
    the context,
    see https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html.
    """

    logger.debug('Handling event: %s', json.dumps(event))

    client = ConcurrentClient(factory=client_factory, in_process=True)
    try:
        futures = [client.read_coils(i * 8, 8) for i in range(10)]
        for future in futures:
            logger.info("Future result is: %s", future.result(timeout=1))
    finally:
        client.shutdown()


if __name__ == '__main__':
    FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(format=FORMAT)
    logger.debug('Starting main...')

    # Mock up event data and a context object
    function_event = {}
    function_context = {}

    function_handler(function_event, function_context)
