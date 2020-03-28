import json, csv, datetime
import pandas as pd
from hubspot import get_all_contact_properties, get_all_contacts
import logging
import missingno as msno 
import numpy as np


logging.basicConfig(filename='logger.log', format='%(asctime)s Module %(module)s %(message)s',level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info("Initialized")

API_KEY = ''

def get_key():
    input_key = input("Enter API key (default demo returns HS demo data):")
    if not input_key:
        input_key = 'demo'
    return input_key

def get_filename_to_analyze():
    filename = input("Please enter filename of the file to analyze (default if blank):")
    if not filename:
        filename = "1584456153hs_contact_list.csv"
        print(f"Will use default filename {filename}")
    return filename



def main():
    input_choice = input("Welcome to PropPose.  \n1) Run local file \n2) Refresh data \n3) Quit \n \n Make a selection:")
    
    if input_choice == '1':
        logger.info(f'User chose to run local file')
        filename = get_filename_to_analyze()
        logger.debug(f"Main will attempt to summarize from file {filename}")        
        outputDF = summarize_csv(filename)
        ts = int(datetime.datetime.now().timestamp())
        summary_file = str(ts) + 'hs_prop_pose' + '.csv'
        outputDF.to_csv(summary_file)
        # outputDF.to_csv(summary_file, index_label=['Property name', 'Records Count', "% of total", "Another assessment"])
        print(f"Your file is now available at \n{summary_file}")
        raise SystemExit

    elif input_choice == '2':
        logger.info(f'User chose to refresh data')
        # get key
        apikey = get_key()    
        logging.debug(f"Before get_data, API Key is {apikey}")
        

        # query Hubspot to get data
        filename = get_data(apikey)
        
        #Summarize data
        logger.debug(f"Main will attempt to summarize from file {filename.name}")
        outputDF = summarize_csv(filename.name)

        ts = int(datetime.datetime.now().timestamp())
        summary_file = str(ts) + 'hs_prop_pose' + '.csv'
        outputDF.to_csv(summary_file)
        # outputDF.to_csv(summary_file, index_label=['Property name', 'Records Count', "% of total", "Another assessment"])
        print(f"Your file is now available at \n{summary_file}")
        raise SystemExit

    elif input_choice == '3':
        logger.info(f'User chose to quit program')
        raise SystemExit
    else:
        print("Invalid choice.")
        raise SystemExit


def get_data(apikey='demo'):
    '''
    This fn gets Data from Hubspot and returns csv output of data.  CSV allows for process to fail nicely

    '''
    logging.debug(f'Inside get_data. api key here is {apikey}')
    property_list = get_all_contact_properties(key_value=apikey)
    logger.debug(f"Property List received.  Length: {len(property_list)}")

    fieldnames = []
    for p in property_list:
        fieldnames.append(p['name'])

    contact_list = get_all_contacts(fieldnames, key_value=apikey)
    logger.info(f" contacts received.  Length: {len(contact_list)}")

    # Format filename to save data
    ts = int(datetime.datetime.now().timestamp())
    contacts_file = str(ts) + 'hs_contact_list' + '.csv'


    # Write field with all fieldnames as headers.  Edit this to include all contacts

    
    
    # opens file and writes rows for each contact 
    with open(contacts_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        i = 0
        for item in contact_list: # for each contact
            logger.debug(f"writing value for contact {i}")
            row = {}
            for k in item['properties']:
                row.update({k : item['properties'][k]['value']})
            writer.writerow(row)            
            i +=1
    return csvfile

def summarize_csv(csv_input):
    '''
    this method takes a csv file as input and analyzes it, adding more data
    '''
    df = pd.read_csv(csv_input, dtype=object, index_col=0)
    
    df1 = pd.DataFrame({'Records Count': df.count()})    
    max_count = df1['Records Count'].max()
    df1['Pct of total'] = 100* (df1['Records Count'] / max_count)

    bins = [0, 
            0.0000001, # from >0 to < 5
            5, # from 5 to < 15
            15, 
            50, 
            90, 
            100, 
            np.inf
            ]
    names = [
        "Not used at all",
        "Extremely low coverage",
        "Low coverage",
        "Some coverage",
        "Majority coverage",
        "Very high coverage"
        "Full coverage - likely default field",
        "Very High coverage",
    ]
    df1['Assessment'] = pd.cut(df1['Pct of total'], bins, labels=names)
    df1['Assessment'] = np.where(df1['Pct of total'] == 0, 'No Coverage', df1['Assessment'])
    df1.index.name = "Property name"
    
    logger.info(f'Function summarize_csv completed.  Returning DataFrame.')
    logger.info(df1.head())
    return df1

if __name__ == '__main__':
    main()