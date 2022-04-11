"""Check Object Database Schema

Validate the schema used in the object database against the JSON version of the schema in git.
Raises an AssertionError and returns with non-zero if the number of fields or names of fields
differ (types are not checked).
"""

import sys
import json
import mysql.connector
import requests
import argparse

def get_mysql_names(conf):
    config = {
      'user': conf['user'], 
      'password': conf['password'], 
      'host': conf['host'], 
      'database': conf['database'], 
      }
    msl = mysql.connector.connect(**config)

    cursor = msl.cursor(buffered=True, dictionary=True)
    query = 'describe objects'
    cursor.execute(query)
    mysql_names = []
    for row in cursor:
        mysql_names.append(row['Field'])
    return mysql_names

def get_schema_names(conf):
    schema_names = []
    my_objects = json.loads(requests.get(conf['url']).text)
    for field in my_objects['fields']:
        schema_names.append(field['name'])
    return schema_names

if __name__ == "__main__":
    # parse cmd line arguments
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--user', default='ztf', type=str, help='MySQL username')
    parser.add_argument('--password', type=str, help='MySQL password')
    parser.add_argument('--host', type=str, help='MySQL hostname')
    parser.add_argument('--port', type=int, default=3306, help='MySQL port number')
    parser.add_argument('--database', type=str, default='ztf', help='Name of database')
    parser.add_argument('--url', type=str, default="https://raw.githubusercontent.com/lsst-uk/lasair-lsst/main/utility/schema/objects.json", help='URL to get the schema from')
    conf = vars(parser.parse_args())

    mysql_names = get_mysql_names(conf)
    schema_names = get_schema_names(conf)

    assert len(mysql_names) == len(schema_names), "Schema validation failed: different length"

    for i in range(len(mysql_names)):
        assert mysql_names[i] == schema_names[i], "Schema validation failed: {} != {}".format(mysql_names[i], schema_names[i])

    print('mysql and object schema identical')

