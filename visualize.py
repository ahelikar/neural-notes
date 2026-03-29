import json
from pyvis.network import Network

def build_ann_graph(triples, node_size, layer_gap):
    # Use cdn_resources='remote' to ensure scripts load on the webpage
    net = Network(height="700px", width="100%", directed=True, bgcolor="#ffffff")
    
    levels = {}
    for s, r, o in triples:
        if s not in levels: levels[s] = 0
        levels[o] = max(levels.get(o, 0), levels[s] + 1)
    
    max_lvl = max(levels.values()) if levels else 1

    for s, r, o in triples:
        # Determine colors for Input, Hidden, and Output layers
        s_col = "#97C2FC" if levels[s] == 0 else ("#FB7E81" if levels[s] == max_lvl else "#C297FC")
        o_col = "#D797FC" if levels[o] == 0 else ("#FB7E81" if levels[o] == max_lvl else "#C297FC")
        
        net.add_node(s, label=s, level=levels[s], color=s_col, shape="circle", size=node_size)
        net.add_node(o, label=o, level=levels[o], color=o_col, shape="circle", size=node_size)
        net.add_edge(s, o, label=r, width=1, color="#848484")

    # The json.dumps fix for your previous syntax error
    options = {
        "layout": {
            "hierarchical": {
                "enabled": True,
                "direction": "LR",
                "sortMethod": "directed",
                "levelSeparation": layer_gap,
                "nodeSpacing": 300 # Increased to prevent squashing
            }
        },
        "physics": {"enabled": False},
        "edges": {"smooth": {"enabled": False}} # False improves loading speed for 100+ nodes
    }
    net.set_options(json.dumps(options))
    return net.generate_html()