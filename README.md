# Scripts Used to Wrangle Icelandic Spending Data

These are scripts I use to transform Icelandic Spendinga Data into a format that's better suited for loading it into [OpenSpending](http://openspending.org).

## wrangle-quarterly-reports.py

The Icelandic government releases quarterly reports showing amounts flowing from ministries to particular agencies.

Within each year these quarterly reports are cumulative, meaning the second quarterly report also includes the first. So in order to see amount flowing each quarter we need to subtract it from the previous quarter. Also there is no time column so this script can add a date to each row.

An example of input CSV files can be found on [opingogn.is](http://opingogn.is/dataset/arshlutauppgjor-rikissjoos-2012)

There are four parameters that can be provided to this script:

* *-i*: input file (csv file to modify) - *required*
* *-o*: output file (resulting csv file) - *required*
* *-d*: date (to append as a date column) - *required*
* *-p*: previous (previous quarterly report) - *optional*

## wrangle-category-rows.py

The Icelandic government releases two interesting datasets on a more visual format than practical (visual in Microsoft Excel terms). These datasets show government expenditure/revenue by category. Each category has its own row and each row includes all of the months.

This script takes such a file and creates 12 rows for each category (one for each month). This makes it more practical for analysis and automatic loading. Since there are two different datasets that use this format (they differ only in what the categories are called, e.g. "Expenditure categories" or "Revenue categories") the script allows the user to give the categories a descriptive header (the datasets use the oh so descriptive "Main category").

An example of input CSV files can be found on [opingogn.is](http://opingogn.is/dataset/gjold-rikissjoos-hagraen-skipting-2012)

There are four parameters that can be provided to this script:

* *-i*: input file (csv file to modify) - *required*
* *-o*: output file (resulting csv file) - *required*
* *-y*: year (will be added to the month) - *required*
* *-c*: category (header for category) - *optional*
