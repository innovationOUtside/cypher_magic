import os
import json
import uuid
from IPython.display import HTML, Javascript, display

DEFAULT_PHYSICS = {
    "physics": {
        "barnesHut": {
            "gravitationalConstant": -15150,
            "centralGravity": 3.45,
            "springLength": 261,
            "damping": 0.3
        }
    }
}


def get_visjs():
    return


def init_notebook_mode():
    """
    Creates a script tag and prints the JS read from the file in the tag.
    """

    display(
        Javascript(data="require.config({ " +
                        "    paths: { " +
                        "        vis: '//cdnjs.cloudflare.com/ajax/libs/vis/4.8.2/vis.min' " +
                        "    } " +
                        "}); " +
                        "require(['vis'], function(vis) { " +
                        " window.vis = vis; " +
                        "}); ",
                   css='https://cdnjs.cloudflare.com/ajax/libs/vis/4.8.2/vis.css')
        )

def vis_network(nodes, edges, physics=True):
    """
    Creates the HTML page with all the parameters
    :param nodes: The nodes to be represented an their information.
    :param edges: The edges represented an their information.
    :param physics: The options for the physics of vis.js.
    :return: IPython.display.HTML
    """
    dir = os.path.dirname(__file__)
    path = os.path.join(dir, 'assets\index.html')
    base = open(path).read()

    # print({nodes:json.dumps(nodes), edges:json.dumps(edges), physics:json.dumps(physics)})

    unique_id = str(uuid.uuid4())
    nd = json.dumps(nodes)
    ed = json.dumps(edges)
    pd = json.dumps(physics)
    html = base.format(id=unique_id, nodes=nd, edges=ed, physics=pd)
    #rint(html)
    return HTML(html)
 
def defineNode(n, options):
    nn = {"id": n.identity, "label": ":".join(n._labels) }
    if (options is not None):
        for l in n._labels:
            if(l in options):
                thisOptions= options[l]
                if(isinstance(thisOptions, dict)):
                    if(thisOptions.get("label") is not None):
                        nn["label"]=n[thisOptions["label"]]
                    if(thisOptions.get("image") is not None):
                        nn["image"]=thisOptions["image"]
                        nn["shape"]="image"
                    if(thisOptions.get("opacity") is not None):
                        nn["opacity"]=thisOptions["opacity"]
                    if(thisOptions.get("shape") is not None):
                        nn["shape"]=thisOptions["shape"]
                elif(isinstance(thisOptions, str)):
                    nn["label"] = n[thisOptions]
    return nn

def defineEdge(rel, options):
    nn = {"from": rel.nodes[0].identity, "to": rel.nodes[1].identity, "label": ":".join(rel.types()), "arrowhead": "box"}
    if (options is not None):
        for l in rel.types():
            if(l in options):
                thisOptions= options[l]
                if(isinstance(thisOptions, dict)):
                    if(thisOptions.get("label") is not None):
                        nn["label"]=rel[thisOptions["label"]]
                    if(thisOptions.get("opacity") is not None):
                        nn["opacity"]=thisOptions["opacity"]
                    if(thisOptions.get("width") is not None):
                        nn["width"]=thisOptions["width"]
                    if(thisOptions.get("color") is not None):
                        c = rel[thisOptions["color"]]
                        if(not c.startswith('#')):
                            c='#'+c
                        nn["color"]=c
                    if(thisOptions.get("colorValue") is not None):
                        c = rel[thisOptions["colorValue"]]
                        if(c is not None):
                            if(not c.startswith('#')):
                                c='#'+c
                            nn["color"]=c
                    if(thisOptions.get("noArrows") is not None):
                        nn["arrows"]={ "to":{"enabled":False} }
                            
                elif(isinstance(thisOptions, str)):
                    nn["label"] = rel[thisOptions]
    return nn


def draw(p, options, physics=True, limit=100):
    nodes = []
    edges = []
    fields = p._fields
    d=p.data()
    for row in d:
        for f in fields:
            o = row[f];
            for n in o.nodes:
                nn = defineNode(n, options)
                # for k in n:
                #     nn[k]= n[k]
                if nn not in nodes:

                    nodes.append(nn)
            for rel in o.relationships:
                if rel is not None:
                    edges.append(defineEdge(rel, options))
    #return 
    return vis_network(nodes, edges, physics=physics)