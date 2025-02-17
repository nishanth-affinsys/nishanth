# import json
# from os import walk
#
# timerange_dict = {
#     "return_key": "timestamp__range",
#     "service": "analytics",
#     "filter_type": "timestamp",
#     "filter_title": "Time Range",
# }
# channel_dict = {
#     "api_url": "get_channels/",
#     "request_method": "GET",
#     "return_key": "channel",
#     "service": "analytics",
#     "filter_type": "select",
#     "filter_title": "Channel",
# }
# campaign_dict = {
#     "api_url": "get_campaigns/",
#     "request_method": "POST",
#     "dependency": ["timestamp__range"],
#     "return_key": "campaign_variants",
#     "service": "analytics",
#     "filter_type": "multiselect",
#     "filter_title": "Campaign Name",
# }
#
# customer_type_dict = {
#     "api_url": "get_customer_types/",
#     "request_method": "GET",
#     "return_key": "customer_type",
#     "service": "analytics",
#     "filter_type": "select",
#     "filter_title": "Customer Type",
# }
# intent_dict = {
#     "api_url": "get_intents/",
#     "request_method": "GET",
#     "return_key": "intents",
#     "service": "analytics",
#     "filter_type": "multiselect",
#     "filter_title": "Intents",
# },
#
# dashboard_names = []
#
# path = "/home/pratham/Desktop/bud-core-Analytics-svc/console/static/"
#
# for _, dir, filenames_walk in walk(path):
#     if dir:
#         filenames = filenames_walk
# for filename in filenames:
#     dashboard_permission = filename.split(".")[0]
#     dashboard_names.append(dashboard_permission)
#
#
# for item in dashboard_names:
#     with open(path + item + ".json", "r") as f:
#         data = json.load(f)
#
#         for key, value in data.items():
#             value["new_filters"] = value["filters"]
#             value.pop("filters")
#
#         for key, value in data.items():
#             value["filters"] = []
#             if value["new_filters"].get("channel"):
#                 value["filters"].append(channel_dict)
#             if value["new_filters"]["time"]:
#                 value["filters"].append(timerange_dict)
#             if value["new_filters"].get("campaignName"):
#                 value["filters"].append(campaign_dict)
#             if value["new_filters"]["customerType"]:
#                 value["filters"].append(customer_type_dict)
#             if value["new_filters"]["intent"]:
#                 value["filters"].append(intent_dict)
#             value.pop("new_filters")
#
#     with open(path + item + ".json", "w") as f:
#         json.dump(data, f, indent=2)
