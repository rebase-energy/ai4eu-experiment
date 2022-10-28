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
            # df = pd.DataFrame(data=data['data'])
            # df.index = pd.MultiIndex.from_arrays(
            #     [pd.to_datetime(df['ref_datetime'].values),
            #     pd.to_datetime(df['valid_datetime'].values)],
            #     names=['ref_datetime', 'valid_datetime'])
            # # Drop now duplicated index columns
            # df = df.drop(columns=['ref_datetime', 'valid_datetime'])

            # df_train = df.loc[df.index[0][0]:'2021-12-31 06:00']
            # df_train = df_train.reset_index()
            # df_train['ref_datetime'] = df_train['ref_datetime'].dt.strftime('%Y-%m-%d %H:%M')
            # df_train['valid_datetime'] = df_train['valid_datetime'].dt.strftime('%Y-%m-%d %H:%M')
            # train_set = df_train.to_dict(orient='list')

            # last_ref_time = df.index[-1][0]

            # df2 = df.loc[last_ref_time]
            # df2 = df2.reset_index()
            # df2.index = pd.MultiIndex.from_arrays(
            #     [
            #         pd.to_datetime([last_ref_time for _ in df2.index.values]),
            #         df2['valid_datetime'].values
            #     ],
            #     names=['ref_datetime', 'valid_datetime']
            # )
            # df2 = df2.drop(columns=['valid_datetime'])
            # df2 = df2.reset_index()
            # df2['ref_datetime'] = df2['ref_datetime'].dt.strftime('%Y-%m-%d %H:%M')
            # df2['valid_datetime'] = df2['valid_datetime'].dt.strftime('%Y-%m-%d %H:%M')
            # pred_set = df2.to_dict(orient='list')

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