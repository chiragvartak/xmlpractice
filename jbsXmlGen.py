from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom
import math

output_file = 'jbs.xml'

# Set user and bs from file here.
bs= [32, 40, 48, 56, 64]
user= [26, 27, 28, 33, 37, 38, 41, 43, 45, 47, 49, 50, 51, 52, 53]
K = 3 # Number of colors

infinity = float('inf')

# For pretty xml output
def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")

# Simply copy-pasted from sim_jbs.py
def get_relatives(us, bss):
    """Returns a dict to tell all the other users to which a user is related
    to."""
    R = {}
    
    for idn in us:
        # Left Basestation
        left_bs = None
        min_dist = 10000
        for bs in bss:
            if bs < idn and abs(idn - bs) < min_dist:
                left_bs = bs
                min_dist = abs(idn - bs)

        # Right Basestation
        right_bs = None
        min_dist = 10000
        for bs in bss:
            if bs > idn and abs(idn - bs) < min_dist:
                right_bs = bs
                min_dist = abs(idn - bs)

        # Both left and right BS cannot be 'None'.
        assert left_bs != None or right_bs != None

        # Finding the relatives
        span = (None, None)
        if left_bs == None:
            span = (idn, right_bs + abs(right_bs - idn))
        elif right_bs == None:
            span = (left_bs - abs(left_bs - idn), idn)
        else:  # No BS is 'None'
            span = (left_bs - abs(left_bs - idn), right_bs + abs(right_bs - idn))

        for u in us:
            if u >= span[0] and u <= span[1] and u != idn:
                if idn in R:
                    R[idn].append(u)
                else:
                    R[idn] = [u]
                if u in R:
                    R[u].append(idn)
                else:
                    R[u] = [idn]

    for key in R:
        R[key] = sorted(list(set(R[key])))
    return R

def get_constraints(user, bs):
    """Returns a set of all pairs of users which are constrained to each
    other."""
    R = get_relatives(user, bs)
    S = set()
    for u1 in R:
        for u2 in R[u1]:
            pair = (u1, u2)
            S.add(tuple(sorted(pair)))
    return S

instance = Element('instance')

presentation = SubElement(instance, 'presentation')
presentation.set('name', 'JBSProblem')
presentation.set('maxConstraintArity', '2')
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
    variable.set('name', 'agent' + str(u) + '_var')
    variable.set('domain', 'domain_of_agent' + str(u))
    variable.set('agent', 'agent' + str(u))

predicates = SubElement(instance, 'predicates')
predicates.set('nbPredicates', '1')

predicate = SubElement(predicates, 'predicate')
predicate.set('name', 'JBSConstraint')

parameters = SubElement(predicate, 'parameters')
parameters.text = 'int v1 int v2'

expression = SubElement(predicate, 'expression')

