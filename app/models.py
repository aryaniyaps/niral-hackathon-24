from enum import StrEnum

from pydantic import BaseModel


class CompanyPolicy(StrEnum):
    FREE_RC_TRANSFER = "free_rc_transfer"
    FIVE_DAY_MONEY_BACK_GUARANTEE = "5_day_money_back_guarantee"
    FREE_RSA_FOR_ONE_YEAR = "free_rsa_for_one_year"
    RETURN_POLICY = "return_policy"


class CustomerRequirements(BaseModel):
    car_type: str | None

    fuel_type: str | None

    color: str | None

    distance_travelled: str | None

    make_year: str | None

    transmission_type: str | None


class CustomerObjections(BaseModel):
    refurbishment_quality: list[str]

    car_issues: list[str]

    price_issues: list[str]

    customer_experience_issues: list[str]


class ExtractedData(BaseModel):
    customer_requirements: CustomerRequirements
    company_policies_discussed: list[CompanyPolicy]
    customer_objections: CustomerObjections
