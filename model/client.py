import pandas as pd
import grpc
import model_pb2
import model_pb2_grpc
import config as config
from google.protobuf.json_format import MessageToJson 
import json





def get_pred(train_set, pred_set):
    with grpc.insecure_channel(f'localhost:{config.PORT}') as channel:
        stub = model_pb2_grpc.RebaseModelStub(channel)

        response = stub.Predict(
            model_pb2.PredictInput(
                train_set=json.dumps(train_set),
                pred_set=json.dumps(pred_set)
        ))
        return json.loads(MessageToJson(response))


def evaluate(train_set, test_set):
    with grpc.insecure_channel(f'localhost:{config.PORT}') as channel:
        stub = model_pb2_grpc.RebaseModelStub(channel)

        response = stub.Evaluate(
            model_pb2.EvalInput(
                train_set=json.dumps(train_set),
                valid_set=json.dumps(test_set)
        ))
        return json.loads(MessageToJson(response))






train_set = {
    'ref_datetime': ['2020-01-01 00:00', '2020-01-01 00:00'],
    'valid_datetime': ['2020-01-01 00:00', '2020-01-01 01:00'],
    'target': [100, 110],
    'WindSpeed': [10, 11]
}

pred_set = {
    'ref_datetime': ['2020-01-01 00:00', '2020-01-01 00:00'],
    'valid_datetime': ['2020-01-01 00:00', '2020-01-01 01:00'],
    'WindSpeed': [10, 11]
}

test_set = {
    'ref_datetime': ['2021-01-01 00:00', '2021-01-01 00:00'],
    'valid_datetime': ['2021-01-01 00:00', '2021-01-01 01:00'],
    'target': [105, 109],
    'WindSpeed': [12, 14]
}

result = get_pred(train_set, pred_set)
print(result)

print(evaluate(train_set, test_set))