# Book Review Generator

A Python tool that uses the Nvidia DeepSeek R1 API to generate book reviews for Chinese books in a Xiaohongshu (Little Red Book) style format.

## Overview

This script automates the generation of book reviews by:

1. Reading book data from a markdown file (default: `top25Book_douban.md`)
2. Sending requests to the Nvidia DeepSeek R1 API to generate reviews for each book
3. Saving the generated reviews as markdown files in a specified directory

## Features

- Automatic generation of 300-500 word book reviews
- Support for custom output directories
- Dry-run mode for testing without API calls
- Option to skip already existing reviews (non-overwrite mode)
- Removal of AI thinking process tags from the output
- File dialog for selecting the input markdown file

## Requirements

- Python 3.6+
- Required packages:
  - `requests`
  - `python-dotenv`
  - `tkinter` (usually comes with Python)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/HermanTeng19/ai-book-comments.git
   cd ai-book-comments
   ```

2. Install the required packages:
   ```
   pip install requests python-dotenv
   ```

3. Create a `.env` file in the project root with your Nvidia API key:
   ```
   api_key=your_nvidia_api_key_here
   ```

## Usage

### Basic Usage

Run the script with default settings:

```
python book_review_generator.py
```

This will:
- Prompt you to select a markdown file (defaults to `top25Book_douban.md`)
- Generate reviews for each book
- Save them to the `bookComments` directory

### Command Line Arguments

The script supports several command line arguments:

- `--output-dir`: Specify a custom output directory
  ```
  python book_review_generator.py --output-dir my_reviews
  ```

- `--dry-run`: Run in dry-run mode (no API calls)
  ```
  python book_review_generator.py --dry-run
  ```

- `--no-overwrite`: Skip books that already have reviews
  ```
  python book_review_generator.py --no-overwrite
  ```

- Combine multiple arguments:
  ```
  python book_review_generator.py --output-dir test_reviews --dry-run --no-overwrite
  ```

## Input File Format

The input markdown file should contain a table with book information in the following format:

| 序号 | 书名 | 作者 | 原书名 | 年份 | 译者 | 出版社 | 评分 | 豆瓣书评 |
|------|------|------|--------|------|------|--------|------|---------|
| 1 | Book Title | Author | Original Title | Year | Translator | Publisher | Rating | Comment |

## Output Format

Each generated review is saved as a markdown file with the following structure:

```markdown
# 《Book Title》书评

作者: Author  
豆瓣评分: Rating  

[Generated review content]
```

## Notes on API Usage

- The Nvidia DeepSeek R1 API does not have specific RPM/RPD limits according to documentation
- The script adds a 2-second delay between requests to avoid potential rate limiting
- During high traffic periods, requests may experience delays

## License

[MIT License](LICENSE)

## Acknowledgements

- This project uses the Nvidia DeepSeek R1 model for review generation
- Book data sourced from Douban Top 25 Books