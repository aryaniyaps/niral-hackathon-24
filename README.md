# Car Sales Audio Transcripts Analyzer and Information Extractor

Completely analyze car sales audio transcripts to extract valuable information by training fine-tuned BERT models.

## [Project resources- Video + Presentation](https://drive.google.com/drive/folders/1SqUv_jYMJ0DxaOfetY8sbM6LvGbdZqOj)

## Table of Contents

1. [Local Development - Instructions](#local-development---instructions)
   - [Prerequisites](#prerequisites)
   - [Install PDM](#install-pdm)
   - [Install Dependencies](#install-dependencies)
   - [Running the Application](#running-the-application)
2. [Project Structure](#project-structure)
3. [Code Explanation](#code-explanation)
   - [**init**.py](#__init__py)
   - [extract_data.py](#extract_datapy)
   - [label_customer_objections.py](#label_customer_objectionspy)
   - [label_company_policies.py](#label_company_policiespy)
   - [1_create_customer_objection_classification_dataset.ipynb](#1_create_customer_objection_classification_datasetipynb)
   - [2_finetune_bert_customer_objection_classification.ipynb](#2_finetune_bert_customer_objection_classificationipynb)
   - [3_create_policy_classification_dataset.ipynb](#3_create_policy_classification_datasetipynb)
   - [4_finetune_bert_policy_classification.ipynb](#4_finetune_bert_policy_classificationipynb)
   - [5_finetune_bert_case_sales_ner_classification.ipynb](#5_finetune_bert_case_sales_ner_classificationipynb)
   - [models.py](#modelspy)
   - [bulk_file_to_text.py](#bulk_file_to_textpy)
   - [label_mapping.py](#label_mappingpy)
   - [pdf_to_text.py](#pdf_to_textpy)
   - [pipeline.py](#pipelinepy)
4. [How It Works](#how-it-works)
5. [References](#references)

## Local Development - Instructions

### Prerequisites

- Python >= 3.12
- Docker Engine >= 4.29.0

### Install PDM

We use PDM as our package manager. PDM simplifies the management of dependencies and eliminates the need for a `requirements.txt` file.

```
pip install pdm -U
```

### Install Dependencies

You can manage project dependencies by running:

```
pdm install
```

### Running the Application

You can run the application using:

```
pdm run app
```

## Project Structure

```
.
├── app
│   ├── constants.py
│   ├── extract_data.py
│   ├── utils
│   │   ├── bulk_file_to_text.py
│   │   ├── pdf_to_text.py
│   │   ├── save_temp_file.py
│   └── __init__.py
├── models.py
├── label_customer_objections.py
├── label_company_policies.py
├── 1_create_customer_objection_classification_dataset.ipynb
├── 2_finetune_bert_customer_objection_classification.ipynb
├── 3_create_policy_classification_dataset.ipynb
├── 4_finetune_bert_policy_classification.ipynb
├── pipeline.py
├── README.md
```

---

## Code Explanation

### init.py

This file sets up the Gradio interface and defines functions to extract data from text, PDF, and bulk CSV files.

### extract_data.py

Contains the logic to extract data from audio transcripts, including chunking the transcripts and classifying policies and objections.

The BERT models applied to text classification tasks result in significant improvement of accuracy, especially in domains requiring nuanced understanding of language like customer interactions" (Devlin et al., 2019).

### label_customer_objections.py

Script to label customer objections in transcripts. It chunks the text and asks user to identify the chunk.

### label_company_policies.py

Similar to the above script but the labels identify company policies discussed by calling the transcripts.

It is extremely powerful how machine learning models can be, but when combined with weak training data, their power is greatly limited. "Manual annotation of complex interactions can, therefore, greatly improve the quality of training data, leading to much better model performance" .
Manning et al., 2020

### 1_create_customer_objection_classification_dataset.ipynb

This notebook creates a dataset for the classification of customer objections by loading labeled data and saving it to a CSV file.

### 2_finetune_bert_customer_objection_classification.ipynb

The goal of the notebook is to fine-tune a BERT model in order to classify customer objections using the dataset created in the first notebook.

_Fine-tuning pre-trained models on domain-specific datasets can yield significant improvements in task-specific performance" (Liu et al., 2019)_.

### 3_create_policy_classification_dataset.ipynb

This notebook reads labeled data and stores it in a CSV file to prepare a dataset for company policy classification.

### 4_finetune_bert_policy_classification.ipynb

This notebook is the one to finetune BERT for company policy classification with the dataset created in the previous step.

### 5_finetune_bert_case_sales_ner_classification.ipynb

This notebook fine-tunes a BERT model for Named Entity Recognition (NER) specific to car sales. It uses labeled data to identify and classify entities such as car models, customer names, and sales terms within the transcripts.

### models.py

In this module of the project, some data models are defined, namely CompanyPolicy, CustomerRequirements, CustomerObjections and ExtractedData.

_"Knowing clear data models is crucial for the structure and processing of textual data within classification tasks" (Jurafsky & Martin, 2020)._

### bulk_file_to_text.py

Utiliity that converts the content of bulk files, either CSV or plain text, to a list of strings, and returns the list.

### label_mapping.py

Mapping util between classifier labels and CompanyPolicy enums.

### pdf_to_text.py

Text extraction from pdf utilities. Support direct content picking or against OCR.

### pipeline.py

Define the policy and objection classification pipelines with pre-trained BERT models.

Automated pipelines in NLP workflow have been helpful in terms of processing big data and improving reproducibility (Mikolov et al., 2018).

---

## How It Works

![new_BERT_Overall (1)](https://github.com/user-attachments/assets/46031f80-99f0-42a2-a8db-a1c3f049b97b)


### Named Entity Recognition (NER) for Car Sales

We have fine tuned a NER model, and ran sentiment analysis in order to accurately extract the correct car details from the transcripts.

### Fine-tuned BERT Models

We make use of fine-tuned BERT models in the classification and extraction of information from car sales audio transcripts. In this regard, fine-tuning pre-trained BERT models on specific datasets for customer objections and company policies proves very accurate in a classification task.

\_" One of the most revolutionary aspects of recent NLP progress for BERT models is the capability to be fine-tuned for specific tasks" Raffel et al. 2020.

### Labeling and Annotating Conversations

The scripts `label_customer_objections.py` and `label_company_policies.py` are used to manually label and annotate the conversation files in chunks. The scripts break down the transcripts into manageable chunks, asking the user to label each chunk in such a way that the annotation is effective towards enhancing user-friendliness.

_"Merging human-in-the-loop approaches with machine learning models can enable more accurate and contextual labeling of conversation data" (Kumar et al., 2020)._

### Data Extraction and Analysis

Data extraction from labeled transcripts is done through the script extract_data.py. This script processes the audio transcripts, chunking them and utilizing the fine-tuned BERT models in classifying the content into customer objections and company policies. Once the data is structured in such a way, further analysis and insights may be derived.

\_ "Automatic information extraction and classification from audio transcripts is an important step towards generating actionable insight in customer service and sales domains" - Zhang et al. (2019) .

**Combining these manual labelings with our automated classification constitutes our solution, providing robustness in the analyses of car sale audio transcripts to businesses for acquiring insight into their customer interactions.**

---

### References

In J. Devlin, M.-W. Chang, K. Lee & K. Toutanova, BERT: Pre-training of deep bidirectional transformers for language understanding. arXiv, 1810.04805.
[Cited in: 10, 12, 12, 12, 14, 26, 26, 26]
INTRODUCTION TO INFORMATION RETRIEVAL, C. D. Manning, H. Schütze, and P. Raghavan, Cambridge University Press, 2020.
Y. Liu, M. Ott,.
Jurafsky, D., & Martin, J. H. (2020). Speech and Language Processing. _Pearson_.
Mikolov, T., Chen, K., Corrado, G., & Dean, J. (2018). Efficient estimation of word representations in vector space. _arXiv preprint arXiv:1301.3781_.
Raffel, C., Shazeer, N., Roberts, A., Lee, K., Narang, S., Matena, M.,. & Liu, P. J. (2020). Exploring the limits of transfer learning with a unified text-to-text transformer. _arXiv preprint arXiv:1910.10683_.Kumar, R., Natarajan, M., & Rose, C. (2020). Grounded representations for dialogue modeling. _arXiv preprint arXiv:2003.06084_. Zhang, Y., Wu, Y., & Sun, X. (2019). Enhancing extractive text summarization with sentiment analysis. \_Proceedings of the AAAI Conference on Artificial Intelligence.

---
