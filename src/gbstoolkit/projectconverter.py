import json
import os


from dsl.project import Project


def format_project(project_file: str):
    if not os.path.exists("out"):
        os.mkdir("out")
    with open(project_file) as file:
        contents = json.load(file)
        project = Project.deserialize(contents)
        proj_docs, names = project.format()
        for name, doc in proj_docs.items():
            path = "out/" + name + ".kdl"
            with open(path, mode="w") as out:
                out.write(str(doc))
                # print("Exported " + path + "!")
        if len(project.custom_events) > 0 and not os.path.exists("out/custom-events"):
            os.mkdir("out/custom-events")
        for event in project.custom_events:
            path = "out/custom-events/" + names.custom_event_for_id(str(event.id)) + ".kdl"
            with open(path, mode="w") as out:
                out.write(str(event.format(names)))
                # print("Exported " + path + "!")
        if len(project.scenes) > 0 and not os.path.exists("out/scenes"):
            os.mkdir("out/scenes")
        for scene in project.scenes:
            scene_path = "out/scenes/" + names.scene_for_id(str(scene.id)) + "/"
            if not os.path.exists(scene_path):
                os.mkdir(scene_path)
            scene_docs, scene_names = scene.format(names)
            for name, doc in scene_docs.items():
                with open(scene_path + name + ".kdl", mode="w") as out:
                    out.write(str(doc))
                    # print("Exported " + scene_path + name + ".kdl!")
            if len(scene.actors) > 0 and not os.path.exists(scene_path + "actors"):
                os.mkdir(scene_path + "actors")
            for actor in scene.actors:
                actor_path = scene_path + "actors/" + scene_names.actor_for_id(str(actor.id)) + "/"
                if not os.path.exists(actor_path):
                    os.mkdir(actor_path)
                actor_docs = actor.format(scene_names)
                for name, doc in actor_docs.items():
                    with open(actor_path + name + ".kdl", mode="w") as out:
                        out.write(str(doc))
                        # print("Exported " + actor_path + name + ".kdl!")
            if len(scene.triggers) > 0 and not os.path.exists(scene_path + "triggers"):
                os.mkdir(scene_path + "triggers")
            for trigger in scene.triggers:
                trigger_path = scene_path + "triggers/" + scene_names.trigger_for_id(str(trigger.id)) + "/"
                if not os.path.exists(trigger_path):
                    os.mkdir(trigger_path)
                trigger_docs = trigger.format(scene_names)
                for name, doc in trigger_docs.items():
                    with open(trigger_path + name + ".kdl", mode="w") as out:
                        out.write(str(doc))
                        # print("Exported " + trigger_path + name + ".kdl!")


if __name__ == "__main__":
    format_project("GBS Sample Project.gbsproj")
