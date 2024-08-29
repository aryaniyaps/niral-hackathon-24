from transformers import pipeline

# Define the pipeline
policy_classifier_pipeline = pipeline(
    "text-classification",
    model="aryaniyaps/finetuned-bert-policy-classifier",
    device="cuda",
)

objection_classifier_pipeline = pipeline(
    "text-classification",
    model="haz3-jolt/finetuned-bert-cst-obj-classifier",
    device="cuda",
)


ner_pipeline = pipeline(
    "ner", model="alstonpeter/finetuned-bert-car-sales-ner", device="cuda"
)

sentiment_pipeline = pipeline("sentiment-analysis", device="cuda")
