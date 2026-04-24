FROM python:3.11-slim

# Install SWI-Prolog and its dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends swi-prolog git && \
    rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy the requirements file into the working directory
COPY backend/requirements.txt /app/backend/

# Install Python dependencies
RUN pip install --no-cache-dir gunicorn
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy the rest of the application
COPY . /app

# Expose the default port for Hugging Face Spaces
EXPOSE 7860

# Run the backend using gunicorn
CMD ["gunicorn", "--chdir", "backend", "-b", "0.0.0.0:7860", "app:app"]
