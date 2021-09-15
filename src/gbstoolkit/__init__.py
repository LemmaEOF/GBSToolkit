import json

from dsl.event import Event
from dsl.marshalling import serialize
from dsl.util import NameUtil

from kdl import Document, parse


class SpecialNameUtil(NameUtil):
    actor_to_id = {"Actor1": "4275dc83-4b64-4f3d-92c1-d54e6bb24eee", "Actor2": "84a068f6-ccd4-4b63-a78f-d4787ed25d87",
                   "Actor3": "566c8812-a204-45b5-b93a-c113c10c20de"}
    id_to_actor = {"4275dc83-4b64-4f3d-92c1-d54e6bb24eee": "Actor1", "84a068f6-ccd4-4b63-a78f-d4787ed25d87": "Actor2",
                   "566c8812-a204-45b5-b93a-c113c10c20de": "Actor3"}
    sprite_to_id = {"bullet": "ec0f660e-c420-43ee-9d1e-6d8e9f320213",
                    "turnip_squash": "6f1e5757-a472-4531-8a65-aee22751e917"}
    id_to_sprite = {"ec0f660e-c420-43ee-9d1e-6d8e9f320213": "bullet",
                    "6f1e5757-a472-4531-8a65-aee22751e917": "turnip_squash"}

    def actor_for_id(self, id: str) -> str:
        if id == "$self$" or id == "player":
            return id
        return self.id_to_actor[id]

    def id_for_actor(self, name: str) -> str:
        if name == "$self$" or name == "player":
            return name
        return self.actor_to_id[name]

    def background_for_id(self, id: str) -> str:
        pass

    def id_for_background(self, name: str) -> str:
        pass

    def scene_for_id(self, id: str) -> str:
        pass

    def id_for_scene(self, name: str) -> str:
        pass

    def song_for_id(self, id: str) -> str:
        pass

    def id_for_song(self, name: str) -> str:
        pass

    def sprite_for_id(self, id: str) -> str:
        return self.id_to_sprite[id]

    def id_for_sprite(self, name: str) -> str:
        return self.sprite_to_id[name]


if __name__ == "__main__":
    names = SpecialNameUtil()
    # with open("sample_events.json") as file:
    #     with open("sample_events.kdl", "w") as outfile:
    #         contents = json.load(file)
    #         doc = Document(preserve_property_order=True)
    #         for i in contents["script"]:
    #             event = Event.deserialize(i)
    #             doc.append(event.format(names))
    #         outfile.write(str(doc))
    #         print("Converted " + str(len(doc)) + " events to KDL!")

    with open("sample_events.kdl") as file:
        with open("reparsed_sample_events.json", "w") as outfile:
            doc = parse(file.read())
            events = []
            for i in doc:
                events.append(Event.parse(i, names))
            json.dump({"script": serialize(events)}, outfile, indent=4)
            print("Converted " + str(len(events)) + " events to JSON!")
