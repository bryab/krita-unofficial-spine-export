# Krita To Spine Export

Unofficial Krita 4 Python Plugin to export into the Spine JSON format

## How to install

* In Krita go to Settings > Manage Resourcs > Open Resource Folder
* Copy `KritaToSpine.desktop` into the pykrita folder
* If you want to be able to easily update the plugin and are familiar with Git, clone this Git repository and create a symlink for the `KritaToSpine` directory in the `prkyira` directory
* Otherwise just copy the `KritaToSpine` folder into that `pykrita` folder

Restart Krita and make sure the plugin is enabled, which means ``Settings > Configure Krita > Python Plugin manager > Krita To Spine Export Plugin`` should be checked.

## How to use

This plugin is inspired by the official [Photoshop plugin](https://github.com/EsotericSoftware/spine-scripts/tree/master/photoshop), and the Krita built-in Document Tools plugin. 

You can find the script under ``Tools > Scripts > Export to Spine``. Select a folder and all your images will be exported into it as well as ``spine.json``

Supported in Group Layers:
* (Bone)
* (Slot)
* (Merge)
* (Ignore)
* [Skin:SkinName]

Various operations such as scaling, resizing and rotating can be applied before export, these are not applied to the original document. 

Notes:
* You should add a single horizontal and single vertical guide to define the origin. You can lock and hide them after adding them.
* Subfolders are **not** supported
* Images will be in ``png`` format
* Both () and [] can be used
* Invisible layers are ignored unless you check `Include Hidden Layers`
* Be careful with filter layers. They will export as merged layer like they are shown in Krita. Consider organizing your scene with merge folders for better control.
