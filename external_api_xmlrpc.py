url = "http://0.0.0.0:8099"
db = "new_db"
username = "admin"
password = "admin"

import xmlrpc.client
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
v = common.version()
print(v)

#getting Uid
uid = common.authenticate(db, username, password, {})
print('Uid = ',uid)

# Endpoint of selecting a model
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Fetch all entity of a particular model
partners = models.execute_kw(db, uid, password,
    'hospital.management', 'search',
    [[]], {'limit':5})
print('partners = ',partners)

#read the specific field values of the achieved entities
records = models.execute_kw(db, uid, password,
    'hospital.management', 'read', [partners], {'fields': ['name_seq', 'patient_name', 'patient_age']})

for record in records:
	print('Records = ',record)

#fetch and read together
records = models.execute_kw(db, uid, password,
    'hospital.management', 'search_read', [[]], {'fields': ['name_seq', 'patient_name']})

for record in records:
	print('Search and Read Records = ',record)

#inspect a model’s fields and check which ones seem to be of interest [fields_get()]
#field_infos = models.execute_kw(
#    db, uid, password, 'hospital.management', 'fields_get',
#    [], {'attributes': ['string', 'help', 'type']})
#for item in field_infos:
#	print('field_info = ',item,'\n')

#The method will create a single record and return its database identifier.
#id = models.execute_kw(db, uid, password, 'hospital.management', 'create', [{
#    'patient_name': "New Patient",
#}])

print("************ Update and Delete **************")

update = models.execute_kw(db, uid, password, 'hospital.management', 'write', [[22], {
    'patient_name': "Third again Updated patient"
}])

update = models.execute_kw(db, uid, password, 'hospital.management', 'name_get', [[22]])
print('update = ',update)
