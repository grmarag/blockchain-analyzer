import os
import json
import tempfile
import pandas as pd
from src.data_loader import DataLoader

def test_load_data():
    data = [
        {"sender": "A", "recipient": "B", "amount": "100", "token": "token1", "height": "1000", "tx_hash": "hash1"},
        {"sender": "B", "recipient": "C", "amount": "200", "token": "token1", "height": "1001", "tx_hash": "hash2"}
    ]
    temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w')
    for record in data:
        temp_file.write(json.dumps(record) + "\n")
    temp_file.close()
    
    loader = DataLoader(temp_file.name)
    df = loader.load_data()
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 2
    os.unlink(temp_file.name)