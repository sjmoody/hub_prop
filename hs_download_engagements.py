import hubspot, csv, json, datetime




def splitEngagements(data):
    # takes input list of engagements, separates into different obj for each type of engagement
    meetings = list(filter(lambda x: x['engagement']['type'] == 'MEETING', data))
    notes = list(filter(lambda x: x['engagement']['type'] == 'NOTE', data))
    tasks = list(filter(lambda x: x['engagement']['type'] == 'TASK', data))
    calls = list(filter(lambda x: x['engagement']['type'] == 'CALL', data))
    emails = list(filter(lambda x: x['engagement']['type'] == 'EMAIL', data))

    newResults = {'meetings': meetings, 'notes': notes, 'tasks': tasks, 'calls': calls, 'emails': emails}
    print("results so far: ")
    print("meetings: ", len(newResults['meetings']))
    return newResults

def saveMeetings(meetings):
    # structures data and then saves csv
    # This approach writes headers into every row
    with open('output-meetings.csv', 'w', newline='') as f:
        print("type of input for meetings: ", type(meetings))
        w = csv.DictWriter(f, [
            'id',
            'portalId',
            'active',
            'createdAt',
            'lastUpdated',
            'ownerId',
            'type',
            'timestamp',
            'contactIds',
            'companyIds',
            'dealIds',
            'ownerIds',
            'body',
            'startTime',
            'endTime',
            'title'
        ], extrasaction='ignore')
        w.writeheader()
        for e in meetings:
            row = {**e['engagement'], **e['associations'], **e['metadata']}
            
            w.writerow(row)    

def saveNotes(notes):
        # structures data and then saves csv
    # This approach writes headers into every row
    with open('output-notes.csv', 'w', newline='') as f:
        print("type of input for notes: ", type(notes))
        print('length of notes: ', len(notes))
        w = csv.DictWriter(f, [
            'id',
            'portalId',
            'active',
            'createdAt',
            'lastUpdated',
            'ownerId',
            'type',
            'timestamp',
            'contactIds',
            'companyIds',
            'dealIds',
            'ownerIds',
            'body'
        ], extrasaction='ignore')
        w.writeheader()
        for e in notes:
            row = {**e['engagement'], **e['associations'], **e['metadata']}
            
            w.writerow(row)    

def saveCalls(calls):
    # structures data and then saves csv
    # This approach writes headers into every row
    with open('output-calls.csv', 'w', newline='') as f:
        print("type of input for calls: ", type(calls))
        w = csv.DictWriter(f, [
            'id',
            'portalId',
            'active',
            'createdAt',
            'lastUpdated',
            'ownerId',
            'type',
            'timestamp',
            'contactIds',
            'companyIds',
            'dealIds',
            'ownerIds',
            'toNumber',
            'fromNumber',
            'status',
            'externalId',
            'durationMilliseconds',
            'externalAccountId',
            'recordingUrl',
            'body',
            'disposition'
        ], extrasaction='ignore')
        w.writeheader()
        for e in calls:
            row = {**e['engagement'], **e['associations'], **e['metadata']}
            
            w.writerow(row)  

def saveTasks(tasks):
   # structures data and then saves csv
    # This approach writes headers into every row
    with open('output-tasks.csv', 'w', newline='') as f:
        print("type of input for tasks: ", type(tasks))
        w = csv.DictWriter(f, [
            'id',
            'portalId',
            'active',
            'createdAt',
            'lastUpdated',
            'ownerId',
            'type',
            'timestamp',
            'contactIds',
            'companyIds',
            'dealIds',
            'ownerIds',
            'body',
            'subject',
            'status',
            'forObjectType'
        ], extrasaction='ignore')
        w.writeheader()
        for e in tasks:
            row = {**e['engagement'], **e['associations'], **e['metadata']}
            
            w.writerow(row)  

def saveEmails(emails):
   # structures data and then saves csv
    # This approach writes headers into every row
    with open('output-emails.csv', 'w', newline='') as f:
        print("type of input for emails: ", type(emails))
        w = csv.DictWriter(f, [
            'id',
            'portalId',
            'active',
            'createdAt',
            'lastUpdated',
            'ownerId',
            'type',
            'timestamp',
            'contactIds',
            'companyIds',
            'dealIds',
            'ownerIds',
            'from',
            'email',
            'firstName',
            'lastName',
            'to',
            'cc',
            'bcc',
            'subject',
            # 'html', # removing to clean
            'text',
            
        ], extrasaction='ignore')
        w.writeheader()
        for e in emails:
            row = {**e['engagement'], **e['associations'], **e['metadata']}
            
            w.writerow(row)  
    

# data = hubspot.getAllContacts()
# gets allproperties and their properties
# property_list = hubspot.getAllContactProperties()
# # make array of propertynames
# property_name_list = []
# for prop in property_list:
#     property_name_list.extend(prop['name'])


property_name_list = [
    'lastmodifieddate',
    'firstname',
    'lastname',
    'email',
    'company',
    'hs_analytics_source',
    'hs_analytics_source_data_1',
    'hs_analytics_source_data_2',
    'leadsource',
    'custom_source',
    'utm_campaign',
    'utm_source',
    'utm_content',
    'utm_term',
    'utm_medium',
    
]

hubspot.saveAllContacts(property_name_list)

print('end')


# load data from file and write to csv 


    


# firstname = data[i]['properties']['firstname']['value']
# lastname = data[i]['properties']['lastname']['value']
# company = data[i]['properties']['company']['value']
# lastmodifieddate = data[i]['properties']['lastmodifieddate']['value']
# profile-url = data[i]['profile-url']


# # get data from API.  Returns 'dict'.  Can convert to string with dumps
# data = hubspot.getAllEngagements()
# print("app has the data")
# # Save data to json file
# with open('output.txt', 'w') as f: 
#     json.dump(data, f)

# # Load data from file
# with open('output.txt') as f:
#     data = json.load(f)
#     print('data loaded from txt. Type:', type(data))
#     print(len(data))
#     slices = splitEngagements(data)
#     print('count of meetings:', len(slices['meetings']))
#     saveMeetings(slices['meetings'])
#     print('count of notes', len(slices['notes']))
#     saveNotes(slices['notes'])
#     print("count of calls", len(slices['calls']))
#     saveCalls(slices['calls'])
#     print("count of tasks", len(slices['tasks']))
#     saveTasks(slices['tasks'])
#     print('count of emails', len(slices['emails']))
#     saveEmails(slices['emails'])
    
    