functional = SubElement(expression, 'functional')
functional.text = 'if(ne(mod(v1, 1000),mod(v2, 1000)), add(mod(v1, 1000),mod(v2, 1000)), if((and(ge(if(lt(div(v1, 1000000), div(mod(v1, 1000000), 1000)), sub(div(mod(v1, 1000000), 1000), abs(sub(div(v1, 1000000), div(mod(v1, 1000000), 1000)))), add(div(mod(v1, 1000000), 1000), abs(sub(div(v1, 1000000), div(mod(v1, 1000000), 1000))))), sub(div(mod(v2, 1000000), 1000), abs(sub(div(v2, 1000000), div(mod(v2, 1000000), 1000))))), le(if(lt(div(v1, 1000000), div(mod(v1, 1000000), 1000)), sub(div(mod(v1, 1000000), 1000), abs(sub(div(v1, 1000000), div(mod(v1, 1000000), 1000)))), add(div(mod(v1, 1000000), 1000), abs(sub(div(v1, 1000000), div(mod(v1, 1000000), 1000))))), add(div(mod(v2, 1000000), 1000), abs(sub(div(v2, 1000000), div(mod(v2, 1000000), 1000))))))), infinity, if((and(ge(if(lt(div(v2, 1000000), div(mod(v2, 1000000), 1000)), sub(div(mod(v2, 1000000), 1000), abs(sub(div(v2, 1000000), div(mod(v2, 1000000), 1000)))), add(div(mod(v2, 1000000), 1000), abs(sub(div(v2, 1000000), div(mod(v2, 1000000), 1000))))), sub(div(mod(v1, 1000000), 1000), abs(sub(div(v1, 1000000), div(mod(v1, 1000000), 1000))))), le(if(lt(div(v2, 1000000), div(mod(v2, 1000000), 1000)), sub(div(mod(v2, 1000000), 1000), abs(sub(div(v2, 1000000), div(mod(v2, 1000000), 1000)))), add(div(mod(v2, 1000000), 1000), abs(sub(div(v2, 1000000), div(mod(v2, 1000000), 1000))))), add(div(mod(v1, 1000000), 1000), abs(sub(div(v1, 1000000), div(mod(v1, 1000000), 1000))))))), infinity, add(mod(v1, 1000), mod(v2, 1000)))))'
# Yes, the above function is too confuscated; but don't get overwhelmed. It's nothing too complicated.

C = get_constraints(user, bs)

constraints = SubElement(instance, 'constraints')
constraints.set('nbConstraints', str(len(C)))

for cons in C:
    constraint = SubElement(constraints, 'constraint')
    constraint.set('name', 'constraint_agents_' + str(cons[0]) + '_and_' +
        str(cons[1]))
    constraint.set('arity', '2')
    constraint.set('scope', 'agent' + str(cons[0]) + '_var' + ' ' + 
        'agent' + str(cons[1]) + '_var')
    constraint.set('reference', 'JBSConstraint')

    parameters = SubElement(constraint, 'parameters')
    parameters.text = 'agent' + str(cons[0]) + '_var' + ' ' + 'agent' + \
        str(cons[1]) + '_var'


# Writing to the output_file
opfile = open(output_file, 'w')
print(prettify(instance), file=opfile)
opfile.close()
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom
import math

output_file = 'jbs.xml'

# Set user and bs from file here.
user = [3, 6, 7, 9, 12]
bs = [2, 5, 8, 11, 14]
K = 3 # Number of colors

infinity = float('inf')

# For pretty xml output
def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")

# Simply copy-pasted from sim_jbs.py
def get_relatives(us, bss):
    """Returns a dict to tell all the other users to which a user is related
    to."""
    R = {}
    
    for idn in us:
        # Left Basestation
        left_bs = None
        min_dist = 10000
        for bs in bss:
            if bs < idn and abs(idn - bs) < min_dist:
                left_bs = bs
                min_dist = abs(idn - bs)

        # Right Basestation
        right_bs = None
        min_dist = 10000
        for bs in bss:
            if bs > idn and abs(idn - bs) < min_dist:
                right_bs = bs
                min_dist = abs(idn - bs)

        # Both left and right BS cannot be 'None'.
        assert left_bs != None or right_bs != None

        # Finding the relatives
        span = (None, None)
        if left_bs == None:
            span = (idn, right_bs + abs(right_bs - idn))
        elif right_bs == None:
            span = (left_bs - abs(left_bs - idn), idn)
        else:  # No BS is 'None'
            span = (left_bs - abs(left_bs - idn), right_bs + abs(right_bs - idn))

        for u in us:
            if u >= span[0] and u <= span[1] and u != idn:
                if idn in R:
                    R[idn].append(u)
                else:
                    R[idn] = [u]
                if u in R:
                    R[u].append(idn)
                else:
                    R[u] = [idn]

    for key in R:
        R[key] = sorted(list(set(R[key])))
    return R

def get_constraints(user, bs):
    """Returns a set of all pairs of users which are constrained to each
    other."""
    R = get_relatives(user, bs)
    S = set()
    for u1 in R:
        for u2 in R[u1]:
            pair = (u1, u2)
            S.add(tuple(sorted(pair)))
    return S

