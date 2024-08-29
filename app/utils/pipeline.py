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

input_text = "Your sample text to classify."

# Perform classification
results = policy_classifier_pipeline(input_text)

# Display the results
print(results)
print(
    f"Predicted label: {results[0]['label']}, Confidence score: {results[0]['score']:.4f}"
)

# Perform classification
results = objection_classifier_pipeline(input_text)

# Display the results
print(results)
print(
    f"Predicted label: {results[0]['label']}, Confidence score: {results[0]['score']:.4f}"
)
