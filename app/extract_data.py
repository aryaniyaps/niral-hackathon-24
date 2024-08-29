from app.constants import MIN_CLASSIFICATION_SCORE
from app.models import (
    CompanyPolicy,
    CustomerObjections,
    CustomerRequirements,
    ExtractedData,
)
from app.utils.label_mapping import ner_label_mapping, policies_discussed_mapping
from app.utils.pipeline import (
    ner_pipeline,
    objection_classifier_pipeline,
    policy_classifier_pipeline,
    sentiment_pipeline,
)


def chunk_transcripts(transcript: str, lines_per_chunk: int = 2) -> list[str]:
    # Split the transcript into individual lines
    lines = transcript.split("\n")

    # Initialize an empty list to store chunks
    chunks = []

    # Iterate through lines and group them in chunks of specified lines_per_chunk
    for i in range(0, len(lines), lines_per_chunk):
        # Create a chunk by joining the selected lines
        chunk = "\n".join(lines[i : i + lines_per_chunk])
        # Append the chunk to the chunks list
        chunks.append(chunk.strip())

    return chunks


def extract_data(audio_transcript: str) -> ExtractedData:
    policies_discussed: list[CompanyPolicy] = []
    refurbishment_quality_issues: list[str] = []
    car_issues: list[str] = []
    price_issues: list[str] = []
    customer_experience_issues: list[str] = []
    for chunk in chunk_transcripts(transcript=audio_transcript):
        policies_output = policy_classifier_pipeline(chunk)
        for label_dict in policies_output:
            if label_dict["score"] >= MIN_CLASSIFICATION_SCORE:
                policy_discussed = policies_discussed_mapping.get(label_dict["label"])
                if (
                    policy_discussed is not None
                    and policy_discussed not in policies_discussed
                ):
                    policies_discussed.append(policy_discussed)

        objections_output = objection_classifier_pipeline(chunk)
        summarized_chunk = chunk
        for label_dict in objections_output:
            if label_dict["score"] >= MIN_CLASSIFICATION_SCORE:
                match label_dict["label"]:
                    case "LABEL_0":
                        # refurbishment quality
                        refurbishment_quality_issues.append(summarized_chunk)
                    case "LABEL_1":
                        # car issues
                        car_issues.append(summarized_chunk)
                    case "LABEL_2":
                        # price issues
                        price_issues.append(summarized_chunk)
                    case "LABEL_3":
                        # customer experience issues
                        customer_experience_issues.append(summarized_chunk)
                    case "LABEL_4":
                        # No label
                        pass
                policy_discussed = policies_discussed_mapping.get(label_dict["label"])
                if policy_discussed is not None:
                    policies_discussed.append(policy_discussed)
    ner_result = ner_pipeline(audio_transcript)
    sentiment_pipeline(audio_transcript)
    customer_requirements = {
        "car_type": None,
        "fuel_type": None,
        "color": None,
        "distance_travelled": None,
        "make_year": None,
        "transmission_type": None,
    }
    for entity_label in ner_result:
        entity = entity_label["entity"]
        lookup_field = ner_label_mapping.get(entity)
        if lookup_field is not None:
            customer_requirements[lookup_field] = entity_label["word"]
    return ExtractedData(
        customer_requirements=CustomerRequirements(**customer_requirements),
        company_policies_discussed=policies_discussed,
        customer_objections=CustomerObjections(
            refurbishment_quality=refurbishment_quality_issues,
            car_issues=car_issues,
            price_issues=price_issues,
            customer_experience_issues=customer_experience_issues,
        ),
    )
