import datetime
import sys
from pymongo import MongoClient

from pprint import pprint

try:
    import shapefile
except ModuleNotFoundError:
    print("Module Not Found Error!, please install pyshp first")
    sys.exit(1)

def main():
    """
    this function is used for converting shapefile to geoJSON
    so you can use it in Leaflet.js or other leaflet API
    requirement : pyshp, https://pypi.org/project/pyshp/
    use : python3 shp2geojson.py "input_file.shp" "output_file.json"
    """

# argument[1]: input, argumen[2]: output
    if len(sys.argv) != 7:
        print('\nuse >>> python3 import2mongodb.py "input_file.shp" "database_uri" "db_name" "user" "password" "database_collection"\n')
        sys.exit(1)

    fin = sys.argv[1]
    host = sys.argv[2]
    db_name = sys.argv[3]
    user = sys.argv[4]
    password= sys.argv[5]
    db_collection = sys.argv[6]

    print(f"{type(fin)} and {type(user)}")
    if not type(fin) == str:
        print('\nuse >>> python3 shp2geojson.py "input_file.shp" "output_file.json"\n')
        sys.exit(1)
        
    # read the shapefile
    try:
        shpfile = shapefile.Reader(fin)
    except shapefile.ShapefileException:
        print("your input file is invalid")
        sys.exit(1)
    fields = shpfile.fields[1:]
    field_names = [field[0] for field in fields]
    buffer = []
    for sr in shpfile.shapeRecords():
        atr = dict(zip(field_names, sr.record))
        # handle datatime
        for k, v in atr.items():
            if isinstance(v, datetime.date):
                atr[k] = datetime.datetime(v.year, v.month, v.day)

        geom = sr.shape.__geo_interface__
        buffer.append(dict(type="Feature", geometry=geom, properties=atr)) 
    
    if len(buffer) == 0:
        print("nothing to be import to database")
        sys.exit(1)
    
    # masukan data ke mongodb
    try:
        # Python 3.x
        from urllib.parse import quote_plus
    except ImportError:
        # Python 2.x
        from urllib import quote_plus

    uri = "mongodb://%s:%s@%s" % (
        quote_plus(user), quote_plus(password), host)
    client = MongoClient(uri)
    db = client[db_name]
    coll = db[db_collection]
    results = coll.insert_many(buffer)
    pprint(f"imported {len(results.inserted_ids)} records")

if __name__ == "__main__":
    main()