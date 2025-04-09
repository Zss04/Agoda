FROM mcr.microsoft.com/playwright/python:v1.51.0-noble

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    playwright install --with-deps

# Copy the rest of your project files
COPY . .

CMD ["./run_tests.sh"]