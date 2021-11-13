import argparse
import json
import os
from queue import SimpleQueue
import sys
from threading import Thread
import tkinter
from tkinter import CENTER, END, filedialog, Frame, StringVar, ttk
import traceback

from kdl import parse

from .dsl.project import Project
from .dsl.util import serialize, ProgressTracker, PrintProgressTracker, QueueProgressTracker

def format_project(project_file: str, project_root: str, progress: ProgressTracker):
    try:
        if not os.path.exists(project_root):
            os.mkdir(project_root)
        with open(project_file, encoding="utf-8") as file:
            progress.set_status("Deserializing " + project_file)
            contents = json.load(file)
            project = Project.deserialize(contents)
            proj_docs, names = project.format(progress)
            for name, doc in proj_docs.items():
                path = project_root + "/" + name + ".kdl"
                with open(path, mode="w", encoding="utf-8") as out:
                    out.write(str(doc))
                    progress.set_status("Exported " + path + "!")
            if len(project.custom_events) > 0 and not os.path.exists(project_root + "/custom-events"):
                os.mkdir(project_root + "/custom-events")
            for event in project.custom_events:
                path = project_root + "/custom-events/" + names.custom_event_for_id(str(event.id)) + ".kdl"
                with open(path, mode="w", encoding="utf-8") as out:
                    out.write(str(event.format(names)))
                    progress.set_status("Exported " + path + "!")
            if len(project.scenes) > 0 and not os.path.exists(project_root + "/scenes"):
                os.mkdir(project_root + "/scenes")
            for scene in project.scenes:
                progress.current_scene = names.scene_for_id(str(scene.id))
                scene_path = project_root + "/scenes/" + names.scene_for_id(str(scene.id)) + "/"
                if not os.path.exists(scene_path):
                    os.mkdir(scene_path)
                scene_docs, scene_names = scene.format(names, progress)
                for name, doc in scene_docs.items():
                    with open(scene_path + name + ".kdl", mode="w", encoding="utf-8") as out:
                        out.write(str(doc))
                        progress.set_status("Exported " + scene_path + name + ".kdl!")
                if len(scene.actors) > 0 and not os.path.exists(scene_path + "actors"):
                    os.mkdir(scene_path + "actors")
                for actor in scene.actors:
                    actor_path = scene_path + "actors/" + scene_names.actor_for_id(str(actor.id)) + "/"
                    if not os.path.exists(actor_path):
                        os.mkdir(actor_path)
                    actor_docs = actor.format(scene_names)
                    for name, doc in actor_docs.items():
                        with open(actor_path + name + ".kdl", mode="w", encoding="utf-8") as out:
                            out.write(str(doc))
                            progress.set_status("Exported " + actor_path + name + ".kdl!")
                if len(scene.triggers) > 0 and not os.path.exists(scene_path + "triggers"):
                    os.mkdir(scene_path + "triggers")
                for trigger in scene.triggers:
                    trigger_path = scene_path + "triggers/" + scene_names.trigger_for_id(str(trigger.id)) + "/"
                    if not os.path.exists(trigger_path):
                        os.mkdir(trigger_path)
                    trigger_docs = trigger.format(scene_names)
                    for name, doc in trigger_docs.items():
                        with open(trigger_path + name + ".kdl", mode="w", encoding="utf-8") as out:
                            out.write(str(doc))
                            progress.set_status("Exported " + trigger_path + name + ".kdl!")
            progress.set_status("Project converted to KDL!")
    except RuntimeError as err:
        traceback.print_exc()
        progress.log_error("Conversion failed: " + str(err))


