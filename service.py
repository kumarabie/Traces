from flask import Flask, request
import flask
import requests
from flask.logging import default_handler
from py_zipkin.transport import SimpleHTTPTransport
from py_zipkin.zipkin import zipkin_span, create_http_headers_for_new_span, ZipkinAttrs, Kind, zipkin_client_span
from py_zipkin.request_helpers import create_http_headers
from py_zipkin.encoding import Encoding
import time
app=flask.Flask(__name__)


@zipkin_span(service_name='service1', span_name='service1_do_stuff')
def do_stuff():
    time.sleep(5)
    return 'OK'


@app.route('/service1/')
def index():
    transport = SimpleHTTPTransport("localhost", 5042)
    with zipkin_span(
        service_name='service1',
        zipkin_attrs=ZipkinAttrs(
            trace_id=request.headers['X-B3-TraceID'],
            span_id=request.headers['X-B3-SpanID'],
            parent_span_id=request.headers['X-B3-ParentSpanID'],
            flags=request.headers['X-B3-Flags'],
            is_sampled=request.headers['X-B3-Sampled'],
        ),
        span_name='index_service1',
        transport_handler=transport,
        port=5042,
        sample_rate=100, #0.05, # Value between 0.0 and 100.0
    ):
        do_stuff()
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5042, debug=False)