# Investing Ratios Scraper

This project is a web scraping tool designed to extract company financial ratios from Investing.com. It is divided into two main scripts: one for scraping company information and links (`scraping_companies.py`) and another for processing these links to extract detailed financial ratios (`process_ratios.py`).

## Project Structure

- `scraping_companies.py`: Script to scrape company names, URLs, and industries from Investing.com.
- `process_ratios.py`: Script to process the company URLs to extract financial ratios and save them to a CSV file.
- `requirements.txt`: List of Python dependencies required for the project.
- `chromedriver.exe`: Chrome WebDriver executable for Selenium.
- `README.md`: Project documentation (this file).

## Requirements

- Python 3.x
- Selenium
- Pandas
- Chrome WebDriver

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/bdonyan/investing-ratios.git
    cd investing-ratios
    ```

2. **Install the required Python packages:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Download and place the Chrome WebDriver executable in the project directory.**

## Usage

### Scraping Company Information

Run `scraping_companies.py` to scrape company names, URLs, and industries from Investing.com and save them to `company_links.csv`.

    ```bash
    python scraping_companies.py
    ```

### Extracting Financial Ratios

Run `process_ratios.py` to process the company URLs in `company_links.csv` and extract their financial ratios. The extracted data will be saved to `company_ratios.csv`.

    ```bash
    python process_ratios.py
    ```

## Error Handling

- The scripts are designed to log errors encountered during scraping and data extraction to a log file (`scraper.log`). This helps in debugging issues without stopping the entire scraping process.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For any inquiries or issues, please contact [Brandon Yan](mailto:branyan@seas.upenn.edu).
