from utils import *

def get_toc_json(root, ignore):
    root_dir = Path(root)
    def recurse(directory):

        store = {}
        store["name"] = str(directory)
        store["type"] = "directory"
        store["contents"] = []

        for path in directory.iterdir():
            if ignore(path):
                print("ignoring", path.name)
                continue

            value = None
            if path.is_dir():
                value = recurse(path)
            elif path.is_file():
                value = {"type": "file", "name": path.name}

            if value == None: continue
            store["contents"].append(value)

        if empty(store["contents"]):
            return None
        return store

    return recurse(root_dir)


def get_toc_string(data):
    def runner(state):
        name = state.get("name")
        type = state.get("type")
        contents = state.get("contents")

        if type == "directory":
            items = map(contents, runner)
            s = "dir: " + name + "\n"
            s += indent(join(items, "\n"))
            return s
        else:
            return name
    return runner(data)


def get_toc(dir):
    return get_toc_string(get_toc_json(dir, default_path_ignore))

def write_toc(dir, name = None):
    s = get_toc(dir)
    if not name:
        name = match(dir, "([\w-]+)\/?$")
    write(name, s, dir = "2024", ext = "toc", log = 1)

# print(get_toc("/home/kdog3682/.vim/"))
