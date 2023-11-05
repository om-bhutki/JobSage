# Job Recommendation System (JobSage)

## Overview

The Job Recommendation System is a web-based platform that utilizes web scraping and APIs to help users find relevant job opportunities and enables companies to post their job listings. Additionally, the system offers a unique "Compare Companies" feature, allowing users to compare different companies based on various factors like average salary, ratings, and more.

## Features

### Job Search and Recommendation
- **Web Scraping**: Utilizes web scraping techniques to gather job listings from various online sources.
- **API Integration**: Integrates with job search APIs to provide an extensive database of job opportunities.

### Company Job Posting
- **Job Listing Management**: Allows companies to add job postings.

### Compare Companies
- **Comparison Metrics**: Enables users to compare companies based on metrics like average salary, employee ratings, company culture, benefits, etc.

## Technologies Used

- **Programming Languages**: Python
- **Frameworks and Libraries**: Flask (Python web framework), Bootstrap (front-end framework)
- **Web Scraping**: Beautiful Soup
- **APIs**: JSearch on rapidAPIS
- **Database**: sqlite

## How to Use

1. **Installation**
    - Clone the repository: `git clone https://github.com/om-bhutki/JobSage.git`
    - Install dependencies: `pip install -r requirements.txt`
    - Set up and configure any API keys required.

2. **Running the Application**
    - Navigate to the project directory.
    - Run `python main.py` to start the Flask server.
    - Access the application at `http://localhost:5000` in your web browser.

3. **Usage**
    - As a User: Search for jobs, view recommendations, and compare companies.
    - As a Company: Post job listings via the company dashboard.

## Contributing

We welcome contributions to improve the system. If you'd like to contribute, please follow these steps:
- Fork the repository.
- Create a new branch for your feature: `git checkout -b feature-name`
- Commit your changes: `git commit -m 'Add a new feature'`
- Push to the branch: `git push origin feature-name`
- Open a pull request.

## Contributors

- List of contributors and their respective contributions.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
