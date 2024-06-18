FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Install Sphinx for documentation generation
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3-sphinx \
    && rm -rf /var/lib/apt/lists/*

# Generate Sphinx configuration (if needed)
# RUN sphinx-quickstart --quiet --sep --dot=_ --suffix=.rst --enable-autodoc .

# Generate documentation using Sphinx
RUN sphinx-apidoc -o docs .

CMD ["python", "app.py"]
