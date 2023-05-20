# Project Name: Baiterek App

This project implements an image classification model using FastAPI and PyTorch to classify images of sightseeing in Astana, Kazakhstan into one of eight categories: 'akorda', 'baiterek', 'khanshatyr', 'mangilikel', 'mosque', 'nuralem', 'piramida', and 'shabyt'. The project is built into a Docker container using the `zironycho/pytorch:1.6.0-slim-py3.7-v1` base image.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)

## Installation

1. Clone the repository:

```
git clone https://github.com/beketm/mnasnet
```

2. Change directory to the cloned repository:

```
cd mnasnet
```

3. Build the Docker image:

```
docker build -t mnasnet-image-classification .
```

4. Run the Docker container:

```
docker run -d -p 80:80 mnasnet-image-classification
```

The service will now be available at `http://localhost:80`.

## Usage

To use the image classification service, you need to send a POST request to the `/predict/image` endpoint with a JSON payload containing the base64 encoded image as a string.

Example using Python:

```python
import requests
import base64

url = "http://localhost:80/predict/image"

with open("path/to/your/image.jpg", "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

payload = {"file": encoded_image}
response = requests.post(url, json=payload)

print(response.json())
```

## API Documentation

### POST /predict/image

Classify an image as one of the eight landmark categories.

#### Request

- Body:
  - `file` (string, required): Base64 encoded image string (JPG or PNG format).

#### Response

- Success (200 OK):
  - `class` (string): Predicted landmark category.
  - `confidence` (float): Confidence level of the prediction.

- Error (400 Bad Request, 500 Internal Server Error):
  - `error` (string): Error message.
  - `error_traceback` (string): Error traceback.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests to improve the project.

