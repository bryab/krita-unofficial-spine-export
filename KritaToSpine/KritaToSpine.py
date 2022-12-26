# Spine export
# Forked from Unofficial Spine Export (https://github.com/chartinger/krita-unofficial-spine-export)
# Based on the Esoteric Software Photoshop plugin, and the Spine Document Tools plugin
# uidocumentools.py contains the main window and logic, including tabs for applying effects on export
# SpineExport.py contains the code and support for doing the exporting

import krita
from krita import (Krita, Extension)

from . import uidocumenttools

class SpineExport(Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        action = window.createAction("spineexportAction",i18n("Spine Export"))
        action.setToolTip(i18n("Plugin to export to Spine."))
        action.triggered.connect(self.initialize)
        #action = window.createAction("spineexportAction", "Export to Spine", "tools/scripts")
        #action.triggered.connect(self.exportDocument)

    def initialize(self):
        self.uidocumenttools = uidocumenttools.UIDocumentTools()
        self.uidocumenttools.initialize()



# And add the extension to Krita's list of extensions:
Krita.instance().addExtension(SpineExport(Krita.instance()))

# End of file
