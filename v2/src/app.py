import os
import pandas as pd
import time
from graph import make_graph

start = time.time()

df = pd.read_csv("net_data.csv")
unique_cati = df['cati'].unique()

for cati in unique_cati:
    print(cati)
    cati_df = df[df['cati'] == cati]
    make_graph(cati_df, cati)

end = time.time()

print('Runtime: {}'.format(end-start))