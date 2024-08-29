from app.models import CompanyPolicy

policies_discussed_mapping = {
    "LABEL_0": CompanyPolicy.FREE_RC_TRANSFER,
    "LABEL_1": CompanyPolicy.FIVE_DAY_MONEY_BACK_GUARANTEE,
    "LABEL_2": CompanyPolicy.FREE_RSA_FOR_ONE_YEAR,
    "LABEL_3": CompanyPolicy.RETURN_POLICY,
    "LABEL_4": None,
}


ner_label_mapping = {
    "LABEL_0": None,
    "LABEL_1": "car_type",
    "LABEl_2": "car_type",
    "LABEL_3": "fuel_type",
    "LABEL_4": "fuel_type",
    "LABEL_5": "color",
    "LABEL_6": "color",
    "LABEL_7": "distance_travelled",
    "LABEL_8": "distance_travelled",
    "LABEL_9": "make_year",
    "LABEL_10": "make_year",
    "LABEL_11": "transmission",
    "LABEL_12": "transmission",
}
