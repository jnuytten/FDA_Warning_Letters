# FDA_Warning_Letters
Evaluate FDA Warning Letters using NLP

The scripts and notebook in this repository provide the following functionality:
- retrieve links and meta-information of warning letters by crawling FDA website
- download warning letters as text file from FDA website
- evaluate warning letters for cited 21CFR references and most common observations


Prerequisites
-------------
You need to have the following installed to run the code
- MySQL Server
- Python
- Jupyter notebooks
- SQLAlchemy
- BeautifulSoup
- Selenium and chrome webdriver
- Pandas
- NLTK

Create a directory 'letters', this is used to download the warning letters.

Create a (new) SQL database and update connection string in script-crawl_to_db.py and script-download_letters.py

Set up two tables in the new database, you can use the following CREATE TABLE statements:

CREATE TABLE `list` (
  `posted` date DEFAULT NULL,
  `issued` date DEFAULT NULL,
  `company` varchar(150) DEFAULT NULL,
  `office` varchar(150) DEFAULT NULL,
  `subject` varchar(150) DEFAULT NULL,
  `link` varchar(250) DEFAULT NULL,
  `id` varchar(150) DEFAULT NULL,
  UNIQUE KEY `id` (`id`)
)

CREATE TABLE `temptable` (
  `posted` date DEFAULT NULL,
  `issued` date DEFAULT NULL,
  `company` varchar(150) DEFAULT NULL,
  `office` varchar(150) DEFAULT NULL,
  `subject` varchar(150) DEFAULT NULL,
  `link` varchar(250) DEFAULT NULL,
  `id` varchar(150) DEFAULT NULL,
  UNIQUE KEY `id` (`id`)
)

Include files
-------------
webcrawl.py : helper functions for crawling the website
pageproc.py : helper functions to download letters
dataprep.py : helper functions for data analysis
obsan.py : helper functions to evaluate observation texts
utility.py : utility functions


Scripts and notebooks
---------------------
script-crawl_to_db.py : crawl complete website and put links in database,
	or if database already contains records add new links while existing links remain in the database

script-download_letters.py : download all missing letters from website to the letters directory

nlp_analysis_report.ipynb : data analysis, requires populated database and downloaded letters




