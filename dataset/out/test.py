import pandas as pd
import pickle


with open('out/output.pickle', 'rb') as f:
    data = pickle.load(f)
    
    df = pd.DataFrame(data['data'])
    df.index = pd.MultiIndex.from_arrays(
        [pd.to_datetime(df['ref_datetime'].values),
        pd.to_datetime(df['valid_datetime'].values)],
        names=['ref_datetime', 'valid_datetime'])
    # Drop now duplicated index columns
    df = df.drop(columns=['ref_datetime', 'valid_datetime'])

    df_train = df.loc[df.index[0][0]:'2021-12-31 06:00']
    print(df_train)
    
    last_ref_time = df.index[-1][0]
    print(last_ref_time)

    df2 = df.loc[last_ref_time]
    df2 = df2.reset_index()
    df2.index = pd.MultiIndex.from_arrays(
        [
            pd.to_datetime([last_ref_time for _ in df2.index.values]),
            df2['valid_datetime'].values
        ],
        names=['ref_datetime', 'valid_datetime']
    )
    df2 = df2.drop(columns=['valid_datetime'])
    print(df2)


