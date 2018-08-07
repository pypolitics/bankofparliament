# Bank of Parliament

## About

A project to inspect and display the register of interests of members of parliament.

Source of data:

* https://www.theyworkforyou.com.
* http://data.parliament.uk.
* https://api.companieshouse.gov.uk.

It is then parsed for data relating to financial interests and presented in a webpage:

https://pypolitics.github.io/bankofparliament/

The MP's can searched for and sorted by financial categories such as private income, property, shareholdings.

The data as well as the website are both a work in progress. I fully expected there to be incorrect data spread throughout.

## Requirements
* easy_install pip
* pip install requests
* pip install plotly
* pip install python-igraph
* pip install fuzzywuzzy
* pip install beautifulsoup4
* pip install fuzzywuzzy