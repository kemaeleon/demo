import pandas as pd
df = pd.read_json('http://127.0.0.1:8000/rest/ST?format=json')
df.head(100)


