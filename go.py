"""
Import script for B556
"""

import sys
from rdflib import Graph, ConjunctiveGraph, URIRef, Namespace
import rdflib
from py2neo import node, rel, neo4j

caffeine = rdflib.term.URIRef("http://rdf.ncbi.nlm.nih.gov/pubchem/compound/CID2519")
has_attr = rdflib.term.URIRef("http://semanticscience.org/resource/has-attribute")
isotope = rdflib.term.URIRef("http://semanticscience.org/resource/CHEMINF_000455")
has_value = rdflib.term.URIRef("http://semanticscience.org/resource/has-value")

def parse_drugbank():
    g = ConjunctiveGraph()
    data = open("./drugbank_drugs.nq", "rb")
    g.parse(data, format="nquads")
    print("graph has %s statements." % len(g))
    return g


def parse_pubchem():
    """
    Currently parsing in the first 100000 items of the compound, descriptor, and
    inchikey files.

    Get them from pubchem_rdf ftp.
    """
    g = Graph()
    print "Starting to parse..."
    g.parse("./pubchem_rdf/compound/general/pc_comp_00000001_00100000.ttl", format="turtle")
    print "next doing comp..."
    g.parse("./pubchem_rdf/descriptor/compound/pc_comp_descr_00000001_00100000.ttl", format="turtle")
    print "next doing inchikey..."
    g.parse("./pubchem_rdf/inchikey/compound/pc_inchikey_comp_00000001_00100000.ttl", format="turtle")
    return g


def add_compound(neograph, uid, props):
    """
    Add a single compound to the graph using the pubchem uri as the uid.
    """
    compounds = neograph.get_or_create_index(neo4j.Node, "uid")    
    # TODO add try
    # http://blog.safaribooksonline.com/2013/08/07/managing-uniqueness-with-py2neo/
    comp = compounds.get_or_create("uid", uid, props)
    comp.add_labels("compound")
    comp.set_properties(props)
    return comp


def add_caffiene(g):
    "This is a demo method that will eventually be removed"
    neo = get_neo4j_instance()
    props = {}
    for s,p,o in g.triples((caffeine,has_attr,None)):
        for descriptor in g.triples((o, has_value, None)):
            print o, descriptor[2]
            props[o[55:]] = descriptor[2]
    comp = add_compound(neo,"http://rdf.ncbi.nlm.nih.gov/pubchem/compound/CID2519", props)
    return comp


def add_lots(g):
    """
    This is a test to load a subset of the compounds for development (currently
    just a few thousand. We will eventually load all the files.
    """
    neo = get_neo4j_instance()
    for i in range(1,1000):
        cid = "http://rdf.ncbi.nlm.nih.gov/pubchem/compound/CID%s" % (i,)
        cidref = rdflib.term.URIRef(cid)
        props = {}
        for s,p,o in g.triples((cidref,has_attr,None)):
            for descriptor in g.triples((o, has_value, None)):
                print o, descriptor[2]
                propname = o.split(str(i)+"_")[1]
                print propname
                props[propname] = descriptor[2]
        add_compound(neo,cid, props)
    

def explore_caffiene(g):
    "This is a demo method that will eventually be removed"
    preds = set()
    for s,p,o in g.triples((caffeine,None,None)):
        preds.add(p)
    print "We have the following preds: ", preds, "\n"

    print "Attributes:"
    for s,p,o in g.triples((caffeine,has_attr,None)):
        for descriptor in g.triples((o, has_value, None)):
            print o, descriptor[2]

    #print "Objectified:"
    #for s,p,o in g.triples((None,None,caffeine)):
    #    print s, " ", p 

    #print "\nIsotopes:"
    #for s,p,o in g.triples((caffeine,isotope,None)):
    #    print o


def get_neo4j_instance():
    "TODO Our production port for Neo4j is 7888"
    return neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
    

def main(args):
    """
    Be sure you have the pubchem rdf in the directory structure loaded inside
    this method
    """
    g = parse_pubchem()
    add_lots(g)

if __name__ == "__main__":
    main(sys.argv[1:])
