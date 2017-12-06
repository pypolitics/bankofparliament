# Notpolitics

## About

A project to inspect and display the register of interests of members of parliament.

Source of data:

* https://www.theyworkforyou.com.
* http://data.parliament.uk.
* https://api.companieshouse.gov.uk.

It is then parsed for data relating to financial interests and presented in a webpage:

https://pypolitics.github.io/notpolitics/

The MP's can searched for and sorted by financial categories such as private income, property, shareholdings.

The data as well as the website are both a work in progress. I fully expected there to be incorrect data spread throughout.

Now that a functioning webpage is up, I intend on cleaning up the data and checking for inaccuracies.

## Requirements
* easy_install pip
* pip install requests
* pip install plotly
* pip install python-igraph

## Todo

* add a back button to shareholding plot
* about page

* companies house lookup on miscellaneous, family lobbyists - find a company to make an item
* find companies for donors
* find companies for private employment
* if there is a shareholder of a company that is also a company they have shares, link with dotted line (example, andrew bridgen)

* Firefox, Chrome etc compatibility
* Use flexbox for grid layout
* Show companies house nodes on separate graph layer
* Mobile / Tablet compatibility
* Add panama and paradise leaks to companies / people linked to mp

* Ability to show web of connections, between other MP's (and thier companies), the members of those other companies. Web to show the entirety of parliament (or selected mps) or single web of one person, that can be travelled.
* Add another record when a company has had previous names.
* Find other companies house users that dont identify themselves as an mp, but do match the date of birth / address as a user this is definately an MP.
* Evaluate the fuzzy filtering.
* Business / Companies House search input.
* Get ownership of shares from Companies House.
* Explore what data there is from https://companycheck.co.uk/. They seem to have net worth, assets, liabilities.
* Figure out the way to display the other appointees of a company the mp is an appointee of. Do we search people too?
* Perform companies house lookup on shareholding data, ascertain value / assets and set the amount value according to the percentage.
* Find properties registered to mp (if possible), query zoopla for current market value (if possible), assign more accurate value to property wealth. Rental income may also be possible.
* For shareholdings less than 15% but more than £70,000, try and use companies house data to find actual value.
* Add better logic for parsing phrases like "i own a third of a cottage", to return 0.33% of the value.
* Add an ability to submit edit requests to allow for the correcting of bad data.
