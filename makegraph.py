import os

PATH = "../"
ignore_paths = [".git"]
ignore_headers_prefix = ["<", "\"llvm/"]

files_path = []
# traverse root directory, and list directories as dirs and files as files
for root, dirs, files in os.walk(PATH):
    path = root.split(os.sep)

    to_ignore = False
    for path_to_ignore in ignore_paths:
        l = len(PATH)+len(path_to_ignore)
        if len(root) >= l and root[0:l] == PATH+path_to_ignore:
            to_ignore = True
            break

    for file in files:
        if not(to_ignore):
            # print(root+os.sep+file)
            files_path.append(root+os.sep+file)

uncompressed_edges = []
# search for #includes directives in the files
for file_path in files_path:
    file_d = open(file_path)
    print(file_path)
    for line in file_d:
        if len(line) > 9 and line[0:9] == "#include ":
            to_ignore = False
            for header_prefix_to_ignore in ignore_headers_prefix:
                l = len(header_prefix_to_ignore)
                if len(line) >= l+9 and line[9:l+9] == header_prefix_to_ignore:
                    to_ignore = True
                    break

            if not(to_ignore):
                # print(file_path, line[10:-2])
                uncompressed_edges.append([file_path, line[10:-2]])
    file_d.close()

unformatted_edges = []
# make headers paths absolute
for uncompressed_edge in uncompressed_edges:
    file_path = uncompressed_edge[0]
    header_path = uncompressed_edge[1]
    norm_header_path = os.path.normpath(header_path)
    # print(file_path, header_path, norm_header_path)
    unformatted_edges.append([file_path, norm_header_path])

edges = []
data = []
max_index = 0
# final analysis and formatting, compressing data
for edge in unformatted_edges:
    file_path = edge[0]
    header_path = edge[1]
    file_basename = os.path.basename(file_path)
    header_basename = os.path.basename(header_path)
    file_basename_wo_ext = os.path.splitext(file_basename)[0]
    header_basename_wo_ext = os.path.splitext(header_basename)[0]
    edge_type = 0

    # same names, conventionnally a source refering its header
    if file_basename_wo_ext == header_basename_wo_ext:
        # source and headers placed in the same dir, could be adapted
        if header_basename == header_path:
            edge_type = 1

    if edge_type == 0:
        shrt_file_path = os.path.relpath(file_path, PATH)
        rel_header_path = os.path.dirname(file_path)+os.sep+header_path
        shrt_header_path = os.path.relpath(rel_header_path, PATH)

        if shrt_file_path in data:
            index_a = data.index(shrt_file_path)
        else:
            data.append(shrt_file_path)
            index_a = max_index
            max_index += 1

        if shrt_header_path in data:
            index_b = data.index(shrt_header_path)
        else:
            data.append(shrt_header_path)
            index_b = max_index
            max_index += 1

        new_edge = [index_a, index_b, edge_type]
        edges.append(new_edge)

dot_repr = []
dot_repr.append('// ')
dot_repr.append('digraph dependencies {')

tab = '    '
key = 0
for value in data:
    s = tab+str(key)+" [label=\""+value+"\"];"
    key += 1
    dot_repr.append(s)
for edge in edges:
    index_a = edge[0]
    index_b = edge[1]
    s = tab+str(index_a)+" -> "+str(index_b)+";"
    dot_repr.append(s)

dot_repr.append('}')

f = open('graph.dot', 'w')
for line in dot_repr:
    print(line)
    f.write(line+"\n")
f.close()
