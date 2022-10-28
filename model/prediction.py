import pandas as pd
import json
import simplejson
import lightgbm as lgb
import pickle
from datetime import datetime

def evaluate(train_set, valid_set, params):
    df_train_X = train_set.drop(columns=['target'])
    df_train_y = train_set['target']
    lgb_trainset = lgb.Dataset(df_train_X, label=df_train_y)

    df_test_X = valid_set.drop(columns=['target'])
    df_test_y = valid_set['target']
    lgb_testset = lgb.Dataset(df_test_X, label=df_test_y)

    valid_sets = [lgb_testset]
    valid_names = ['test']

    evals_result = {}
    gbm = lgb.train(
        params, 
        lgb_trainset,
        valid_sets=valid_sets,
        valid_names=valid_names,
        evals_result=evals_result
    )
    
    return evals_result


def get_prediction(train_set, val_x, params):
    df_X = train_set.drop(columns=['target'])
    df_y = train_set['target']
    lgb_trainset = lgb.Dataset(df_X, label=df_y)

    # Train
    gbm = lgb.train(
        params, 
        lgb_trainset
    )
    
    # drop target in case it exists
    if 'target' in val_x.columns:
        val_x = val_x.drop(columns=['target'])

    # Run prediction
    val_x['target'] = gbm.predict(val_x)
    return val_x




def to_multiindex(df):
    df.index = pd.MultiIndex.from_arrays(
            [pd.to_datetime(df['ref_datetime'].values),
            pd.to_datetime(df['valid_datetime'].values)],
            names=['ref_datetime', 'valid_datetime'])
    # Drop now duplicated index columns
    df = df.drop(columns=['ref_datetime', 'valid_datetime'])
    return df

def to_df(json_data):
    data = simplejson.loads(json_data)
    df = pd.DataFrame(data)
    return to_multiindex(df)



def get_params(file_name='params.json'):
    with open(file_name, 'r') as f:
        return json.load(f)


def store_result(result):
    with open('out/result.pickle', 'wb') as f:
        pickle.dump({
            'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'result': result
        }, f)