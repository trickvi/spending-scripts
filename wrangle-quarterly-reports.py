#! /usr/env python
# -*- encoding: utf-8 -*-
#
# Add and modify fiels of the Icelandic government's quarterly report
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

def split_ministry_name(ministry):
    '''
    In the data the ministry is shown as:
    "02 Mennta- og menningarmálaráðuneyti"

    We want to split the first two id numbers and the name into
    separate fields (to get more beatiful names
    '''

    # This really needs to be checked (should be two digits)
    ministry_id = ministry[:2]
    # Remove whitespace
    ministry_name = ministry[2:].strip()

    # Return as list
    return [ministry_id, ministry_name]

def wrangle_data(rows, date):
    '''
    Modify the data, split out the ministry id and add the date.
    Set the amount as integer
    '''

    # Modify the header
    header = rows[0]
    # First field should be id
    header.insert(0, 'Auðkenni ráðuneytis')
    # Last field should be last date of quarter
    header.append('Lokadagsetning ársfjórðungs')

    # Header is the first row
    modified_data_rows = [header]

    # Go through the rest of the rows in input data and modify it
    for row in rows[1:]:
        # Split the ministry name
        modified = split_ministry_name(row[0])
        # Append 'rasto' (whatever that is) and receiving public agency
        modified.extend(row[1:3])
        # Append amount as int
        modified.append(int(row[3]))
        # Add the date
        modified.append(date)

        # Add row to modified data rows 
        modified_data_rows.append(modified)

    # Return the modified rows
    return modified_data_rows

def subtract_previous_total(rows, previous_rows):
    '''
    Go through the previous year and subtract it from the current one
    since the amount is cumulative in each quarter. Assuming unique key
    is ministry (list item no. 1 and ministry, list item no. 3) and
    amount is stored in list item no. 4.
    '''

    # Parse previous year into a dictionary
    previous_quarter = {}
    for row in previous_rows[1:]:
        previous_quarter[(row[1], row[3])] = row[4]

    # Subtract previous amount from the amount in current quarter
    # Spit out the row with the adjusted amount
    modified_rows = rows[:1]
    for row in rows[1:]:
        previous_amount = previous_quarter.get((row[1], row[3]), 0)
        row[4] -= previous_amount
        modified_rows.append(row)

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
    -d date-to-add
    -p previous-total
    '''

    # Read command line args (-i, -o and -d are allowed)
    myopts, args = getopt.getopt(sys.argv[1:],"i:o:d:p:")
 
    # Store parse results in argument dictionary
    arguments = {}

    for option, argument in myopts:
        if option == '-i':
            arguments['input'] = argument
        elif option == '-o':
            arguments['output'] = argument
        elif option == '-d':
            arguments['date'] = argument
        elif option == '-p':
            arguments['previous'] = argument
        else:
            # Do nothing if unrecognized
            pass

    return arguments

if __name__ == "__main__":
    # Get all the important arguments
    args = parse_commandline()

    # Parse csv file and split into headers and data
    input_rows = parse_csv(args['input'])
    
    # Modify the data
    modified_rows = wrangle_data(input_rows, args['date'])

    # Check for previous quarter and parse+wrangle if exists
    # then adjust current modified_rows
    if 'previous' in args:
        previous_parsed = parse_csv(args['previous'])
        previous_rows = wrangle_data(previous_parsed, "don't care")
        modified_rows = subtract_previous_total(modified_rows, previous_rows)

    # Write the data to a new file (default file name: 'output.csv')
    write_csv(modified_rows, args.get('output', 'output.csv'))
