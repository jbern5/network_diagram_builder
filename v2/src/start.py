import os
import pandas as pd
import time

start = time.time()

df = pd.read_csv("net_data.csv")
unique_cati = df['cati'].unique()

for cati in unique_cati:
    os.system('python3 main.py {}'.format(cati))

end = time.time()

print('Runtime: {}'.format(end-start))