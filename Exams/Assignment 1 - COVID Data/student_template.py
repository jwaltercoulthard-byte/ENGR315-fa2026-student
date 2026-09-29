import sys
import numpy as np

"""
Create a program which will provide answers to the questions posed in the assignment description.
We've provided a function which will parse the NYT covid database file (named "us-counties.csv"); 
however, its correct implementation will be up to you. DO NOT MODIFY THIS FUNCTION.
Your code needs to be successful as well as sufficiently commented/documented to receive full credit.
"""

#SETUP FILEPATH
myfilepath = "data/covid/us-counties.csv"



def parse_nyt_data(file_path=''):
    """
    Parse the NYT covid database and return a list of tuples. Each tuple describes one entry in the source data set.
    Date: the day on which the record was taken in YYYY-MM-DD format
    County: the county name within the State
    State: the US state for the entry
    Cases: the cumulative number of COVID-19 cases reported in that locality
    Deaths: the cumulative number of COVID-19 death in the locality

    :param file_path: Path to data file
    :return: A List of tuples containing (date,county, state, fips, cases, deaths) information

    ____________________ DO NOT MODIFY THIS FUNCTION ___________________
    """
    # data point list
    data=[]

    # open the NYT file path
    try:
        fin = open(file_path)
    except FileNotFoundError:
        print('File ', file_path, ' not found. Exiting!')
        sys.exit(-1)

    # get rid of the headers
    fin.readline()

    # while not done parsing file
    done = False

    # loop and read file
    while not done:
        line = fin.readline()

        if line == '':
            done = True
            continue

        # format is date,county,state,fips,cases,deaths
        (date,county, state, fips, cases, deaths) = line.rstrip().split(",")

        # clean up the data to remove empty entries
        if cases=='':
            cases=0
        if deaths=='':
            deaths=0

        # convert elements into ints
        try:
            entry = (date,county,state, fips, int(cases), int(deaths))
        except ValueError:
            print('Invalid parse of ', entry)

        # place entries as tuple into list
        data.append(entry)


    return data

### YOUR CODE HERE ###

def main(filepath):
    #Function to run program logic


    # Parse the NYT data
    covid_data = parse_nyt_data(filepath)

    # Print the parsed data for verification
    
    #First, need to go through the data and find only the harrisonburg and rockingham county data
    #This will make the rest of the analysis easier

    #setup lists
    harrisonburg_data = []
    rockingham_data = []


    #iterate through the data and filter for harrisonburg and rockingham county data
    for entry in covid_data:
        date, county, state, fips, cases, deaths = entry #extract the data from the tuple

        if county.lower() in ['harrisonburg city'] and state.lower() in ['virginia']: #check for location and state
            harrisonburg_data.append(entry)

        elif county.lower() in ['rockingham'] and state.lower() in ['virginia']: #do the same for rockingham
            rockingham_data.append(entry)

    # Print the filtered data commented out for sanity check
    # for entry in harrisonburg_data:
    #     date, county, state, fips, cases, deaths = entry
    #     print(f"Date: {date}, County: {county}, State: {state}, FIPS: {fips}, Cases: {cases}, Deaths: {deaths}")

    # for entry in rockingham_data:
    #     date, county, state, fips, cases, deaths = entry
    #     print(f"Date: {date}, County: {county}, State: {state}, FIPS: {fips}, Cases: {cases}, Deaths: {deaths}")

    """
    QUESTION 1: When was the first positive COVID case in Harrisonburg? 
    When was the first positive case in Rockingham County? (2 questions)
    """

    #Since the data is sorted by date, the loop method won't have to loop very many times, so I'll use that one here


    #start with harrisonburg data
    first_harrisonburg_case = None
    for entry in harrisonburg_data:
        date, county, state, fips, cases, deaths = entry
        if cases > 0: #check for first positive case
            first_harrisonburg_case = date
            break

    # Now find the first positive case in Rockingham County
    first_rockingham_case = None
    for entry in rockingham_data:
        date, county, state, fips, cases, deaths = entry
        if cases > 0: #check for first positive case
            first_rockingham_case = date
            break

    # Print the answer
    print(f"First positive case in Harrisonburg: {first_harrisonburg_case}")
    print(f"First positive case in Rockingham County: {first_rockingham_case}")



    """
    QUESTION 2: On what date was the greatest number of new cases reported in Harrisonburg? 
    What date in Rockingham County? (2 questions)
    """

    #start with harrisonburg data, I'm gonna do this one with list functions
    hburg_dates = [entry[0] for entry in harrisonburg_data] #get the dates
    hburg_cases = [entry[4] for entry in harrisonburg_data] #get the cases

    #find the max cases, entry number of that, and the corresponding date
    max_hburg_cases = max(hburg_cases)
    max_hburg_index = hburg_cases.index(max_hburg_cases)
    max_hburg_date = hburg_dates[max_hburg_index]

    # Now find the date with the greatest number of new cases in Rockingham County
    rockingham_dates = [entry[0] for entry in rockingham_data]
    rockingham_cases = [entry[4] for entry in rockingham_data]
    max_rockingham_cases = max(rockingham_cases)
    max_rockingham_index = rockingham_cases.index(max_rockingham_cases)
    max_rockingham_date = rockingham_dates[max_rockingham_index]

    # Print the answer
    print(f"Date with greatest number of new cases in Harrisonburg: {max_hburg_date} with {max_hburg_cases} cases")
    print(f"Date with greatest number of new cases in Rockingham County: {max_rockingham_date} with {max_rockingham_cases} cases")

    """
    QUESTION 3: What was the worst seven-day period in Harrisonburg city for new COVID cases? 
    What period in Rockingham County? 
    These are the seven-day periods when the number of new cases was maximal. (2 questions)
    """

    #So there's two ways this question could be intended to be answered
    #One is to go week by week and find the week with the most cases, but since the data sets
    #start on different days of the week, that would be odd
    #I will therefore answer this with the a rolling 7 day sum, which is more accurate anyways

    #Thankfully, we already have dates and cases lists, so we can continue with those, just make them njmpy arrays
    np_hburg_cases = np.array(hburg_cases)
    np_rockingham_cases = np.array(rockingham_cases)

    hburg_rolling_sum = np.convolve(np_hburg_cases, np.ones(7), 'valid') #rolling sum of 7 days
    rockingham_rolling_sum = np.convolve(np_rockingham_cases, np.ones(7), 'valid')

    #find the max rolling sum and the corresponding date range and entry of max
    max_hburg_rolling_sum = np.max(hburg_rolling_sum)
    entry_of_max_hburg = np.argmax(hburg_rolling_sum)
    start_date_hburg = hburg_dates[entry_of_max_hburg]
    end_date_hburg = hburg_dates[entry_of_max_hburg + 6] # Assuming 7-day period


    max_rockingham_rolling_sum = np.max(rockingham_rolling_sum)
    entry_of_max_rockingham = np.argmax(rockingham_rolling_sum)
    start_date_rockingham = rockingham_dates[entry_of_max_rockingham]
    end_date_rockingham = rockingham_dates[entry_of_max_rockingham + 6] # Assuming 7-day period

    # Print the answer
    print(f"Worst seven-day period in Harrisonburg: {start_date_hburg} to {end_date_hburg} with {max_hburg_rolling_sum} cases")
    print(f"Worst seven-day period in Rockingham County: {start_date_rockingham} to {end_date_rockingham} with {max_rockingham_rolling_sum} cases")








#Run main
main(myfilepath)