import pandas as pd
df = pd.DataFrame({'num_legs': [4, 2], 'num_wings': [0, 2]})
print(tuple(df.itertuples(index=False, name='bgp')))
