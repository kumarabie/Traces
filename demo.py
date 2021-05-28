import flask
from flask import Flask, request
import requests
from flask.logging import default_handler
from py_zipkin.transport import SimpleHTTPTransport
from py_zipkin.zipkin import zipkin_span, create_http_headers_for_new_span, ZipkinAttrs, Kind, zipkin_client_span
from py_zipkin.request_helpers import create_http_headers
from py_zipkin.encoding import Encoding
import time
from py_zipkin.encoding import Encoding
app=flask.Flask(__name__)

def default_handler(encoded_span):
    body = encoded_span

    # decoded = _V1ThriftDecoder.decode_spans(encoded_span)
    app.logger.debug("body %s", body)

    # return requests.post(
    #     "http://zipkin:9411/api/v1/spans",
    #     data=body,
    #     headers={'Content-Type': 'application/x-thrift'},
    # )

    return requests.post(
        "http://zipkin:9411/api/v2/spans",
        data=body,
        headers={'Content-Type': 'application/json'},
    )



@zipkin_span(service_name='webapp', span_name='do_stuff')
def do_stuff():
    time.sleep(5)
    headers = create_http_headers_for_new_span()
    requests.get('http://localhost:5042/service1/', headers=headers)
    return 'OK'

@app.route('/')
def index():
    #transport = SimpleHTTPTransport("localhost", 4042)
    with zipkin_span(
        service_name='webapp',
        span_name='index',
        transport_handler=default_handler(),
        port=4042,
        sample_rate=100, #0.05, # Value between 0.0 and 100.0
    ):
        do_stuff()
        time.sleep(10)
    return 'OK', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 4042, debug=True)
