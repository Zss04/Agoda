FROM mcr.microsoft.com/playwright/python:v1.51.0-noble

WORKDIR /app

ENV PYTHONPATH=/app

RUN apt-get update && \
    apt-get install -y nodejs npm libglib2.0-0 libnss3 libatk1.0-0 libcups2 libxss1 libxrandr2 libgbm1

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    playwright install --with-deps

# Copy Node.js dependencies and install them
COPY package*.json .
RUN npm install 


# Copy the rest of your project files
COPY . .

CMD ["npm", "run","test:all-browsers"]