import json

from dsl.event import Event
from dsl.marshalling import serialize
from dsl.util import NameUtil

from kdl import Document, parse


class SpecialNameUtil(NameUtil):
    actor_to_id = {"Actor1": "4275dc83-4b64-4f3d-92c1-d54e6bb24eee", "Actor2": "84a068f6-ccd4-4b63-a78f-d4787ed25d87",
                   "Actor3": "9a2ed4e7-8bcc-4be2-bcf6-fc1c69a2b565"}
    id_to_actor = {"4275dc83-4b64-4f3d-92c1-d54e6bb24eee": "Actor1", "84a068f6-ccd4-4b63-a78f-d4787ed25d87": "Actor2",
                   "9a2ed4e7-8bcc-4be2-bcf6-fc1c69a2b565": "Actor3"}

    def actor_for_id(self, id: str) -> str:
        if id == "$self$" or id == "player":
            return id
        return self.id_to_actor[id]

    def id_for_actor(self, name: str) -> str:
        if name == "$self$" or name == "player":
            return name
        return self.actor_to_id[name]

    def trigger_for_id(self, id: str) -> str:
        return ""

    def id_for_trigger(self, name: str) -> str:
        return ""


if __name__ == "__main__":
    names = SpecialNameUtil()
    with open("sample_events.json") as file:
        with open("sample_events.kdl", "w") as outfile:
            contents = json.load(file)
            doc = Document(preserve_property_order=True)
            for i in contents["script"]:
                event = Event.deserialize(i)
                doc.append(event.format(names))
            outfile.write(str(doc))
            print("Converted " + str(len(doc)) + " events to KDL!")

    with open("sample_events.kdl") as file:
        with open("reparsed_sample_events.json", "w") as outfile:
            doc = parse(file.read())
            events = []
            for i in doc:
                events.append(Event.parse(i, names))
            json.dump({"script": serialize(events)}, outfile, indent=2)
            print("Converted " + str(len(events)) + " events to JSON!")
