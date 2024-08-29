from app.models import (
    CompanyPolicy,
    CustomerObjections,
    CustomerRequirements,
    ExtractedData,
)


def extract_data(audio_transcript: str) -> ExtractedData:
    return ExtractedData(
        customer_requirements=CustomerRequirements(
            car_type="",
            fuel_type="",
            color="",
            distance_travelled=10,
            make_year=2024,
            transmission_type="",
        ),
        company_policies_discussed=[CompanyPolicy.RETURN_POLICY],
        customer_objections=CustomerObjections(
            refurbishment_quality=[""],
            car_issues=[""],
            price_issues=[""],
            customer_experience_issues=[""],
        ),
    )
