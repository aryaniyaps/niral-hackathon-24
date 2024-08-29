# First stage: Build environment
FROM python:3.12-slim as builder

# Install PDM
RUN pip install pdm==2.17.3
# disable update check
ENV PDM_CHECK_UPDATE=false

# Configure PDM to use a specific location for the virtual environment
RUN pdm config python.use_venv true
RUN pdm config venv.location /project/.venv

# Set the working directory
WORKDIR /project

# Copy project files
COPY pyproject.toml pdm.lock ./

# Copy the rest of the application files
COPY . .

# Install dependencies
RUN pdm install --prod --frozen-lockfile --no-editable

# Second stage: Runtime environment
FROM python:3.12-slim

# Install linux packages (if needed)
# Install poppler and tesseract dependencies
RUN apt-get update && apt-get install -y poppler-utils tesseract-ocr libtesseract-dev && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /project

# Copy only the necessary files from the builder stage
COPY --from=builder /project/.venv/ /project/.venv
COPY --from=builder /project /project

ENV PYTHONPATH="."
ENV PATH="/project/.venv/bin:$PATH"

EXPOSE 7860

ENV GRADIO_SERVER_NAME="0.0.0.0"

# Set the entry point
CMD ["python", "app/__init__.py"]