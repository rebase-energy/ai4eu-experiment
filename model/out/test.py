import pandas as pd

data = {
    'ref_datetime': ['2020-01-01 00:00', '2020-01-01 00:00', '2020-01-01 00:00', '2020-01-01 03:00', '2020-01-01 03:00', '2020-01-01 03:00'],
    'valid_datetime': ['2020-01-01 00:00', '2020-01-01 06:00', '2020-01-01 12:00', '2020-01-01 06:00', '2020-01-01 12:00', '2020-01-01 18:00'],
    'target': [1, 2, 3, 4, 5, 6]
}

df = pd.DataFrame(data)
df.index = pd.MultiIndex.from_arrays(
        [pd.to_datetime(df['ref_datetime'].values),
        pd.to_datetime(df['valid_datetime'].values)],
        names=['ref_datetime', 'valid_datetime'])
# Drop now duplicated index columns
df = df.drop(columns=['ref_datetime', 'valid_datetime'])

print(df)