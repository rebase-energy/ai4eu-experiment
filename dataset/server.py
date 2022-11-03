import logging
from concurrent import futures
import threading
import requests
import grpc
from main import run
import model_pb2
import model_pb2_grpc
import config
import simplejson
import pickle
import pandas as pd

# Get the dataset from Rebase Energy dataset API
def get_data(name, asset):
    print("Getting dataset:", name)
    url = f"{config.HOST_NAME}/api/v1/datasets/{name}"
    params = {
        'asset': asset
    }
    resp = requests.get(url, params=params)
    print("API status code:", resp.status_code)
    resp.raise_for_status()
    return resp.content




class RebaseDatasetService(model_pb2_grpc.RebaseDatasetServicer):

    def LoadData(self, request, context):
        with open('out/output.pickle', 'rb') as f:
            data = pickle.load(f)

        # Return the JSON response from the API
        response = model_pb2.Response(
            train_set=simplejson.dumps(data['data']['train'], ignore_nan=True),
            valid_set=simplejson.dumps(data['data']['valid'], ignore_nan=True)
        )

        return response



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    model_pb2_grpc.add_RebaseDatasetServicer_to_server(
        RebaseDatasetService(), server)
    server.add_insecure_port(f'[::]:{config.PORT}')
    server.start()
    threading.Thread(target=run()).start()
    server.wait_for_termination()


if __name__ == '__main__':
    print("Starting dataset server")
    logging.basicConfig()
    serve()