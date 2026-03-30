from pyvis.network import Network
import json

def draw_ann(triples, l_gap):
    # 'notebook=False' is better for standalone webpages
# 'cdn_resources=remote' ensures the webpage can load the graphics engine
    net = Network(height="750px", width="100%", directed=True, bgcolor="#ffffff", cdn_resources='remote')    
    levels = {}
    for s, r, o in triples:
        if s not in levels: levels[s] = 0
        levels[o] = max(levels.get(o, 0), levels[s] + 1)
    
    max_lvl = max(levels.values()) if levels else 1

    for s, r, o in triples:
        s_col = "#97C2FC" if levels[s] == 0 else ("#FB7E81" if levels[s] == max_lvl else "#C297FC")
        o_col = "#97C2FC" if levels[o] == 0 else ("#FB7E81" if levels[o] == max_lvl else "#C297FC")
        
        net.add_node(s, label=s, level=levels[s], color=s_col, shape="circle", size=35)
        net.add_node(o, label=o, level=levels[o], color=o_col, shape="circle", size=35)
        net.add_edge(s, o, color="#848484")
    options = {
    "physics": {
        "enabled": False  # This stops the nodes from flying away
    },
    "layout": {
        "hierarchical": {
            "enabled": True,
            "direction": "LR",
            "levelSeparation": 1000, # Gives the 123 neurons space
            "nodeSpacing": 400
        }
    }
}
    net.set_options(json.dumps(options))
    return net.generate_html()