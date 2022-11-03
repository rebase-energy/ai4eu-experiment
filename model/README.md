
This project has received funding from the European Union's Horizon 2020 research and innovation programme within the framework of the I-NERGY Project, funded under grant agreement No 101016508

## Rebase model

[rebase.energy](https://rebase.energy) is an open and collaborative energy modelling platform.

This is model is a LightGBM time-series forecasting model. LightGBM is a gradient boosting decision tree framework developed by Microsoft. 


# Deploy

## Kubernetes
You can deploy this in Kubernetes

1. Go to the asset [here](https://aiexp.ai4europe.eu/#/marketSolutions?solutionId=6662fc35-2e6c-4f48-8e26-f7b677acbb62&revisionId=97313833-7e70-47b1-8524-139c2dc26a78&parentUrl=marketplace#md-model-detail-template)

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

# How to use

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



## Development

If you use this code and change anything in the protocol **model.proto**, you need to generate the new stubs:

```
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. model.proto
```


