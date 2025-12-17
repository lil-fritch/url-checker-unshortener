# URL Parser & Unshortener

A Python utility designed to extract URLs from a pickled dataset, check their availability status, and resolve shortened links (unshorten).

## 📋 Features

* **Data Extraction:** Loads raw data using the `pickle` module and extracts URLs using `urlextract`.
* **Status Checking:** Verifies the availability of each URL via `requests.head` (with a fallback to `GET` for 405 responses).
* **Unshortening:** Resolves redirects to determine the final destination URL.
* **Concurrency:** Utilizes multi-threading for efficient network I/O operations.
* **Robust Logging:** Implemented with `loguru` featuring file rotation (every 5 mins) and retention (20 mins history).

## 🛠 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/lil-fritch/url-checker-unshortener.git
    cd url-checker-unshortener
    ```

2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Usage

Run the main entry point:

```bash
python main.py

```

The script will:

1. Read data from `data/messages_to_parse.dat`.
2. Process URLs in parallel.
3. Output logs to the `logs/` directory.
4. Print execution statistics to the console.

## 🏗 Architecture & Design Decisions

### Why Threading?

I utilized `concurrent.futures.ThreadPoolExecutor` for this task.

* **I/O Bound Task:** The primary bottleneck in this application is network latency (waiting for HTTP responses), not CPU computation.
* **GIL Efficiency:** In Python, the Global Interpreter Lock (GIL) is released during I/O operations. This allows multiple threads to wait for network responses concurrently, significantly speeding up the process compared to synchronous execution.
* **Overhead:** `Multiprocessing` was deemed unnecessary as it incurs higher memory and startup overhead without providing benefits for non-CPU-intensive tasks.

### Logging Configuration

Logs are handled by `loguru` to meet the specific rotation requirements:

* **Rotation:** New log file created every 5 minutes.
* **Retention:** Old log files are automatically removed after 20 minutes.

## 📊 Performance Results

* **Execution Time:** 22.73 seconds
* **Total URLs Processed:** 71

---

*Author: Bohdan Pupkov*

```