#!/usr/bin/env python
"""
Pymodbus Server Payload Example
--------------------------------------------------------------------------

If you want to initialize a server context with a complicated memory
layout, you can actually use the payload builder.
"""
import logging

from pymodbus.server.sync import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder

logging.basicConfig()
# pylint: disable=C0103
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def run_payload_server():
    """
    Creates the Modbus server and starts it.
    """

    # build your payload
    payload = BinaryPayloadBuilder(byteorder=Endian.Little)
    # builder.add_string('abcdefgh')
    # builder.add_32bit_float(22.34)
    # builder.add_16bit_uint(4660)
    # builder.add_8bit_int(18)
    payload.add_bits([0, 1, 0, 1, 1, 0, 1, 0])

    block = ModbusSequentialDataBlock(1, payload.to_registers())
    store = ModbusSlaveContext(di=block, co=block, hr=block, ir=block)
    context = ModbusServerContext(slaves=store, single=True)

    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/bashwork/pymodbus/'
    identity.ProductName = 'Pymodbus Server'
    identity.ModelName = 'Pymodbus Server'
    identity.MajorMinorRevision = '1.0'

    StartTcpServer(context, identity=identity, address=("127.0.0.1", 5020))


if __name__ == "__main__":
    logger.info("Starting Modbus server...")
    run_payload_server()
