FROM python:3.10

WORKDIR /usr/src/app

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .


# Run the app
CMD ["python", "app.py"]
