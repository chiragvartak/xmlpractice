from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom
import math

output_file = 'jbs.xml'

# Set user and bs from file here.
user = [1, 3, 6, 7, 9, 12, 15]
bs = [2, 5, 8, 11, 14]
K = 3 # Number of colors

infinity = math.inf

# For pretty xml output
def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")


instance = Element('instance')

presentation = SubElement(instance, 'presentation')
presentation.set('name', 'JBSProblem')
presentation.set('maxConstraintArity', 'dunno')
presentation.set('maximize', 'false')
presentation.set('format', 'XCSP 2.1_FRODO')

agents = SubElement(instance, 'agents')
agents.set('nbAgents', str(len(user)))

for x in user:
    agent = SubElement(agents, 'agent')
    agent.set('name', 'agent'+str(x))


# Create all the domains here

domains = SubElement(instance, 'domains')
domains.set('nbDomains', str(len(user)))

for u in user:
    # Left basestation
    left_bs = None
    min_dist = infinity
    for b in bs:
        if b < u and abs(u - b) < min_dist:
            left_bs = b
            min_dist = abs(u - b)

    # Right Basestation
    right_bs = None
    min_dist = infinity
    for b in bs:
        if b > u and abs(u - b) < min_dist:
            right_bs = b
            min_dist = abs(u - b)

    # Both left and right BS cannot be 'None'.
    assert left_bs != None or right_bs != None

    domain = SubElement(domains, 'domain')
    domain.set('name', 'domain_of_agent' + str(u))

    B = []
    if left_bs != None:
        B.append(left_bs)
    if right_bs != None:
        B.append(right_bs)
    D = [(u*1000000 + b*1000 + k) for b in B for k in range(1, K+1)]

    domain.set('nbValues', str(len(D)))
    domain.text = ' '.join(str(x) for x in D)

variables = SubElement(instance, 'variables')
variables.set('nbVariables', str(len(user)))

for u in user:
    variable = SubElement(variables, 'variable')
    variable.set('name', 'agent' + str(u) + '_variable')
    variable.set('domain', 'domain_of_agent' + str(u))
    variable.set('agent', 'agent' + str(u))

predicates = SubElement(instance, 'nbPredicates')
predicates.set('nbPredicates', '1')

predicate = SubElement(predicates, 'predicate')
predicate.set('name', 'JbsConstraint')

parameters = SubElement(predicate, 'parameters')



# Writing to the output_file
opfile = open(output_file, 'w')
print(prettify(instance), file=opfile)
opfile.close()
