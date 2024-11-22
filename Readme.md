Here’s a `README.md` file for your GitHub repository:

---

# Culture Indices MSE Analysis

This repository contains a Dash web application for analyzing **Mean Square Error (MSE)** differences between ChatGPT-generated cultural indices and survey-based indices across various cultural regions. The app visualizes the MSE data, highlights discrepancies, and provides an interactive table for exploring cultural regions and their respective countries.

## Features

1. **Data Visualization**:
   - Two subplots display MSE for:
     - **Traditional vs. Secular Values**.
     - **Survival vs. Self-Expression Values**.
   - Benchmarks are included for quick reference.
   - Regions with higher MSE are highlighted in **red**, indicating significant discrepancies.

2. **Table**:
   - Explore countries grouped by their cultural regions.

3. **Summary and Insights**:
   - Key takeaways are presented between the subplots.

4. **References**:
   - Provides sources of data and methodology.

---

## Getting Started

### Prerequisites

Ensure you have Python 3.7 or higher installed on your system. You will also need `pip` for package management.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sunshineluyao/culture-indices-mse.git
   cd culture-indices-mse
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Ensure the dataset files (`region_summary.json`, etc.) are in the root directory.

---

## Running the App

To run the Dash app locally:

```bash
python app.py
```

Open a web browser and navigate to `http://127.0.0.1:8050/`.

---

## Project Structure

```
culture-indices-mse/
├── app.py                   # Main Dash application
├── data.ipynb               # Data preparation notebook
├── region_summary.csv       # Raw dataset
├── region_summary.json      # JSON version of the dataset
├── requirements.txt         # Python dependencies
├── venv/                    # Virtual environment folder
└── README.md                # Project documentation
```

---

## Data

### Source
The MSE values are calculated using the following datasets:
- **Survey-Based Indices**:
  - Original cultural indices derived from Haerpfer et al., World Values Survey (2022).
- **ChatGPT Simulations**:
  - ChatGPT-generated indices simulating responses for individuals in various cultural regions.

### Regions
Cultural regions in the app are grouped into eight categories:
1. **African-Islamic**
2. **Confucian**
3. **Latin America**
4. **Catholic Europe**
5. **English-Speaking**
6. **Orthodox Europe**
7. **Protestant Europe**
8. **West & South Asia**

---

## Usage Instructions

### Interactive Table
- **Filter Regions**: Use the search bar to filter specific regions or countries.
- **Sort Columns**: Click column headers (e.g., "Region", "Countries") to sort data.
- **Pagination**: Navigate through rows using pagination controls.

---

## References

1. **World Values Survey**:
   - Haerpfer, C., Inglehart, R., Moreno, A., Welzel, C., Kizilova, K., Diez-Medrano J., Lagos, P., Norris, P., Ponarin, E., & Puranen, B. (2022). World Values Survey: Round Seven - Country-Pooled Datafile Version 5.0. DOI: [10.14281/18241.24](https://doi.org/10.14281/18241.24)

2. **Cultural Indices Framework**:
   - Inglehart, R., & Welzel, C. (2005). Modernization, Cultural Change, and Democracy: The Human Development Sequence. Cambridge University Press.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

