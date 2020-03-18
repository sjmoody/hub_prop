import hubspot, csv, json
import logging
# checks local file for last names containing first name
logging.basicConfig(filename='logger.log', format='%(asctime)s Module %(module)s %(message)s',level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info("Initialized")



def nameNormalizationFromCsv():
    firstInLastCount = 0
    firstEqualsLastCount = 0
    totalCounted = 0
    with open('hs_contact_list1583775945.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['firstname'] in row['lastname']: 
                firstInLastCount+=1            
            if row['firstname'] == row['lastname']:
                firstEqualsLastCount +=1
            totalCounted += 1
        logger.info(f"count completed.  First in last: {firstInLastCount}. First Equals Last: {firstEqualsLastCount}.  Total processed: {totalCounted}")
