# Webpage Summarizer using Flask and Sumy

## Webpage Summarizer

This project is a simple Flask web application that provides a REST API to summarize the content of a webpage. The summarization is performed using the Sumy library.

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- Sumy
- Other dependencies can be installed using `requirements.txt`.

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your_username/webpage-summarizer.git
    cd webpage-summarizer
    ```

2. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### Usage

1. **Run the Flask application:**

    ```bash
    python app.py
    ```

    The application will start, and you can access it at [http://localhost:5000](http://localhost:5000).

2. **Use the `/summarize` endpoint to get the summary of a webpage:**

    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"url": "https://example.com"}' http://localhost:5000/summarize
    ```

    Replace `"https://example.com"` with the URL of the webpage you want to summarize.

## API Endpoints

### 1. `/`

- **Method:** GET
- **Description:** Returns a welcome message.

### 2. `/summarize`

- **Method:** POST
- **Description:** Summarizes the content of a webpage.
- **Request Body:**
  ```json
  {
    "url": "https://example.com"
  }
 **Response:**
   ```
    {
      "summary": "The summarized content of the webpage."
    }

