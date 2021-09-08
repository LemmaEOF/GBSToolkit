import json
import os
import platform
import re

from dsl.project import Project


def make_actor_ref(project_file: str):
    if not os.path.exists("out"):
        os.mkdir("out")
    with open(project_file) as file:
        count_actors = 0
        count_scenes = 0
        contents = json.load(file)
        project = Project.deserialize(contents)
        for scene in project.scenes:
            count_scenes += 1
            scene_name = sanitize_name(scene.name, "Scene")
            seen_names = []
            actor_names = {}
            for actor in scene.actors:
                count_actors += 1
                name = actor.name
                if name == "":
                    name = "Actor " + str(scene.actors.index(actor))
                if name in seen_names:
                    name = name + " " + str(scene.actors.index(actor))
                    print("Found actor name " + actor.name + " in scene " + scene_name + " multiple times!")
                    print("Renaming to `" + name + "` for distinguishability.")
                    print("The original name will be preserved in the .gbsproj!")
                else:
                    seen_names.append(name)
                actor_names[actor.id] = (name, actor.name)
            path = "out/" + scene_name
            if not os.path.exists(path):
                os.mkdir(path)
            with open(path + "/actors.txt", mode="w") as outfile:
                outfile.write("".join([str(k) + ": " + v[0] + " (" + v[1] + ")\n" for k, v in actor_names.items()]))
        print("Found " + str(count_actors) + " actors in " + str(count_scenes) + " scenes!")


def sanitize_name(name: str, context: str) -> str:
    illegal_filenames = ["CON", "PRN", "AUX", "CLOCK$", "NUL", "COM0", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6",
                         "COM7", "COM8", "COM9", "LPT0", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8",
                         "LPT9"]
    ret = re.sub(r'[\/\\\*\:\?\"\;\|\,\[\]\&\<\>\=]', '-', name)
    if platform.system() == "Windows" and ret in illegal_filenames:
        print("WARNING! " + context + " name '" + ret + "' is reserved on Windows. Renaming!")
        print("For more information, see this video: https://youtu.be/bC6tngl0PTI")
        ret += "-"
    return ret


if __name__ == "__main__":
    make_actor_ref("samples/GBS Sample Project.gbsproj")
