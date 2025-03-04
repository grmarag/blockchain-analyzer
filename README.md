# Blockchain Analyzer

Blockchain Analyzer is a robust, end-to-end Python toolkit for analyzing blockchain transaction data. It provides capabilities for:

- **Clustering & Address Profiling:** Identify transaction behavior patterns using clustering algorithms like HDBSCAN (or KMeans), and profile addresses based on transaction activity.
- **Anomaly Detection:** Detect outliers in transaction amounts (using Isolation Forest) and sender activity (using Local Outlier Factor).
- **Network Analysis:** Build a directed transaction graph, compute centrality metrics, and identify key network hubs.
- **AI-Driven Insights:** Generate comprehensive insight reports by leveraging the OpenAI API, summarizing clustering, anomaly, and network analysis findings.
- **Visualization:** Create static plots and interactive network visualizations to better understand and present the data.

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Running the Analysis Pipeline](#running-the-analysis-pipeline)
  - [Generating Visualizations](#generating-visualizations)
  - [Generating Insight Reports](#generating-insight-reports)
- [Directory Structure](#directory-structure)
- [Testing](#testing)
- [Docker Support](#docker-support)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Data Loading:** Efficiently load and validate blockchain transaction data from JSONL files.
- **Clustering:** Compute address features (e.g., sent/received totals and counts) and cluster addresses using scalable algorithms.
- **Anomaly Detection:** Identify unusual transaction amounts and sender activities with proven machine learning methods.
- **Network Analysis:** Build and analyze a transaction graph to reveal influential addresses and network properties.
- **AI Insights:** Automatically generate detailed insight reports using the OpenAI API.
- **Visualization:** Export plots for clustering, anomaly detection, and network graphs, including interactive network visualizations.

---

## Prerequisites

- **Python 3.8+**
- **Poetry** (or use pip with the provided `pyproject.toml`/`poetry.lock` for dependency management)
- A valid **OpenAI API Key** (to be set in the environment)
- [Docker](https://www.docker.com/) *(optional, for containerized deployment)*

---

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your_username/blockchain-analyzer.git
   cd blockchain-analyzer
   ```

2. **Install dependencies using Poetry:**

   ```bash
   poetry install
   eval $(poetry env activate)
   ```

   *Alternatively, if you prefer pip, install the required packages from `pyproject.toml`.*

3. **Set up the environment:**

   Create a `.env` file in the root directory with the following content:

   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   This key is required for generating AI-based insight reports.

---

## Configuration

- **API Keys & Environment Variables:**  
  The project uses a configuration module (`src/config.py`) to load environment variables from the `.env` file using [python-dotenv](https://github.com/theskumar/python-dotenv). Ensure that your `.env` file contains a valid `OPENAI_API_KEY`.

- **Clustering Parameters:**  
  The default clustering method is HDBSCAN with a minimum cluster size of 5. You can adjust parameters in the code if needed.

- **Anomaly Detection Settings:**  
  Both Isolation Forest and Local Outlier Factor are used with a contamination rate of 0.01 by default. Adjust these parameters in `src/anomaly_detection.py` as needed.

---

## Usage

### Running the Analysis Pipeline

The main analysis pipeline is implemented in `src/analyzer.py`. To run the full blockchain analysis, execute the following command:

```bash
python src/analyzer.py --input data/raw/transfers.jsonl
```

This script performs the following steps:
- Loads transaction data from the specified JSONL file.
- Executes clustering, anomaly detection, and network analysis.
- Saves results (CSV files) in the `data/final` directory.
- Generates visualizations and interactive network visualizations in the `figures` directory.
- Generates AI-powered report.

### Generating Visualizations

The project includes utilities for plotting:
- **Clusters:** View the clustering of addresses.
- **Anomalies:** Visualize both amount and activity anomalies.
- **Network Graph:** Generate an interactive HTML visualization of the transaction network.

These visualizations are automatically saved to the `figures` directory when running the analysis.

### Generating Insight Reports

For an AI-powered insight report:
- This module uses `AIAgent` (in `src/ai_agent.py`) to generate a detailed report via OpenAI’s API.
- Optionally, the generated report can be exported as a PDF using FPDF.

---

## Directory Structure

```
├── Dockerfile
├── LICENSE
├── README.md
├── data
│   ├── final                  # Output CSVs from the analysis
│   │   ├── activity_anomalies.csv
│   │   ├── amount_anomalies.csv
│   │   ├── clustering_results.csv
│   │   ├── network_centrality.csv
│   │   ├── network_edges.csv
│   │   └── network_hubs.csv
│   └── raw                    # Raw blockchain transaction data
│       └── transfers.jsonl
├── figures                    # Generated visualizations (PNG and HTML)
│   ├── activity_anomalies.png
│   ├── amount_anomalies.png
│   ├── clustering.png
│   ├── transaction_network.html
│   └── transcaction_network.png
├── poetry.lock
├── pyproject.toml
├── reports                    # AI-generated report files
│   └── report.md
├── src                        # Main project source code
│   ├── ai_agent.py            # AI insight report generation using OpenAI API
│   ├── analyzer.py            # Main analysis pipeline
│   ├── anomaly_detection.py   # Transaction anomaly detection
│   ├── clustering.py          # Address feature computation and clustering
│   ├── config.py              # Environment configuration and API keys
│   ├── data_loader.py         # Data loading and validation
│   ├── network_analysis.py    # Transaction network construction and analysis
│   └── utils.py               # Utility functions for plotting and visualization
└── tests                      # Unit tests for all modules
    ├── test_ai_agent.py
    ├── test_anomaly_detection.py
    ├── test_clustering.py
    ├── test_data_loader.py
    └── test_network_analysis.py
```

---

## Testing

Run the test suite to verify that all modules are working correctly:

```bash
poetry run python -m pytest
```

This command will run all the tests defined in the `tests` directory.

---

## Docker Support

A Dockerfile is provided for containerized deployment. To build and run the Docker container:

1. **Build the image:**

   ```bash
   docker build -t blockchain-analyzer .
   ```

2. **Run the container:**

   ```bash
   docker run blockchain-analyzer
   ```

This mounts local `data` and `figures` directories into the container so that outputs can be easily accessed.

---

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your_feature`.
3. Commit your changes: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature/your_feature`.
5. Open a Pull Request.

For major changes, please open an issue first to discuss what you would like to change.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

With this toolkit, you can gain valuable insights into blockchain transaction behavior, detect suspicious activity, and visualize complex network interactions—all while leveraging advanced AI insights.

Enjoy!