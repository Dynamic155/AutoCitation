# AutoCitation
Generate Harvard-style references for web pages. Given a list of URLs, it fetches each page, extracts relevant metadata (like title, author, and publication date), and formats it into a reference. The references are then written to an output file.

## Features

- Fetches web pages using the provided URLs.
- Extracts title, author, and publication date from the web pages.
- Formats the extracted information into Harvard-style references.
- Writes the references to an output file.

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library

You can install the required libraries using pip:

```sh
pip install requests beautifulsoup4
```

## Usage

1. **Prepare the input file**: Create a file named `urls.txt` in the same directory as the script, or just clone the repository. Then list each URL you want to process on a new line.

2. **Run the script**: Execute the script by running the following command in your terminal:

    ```sh
    python autocite.py
    ```

3. **Check the output**: The generated references will be written to a file named `references.txt` in the same directory.

## Example

**urls.txt**

```
https://example.com/article1
https://example.com/article2
```

**Generated references.txt**

```
Doe, J. (2020) Example Article 1. Available at: https://example.com/article1 (Accessed: 27 May 2024).

Smith, A. (2021) Example Article 2. Available at: https://example.com/article2 (Accessed: 27 May 2024).
```

## Thank you for using
If you found this tool helpful please star the repository <3

## Contributing

If you encounter any issues or have suggestions for improvement, please open an issue or submit a pull request.
