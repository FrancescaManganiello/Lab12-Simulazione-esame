from model.model import Model

mymodel = Model()

mymodel.buildGraph(1.2, 2.7)

print(f"Nodi: {mymodel.getNumNodes()}")
print(f"Archi: {mymodel.getNumEdges()}")