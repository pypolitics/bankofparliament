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

At the time of writing, the British General Election is just over a week away.

## Todo

* Add photo's of MP's.
* Parse for values other than 15% when parsing the shareholding data.
* Perform companies house lookup on shareholding data, ascertain value / assets and set the amount value according to the percentage.
* Find properties registered to mp (if possible), query zoopla for current market value (if possible), assign more accurate value to property wealth. Rental income may also be possible.
* Ensure government positions are correctly matched. Currently, The Prime Minister matches Minister, so Theresa May gets underpaid by £40,000.
* For shareholdings less than 15% but more than £70,000, try and use companies house data to find actual value.
* Add better logic for parsing phrases like "i own a third of a cottage", to return 0.33% of the value.
* Add citation links to data.
* Add a third view where the all the data for a single MP is exposed, including all the records.
* Add an ability to submit edit requests to allow for the correcting of bad data.
