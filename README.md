# GBS Toolkit
 *Python tools for messing around with GB Studio projects.*

GBS Toolkit is a tool I've built while working on Soul and Silicon, a
queer/trans dating simulator I'm writing for the GameBoy Color. It's a very
text-heavy game, and while GB Studio has a dialogue review section, it can't
always easily handle lots of branching dialogue, and there's no way for it to
add new dialogue.

GBS Toolkit allows you to export the *entirety* of a GB Studio project into a
collection of files written in [kdl](https://kdl.dev). These files define the
properties and scripts for every scene, actor, trigger, asset, and more in the
game, and can be reimported into a GB Studio `.gbsproj` file once you're done
editing them. **No data should be lost between importing and exporting**, so
you can edit freely without worrying about having to reimplement things.

The GBS Toolkit project is also set up so that other Python projects can use it
as a library for interacting with GB Studio project files.

## Requirements
- Tested with GB Studio v2.0 beta 5. Other versions may not work properly.
- Python 3.6 or higher.
- [kdl-py](https://pypi.org/project/kdl-py/) 1.0.0 or higher.

## Installation and Usage
GBS Toolkit can be used either through the command line or a GUI. There are
executable bundles for MacOS, Windows, and Linux available in
[Releases](https://github.com/LemmaEOF/GBSToolkit/releases). Otherwise,
GBS Toolkit can be installed from PyPI:
```shell
pip install gbstoolkit
```

In order to run the GBS Toolkit GUI from the command line:
```shell
gbstoolkit gui
```

In order to convert a project from a .gbsproj file to kdl:
```shell
gbstoolkit format <gbsproj file> <kdl directory>
```

In order to convert a project from kdl to a .gbsproj file:
```shell
gbstoolkit parse <kdl directory> <gbsproj file>
```

Running a bundled executable will launch the GUI immediately.

## Future Plans
Currently, **there is no support for custom plugins or engines**. Support is
planned for future versions, but I'm still figuring out how to write a plugin
system that doesn't allow for arbitrary code execution.

GBS Toolkit will be updated to support GB Studio v3 once it exits alpha and is
recommended for games to use.

## Licensing and Contribution
Contributions are more than welcome, and GBS Toolkit is publicly available
under [FAFOL 0.2](LICENSE.md). You can use, modify, and even redistribute it
however you want, as long as you're not being exploitative with it. Thank you
for giving GBS Toolkit a look!
