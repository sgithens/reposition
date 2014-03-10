import sys
from rdflib import Graph, ConjunctiveGraph, URIRef, Namespace
import rdflib

caffeine = rdflib.term.URIRef("http://rdf.ncbi.nlm.nih.gov/pubchem/compound/CID2519")
has_attr = rdflib.term.URIRef("http://semanticscience.org/resource/has-attribute")
isotope = rdflib.term.URIRef("http://semanticscience.org/resource/CHEMINF_000455")

def parse_drugbank():
    g = ConjunctiveGraph()
    data = open("./drugbank_drugs.nq", "rb")
    result = g.parse(data, format="nquads")
    print("graph has %s statements." % len(g))

def parse_pubchem():
    g = Graph()
    print "Starting to parse..."
    g.parse("./pubchem_rdf/compound/general/pc_comp_00000001_00100000.ttl", format="turtle")
    return g

def explore_caffiene(g):
    preds = set()
    for s,p,o in g.triples((caffeine,None,None)):
        preds.add(p)
    print "We have the following preds: ", preds, "\n"

    print "Attributes:"
    for s,p,o in g.triples((caffeine,has_attr,None)):
        print o

    print "Isotopes:"
    for s,p,o in g.triples((caffeine,isotope,None)):
        print o

    

def main(args):
    #parse_pubchem()
    pass

if __name__ == "__main__":
    main(sys.argv[1:])
