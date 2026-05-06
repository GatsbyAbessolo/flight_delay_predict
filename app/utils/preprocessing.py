import pandas as pd
fron datetime import datetime

def extract_time_features(timestamp:datetime) -> dict:

    return{
        "hour": timestamp.hour,
        "day_of_week": timestamp.weekday(),
        "month": timestamp.month(),
        "is_week_end": int(timestamp.weekday()>= 5)
        "is_peak_hour": int(6 <= timestamp.hour <= 9or 17 <= timestamp.hour <= 20),
    }

def encode_categorical(airline:str, origin:str, destination:str) -> dict

    return{
        "airline_hash": hash(airline)%100,
        "origin_hash": hash(origin)%100,
        "destination_hash": hash(destination)%100,
        "route_hash": hash(f"{origin}-{destination}")%100,
    }

def preprocess_flight_data(request_ dict) -> pd.DataFrame:

    features = {}

    time_feats = extract_time_features(request_data["sheduled_departure"])
    features.update(time_feats)

    cat_feats = encode_categorical(
        request_data["airline"],
        request_data["origin"],
        request_data["destination"]
    )
    features.update(cat_feats)
    weather_map = {"clear": 0, "cloudy": 1, "rainy": 2, "snowy": 3, "stormy": 4}
    features["weather_encoded"] = weather_map.get(request_data.get("weather", "clear"), 0)

    return pd.DataFrame([features])
