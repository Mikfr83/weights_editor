from PySide2 import QtCore
from PySide2 import QtGui

from weights_editor_tool.enums import Hotkeys


class Hotkey:

    Defaults = {
        Hotkeys.ToggleTableListViews: {"key": QtCore.Qt.Key_QuoteLeft, "ctrl": True},
        Hotkeys.ShowUtilities: {"key": QtCore.Qt.Key_1, "ctrl": True},
        Hotkeys.ShowAddPresets: {"key": QtCore.Qt.Key_2, "ctrl": True},
        Hotkeys.ShowScalePresets: {"key": QtCore.Qt.Key_3, "ctrl": True},
        Hotkeys.ShowSetPresets: {"key": QtCore.Qt.Key_4, "ctrl": True},
        Hotkeys.ShowInfList: {"key": QtCore.Qt.Key_5, "ctrl": True},
        Hotkeys.ShowInfColors: {"key": QtCore.Qt.Key_6, "ctrl": True},
        Hotkeys.MirrorAll: {"key": QtCore.Qt.Key_M, "ctrl": True},
        Hotkeys.Prune: {"key": QtCore.Qt.Key_P, "ctrl": True},
        Hotkeys.RunSmooth: {"key": QtCore.Qt.Key_S, "ctrl": True, "shift": True},
        Hotkeys.RunSmoothAllInfs: {"key": QtCore.Qt.Key_D, "ctrl": True, "shift": True},
        Hotkeys.Undo: {"key": QtCore.Qt.Key_Z, "ctrl": True, "shift": True},
        Hotkeys.Redo: {"key": QtCore.Qt.Key_X, "ctrl": True, "shift": True},
        Hotkeys.GrowSelection: {"key": QtCore.Qt.Key_Greater},
        Hotkeys.ShrinkSelection: {"key": QtCore.Qt.Key_Less},
        Hotkeys.SelectEdgeLoop: {"key": QtCore.Qt.Key_E, "ctrl": True},
        Hotkeys.SelectRingLoop: {"key": QtCore.Qt.Key_R, "ctrl": True},
        Hotkeys.SelectPerimeter: {"key": QtCore.Qt.Key_T, "ctrl": True},
        Hotkeys.SelectShell: {"key": QtCore.Qt.Key_A, "ctrl": True, "shift": True},
        Hotkeys.ToggleInfLock: {"key": QtCore.Qt.Key_Space},
        Hotkeys.ToggleInfLock2: {"key": QtCore.Qt.Key_L}
    }

    def __init__(self, caption, key, func, ctrl=False, shift=False, alt=False):
        self.caption = caption
        self.key = key
        self.func = func
        self.ctrl = ctrl
        self.shift = shift
        self.alt = alt

    @staticmethod
    def serialize_key_event(key_event):
        modifiers = key_event.modifiers()
        char = key_event.text()

        # Only include shift for alphabetical characters or it won't work.
        return {
            "shift": char.lower() != char and (QtCore.Qt.SHIFT & modifiers > 0),
            "ctrl": QtCore.Qt.CTRL & modifiers > 0,
            "alt": QtCore.Qt.ALT & modifiers > 0,
            "key": key_event.key()
        }

    @classmethod
    def create_from_default(cls, caption, func):
        if caption not in cls.Defaults:
            raise ValueError("{cap} is not a default shortcut".format(cap=caption))

        return cls(
            caption,
            cls.Defaults[caption]["key"],
            func,
            cls.Defaults[caption].get("ctrl", False),
            cls.Defaults[caption].get("shift", False),
            cls.Defaults[caption].get("alt", False)
        )

    def key_code(self):
        ctrl = QtCore.Qt.CTRL if self.ctrl else 0
        shift = QtCore.Qt.SHIFT if self.shift else 0
        alt = QtCore.Qt.ALT if self.alt else 0
        return self.key | ctrl | shift | alt

    def key_to_string(self):
        ctrl = "Ctrl" if self.ctrl else None
        shift = "Shift" if self.shift else None
        alt = "Alt" if self.alt else None
        key = QtGui.QKeySequence(self.key).toString()
        return " + ".join(filter(None, [ctrl, shift, alt, key]))

    def matches(self, other_hotkey):
        return (
            other_hotkey.shift == self.shift and
            other_hotkey.ctrl == self.ctrl and
            other_hotkey.alt == self.alt and
            other_hotkey.key == self.key
        )

    def reset_to_default(self):
        if self.caption not in self.__class__.Defaults:
            return

        values = self.__class__.Defaults[self.caption]

        self.key = values["key"]
        self.ctrl = values.get("ctrl", False)
        self.shift = values.get("shift", False)
        self.alt = values.get("alt", False)

    def serialize(self):
        return {
            self.caption: {
                "key": int(self.key),
                "ctrl": self.ctrl,
                "shift": self.shift,
                "alt": self.alt
            }
        }

    def copy(self):
        return Hotkey(
            self.caption,
            self.key,
            self.func,
            ctrl=self.ctrl,
            shift=self.shift,
            alt=self.alt
        )
