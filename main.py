import os
import json
from bson import json_util
import click
from pymongo import MongoClient


client = MongoClient('localhost', 27017, username='root', password='root')

@click.group()
def cli():
    pass

@cli.command()
@click.option('--db_name', default='cr-db')
@click.option('--collection_name', default='users')
@click.option('--file_path', default='data/data.txt')
def initdb(db_name, collection_name, file_path):
    click.echo(f'Initialize the database: {db_name}')

    db = client[db_name]
    users_col = db[collection_name]

    docs = []
    with open(file_path) as f:
        for line in f:
            line = line.rstrip('\n')
            fields = [field.replace(' ', '') for field in line.split(",")]
            doc = dict(field.split(':') for field in fields)
            docs.append(doc)

    users_col.insert_many(docs)
    return True


@cli.command()
@click.option('--db_name', default='cr-db')
@click.option('--collection_name', default='users')
@click.option('--json_file_path', default='exports/data.json')
def exportdb(db_name, collection_name, json_file_path):
    click.echo(f'Export the database collection: {str(collection_name)}')

    db = client[db_name]
    users_col = db[collection_name]

    print("Total docs in collection:", users_col.count_documents({}))

    docs = users_col.find()

    if not os.path.exists(json_file_path):
        os.makedirs(os.path.dirname(json_file_path))

    with open(json_file_path, 'w') as outfile:
       dump = json.dumps([doc for doc in docs], sort_keys=False, indent=4, default=json_util.default)
       outfile.write(dump)

    return True


@cli.command()
@click.option('--field_name', default='_id')
@click.option('--json_file_path', default='exports/data.json')
def removefield(field_name, json_file_path):    
    with open(json_file_path, 'r') as data_file:
        data = json.load(data_file)

    for element in data:
        element.pop(field_name, None)

    with open(json_file_path, 'w') as data_file:
        data = json.dump(data, data_file)
    
    return json_file_path


@cli.command()
@click.option('--field_name', default='firstname')
@click.option('--json_file_path', default='exports/data.json')
def upperfield(field_name, json_file_path):
    with open(json_file_path, 'r') as data_file:
        data = json.load(data_file)

    for element in data:
        if not field_name in element:
            continue
        element[field_name] = element[field_name].capitalize() 

    with open(json_file_path, 'w') as data_file:
        data = json.dump(data, data_file)
    
    return json_file_path


@cli.command()
@click.option('--field_name', default='password')
@click.option('--json_file_path', default='exports/data.json')
def clearfield(field_name, json_file_path):
    with open(json_file_path, 'r') as data_file:
        data = json.load(data_file)

    for element in data:
        if not field_name in element:
            continue
        element[field_name] = "" 

    with open(json_file_path, 'w') as data_file:
        data = json.dump(data, data_file)
    
    return json_file_path


@cli.command()
@click.option('--by_field_name', default='firstname')
@click.option('--json_file_path', default='exports/data.json')
def sortjson(by_field_name, json_file_path):
    with open(json_file_path, 'r') as data_file:
        data = json.load(data_file)

    data = sorted(data, key=lambda rec: rec.get(by_field_name, 0))

    with open(json_file_path, 'w') as data_file:
        data = json.dump(data, data_file)
    
    return json_file_path

if __name__ == '__main__':
    cli()
