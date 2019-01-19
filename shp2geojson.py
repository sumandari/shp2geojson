import datetime
import sys
from json import dumps

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
    if len(sys.argv) != 3:
        print('\nuse >>> python3 shp2geojson.py "input_file.shp" "output_file.json"\n')
        sys.exit(1)

    fin = sys.argv[1]
    fout = sys.argv[2]
    print(f"{type(fin)} and {type(fout)}")
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
        geom = sr.shape.__geo_interface__
        buffer.append(dict(type="Feature", \
         geometry=geom, properties=atr)) 

    # write the GeoJSON file
    geojson = open(fout, "w")
    geojson.write(dumps({"type": "FeatureCollection",\
     "features": buffer}, indent=2, default=konversi) + "\n")
    geojson.close()

# handle date type
def konversi(o):
    if isinstance(o, datetime.date):
        return o.__str__()


if __name__ == "__main__":
    main()