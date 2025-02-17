def convert_seconds_to_hhmmss(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"


def add_args(params, key, value):
    if key:
        params[key] = value
    return params


def custom_filters(data, timestamp_key=None, channel_key=None, campaign_key=None, customer_type=None, intents=None):
    internal_data = dict()
    if "timestamp__range" in data and timestamp_key:
        internal_data[timestamp_key] = data.get("timestamp__range")
    if "channel" in data and channel_key:
        internal_data[channel_key] = data.get("channel")
    if "campaign_variants" in data and campaign_key:
        internal_data[campaign_key] = data.get("campaign_variants")
    if "customer_type" in data and customer_type:
        internal_data[customer_type] = data.get("customer_type")
    if "intents" in data and intents:
        internal_data[intents] = data.get("intents")

    return internal_data
