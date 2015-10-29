#!/usr/bin/python
from collections import defaultdict
import json
from py2neo import Graph

def get_graph_json():
    #graph = Graph("http://neo4j:shelter@localhost:7474/db/data/")
    graph = Graph("http://neo4j:shelter@10.8.30.170:7474/db/data/")

    #system_name = 'USERMGMNT'
    #nodes_query = "match (n)-[:IS_IN]-(e:Environment), (n)-[:CONNECTS_TO]-() where  e.name = 'TEST' and n.system = 'PAS' return n.name, n.system"
    nodes_query = "MATCH (n:VM), (n)-[:IS_PART_OF]->(e) RETURN DISTINCT ID(n) AS id, n.name AS name, n.system AS cluster, e.name AS environment"
    #nodes_query = "MATCH (n)-[:CONNECTS_TO]-(y), (n)-[:IS_IN]->(e)  RETURN DISTINCT ID(n) AS id, n.name AS name, n.system AS cluster, e.name AS environment"
    edges_query = "MATCH (n:VM)-[r:CONNECTS_TO]-(y:VM), (n)-[:IS_PART_OF]->(e), (y)-[:IS_PART_OF]->(e) RETURN DISTINCT ID(n) AS source, ID(y) AS target, type(r) AS caption"

    graph_data = defaultdict(list)

    for record in graph.cypher.stream(nodes_query):
        # id, name, type
        #print(record)
        node={}
        node['id'] = str(record[0])
        node['caption'] = record[1]
        node['system'] = record[2]
        node['environment'] = record[3]
        graph_data['nodes'].append(node)

    for record in graph.cypher.stream(edges_query):
        # source, target, comment
        #print str(record[0]) + " " + str(record[1]) + " " + record[2]
        edge={}
        edge['source'] = str(record[0])
        edge['target'] = str(record[1])
        edge['comment']= record[2]
        graph_data['edges'].append(edge)

    graph_json = json.dumps(graph_data)

    outputfile = 'static/data/integration.json'
    outfile = open(outputfile, 'w')
    outfile.write(graph_json)
    outfile.close()

    return graph_json

def get_domain_json():
    #graph = Graph("http://neo4j:shelter@localhost:7474/db/data/")
    graph = Graph("http://neo4j:shelter@10.8.30.170:7474/db/data/")

    nodes_query = "MATCH (n:Domain) RETURN  ID(n) AS id, n.name AS name"

    edges_query = "MATCH (n:Domain)-[r]-(y) RETURN DISTINCT ID(n) AS source, ID(y) AS target, type(r) AS caption"

    graph_data = defaultdict(list)

    for record in graph.cypher.stream(nodes_query):
        # id, name, type
        #print(record)
        node={}
        node['id'] = str(record[0])
        node['caption'] = record[1]

        graph_data['nodes'].append(node)

    for record in graph.cypher.stream(edges_query):
        # source, target, comment
        #print str(record[0]) + " " + str(record[1]) + " " + record[2]
        edge={}
        edge['source'] = str(record[0])
        edge['target'] = str(record[1])
        edge['comment']= record[2]
        graph_data['edges'].append(edge)

    graph_json = json.dumps(graph_data)

    outputfile = 'static/data/domains.json'
    outfile = open(outputfile, 'w')
    outfile.write(graph_json)
    outfile.close()

    return graph_json

def main():
    test = get_graph_json()
    print(test)
    outputfile = 'static/data/graph_json.json'
    outfile = open(outputfile, 'w')
    outfile.write(test)
    outfile.close()
# Start program
if __name__ == "__main__":
   main()
