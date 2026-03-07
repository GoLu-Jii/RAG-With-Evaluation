# Use a lightweight Python base image
FROM python:3.11-slim

# Set up a new user named "user" with user ID 1000
# Hugging Face Spaces requires a non-root user for security
RUN useradd -m -u 1000 user

# Switch to the new user
USER user

# Set home to the user's home directory
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Set the working directory
WORKDIR $HOME/app

# Copy your requirements first to leverage Docker cache
COPY --chown=user requirements.txt $HOME/app/

# Install dependencies (PyTorch, FastAPI, sentence-transformers, etc.)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your FastAPI code into the container
COPY --chown=user . $HOME/app/

# Hugging Face Spaces strictly routes traffic to port 7860
EXPOSE 7860

# Run Uvicorn on port 7860
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]