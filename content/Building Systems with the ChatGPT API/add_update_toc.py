import os 
import codecs
import json

def add_toc(ipynb_file):
    f = codecs.open(ipynb_file, 'r')
    source = f.read()
    y = json.loads(source)
    toc = ["\n"]
    for item in y["cells"]:
        if item["cell_type"]=='markdown' and len(item['source'])>0:
            item_start = item['source'][0].strip("\n")
            if item_start.startswith("#"):
                l = len(item_start.split()[0])
                if l<=3 and l>1: 
                    name = " ".join(item_start.split(" ")[1:])
                    tag = "-".join(item_start.split(" ")[1:])
                    tab = "    "*(l-2)
                    toc.append(f' {tab}- [{name}](#{tag})\n')     

    y["cells"][0]['source']= y["cells"][0]['source'][0:1]
    y["cells"][0]['source'].extend(toc)
    f = codecs.open(ipynb_file, 'w')
    f.write(json.dumps(y))
    f.close()

for file in os.listdir("."):
    print(file)
    if file.endswith("ipynb") and file[0].isdigit():
        print(file)
        add_toc(file)