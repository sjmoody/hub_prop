
import json, csv, datetime
import pandas as pd
from hubspot import getAllContactProperties, getAllContacts
import logging

logging.basicConfig(filename='logger.log', format='%(asctime)s Module %(module)s %(message)s',level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info("Initialized")




def main():
    ts = int(datetime.datetime.now().timestamp())
    contacts_file = str(ts) + 'hs_contact_list' + '.csv'
    summary_file = str(ts) + 'hs_field_trip' + '.csv'
    # get data
    getData(contacts_file)
    # count fields in csv
    countFieldsInCsv(contacts_file, summary_file)

def getData(csv_output):    
    property_list = getAllContactProperties()
    logger.debug(f"Property List received.  Length: {len(property_list)}")

    fieldnames = []
    for p in property_list:
        fieldnames.append(p['name'])

    contact_list = getAllContacts(fieldnames)
    logger.info(f" contacts received.  Length: {len(contact_list)}")
    # Write field with all fieldnames as headers.  Edit this to include all contacts
    
    
    # opens file and writes rows for each contact 
    with open(csv_output, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        i = 0
        for item in contact_list: # for each contact
            logger.info(f"value for contact {i}: ")
            row = {}
            for k in item['properties']:
                row.update({k : item['properties'][k]['value']})
            writer.writerow(row)            
            i +=1
    return

def countFieldsInCsv(csv_input, csv_output):
    df = pd.read_csv(csv_input, index_col=0)
    # creates df with property values in col 1, count of non null contacts in col 2.  No headers yet
    trip = df.count()
    trip.to_csv(csv_output, index_label=['property', 'contacts'])
    logger.info(f'countFieldsInCsv completed.  Informating placed in {csv_output}')


if __name__ == '__main__':
    main()