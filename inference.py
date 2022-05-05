# CATS docker inference.
import requests
import argparse
import pandas as pd
from typing import Dict, List


def parse_args():
    """Parse commandline args."""
    p = argparse.ArgumentParser(description='Inference with CATS docker.')
    p.add_argument("--endpoint", default='http://127.0.0.1:5000/summarize',
                   type=str,
                   help='Docker API endpoint. Defaults to localhost.')
    p.add_argument("--data_path", type=str,
                   help="Path to data excel.")
    p.add_argument("--text_column", type=str, default='text',
                   help="name of the text column to summarize")
    args = p.parse_args()
    return vars(args)


def send_api_request(endpoint: str, csv: str, textcol: str):
    """Sends a single string to Docker API in correct format."""
    outputs = []
    form_data = get_form_data(path=csv, text_column=textcol)
    for row in form_data:
        row['target'] = (None, row['target'])
        response = requests.post(endpoint, files=row)
        print(response.status_code)
        outputs.append(response.json())
    return outputs


def get_form_data(path: str, text_column: str) -> List[Dict[str, str]]:
    """Reands and Transforms textual data to form data.
    Structure should be: {target: <text>}"""
    data = pd.read_excel(path)
    data = data.rename(columns={text_column: 'target'})
    form_data = data[['target']].to_dict('records')
    return form_data
    


if __name__ == "__main__":

    args = parse_args()
    outputs = send_api_request(endpoint=args["endpoint"],
                               csv=args["data_path"],
                               textcol=args['text_column'])
    print(outputs)

