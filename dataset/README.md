
This project has received funding from the European Union's Horizon 2020 research and innovation programme within the framework of the I-NERGY Project, funded under grant agreement No 101016508

## What is the Rebase Dataset Broker?

[rebase.energy](https://rebase.energy) is an open and collaborative energy modelling platform that provides open energy datasets. The datasets can be found [here](https://rebase.energy/datasets)

This broker is a wrapper that can load these datasets. The dataset platform is under development. Currently one dataset exists, but many more will be added. 

Available datasets:

- **rebase-energy/NVE-Wind-Power-Production-in-Norway**. The name of assets can be found here: https://github.com/rebase-energy/NVE-Wind-Power-Production-in-Norway/tree/master/data



# Deploy

## Kubernetes
You can deploy this in Kubernetes

1. Go to the asset [here](https://aiexp.ai4europe.eu/#/marketSolutions?solutionId=a514218c-d37f-4c38-a06d-c60a267eda42&revisionId=8ad34ae9-6fd3-4815-b890-99d6f22bf929&parentUrl=marketplace#md-model-detail-template)

2. Click on "Deploy for Execution" in the top right corner, or "Sign In To Download" first if you're not logged in

3. Click on Local Kubernetes

4. unzip solution.zip

5. Create a new namespace: ``kubectl create ns <namespace>``

6. Install the deployment and service: ``python solution/kubernetes-client-script.py -n <namespace>``

7. Confirm the setup by running: ``kubectl get pods -n <namespace>``


## Install locally

``pip install -r requirements.txt``

## Start server
Run:
``python -m server``

This will start the gRPC server at http://localhost:8061 and UI at http://localhost:8062



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



## Development

If you use this code and change anything in the protocol **model.proto**, you need to generate the new stubs:

```
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. model.proto
```


