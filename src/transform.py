def categorize_weather(temp):
    if temp > 30:
        return "Hot weather"
    elif temp > 20:
        return "Warm weather"
    elif temp > 0:
        return "Cold weather"
    else:
        return "Very cold weather"


def convert_to_farenheit(temp):
    f = (temp * 9 / 5) + 32
    return round(f, 2)


def transform_weather_data(df):
    df["temperatureInCelcius"] = df["temperatureInCelcius"].round(2)
    df.loc[:, "weatherAlert"] = df["temperatureInCelcius"].apply(categorize_weather)
    df.loc[:, "temperatureInFarenheit"] = df["temperatureInCelcius"].apply(
        convert_to_farenheit
    )
    return df
