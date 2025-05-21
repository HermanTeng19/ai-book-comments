# 图书评论生成器

一个使用Nvidia DeepSeek R1 API为中文图书生成小红书风格书评的Python工具。

## 概述

该脚本通过以下步骤自动生成图书评论：

1. 从Markdown文件（默认：`top25Book_douban.md`）中读取图书数据
2. 向Nvidia DeepSeek R1 API发送请求，为每本书生成评论
3. 将生成的评论保存为指定目录中的Markdown文件

## 特点

- 自动生成300-500字的图书评论
- 支持自定义输出目录
- 提供干运行模式（不调用API）
- 可选择跳过已存在的评论（不覆盖模式）
- 自动移除AI输出中的思考过程标签
- 提供文件对话框选择输入的Markdown文件

## 环境要求

- Python 3.6+
- 所需包：
  - `requests`
  - `python-dotenv`
  - `tkinter`（通常随Python一起安装）

## 安装步骤

1. 克隆此仓库：
   ```
   git clone https://github.com/HermanTeng19/ai-book-comments.git
   cd ai-book-comments
   ```

2. 安装所需包：
   ```
   pip install requests python-dotenv
   ```

3. 在项目根目录创建`.env`文件，包含您的Nvidia API密钥：
   ```
   api_key=your_nvidia_api_key_here
   ```

## 使用方法

### 基本用法

使用默认设置运行脚本：

```
python book_review_generator.py
```

这将：
- 提示您选择一个Markdown文件（默认为`top25Book_douban.md`）
- 为每本书生成评论
- 将评论保存到`bookComments`目录

### 命令行参数

该脚本支持多个命令行参数：

- `--output-dir`：指定自定义输出目录
  ```
  python book_review_generator.py --output-dir 我的评论
  ```

- `--dry-run`：在干运行模式下运行（不调用API）
  ```
  python book_review_generator.py --dry-run
  ```

- `--no-overwrite`：跳过已有评论的图书
  ```
  python book_review_generator.py --no-overwrite
  ```

- 组合多个参数：
  ```
  python book_review_generator.py --output-dir 测试评论 --dry-run --no-overwrite
  ```

## 输入文件格式

输入的Markdown文件应包含以下格式的图书信息表格：

| 序号 | 书名 | 作者 | 原书名 | 年份 | 译者 | 出版社 | 评分 | 豆瓣书评 |
|------|------|------|--------|------|------|--------|------|---------|
| 1 | 书名 | 作者 | 原书名 | 年份 | 译者 | 出版社 | 评分 | 评论 |

## 输出格式

每个生成的评论将保存为具有以下结构的Markdown文件：

```markdown
# 《书名》书评

作者: 作者名  
豆瓣评分: 评分  

[生成的评论内容]
```

## API使用说明

- 根据文档，Nvidia DeepSeek R1 API没有特定的RPM/RPD限制
- 脚本在请求之间添加了2秒的延迟，以避免潜在的速率限制
- 在高流量期间，请求可能会出现延迟

## 许可证

[MIT许可证](LICENSE)

## 致谢

- 本项目使用Nvidia DeepSeek R1模型生成评论
- 图书数据来源于豆瓣Top 25图书