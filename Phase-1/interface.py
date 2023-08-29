from neo4j import GraphDatabase

class Interface:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)
        self._driver.verify_connectivity()

    def close(self):
        self._driver.close()

    def bfs(self, start_node, last_node):
        # TODO: Implement this method
        with self._driver.session() as session:
            bfs_query = f"""
            MATCH (a:Location{{name:{start_node}}}), (d:Location{{name:{last_node}}})
            WITH id(a) AS source, id(d) AS targetNodes
            CALL gds.bfs.stream('myGraph', {{
                sourceNode: source,
                targetNodes: targetNodes
            }})
            YIELD 
            path
            RETURN path
            """
            result  = session.run(bfs_query)
            
            return result.data()

        # raise NotImplementedError

    def pagerank(self, max_iterations, weight_property):
        # TODO: Implement this method
        with self._driver.session() as session:
            # Load the graph in-memory
            load_graph_query = f"""
            CALL gds.graph.project(
                'myGraph',
                'Location',
                {{  
                    TRIP: {{
                        type: 'TRIP',
                        properties: '{weight_property}'
                    }}
                }}
            )
            """
            session.run(load_graph_query)

            # Run the PageRank algorithm
            pagerank_query = f"""
            CALL gds.pageRank.stream('myGraph', {{
                maxIterations: {max_iterations},
                dampingFactor: 0.85,
                relationshipWeightProperty: '{weight_property}'
            }})
            YIELD nodeId, score
            RETURN gds.util.asNode(nodeId).name AS name, score
            ORDER BY score DESC
            """
            result = session.run(pagerank_query)

            # Get the highest and lowest PageRank nodes
            # max_node = None
            # min_node = None
            # for record in result:
            #     location = record["location"]
            #     score = record["score"]
            #     if max_node is None or score > max_node[1]:
            #         max_node = (location, score)
            #     if min_node is None or score < min_node[1]:
            #         min_node = (location, score)
            # print(max_node,"maxnode")
            # print(min_node,"minnode")

            # # Unload the in-memory graph
            # unload_graph_query = "CALL gds.graph.drop('myGraph')"
            # session.run(unload_graph_query)

            # return [max_node,min_node]

            var=result.data()
            return [var[0],var[-1]]
        # raise NotImplementedError

