#!/usr/bin/python
#
# ---- Searching words under Snowflake DDL Views ----
# 
# Search for word / table name or any text under Snowflake schema names
#
# Version : 1.0v
# 
#

import snowflake.connector
import sys
 
# Gets the version
sqlSnowflake = snowflake.connector.connect(
user='XXXXXXX',
password='XXXXXX',
account='XXXXXX',
region='us-east-1',
database='XXXXX',
warehouse='XXXXXX',
schema='XXXXXX'
)

print('\033c')
print('\n        ***** Searching words under Snowflake DDL Views ***** \n')

table_schema = input('Enter schema name: ')
searchWord = input('Search for: ')

SQLselect = "SELECT table_name FROM INFORMATION_SCHEMA.VIEWS WHERE table_schema = '" + table_schema + "'"

try:
	sqlSnowflake = sqlSnowflake.cursor()
except:
	print('Unable to connect into Snowflake account')
	sqlSnowflake.close()
	exit()

#### - Option 1: -------- If you want to use different WareHouse for example SNOWFLAKE_XS_BI 
#sqlSnowflake.cursor().execute("USE warehouse SNOWFLAKE_XS_BI") 

#### - Option 2: -------- If you want to use different DataBase for example DWH_DEV
#sqlSnowflake.cursor().execute("USE database DWH_DEV") 

print('\n- Searching all views under schema name: %s \n' % (table_schema))
sqlSnowflake.execute(SQLselect)
data = sqlSnowflake.fetchall()

if len(data) == 0:
	print(str(len(data)) + ' views found under scehma name: ' + table_schema + '\n')
	sqlSnowflake.close()
	exit()
 


SQLstmt = []
for row in data:
	SQLstmt.append("Select get_ddl('VIEW', '" + table_schema + '.' + str(row[0]) + "');")

fetchViews = []
for command in SQLstmt:
	exe = sqlSnowflake.execute(command).fetchall()
	fetchViews.append(exe[0][0])

num = 1
for i,l in enumerate(fetchViews):
	if l.lower().count(searchWord) > 0:
		if num == 1:
			print('View names result: \n')
			print(str(num) + '> ' + data[i][0] + '\n')
			num+=1
		else:
			print(str(num) + '> ' + data[i][0] + '\n')
			num+=1
		
if num == 1:
		print('0 results when searching: "' + searchWord + '" under schema name: ' + table_schema + '\n')
		
sqlSnowflake.close()
