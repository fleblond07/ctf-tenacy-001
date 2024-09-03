FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN echo TENACY{$(head -c 16 /dev/urandom | base64 | tr -dc 'a-zA-Z0-9' | head -c 32)} > /app/secrets.txt

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn
# Copy the Flask application code into the container
COPY app.py .

EXPOSE 5000

# Run the Flask application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
