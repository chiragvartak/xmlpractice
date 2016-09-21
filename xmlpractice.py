"""This module gives a demo of how to generate an XML file using Python."""

from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom

output_file = 'example.xml'

# For pretty xml output
def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")

data = Element('data')

country = SubElement(data, 'country')
country.set('name', 'Liechtenstein')

rank = SubElement(country, 'rank')
rank.text = "1"
year = SubElement(country, 'year')
year.text = "2008"
gdppc = SubElement(country, 'gdppc')
gdppc.text = "141100"
neighbor = SubElement(country, 'neighbor')
neighbor.set('name', 'Austria')
neighbor.set('direction', 'E')
neighbor = SubElement(country, 'neighbor')
neighbor.set('name', 'Switzerland')
neighbor.set('direction', 'W')

country = SubElement(data, 'country')
country.set('name', 'Singapore')

rank = SubElement(country, 'rank')
rank.text = '4'
year = SubElement(country, 'year')
year.text = "2011"
gdppc = SubElement(country, 'gdppc')
gdppc.text = "59900"
neighbor = SubElement(country, 'neighbor')
neighbor.set('name', 'Malaysia')
neighbor.set('direction', 'N')

country = SubElement(data, 'country')
country.set('name', 'Panama')

rank = SubElement(country, 'rank')
rank.text = "68"
year = SubElement(country, 'year')
year.text = "2011"
gdppc = SubElement(country, 'gdppc')
gdppc.text = "13600"
neighbor = SubElement(country, 'neighbor')
neighbor.set('name', 'Costa Rica')
neighbor.set('direction', 'W')
neighbor = SubElement(country, 'neighbor')
neighbor.set('name', 'Colombia')
neighbor.set('direction', 'E')

# Writing to the output_file
opfile = open(output_file, 'w')
print(prettify(data), file=opfile)
opfile.close()
