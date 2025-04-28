# This is a script to inline single use references in a JSON schema
# May be useful to save some tokens when using the schema in a LLM


def get_refs(tree_sart):
    all_refs = []
    for key, value in tree_sart["properties"].items():
        if "$ref" in value:
            all_refs.append((["properties",key], value["$ref"]))
        elif "anyOf" in value:
            for i, v in enumerate(value["anyOf"]):
                if "$ref" in v:
                    all_refs.append((["properties",key, "anyOf", i], v["$ref"]))
                elif "items" in v:
                    if "$ref" in v["items"]:
                        all_refs.append((["properties",key, "anyOf", i, "items"], v["items"]["$ref"]))
        elif "properties" in value:
            all_refs += [(["properties",key]+loaction,ref_val)for (loaction,ref_val)in get_refs(value)]
    return all_refs


def inline_singe_use_refs(schema):
    content = schema["json_schema"]["schema"]

    while True:
        all_refs = get_refs(content)

        for key, val in content["$defs"].items():
            if "properties" not in val:
                continue
            all_refs += [(["$defs",key]+loaction,ref_val) for (loaction,ref_val)in get_refs(val)]

        singular_refs = []
        duplicate_refs = []
        for ref in all_refs:
            if ref[1] not in singular_refs and ref[1] not in duplicate_refs:
                singular_refs.append(ref[1])
            else:
                if ref[1] in singular_refs:
                    singular_refs.remove(ref[1])
                duplicate_refs.append(ref[1])
        if len(singular_refs) == 0:
            break

        ref_to_inline = singular_refs[0]
        ref_position = [pos for pos, val in all_refs if val == ref_to_inline][0]
        #print(ref_to_inline, ref_position)
        
        ref_name = ref_to_inline.split("/")[-1]
        ref_content = content["$defs"][ref_name]

        position_to_insert = content
        for i in ref_position:
            position_to_insert = position_to_insert[i]
        # remove ref from position to insert
        del position_to_insert["$ref"]
        position_to_insert.update(ref_content)
        del content["$defs"][ref_name]
    return schema