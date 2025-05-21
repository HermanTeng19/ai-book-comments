#!/usr/bin/env python3
"""
Book Review Generator using Nvidia DeepSeek R1 API

This script:
1. Allows user to select an MD file (default: top25Book_douban.md)
2. Reads book data from the selected file
3. Generates book reviews using the Nvidia DeepSeek R1 API
4. Saves reviews as markdown files in the bookComments folder

Note: The Nvidia DeepSeek R1 API does not have specific RPM/RPD limits,
but requests during high traffic may experience delays.
"""

import os
import re
import json
import time
import requests
import tkinter as tk
import argparse
from tkinter import filedialog
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Constants
DEFAULT_FILE = "top25Book_douban.md"
DEFAULT_OUTPUT_DIR = "bookComments"
NVIDIA_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Generate book reviews using Nvidia DeepSeek R1 API.')
    parser.add_argument('--output-dir', type=str, default=DEFAULT_OUTPUT_DIR,
                        help=f'Output directory for reviews (default: {DEFAULT_OUTPUT_DIR})')
    parser.add_argument('--dry-run', action='store_true',
                        help='Run in dry-run mode (no API calls)')
    parser.add_argument('--no-overwrite', action='store_true',
                        help='Skip books that already have reviews (do not overwrite)')
    return parser.parse_args()

def select_file():
    """Open a file dialog to select an MD file, defaulting to top25Book_douban.md."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    default_file = os.path.join(current_dir, DEFAULT_FILE)
    
    # Open file dialog with the default file selected
    file_path = filedialog.askopenfilename(
        initialdir=current_dir,
        initialfile=DEFAULT_FILE,
        title="Select a book list file",
        filetypes=(("Markdown files", "*.md"), ("All files", "*.*"))
    )
    
    # If no file is selected, use the default
    if not file_path:
        file_path = default_file
        print(f"No file selected, using default: {DEFAULT_FILE}")
    else:
        print(f"Selected file: {file_path}")
        
    root.destroy()
    return file_path

def parse_book_data(file_path):
    """Parse book data from the markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find table rows
    table_pattern = r'\|\s*(\d+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|'
    rows = re.findall(table_pattern, content)
    
    books = []
    for row in rows:
        # Skip header row or separator row (if any)
        if row[0].isdigit():
            book = {
                'rank': row[0],
                'title': row[1].strip(),
                'author': row[2].strip(),
                'original_title': row[3].strip(),
                'year': row[4].strip(),
                'translator': row[5].strip(),
                'publisher': row[6].strip(),
                'rating': row[7].strip(),
                'comment': row[8].strip()
            }
            books.append(book)
    
    return books

def remove_think_tags(content):
    """Remove content within <think>...</think> tags."""
    if not content:
        return content
    # Remove think tags and their contents
    return re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL)

def generate_dummy_review(book):
    """Generate a dummy review for dry-run mode."""
    return f"""【这是一个模拟生成的书评，没有实际调用API】

《{book['title']}》是一本令人印象深刻的作品，豆瓣评分高达{book['rating']}分！

作者{book['author']}以其独特的写作风格带领读者进入了一个引人入胜的世界。正如豆瓣短评所说："{book['comment']}"，这本书确实值得每个人细细品味。

出版于{book['year']}年的这部作品展现了作者深厚的功力和独到的见解。无论是情节构建还是人物塑造，都堪称一流。

如果你正在寻找一本能够带给你思考和感动的好书，《{book['title']}》绝对是不二之选。它不仅仅是一本书，更是一次心灵的旅程。

强烈推荐给所有热爱阅读的朋友们！
"""

