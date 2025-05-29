from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

import pandas as pd
from sentinelhub import parse_time

from utils import evalscript

def stats_to_df(stats_data):
    """Transform Statistical API response into a pandas.DataFrame"""
    df_data = []

    for single_data in stats_data["data"]:
        df_entry = {}
        is_valid_entry = True

        df_entry["interval_from"] = parse_time(single_data["interval"]["from"]).date()
        df_entry["interval_to"] = parse_time(single_data["interval"]["to"]).date()

        for output_name, output_data in single_data["outputs"].items():
            for band_name, band_values in output_data["bands"].items():
                band_stats = band_values["stats"]
                if band_stats["sampleCount"] == band_stats["noDataCount"]:
                    is_valid_entry = False
                    break

                for stat_name, value in band_stats.items():
                    col_name = f"{output_name}_{band_name}_{stat_name}"
                    if stat_name == "percentiles":
                        for perc, perc_val in value.items():
                            perc_col_name = f"{col_name}_{perc}"
                            df_entry[perc_col_name] = perc_val
                    else:
                        df_entry[col_name] = value

        if is_valid_entry:
            df_data.append(df_entry)

    return pd.DataFrame(df_data)


def authenticate_sentinel_hub(client_id, client_secret):
    """Authenticate the user"""
    # set up credentials
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)

    # get an authentication token
    token = oauth.fetch_token(token_url='https://services.sentinel-hub.com/auth/realms/main/protocol/openid-connect/token',
                            client_secret=client_secret, include_client_id=True)
    
    return oauth


def build_json_request(geometry, start_date, end_date, day_interval, data_set):
    """Builds a custom JSON request"""
    return {
    "input": {
        "bounds": {
        "geometry": geometry
        },
        "data": [
        {
            "dataFilter": {},
            "type": "byoc-" + data_set # data id
        }
        ]
    },
    "aggregation": {
        "timeRange": { # the time interval for the data
        "from": start_date + "T00:00:00Z",
        "to": end_date + "T23:59:59Z"
        },
        "aggregationInterval": {
        "of": "P" + day_interval + "D" # day interval 
        },
        "width": None,
        "height": None,
        "evalscript": evalscript # evalscript
    },
    "calculations": {
        "default": {}
    }
    }