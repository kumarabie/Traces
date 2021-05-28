from flask import Flask, request
import requests
from flask.logging import default_handler
from py_zipkin.zipkin import zipkin_span, create_http_headers_for_new_span, ZipkinAttrs, Kind, zipkin_client_span
from py_zipkin.request_helpers import create_http_headers
from py_zipkin.encoding import Encoding

@app.route('/')
def index():
    with zipkin_span(
        service_name='api_01',
        span_name='index_api_01',
        transport_handler=default_handler,
        port=5000,
        sample_rate=100,
        encoding=Encoding.V2_JSON
    ):
        call_api_02()
        call_api_03()
    return 'OK', 200


@zipkin_client_span(service_name='api_01', span_name='call_api_02')
def call_api_02():
    headers = create_http_headers()
    requests.get('http://api_02:5000/', headers=headers)
    return 'OK'

@zipkin_client_span(service_name='api_01', span_name='call_api_03_FROM_01')
def call_api_03():
    headers = create_http_headers()
    requests.get('http://api_03:5000/', headers=headers)
    return 'OK'



app = Flask(__name__)
# Start the app server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True)
