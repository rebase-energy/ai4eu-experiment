
This project has received funding from the European Union's Horizon 2020 research and innovation programme within the framework of the I-NERGY Project, funded under grant agreement No 101016508

## What is the Rebase Dataset Broker?

[rebase.energy](https://rebase.energy) is an open and collaborative energy modelling platform that provides open energy datasets. The datasets can be found [here](https://rebase.energy/datasets)

This broker is a wrapper that can load these datasets.



# How to use

## Install dependencies

``pip install -r requirements.txt``

## Start server
Run:
``python -m server``

This will start a UI at http://localhost:8062

See a demonstration video [here](https://drive.google.com/file/d/1SlDUP5Arn1UChUAcYSfEZtIEWdGBtT7Y/view) how it can be used. 


The dataset platform is under development. Currently one dataset exists, but many more will be added. 

Available datasets:

- **rebase-energy/NVE-Wind-Power-Production-in-Norway**. The name of assets can be found here: https://github.com/rebase-energy/NVE-Wind-Power-Production-in-Norway/tree/master/data





## Test with client
Run:

``python -m client``

The LoadData rpc method as described in model.proto, returns:
* train_set
* valid_set

as 2 JSON strings, where each JSON string represents an object with the following format:

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

ref_datetime, valid_datetime and target are always returned in the data. There might be other features of same length depending on if the dataset has those features in Rebase Energy datasets.

- **ref_datetime** - the point in time that the features were available to you, etc if you are using weather forecasts, it represents at what point in time you would have gotten those features from the forecast
- **valid_datetime** - the timestamp when the each feature value rows was valid
- **target** - the target to predict
- **features_0/features_n** - optional features of same length



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