def generate_review(book, api_key, dry_run=False):
    """Generate a book review using the Nvidia DeepSeek R1 API."""
    if dry_run:
        print(f"[Dry Run] Generating dummy review for '{book['title']}'")
        return generate_dummy_review(book)
    
    prompt = f"""
请你写一篇关于《{book['title']}》的书评，以发布在小红书平台上。
要求：
1. 字数控制在300-500字
2. 风格要符合小红书的文风，生动活泼，有吸引力
3. 引用书中的经典段落或观点
4. 给出个人感受和推荐理由
5. 提到作者{book['author']}的写作风格特点

书籍信息：
- 作者：{book['author']}
- 原书名：{book['original_title']}
- 出版年份：{book['year']}
- 出版社：{book['publisher']}
- 豆瓣评分：{book['rating']}
- 豆瓣短评：{book['comment']}

请直接给出书评内容，不要有多余的解释。
"""

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": "deepseek-ai/deepseek-r1",
        "temperature": 0.6,
        "top_p": 0.7,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "max_tokens": 4096,
        "stream": False,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    try:
        print(f"正在调用API生成《{book['title']}》的书评...")
        response = requests.post(NVIDIA_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise exception for non-200 status codes
        
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        # Remove thinking process from the response
        content = remove_think_tags(content)
        return content
    except requests.exceptions.RequestException as e:
        print(f"Error calling API for book '{book['title']}': {str(e)}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return None
    except (KeyError, IndexError) as e:
        print(f"Error parsing API response for book '{book['title']}': {str(e)}")
        print(f"Response: {response.text if response else 'No response'}")
        return None

def get_review_path(book, output_dir):
    """Get the path for a book review file."""
    # Create a valid filename from the book title
    filename = re.sub(r'[\\/*?:"<>|]', '', book['title'])
    filename = filename.replace(' ', '_')
    return os.path.join(output_dir, f"{filename}.md")

def save_review(book, review, output_dir, overwrite=True):
    """Save the generated review to a markdown file."""
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = get_review_path(book, output_dir)
    
    # Check if file exists
    if os.path.exists(file_path):
        if not overwrite:
            print(f"跳过 - 文件已存在: {file_path}")
            return file_path
        else:
            print(f"覆盖旧文件: {file_path}")
    
    # Write to file (overwriting if it exists)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"# 《{book['title']}》书评\n\n")
        f.write(f"作者: {book['author']}  \n")
        f.write(f"豆瓣评分: {book['rating']}  \n\n")
        f.write(f"{review}\n")
    
    print(f"成功保存书评: {file_path}")
    return file_path

def main():
    # Parse command line arguments
    args = parse_arguments()
    
    # Get API key from .env file (not needed in dry-run mode)
    api_key = None
    if not args.dry_run:
        api_key = os.environ.get("api_key")
        if not api_key:
            api_key = input("API key not found in .env file. Please enter your Nvidia API key: ")
            if not api_key:
                print("No API key provided. Exiting.")
                return
    
    # Select markdown file
    file_path = select_file()
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    # Parse book data
    books = parse_book_data(file_path)
    if not books:
        print("No book data found in the file.")
        return
    
    print(f"找到 {len(books)} 本书。开始生成书评...")
    print(f"输出目录: {args.output_dir}")
    if args.dry_run:
        print("运行在【模拟模式】(不会调用API)")
    if args.no_overwrite:
        print("运行在【不覆盖模式】(已有书评将被跳过)")
    
    # Generate reviews for each book
    for i, book in enumerate(books):
        print(f"\n处理第 {i+1}/{len(books)} 本书: {book['title']}")
        
        # Check if review already exists
        review_path = get_review_path(book, args.output_dir)
        if os.path.exists(review_path) and args.no_overwrite:
            print(f"跳过 - 书评已存在: {review_path}")
            continue
        
        # Add delay to respect API rate limits (not needed in dry-run mode)
        if i > 0 and not args.dry_run:
            delay_time = 2  # 2-second delay between requests
            print(f"等待 {delay_time} 秒以避免API限流...")
            time.sleep(delay_time)
        
        # Generate review
        review = generate_review(book, api_key, args.dry_run)
        if review:
            # Save review (overwrite if exists unless --no-overwrite is set)
            save_review(book, review, args.output_dir, not args.no_overwrite)
        else:
            print(f"为《{book['title']}》生成书评失败")
    
    print(f"\n所有书评已生成! 文件保存在 '{args.output_dir}' 目录下。")

if __name__ == "__main__":
    main()