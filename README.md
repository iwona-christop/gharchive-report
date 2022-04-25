# Allegro. Data Engineer

An application processing archive of the public GitHub timeline.

## Installation
Application uses [Python 3](https://www.python.org/downloads/), [PySpark 3.2.1](https://spark.apache.org/docs/latest/api/python/) and [Github Archive Python SDK](https://github.com/nickderobertis/py-gh-archive).

To install required packages, run the following line in terminal:
```python
pip install -r requirements.txt
# If the above line doesn't work, try:
# python3 -m pip install -r requirements.txt
```

## Run
To use application, go to the project directory and run the following line in terminal:
```python
python3 main.py
```
Application will ask you to provide the month and year (`M/YYY`, e.g. `1/2015` or `12/2021`) to get events from the GitHub Archive for the desired period of time.

Then, if you wish, you can list all of the repositories available in selected period. After choosing one of them, enter the name of the repository.

Application will filter the data by repository name and ask you to choose the form of the report:
- `-sc` - to show the report in terminal,
- `-csv` - to export the report to csv file (`report.csv`),
- `-txt` - to export the report to txt file (`report.txt`).

## Technologies

### Python
**Python** language was selected mainly because of widely available libraries that save time and effort. It is also efficient, reliable, and much faster than most programming languages. That makes Python one of the most popular tools for **data science** and analytics.

### PySpark
**PySpark** is an interface for Apache Spark in **Python**. It allows to write Spark applications using Python APIs and provides the PySpark shell for interactively analyzing data in a distributed environment. Also, PySpark supports *most* of Spark's features.

### Github Archive Python SDK
**Github Archive Python SDK** is a simple Python SDK to access GitHub Archive.

It was chosen mainly because of issues with getting JSON archives directly from [GH Archive](http://www.gharchive.org/).

## Issues
As mentioned above, the **Github Archive Python SDK** was used because of issues with gettin archives directly from the [GH Archive](http://www.gharchive.org/). While trying to access the url with PySpark, some of the archives couldn't be received because of the HTTP `403 Forbidden` response status code, which means that the access is permanently forbidden and tied to the application logic, such as insufficient rights to a resource.

Second frustrating issue were the null objects in given `Archive`, which resulted in declaration of Spark's `DataFrame()` schema in the code.

The last problem was less annoying - the data type of `value` in all of the `MapType` fields in the `StructType` had to be changed to `StrinType()` (instead of `LongType()`), because `LongType()` couldn't accept some objects.