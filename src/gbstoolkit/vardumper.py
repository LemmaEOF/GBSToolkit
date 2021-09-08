import json
import os


def dump_vars(project_file: str):
    with open(project_file) as project:
        contents = json.load(project)
    if not os.path.exists("out"):
        os.makedirs("out")

    out_text = ""
    vars = contents["variables"]
    for var in vars:
        out_text += var["id"] + "=" + var["name"] + "\n"

    with open("out/variables.txt", mode="w") as file:
        file.write(out_text)

    print("Dumped " + str(len(vars)) + " variables into `out/variables.txt`")


def load_vars(project_file: str, vars_file: str):
    with open(project_file) as project:
        with open("modified_" + project_file, "w") as new_project:
            with open(vars_file) as file:
                contents = json.load(project)
                vars = []
                vars_contents = file.read()
                lines = vars_contents.split("\n")
                for line in lines:
                    segments = line.split("=")
                    var = {"id": segments[0], "name": "".join(segments[1:])}
                    vars.append(var)
                contents["variables"] = vars
                json.dump(contents, new_project, indent=4)
                print("Loaded " + str(len(lines)) + " variables into `modified_" + project_file + "`")
