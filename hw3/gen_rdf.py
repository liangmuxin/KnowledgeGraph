import json
import os

from rdflib import URIRef, BNode, Literal, Namespace, Graph

from rdflib.namespace import RDF, RDFS, XSD, NamespaceManager


SCHEMA = Namespace("http://schema.org/")
ARTWORK = "artwork_info.json"
ARTIST = "artist_info.json"
O_ARTWORK = "artwork.ttl"
O_ARTIST = "artist.ttl"
namespace_manager = NamespaceManager(Graph())
namespace_manager.bind("schema", SCHEMA, override=False)
class GenRDF(object):
    def __init__(self, name):
        self.name = name
        self.data = None
        self.g = Graph()

    def read_json(self):

        if self.name == "ARTIST":
            path = os.path.join(os.getcwd(), ARTIST)
            with open(path, "r") as p:
                self.data = json.load(p)
        else:
            path = os.path.join(os.getcwd(), ARTWORK)
            with open(path, "r") as p:
                self.data = json.load(p)

    def gen_rdf(self):
        if self.name == "ARTIST":
            self.rdf_artist()
        else:
            self.rdf_artwork()

    def rdf_artist(self):
        # self.g  = Graph()

        for js in self.data:
            tmp = URIRef(js["artist_url"])
            name = Literal(js["artist_name"])
            birthDate = Literal(js["birth_date"], datatype=XSD.integer)
            nationality = Literal(js["nationalities"], datatype=XSD.nationality)
            self.g.add((tmp, RDF.type, SCHEMA.Artist))
            self.g.set((tmp, SCHEMA.name, name))
            self.g.set((tmp, SCHEMA.birthDate, birthDate))
            self.g.set((tmp, SCHEMA.nationality, nationality))
            try: 
                year = int(js["death_date"])
                self.g.set((tmp, SCHEMA.deathDate, Literal(js["death_date"], datatype=XSD.integer)))
            except:
                pass

        self.g.namespace_manager = namespace_manager
        self.g.serialize(destination=O_ARTIST, format='turtle')
            
    def rdf_artwork(self):
        for js in self.data:
            tmp = URIRef(js["artwork_url"])
            name = Literal(js["title"])
            artist_url = Literal(js["artist_url"])
            object_number = Literal(js["object_number"])
            produce = Literal(js["date"])
            self.g.add((tmp, RDF.type, SCHEMA.Artwork))
            self.g.set((tmp, SCHEMA.name, name))
            self.g.set((tmp, SCHEMA.artistUrl, artist_url))
            self.g.set((tmp, SCHEMA.objectNumber, object_number))
            self.g.set((tmp, SCHEMA.produceTime, produce))
        self.g.namespace_manager = namespace_manager
        self.g.serialize(destination=O_ARTWORK, format='turtle')


def main():
    p = GenRDF("ARTIST")
    p.read_json()
    p.gen_rdf()
    q = GenRDF("ARTWORK")
    q.read_json()
    q.gen_rdf()

if __name__ == "__main__":
    main()
# t.gen_results()
