import json

SCHEMA = "scripts/schema.json"
KEYS = ['provider', 'resource_schemas', 'datasource_schemas']

BASE = []


def get_attrs(obj):
    c = []
    r = []
    o = []
    attrs = obj['block']['attributes']
    for k, v in attrs.items():
        desc = "_{}_".format(v['description']) if 'description' in v else ''
        s = "**{}** {}".format(k, desc)
        if 'computed' in v and v['computed']:
            c.append(s)
        elif 'required' in v and v['required']:
            r.append(s)
        elif 'optional' in v and v['optional']:
            o.append(s)
    return c, r, o


def gen_list(arr, section=False, numbered=False):
    out = []
    if len(arr) == 0:
        return out
    if section is not False:
        out += section
    for req in arr:
        idx = '*'
        out.append("{} {} \n".format(idx, req))
    return out


def gen_attributes(c, r, o, section=False):
    tmpl = []
    if section is not False:
        tmpl.append("### {} \n".format(section))
    tmpl += gen_list(r, '#### Required \n')
    tmpl += gen_list(o, '#### Optional \n')
    tmpl += gen_list(c, '##### Computed \n')
    return tmpl


with open(SCHEMA) as source:
    json_src = json.load(source)
    md_obj = {}
    md_str = []
    md_str.append("# terraform-provider-aiven \n")
    c, r, o = get_attrs(json_src['provider'])
    md_str += gen_attributes(c, r, o)
    md_str.append('--- \n')
    md_str.append('## Resources \n')
    for k, v in json_src['resource_schemas'].items():
        c, r, o = get_attrs(v)
        md_str += gen_attributes(c, r, o, k)
    md_str.append('--- \n')
    md_str.append('## Data-sources \n')
    for k, v in json_src['data_source_schemas'].items():
        c, r, o = get_attrs(v)
        md_str += gen_attributes(c, r, o, k)

    print(''.join(md_str))
