import lxml
from lxml import etree as etree


tree = etree.parse('curriculo.xml')
myroot = tree.getroot()	


pretty = lxml.etree.tostring(tree, encoding="unicode", pretty_print=True)

with open('output-marcioaparecido.xml', 'w') as f:
	f.write(pretty)