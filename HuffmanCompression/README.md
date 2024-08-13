# Huffman Compression and Decompression
Welcome to the Huffman Compression and Decompression project! 
This project implements the Huffman algorithm, a popular method for lossless data compression.

## Installation
To get started, follow these steps:
1.Clone the repository:
```bash
git clone https://github.com/JadeAffolabi/Python-Projects.git
cd HuffmanCompression
```
2.Install the required dependencies:
```bash
poetry install
or
pip install -r requirements.txt
```
3.Activate virtual environment:
```bash
poetry shell
```

## Usage
The project provides a command-line interface for compressing and decompressing files.
### Compress a File
To compress a file, use the following command:
```bash
python3 huff.py c file_name compressed_file_name
```
### Decompress a File
To decompress a file, use the following command:
```bash
python3 huff.py d compressed_file_name decompressed_file_name
```
