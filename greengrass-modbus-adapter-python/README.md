# Modbus Adapter Example for AWS Greengrass (Python)

This folder contains a sample AWS Lambda function implemented in Python that demonstrates how to
create a listener for communications using the [Modbus](https://en.wikipedia.org/wiki/Modbus)
protocol.

## Files

### `lambda_function.py`

This file contains the AWS Lambda code.

### `server.py`

To test the AWS Lambda function, the `server.py` contents were directly based on the documentation
for **PyModbus**. See [the example here](https://pymodbus.readthedocs.io/en/latest/source/example/modbus_payload_server.html).

## Testing

To test the function, first start the server using `python server.py`. This will create the
server and bind it to `localhost:5020`.

The AWS Lambda function in `lambda_function.py` can be executed directly from the command line
for testing.