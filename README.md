# hub_prop

field_trip.py: Runs a query of Hubspot database for all records with all properties and sums count of records with a non null value for each property.  Saves as local file.

hubspot.py: wrapper(?) for hubspot api 

csvHandler.py - manages some of the read/write for csv files.  

hs_download_engagements.py - addresses a specific use case where the engagements returned by Hubspot can not be filtered on the search, need to return all engagements and then filter for the type.  Each type has its own metadata structure.  This file collects them and then creates separate files for each.  Can be used for migrating to another CRM and keeping activity history