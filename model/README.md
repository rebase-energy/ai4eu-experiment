
This project has received funding from the European Union's Horizon 2020 research and innovation programme within the framework of the I-NERGY Project, funded under grant agreement No 101016508

## Rebase model

[rebase.energy](https://rebase.energy) is an open and collaborative energy modelling platform.

This is model is a LightGBM time-series forecasting model. LightGBM is a gradient boosting decision tree framework developed by Microsoft. 


# How to use

## Install dependencies

``pip install -r requirements.txt``

## Start server
Run:
``python -m server``

This will start a UI at http://localhost:8062

See a demonstration video [here](https://drive.google.com/file/d/1QD6UlpGk3Aczxl4i2hWH_FGh0U-VUJzZ/view?usp=sharing) how it can be used. 



## Test with client
Run:

``python -m client``

client.py describes how you can call the Predict method.

The Predict method expects a PredictInput message
```
message PredictInput {
    string train_set = 1;
    string pred_set = 2;
}
```
where:
- **train_set** is a JSON string, like the following object
```json
{
    "ref_datetime": ["2021-01-01 00:00", "2021-01-01 00:00", ...],
    "valid_datetime": ["2021-01-01 00:00", "2021-01-01 01:00", ...],
    "target": [133.1, 122.7, ...],
    "feature_0": [11.2, 9.7, ...],
    ...
    "feature_n": [23.1, 17.9, ...]
}
```
- **pred_set** is a JSON string, with the same structure, except for not having a target since that is what you are predicting. 
```json
{
    "ref_datetime": ["2021-05-01 00:00", "2021-05-01 00:00", ...],
    "valid_datetime": ["2021-05-01 00:00", "2021-05-01 01:00", ...],
    "feature_0": [13.1, 10.4, ...],
    ...
    "feature_n": [22.9, 16.2, ...]
}
```

The result is returned as Result
```
message Result {
    repeated string ref_datetime = 1;
    repeated string valid_datetime = 2;
    repeated float target = 3 ;
}
```

### Note about the input
ref_datetime, valid_datetime and target should always be in the input data. The other features are optional.

- **ref_datetime** - the point in time that the features were available to you, etc if you are using weather forecasts, it represents at what point in time you would have gotten those features from the forecast
- **valid_datetime** - the timestamp when the each feature value rows was valid
- **target** - the target to predict



## Deploy
You can deploy this in Kubernetes

```
kubectl create ns <namespace_name>
```
```
kubectl apply -f pod.yaml -n <namespace_name>
```



## Development

If you use this code and change anything in the protocol **model.proto**, you need to generate the new stubs:

```
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. model.proto
```


