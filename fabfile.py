from fabric.api import *
import ftputil

def hello():
    print("Hello World!")

def fetch_pubchem_rdf(section="pubchem/RDF/compound/general"):
    local('mkdir -p pubchem_rdf/compound/general')
    #ftp://ftp.ncbi.nlm.nih.gov/pubchem/RDF/
    with ftputil.FTPHost('ftp.ncbi.nlm.nih.gov','anonymous','anonymous') as host:
        names = host.listdir(section)
        for name in names:
            print "Doing name: ", name
            if host.path.isfile(name):
                host.download(name, name, 'b')
            return
