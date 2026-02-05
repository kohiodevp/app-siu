FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# --- Dépendances système ---
RUN apt-get update && apt-get install -y \
    software-properties-common \
    gnupg \
    wget \
    python3 \
    python3-pip \
    python3-dev \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*


# Copier ton code
COPY . /app

# Installer requirements Python
RUN pip3 install --no-cache-dir -r requirements.txt

# Lancer Django
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "10000"]