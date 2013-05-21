#! /usr/env python
# -*- encoding: utf-8 -*-
#
# Spread Icelandic government expenditure/revenue columns into lines
# Copyright (C) 2013  Tryggvi Björgvinsson
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys, getopt
import csv

import datetime
from dateutil.relativedelta import relativedelta

# Icelandic month names
MONTHS = ['Janúar', 'Febrúar', 'Mars', 'Apríl', 'Maí', 'Júní', 'Júlí',
          'Ágúst', 'September', 'Október', 'Nóvember', 'Desember']

def get_last_date(month, year):
    '''
    Get the last day of a given month. Month is given as a capitalized name
    and the year as integer.
    '''

    # Get first day of the month - we need to get the month number from
    # the MONTHS variable (and add one because of 0-index)
    first_day = datetime.datetime(year, MONTHS.index(month)+1, 1)

    # Use dateutil's relativedelta to get the last day
    last_day = first_day + relativedelta(day=31)

    # Return the last day as string
    return last_day.strftime('%Y-%m-%d')

def parse_csv(filename):
    '''
    Read the contents of the csv file into a list of lists for manipulation
    '''
    
    # Open the file and parse it
    csvfile = open(filename)
    csvread = csv.reader(csvfile)
    
    # Read rows into list and return them
    rows = [row for row in csvread]
    return rows

def wrangle_data(rows, year, category_name):
    '''
    Modify the data and create our actual output
    '''

    # Add header as first row
    modified_rows = [[category_name, 'Undirflokkur', 'Upphæð', 'Dagsetning']]

    # Get old header (to get the month names)
    old_header = rows[0]

    # Go through the rows in input data (skip header) and modify it
    # We also skip the last line because that's a total
    for row in rows[1:-1]:
        # Static within this row
        category = row[0]
        subcategory = row[1]

        # Go through the months and add a new row for each month
        for idx in range(2, len(row)):
            # Get last day of the month from the month name
            last_day = get_last_date(old_header[idx], year)
            # Parse the amount as integer (some entries have precision errors
            # so we need to parse it as float, add 0.5 to round properly
            amount = int(float(row[idx])+0.5)
            # Append the new row
            modified_rows.append([category, subcategory, amount, last_day])

    # Return the modified rows
    return modified_rows

def write_csv(rows, output):
    '''
    Write the rows to a new file. We use comma seperation and 
    quote all nonnumeric fields (it's simpler to work with).
    '''

    # Just open the file and write the rows to it
    csvfile = open(output, 'w')
    csvwrite = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
    csvwrite.writerows(rows)

def parse_commandline():
    '''
    Parse command line variables
    -i input-file (can also be args)
    -o output-file
    -y year
    -c category-name
    '''

    # Read command line args (-i, -o and -d are allowed)
    myopts, args = getopt.getopt(sys.argv[1:],"i:o:y:c:")
 
    # Store parse results in argument dictionary
    arguments = {}

    for option, argument in myopts:
        if option == '-i':
            arguments['input'] = argument
        elif option == '-o':
            arguments['output'] = argument
        elif option == '-y':
            arguments['year'] = int(argument)
        elif option == '-c':
            arguments['category name'] = argument
        else:
            # Do nothing if unrecognized
            pass

    return arguments

if __name__ == "__main__":
    # Get all the important arguments
    args = parse_commandline()

    # Parse csv file and split into headers and data
    input_rows = parse_csv(args['input'])
    
    # Get main category name (defaults to Yfirflokkur)
    category_name = args.get('category name', 'Yfirflokkur')
    
    # Modify the data
    modified_rows = wrangle_data(input_rows, args['year'], category_name)

    # Write the data to a new file (default file name: 'output.csv')
    write_csv(modified_rows, args.get('output', 'output.csv'))
