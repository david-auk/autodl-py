import os
import mysql.connector as database
import json
import getpass
import functions

# Defining the dictionary structure
mariadb = {
	'credentials': {
		'user': "",
		'password': "",
	},
	'connection': {
		'host': "",
		'database': ""
	}
}

telegram = {
	'credentials': {
		'token': ''
	},
	'chatid': {
		'hostChatId': '',
		'adminChatId': [''],
		'userChatId': ['']
	}
}

configuration = {
	'general': {
		'backupDir': ''
	}, 
}

# Defining diffirent tables and types
myTables = {
	'account': {
		'title': {
			'type': 'text'
		},
		'id': {
			'type': 'char(25)'
		},
		'priority': {
			'type': 'int(11)'
		}
	},
	'content': {
		'title': {
			'type': 'text'
		},
		'childfrom': {
			'type': 'text'
		},
		'id': {
			'type': 'char(12)'
		},
		'videopath': {
			'type': 'text'
		},
		'extention': {
			'type': 'text'
		},
		'deleted': {
			'type': 'int(11)'
		},
		'requestuser': {
			'type': 'varchar(11)'
		},
		'downloaddate': {
			'type': 'text'
		}
	},
	'chatid': {
		'name': {
			'type': 'text'
		},
		'id': {
			'type': 'char(25)'
		},
		'priority': {
			'type': 'int(11)'
		}
		'authenticated': {
			'type': 'char(3)'
		},
	},
	'deletedcontent': {
		'id': {
			'type': 'char(12)'
		},
		'deleteddate': {
			'type': 'text'
		},
		'deletedtype': {
			'type': 'int(11)'
		}
	}
}

for key in mariadb:
	for sub_key in mariadb[key]:
		if sub_key == 'password':
			mariadb[key][sub_key] = getpass.getpass(prompt=f"DB {sub_key}: ")
		else:
			mariadb[key][sub_key] = input(f"DB {sub_key}: ")

for key in telegram:
	if key == 'credentials':
		for sub_key in telegram[key]:
			telegram[key][sub_key] = getpass.getpass(prompt=f"Telegram {sub_key}: ")
	else:
		for sub_key in telegram[key]:
			if sub_key == 'hostChatId':
				telegram[key][sub_key] = input(f"Telegram {sub_key}: ")	
			else:
				value = input(f"Telegram (seperate w/ ',') {sub_key}: ")
				if ',' in value:
					telegram[key][sub_key] = value.split(',')
				else:
					telegram[key][sub_key] = value

for key in configuration:
	for sub_key in configuration[key]:
		if sub_key == 'password':
			mariadb[key][sub_key] = getpass.getpass(prompt=f"DB {sub_key}: ")
		else:
			mariadb[key][sub_key] = input(f"DB {sub_key}: ")

# Write the resulting dictionary to a secret.py file
with open('secret.py', 'w') as file:
	file.write("mariadb = " + json.dumps(mariadb, indent=4).replace('"', "'").replace("    ","\t") + "\n")
	file.write("telegram = " + json.dumps(telegram, indent=4).replace('"', "'").replace("    ","\t") + "\n")
	file.write("configuration = " + json.dumps(configuration, indent=4).replace('"', "'").replace("    ","\t"))

import secret

# Defining connection variable
mydb = database.connect(
	host=secret.mariadb['connection']['host'],
	user=secret.mariadb['credentials']['user'],
	password=secret.mariadb['credentials']['password'],
	database=secret.mariadb['connection']['database']
)

myCursor = mydb.cursor()

# Creating list of added tables
myCursor.execute("SHOW TABLES")
existingTables = []
for x in myCursor:
	existingTables.append(x[0])

# Creating (non installed) tables from myTables dictionary
tableAddedCount = 0
for table in myTables:
	if table not in existingTables:
		fieldOutput = ''
		statement = ''

		# Generating arguments for the SQL statement
		for fieldName, fieldInfo in myTables[table].items():
		    fieldOutput += f"{fieldName} {fieldInfo['type']}, "

		# Remove the extra ", " at the end
		fieldOutput = fieldOutput[:-2]

		# Generating SQL statement from variables
		statement = 'CREATE TABLE ' + table + ' (' + fieldOutput + ')'

		# Executing the SQL statement
		myCursor.execute(statement)
		tableAddedCount += 1

print(f"{tableAddedCount} TABLES added.")
myCursor.close()