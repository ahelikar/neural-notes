from pyvis.network import Network
import json

def draw_ann(triples, l_gap):
    # CRITICAL: Use cdn_resources='remote' so the library loads from the web
    net = Network(
        height="750px", 
        width="100%", 
        directed=True, 
        bgcolor="#ffffff", 
        cdn_resources='remote'
    )    
    
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

    # We use a raw string here to ensure the browser interprets the JS correctly
    # Physics is False to prevent the "gravitational" flying issue
    options = """
    {
      "physics": {
        "enabled": false
      },
      "layout": {
        "hierarchical": {
          "enabled": true,
          "direction": "LR",
          "levelSeparation": """ + str(l_gap) + """,
          "nodeSpacing": 400
        }
      },
      "interaction": {
        "navigationButtons": true,
        "keyboard": true
      }
    }
    """
    net.set_options(options)
    return net.generate_html()