def parse_project(project_file: str, project_root: str, progress: ProgressTracker):
    try:
        progress.set_status("Parsing project metadata and assets")
        docs = {i.name[:-4]: parse(open(project_root + "/" + i.name, encoding="utf-8").read()) for i in
                os.scandir(project_root)
                if i.is_file() and i.name.endswith(".kdl")}
        project = Project.parse(docs, project_root, progress)
        progress.set_status("Exporting into JSON")
        contents = project.serialize()
        if os.path.exists(project_file):
            if os.path.exists(project_file + ".bak"):
                os.remove(project_file + ".bak")
            os.rename(project_file, project_file + ".bak")
        with open(project_file, "w", encoding="utf-8") as out:
            json.dump(serialize(contents), out, indent=4)
        progress.set_status("Project converted to JSON!")
    except RuntimeError as err:
        traceback.print_exc()
        progress.log_error("Conversion failed: " + str(err))


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.status = StringVar()
        self.errors = StringVar()
        self.status_queue = SimpleQueue()
        self.errors_queue = SimpleQueue()
        self.proj_file_label = ttk.Label(self, text=".gbsproj location")
        self.proj_file_field = ttk.Entry(self)
        self.proj_file_browse = ttk.Button(self, text="Browse...", command=self.browse_file)
        self.proj_dir_label = ttk.Label(self, text=".kdl tree location")
        self.proj_dir_field = ttk.Entry(self)
        self.proj_dir_browse = ttk.Button(self, text="Browse...", command=self.browse_dir)
        self.format_btn = ttk.Button(self, text="Convert .gbsproj to .kdl tree", command=self.execute_format)
        self.parse_btn = ttk.Button(self, text="Convert .kdl tree to .gbsproj", command=self.execute_parse)
        self.status_label = ttk.Label(self, textvar=self.status, justify=CENTER)
        self.error_label = ttk.Label(self, textvar=self.errors, foreground="red", justify=CENTER)
        self.proj_file_label.grid(row=0, column=0)
        self.proj_file_field.grid(row=0, column=1)
        self.proj_file_browse.grid(row=0, column=2)
        self.proj_dir_label.grid(row=1, column=0)
        self.proj_dir_field.grid(row=1, column=1)
        self.proj_dir_browse.grid(row=1, column=2)
        self.format_btn.grid(row=2, column=0)
        self.parse_btn.grid(row=2, column=2)
        self.status_label.grid(row=3, column=0, columnspan=3)
        self.error_label.grid(row=4, column=0, columnspan=3)

    def browse_file(self):
        result = filedialog.askopenfilename(filetypes=[("GB Studio projects", "*.gbsproj")])
        self.proj_file_field.delete(0, END)
        self.proj_file_field.insert(0, result)

    def browse_dir(self):
        result = filedialog.askdirectory()
        self.proj_dir_field.delete(0, END)
        self.proj_dir_field.insert(0, result)

    def execute_format(self):
        file = self.proj_file_field.get()
        dir = self.proj_dir_field.get()
        can_run = True
        errors = []
        if file == "" or not os.path.exists(file):
            can_run = False
            errors.append("Cound not find file '" + file + "'")
        if dir == "" or not os.path.exists(dir):
            can_run = False
            errors.append("Could not find directory '" + dir + "'")
        if can_run:
            self.master.after(50, self.update_status())
            exec_thread = Thread(
                target=format_project,
                args=(file, dir, QueueProgressTracker(self.status_queue, self.errors_queue))
            )
            exec_thread.start()
        else:
            self.status.set("Could not format project")
            self.errors.set("\n".join(errors))

    def execute_parse(self):
        file = self.proj_file_field.get()
        dir = self.proj_dir_field.get()
        can_run = True
        errors = []
        if file == "" or not os.path.exists(file):
            can_run = False
            errors.append("Cound not find file '" + file + "'")
        if dir == "" or not os.path.exists(dir):
            can_run = False
            errors.append("Could not find directory '" + dir + "'")
        if can_run:
            self.master.after(50, self.update_status())
            exec_thread = Thread(
                target=parse_project,
                args=(file, dir, QueueProgressTracker(self.status_queue, self.errors_queue))
            )
            exec_thread.start()
        else:
            self.status.set("Could not parse project")
            self.errors.set("\n".join(errors))

    def update_status(self):
        while not self.status_queue.empty():
            self.status.set(self.status_queue.get())
        while not self.errors_queue.empty():
            current = self.errors.get()
            if current == "":
                self.errors.set(self.errors_queue.get())
            else:
                self.errors.set(current + "\n" + self.errors_queue.get())
        self.master.after(50, self.update_status)


def run_cli():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # running from a bundle!
        root = tkinter.Tk()
        app = Application(root)
        app.master.title("GBS Toolkit")
        app.mainloop()
    else:
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="action")
        parser_gui = subparsers.add_parser("gui", help="Run as a GUI application instead.")
        parser_format = subparsers.add_parser("format", help="Format a .gbsproj file into a tree of .kdl files.")
        parser_format.add_argument("file", help="The .gbsproj file to read from.")
        parser_format.add_argument("dir", help="The directory to write the .kdl tree to.")
        parser_parse = subparsers.add_parser("parse", help="Parse a tree of .kdl files into a .gbsproj file.")
        parser_parse.add_argument("dir", help="The directory to read the .kdl tree from.")
        parser_parse.add_argument("file", help="The .gbsproj file to write to. Will be backed up if exists.")
        args = parser.parse_args()
        if args.action == "gui":
            root = tkinter.Tk()
            app = Application(root)
            app.master.title("GBS Toolkit")
            app.mainloop()
        elif args.action == "format":
            format_project(args.file, args.dir, PrintProgressTracker())
        elif args.action == "parse":
            parse_project(args.file, args.dir, PrintProgressTracker())


def run_app():
    root = tkinter.Tk()
    app = Application(root)
    app.master.title("GBS Toolkit")
    app.mainloop()


if __name__ == "__main__":
    run_cli()
