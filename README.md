# Unbabel Command Line Interface

The Unbabel CLI is a command line tool that allows you to parse the log files to extract the moving average of the translation delivery time split by minute, you can also extract the amount of requests done by each client and the language pairs used in the translations and how many times it was used.
It can parse a log file containing a stream of json objects, separated by line or inside a json array.

## Instalation

This software was developed using only the builtin libs of Python and, theoretically, should work with Python 3.6+, but it was only tested using Python 3.8.0 for Windows.
It can be installed by cloning this repo:
```bash
git clone https://github.com/legionaryu/backend-engineering-challenge.git
```
Or downloading it as zip from GitHub and unpacking it to a folder:
![Download zip from GitHub](/doc/download_zip.jpg?raw=true)

Then if you want to use it as a module in your own program, you will have to install it by running the following command:
```bash
python3 setup.py install
```

## Usage

To use the software you can use the python interpreter to execute the script **unbabel_cli.py** like the following example:
```bash
python3 unbabel_cli.py --input-file sample.txt
```
Or use it as a module in your python program by importing like this:
```python
import unbabel_cli
```

The script accepts the following arguments:
```
__*--input-file*__
    The log file path that will be parsed, this argument is required.

*--window-size*
    The window size, in minutes, that will be used to calculate the moving average. The default window size is **10** minutes.

*--property*
    The property that will be used as reference to calculate the average. The possible values are **duration** or **nr_words**, the default value is **duration**.

*--clients-report*
    If this flag is added to the argument list, the software will print a report of all clients that have requested a translation and the number of requests per client

*--languages-report*
    If this flag is added to the argument list, the software will print a report of all language pairs, a language pair consists in a unique set of source language and target language, used in the translations request and the amount of requests per language pair
```
