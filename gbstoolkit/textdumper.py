import json
import os
import shutil

sprites = {}  # uuid-to-readable-name key for avatar names TODO: somehow move into function?
available_actors = {}  # uuid-to-readable-name key for actors TODO: somehow move into function?
emotes = ["shock", "question", "heart", "pause", "angry", "sweat", "note", "sleep"]  # the built-in emote bubbles


def dump_text(project_file: str):
    """
    Grabs all the text (and some events) from a GB Studio project
    and exports it into files per scene, actor, and trigger.
    :param project_file: A string path to the .gbsproj or .json file for the GB Studio project.
    """
    # volatiles for determining paths
    current_scene = ""  # scene name, used for path
    current_name = ""  # actor or trigger name, used for file name

    # important stuff for the whole process
    # TODO: don't have to edit the file to find your .gbsproj
    project = open(project_file)
    contents = json.load(project)  # the parsed JSON

    sprite_sheets = contents["spriteSheets"]

    if os.path.exists("out"):
        try:
            shutil.rmtree("out")
        except OSError as e:
            print("Error: %s : %s" % ("out", e.strerror))
    os.makedirs("out")

    with open("out/sprites.txt", mode="w") as out:
        outcont = ""
        for i in sprite_sheets:
            if i["numFrames"] == 1:
                sprites[i["id"]] = i["name"]
                outcont = outcont + i["name"] + " (" + i["id"] + ")\n"
        out.write(outcont)

    scenes = contents["scenes"]
    for scene in scenes:
        current_scene = scene["name"]

        # Dump scene init text
        script = scene["script"]
        dialogue = []
        for event in script:
            iter_event(event, dialogue, current_scene + " init", 0)
        if len(dialogue) > 0:
            file_path = "out/scripts/" + current_scene
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            with open(file_path + "/init.txt", mode="w", encoding="utf-8") as file:
                file.write("".join(dialogue))

        # Dump actor text
        actors = scene["actors"]
        # TODO: this sucks but I have to iterate through two separate times
        #  bc one is deep & I need everything prepped early
        available_actors.clear()
        for actor in actors:
            name = actor["name"]
            if name == "":
                name = "Actor " + str(actors.index(actor))
            available_actors[actor["id"]] = name
        for actor in actors:
            current_name = actor["name"].replace('/', '-').replace('\\', '-').replace(':', '-')
            if current_name == "":
                current_name = "Actor " + str(actors.index(actor))
            dialogue = []
            script_contents = []
            script = actor["script"]
            if len(script) > 0:
                for event in script:
                    iter_event(event, script_contents, current_scene + " actor " + current_name + " interact", 0)
                if len(script_contents) > 0:
                    dialogue.append("# On interact: \n\n")
                    dialogue.extend(script_contents)
            start_contents = []
            start_script = actor["startScript"]
            if len(start_script) > 0:
                for event in start_script:
                    iter_event(event, start_contents, current_scene + " actor " + current_name + " init", 0)
                if len(start_contents) > 0:
                    dialogue.append("# On initialize: \n\n")
                    dialogue.extend(start_contents)
            if len(dialogue) > 0:
                file_path = "out/scripts/" + current_scene + "/" + "actors"
                if not os.path.exists(file_path):
                    os.makedirs(file_path)
                with open(file_path + "/" + current_name + ".txt", mode="w", encoding="utf-8") as file:
                    file.write("".join(dialogue))

        # Dump trigger text
        triggers = scene["triggers"]
        for trigger in triggers:
            current_name = trigger["name"].replace('/', '-').replace('\\', '-').replace(':', '-')
            if current_name == "":
                current_name = "Trigger " + str(triggers.index(trigger))
            dialogue = []
            script = trigger["script"]
            for event in script:
                iter_event(event, dialogue, current_scene + " trigger " + current_name, 0)
            if len(dialogue) > 0:
                file_path = "out/scripts/" + current_scene + "/" + "triggers"
                if not os.path.exists(file_path):
                    os.makedirs(file_path)
                with open(file_path + "/" + current_name + ".txt", mode="w", encoding="utf-8") as file:
                    file.write("".join(dialogue))
    project.close()
    project.close()


def iter_event(event: dict, dialogue: list, location: str, current_depth: int):
    global sprites, available_actors, emotes
    if "children" in event:  # text events can't have children so safe to go deeper
        # TODO: mark that the node happens? might be important for branches
        has_text = False
        header_point = len(dialogue)
        children = event["children"]
        current_depth += 1
        for k, v in children.items():
            before_point = len(dialogue)
            for e in v:
                iter_event(e, dialogue, location, current_depth)
            if len(dialogue) != before_point:
                if not has_text:
                    dialogue.insert(header_point, current_depth * "  " + "## Branch Condition, depth " +
                                    str(current_depth) + "\n\n")
                    before_point += 1
                    has_text = True
                dialogue.insert(before_point, current_depth * "  " + "### Case " + k + "\n\n")
        if len(dialogue) != header_point:
            dialogue.append(current_depth * "  " + "--End branch condition, depth " + str(current_depth) + "\n\n")
    elif event["command"] == "EVENT_ACTOR_EMOTE":
        args = event["args"]
        actor_id = args["actorId"]
        actor = ""
        if actor_id == "player":
            actor = "player"
        elif actor_id == "$self$":
            actor = "self"
        elif actor_id in available_actors:
            actor = available_actors[actor_id]
        else:
            print("ERROR parsing emote in " + location + ": Missing actor for UUID " + actor_id +
                  "! Make sure the actor isn't null in GB Studio!")
            actor = "NULL"
        dialogue.append("<" + actor + " " + emotes[int(args["emoteId"])] + ">\n\n")
    elif event["command"] == "EVENT_TEXT":
        args = event["args"]
        avatar = ""
        if "avatarId" in args:  # for some reason this can just. not exist???
            if args["avatarId"] != "":
                actor_id = args["avatarId"]
                if actor_id not in sprites:
                    print("ERROR parsing dialogue in " + location + ": Missing avatar name for UUID " + actor_id +
                          "! Make sure the sprite isn't null in GB Studio!")
                    print("Errored dialogue: '''" + str(args["text"]) + "'''")
                    dialogue.append("NULL:\n")
                    avatar = "NULL"
                else:
                    dialogue.append(sprites[actor_id] + ":\n")
                    avatar = sprites[actor_id]
        text = args["text"]
        if isinstance(text, list):
            for t in text:
                if text.index(t) != 0 and avatar != "":
                    dialogue.append(avatar + ":\n")
                dialogue.append(t.replace('Â…', '…'))
                dialogue.append("\n\n")
        else:
            dialogue.append(text.replace('Â…', '…'))
            dialogue.append("\n\n")
        # TODO: mark other sorts of events - moves, shows/hides, etc.?
        # TODO: other 1252-to-utf8 conversions because we. live. in. hell.

