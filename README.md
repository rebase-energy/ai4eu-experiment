
This project has received funding from the European Union's Horizon 2020 research and innovation programme within the framework of the I-NERGY Project, funded under grant agreement No 101016508

## What is the Rebase Dataset Broker?

[rebase.energy](https://rebase.energy) is an open and collaborative energy modelling platform that provides open energy datasets. The datasets can be found [here](https://rebase.energy/datasets)

This broker is a wrapper that can load these datasets.



## How to use

### Install dependencies

``pip install -r requirements.txt``

### Start server

``python -m broker.server``

### Test with client

``python -m broker.client <dataset_name>``

### Documentation

The Rebase Energy dataset platform is heavily under development. Currently one dataset exists, but many more will be added. 

Dataset:
rebase-energ/NVE-Wind-Power-Production-in-Norway
The available assets are can be found here https://github.com/rebase-energy/NVE-Wind-Power-Production-in-Norway/tree/master/data




Generate stubs from model.proto

```
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. model.proto
```

Then it can model_pb2_grpc and model_pb2 can be imported in the python files


### How to run
```
python -m dataset.server
```