instance = Element('instance')

presentation = SubElement(instance, 'presentation')
presentation.set('name', 'JBSProblem')
presentation.set('maxConstraintArity', '2')
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
    variable.set('name', 'agent' + str(u) + '_var')
    variable.set('domain', 'domain_of_agent' + str(u))
    variable.set('agent', 'agent' + str(u))

predicates = SubElement(instance, 'predicates')
predicates.set('nbPredicates', '1')

predicate = SubElement(predicates, 'predicate')
predicate.set('name', 'JBSConstraint')

parameters = SubElement(predicate, 'parameters')
parameters.text = 'int v1 int v2'

expression = SubElement(predicate, 'expression')

functional = SubElement(expression, 'functional')
functional.text = 'if(ne(mod(v1, 1000),mod(v2, 1000)), add(mod(v1, 1000),mod(v2, 1000)), if((ge(if(lt(div(v1, 1000000), div(mod(v1, 1000000), 1000)), sub(div(mod(v1, 1000000), 1000), abs(sub(div(v1, 1000000), div(mod(v1, 1000000), 1000)))), add(div(mod(v1, 1000000), 1000), abs(sub(div(v1, 1000000), div(mod(v1, 1000000), 1000))))), sub(div(mod(v2, 1000000), 1000), abs(sub(div(v2, 1000000), div(mod(v2, 1000000), 1000))))) and le(if(lt(div(v1, 1000000), div(mod(v1, 1000000), 1000)), sub(div(mod(v1, 1000000), 1000), abs(sub(div(v1, 1000000), div(mod(v1, 1000000), 1000)))), add(div(mod(v1, 1000000), 1000), abs(sub(div(v1, 1000000), div(mod(v1, 1000000), 1000))))), add(div(mod(v2, 1000000), 1000), abs(sub(div(v2, 1000000), div(mod(v2, 1000000), 1000)))))), infinity, if((ge(if(lt(div(v2, 1000000), div(mod(v2, 1000000), 1000)), sub(div(mod(v2, 1000000), 1000), abs(sub(div(v2, 1000000), div(mod(v2, 1000000), 1000)))), add(div(mod(v2, 1000000), 1000), abs(sub(div(v2, 1000000), div(mod(v2, 1000000), 1000))))), sub(div(mod(v1, 1000000), 1000), abs(sub(div(v1, 1000000), div(mod(v1, 1000000), 1000))))) and le(if(lt(div(v2, 1000000), div(mod(v2, 1000000), 1000)), sub(div(mod(v2, 1000000), 1000), abs(sub(div(v2, 1000000), div(mod(v2, 1000000), 1000)))), add(div(mod(v2, 1000000), 1000), abs(sub(div(v2, 1000000), div(mod(v2, 1000000), 1000))))), add(div(mod(v1, 1000000), 1000), abs(sub(div(v1, 1000000), div(mod(v1, 1000000), 1000)))))), infinity, add(mod(v1, 1000), mod(v2, 1000)))))'
# Yes, the above function is too confuscated; but don't get overwhelmed. It's nothing too complicated.

C = get_constraints(user, bs)

constraints = SubElement(instance, 'constraints')
constraints.set('nbConstraints', str(len(C)))

for cons in C:
    constraint = SubElement(constraints, 'constraint')
    constraint.set('name', 'constraint_agents_' + str(cons[0]) + '_and_' +
        str(cons[1]))
    constraint.set('arity', '2')
    constraint.set('scope', 'agent' + str(cons[0]) + '_var' + ' ' + 
        'agent' + str(cons[1]) + '_var')
    constraint.set('reference', 'JBSConstraint')

    parameters = SubElement(constraint, 'parameters')
    parameters.text = 'agent' + str(cons[0]) + '_var' + ' ' + 'agent' + \
        str(cons[1]) + '_var'


# Writing to the output_file
opfile = open(output_file, 'w')
print(prettify(instance), file=opfile)
opfile.close()
