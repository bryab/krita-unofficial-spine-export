
import os
import re
import krita

from krita import (Krita, Extension)

import os
import json
import re


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QFormLayout, QListWidget, QAbstractItemView,
                             QDialogButtonBox, QVBoxLayout, QFrame, QTabWidget, QFileDialog,
                             QPushButton, QAbstractScrollArea, QMessageBox)


class SpineExport(object):

    def __init__(self, parent=None):
        self.msgBox = None
        self.fileFormat = 'png'

        self.bonePattern = re.compile("\(bone\)|\[bone\]", re.IGNORECASE)
        self.mergePattern = re.compile("\(merge\)|\[merge\]", re.IGNORECASE)
        self.slotPattern = re.compile("\(slot\)|\[slot\]", re.IGNORECASE)
        self.skinPattern = re.compile("\(skin\)|\[skin\]", re.IGNORECASE)

    def exportDocument(self, document, directory, boneLength, includeHidden):
        if document is not None:
            self.json = {
                "skeleton": {"images": directory},
                "bones": [{"name": "root"}],
                "slots": [],
                "skins": {"default": {}},
                "animations": {}
            }
            self.spineBones = self.json['bones']
            self.spineSlots = self.json['slots']
            self.spineSkins = self.json['skins']['default']
            self.boneLength = boneLength
            self.skinsCount = 1 # default, incremented with new skins
            self.boneRotation = 0
            self.includeHidden = includeHidden

            horGuides = document.horizontalGuides()
            verGuides = document.verticalGuides()
           
            #self._alert("Guides: ({0}, {1})".format(horGuides, verGuides))
           
            xOrigin = 0
            yOrigin = 0
                        
            if len(horGuides) == 1 and len(verGuides) == 1:
                xOrigin = verGuides[0]
                yOrigin = -horGuides[0] + 1

            Krita.instance().setBatchmode(True)
            self.document = document
            self._export(document.rootNode(), directory, "root", xOrigin, yOrigin)
            Krita.instance().setBatchmode(False)
            with open('{0}/{1}'.format(directory, 'spine.json'), 'w') as outfile:
                json.dump(self.json, outfile, indent=2)
        else:
            self._alert("Please select a Document")

    @staticmethod
    def quote(value):
        return '"' + value + '"'

    def _alert(self, message):
        self.msgBox = self.msgBox if self.msgBox else QMessageBox()
        self.msgBox.setText(message)
        self.msgBox.exec_()

    def _export(self, node, directory, bone="root", xOffset=0, yOffset=0, slot=None):
        for child in node.childNodes():
            if "selectionmask" in child.type():
                continue

            if not self.includeHidden and not child.visible():
                continue

            if '[ignore]' in child.name():
                continue
                
            # Special "fake" Krita layer - maybe used for showing guides?
            if child.name() == "decorations-wrapper-layer":
                continue;

            if child.childNodes():
                if not self.mergePattern.search(child.name()):
                    newBone = bone
                    newSlot = slot
                    newX = xOffset
                    newY = yOffset

                    # Found a bone
                    if self.bonePattern.search(child.name()):
                        newBone = self.bonePattern.sub('', child.name()).strip()
                        rect = child.bounds()
                        newX = rect.left() + rect.width() / 2 - xOffset
                        newY = (- rect.bottom() + rect.height() / 2) - yOffset
                        self.spineBones.append({
                            'name': newBone,
                            'parent': bone,
                            'length': self.boneLength,
                            'rotation': self.boneRotation,
                            'x': newX,
                            'y': newY
                        })
                        newX = xOffset + newX
                        newY = yOffset + newY

                    # Found a slot
                    if self.slotPattern.search(child.name()):
                        newSlotName = self.slotPattern.sub('', child.name()).strip()
                        newSlot = {
                            'name': newSlotName,
                            'bone': bone,
                            'attachment': None,
                        }
                        self.spineSlots.append(newSlot)

                    ## Found a skin
                    if self.skinPattern.search(child.name()):
                        new_skin_name = self.skinPattern.sub('', child.name()).strip()
                        #problem
                        #new_skin = "#'\t{ "name": ' + self.quote(new_skin_name) + ', "bone": '# + self.quote(slot.bone ? slot.bone.name : "root");
                        new_skin = "FIXSKIN"
                        self.spineSkins.append(new_skin)
                        self.skinsCount = self.skinsCount + 1

                    self._export(child, directory, newBone, newX, newY, newSlot)
                    continue

            name = self.mergePattern.sub('', child.name()).strip()
            layer_file_name = '{0}/{1}.{2}'.format(directory, name, self.fileFormat)
            ## Note there is an optional bounds setting here
            child.save(layer_file_name, 96, 96, krita.InfoObject()) 

            newSlot = slot

            if not newSlot:
                newSlot = {
                    'name': name,
                    'bone': bone,
                    'attachment': name,
                }
                self.spineSlots.append(newSlot)
            else:
                if not newSlot['attachment']:
                    newSlot['attachment'] = name

            rect = child.bounds()
            slotName = newSlot['name']
            if slotName not in self.spineSkins:
                self.spineSkins[slotName] = {}
            self.spineSkins[slotName][name] = {
                'x': rect.left() + rect.width() / 2 - xOffset,
                'y': (- rect.bottom() + rect.height() / 2) - yOffset,
                'rotation': -self.boneRotation,
                'width': rect.width(),
                'height': rect.height(),
            }



