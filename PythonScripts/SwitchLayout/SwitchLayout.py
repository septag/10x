'''
Switch Layout 
Version: 0.1.0
'''
from enum import Enum, IntEnum
import win32gui, win32con

from N10X import Editor

class SL_WindowAlign(IntEnum):
    NONE = 0,
    RIGHT = 1
    LEFT = 2
    CENTER = 3

class SL_LayoutMode(IntEnum):
    SINGLE = 1
    DOUBLE = 2

class SL_Options():
    def translate_align(self, align:str):
        if not align:                   return SL_WindowAlign.NONE
        if align.upper() == 'RIGHT':    return SL_WindowAlign.RIGHT
        elif align.upper() == 'LEFT':   return SL_WindowAlign.LEFT
        elif align.upper() == 'CENTER': return SL_WindowAlign.CENTER
        else:                           return SL_WindowAlign.NONE

    def __init__(self):
        self.align_single = self.translate_align(Editor.GetSetting("SwitchLayout.AlignSingle"))
        self.align_double = self.translate_align(Editor.GetSetting("SwitchLayout.AlignDouble"))

_sl_hwnd = None
_sl_options:SL_Options = SL_Options()

def _SL_SetWindowWidth(width:int, mode:SL_LayoutMode):
    if not _sl_hwnd:
        return
        
    desktop_rect = win32gui.GetWindowRect(win32gui.GetDesktopWindow())
    desktop_x:int = desktop_rect[0] + 64 # taskbar area
    desktop_y:int = desktop_rect[1]
    desktop_width:int = desktop_rect[2] - desktop_x
    desktop_height:int = desktop_rect[3] - desktop_y
    if (width > desktop_width):
        width = desktop_width

    alignment:SL_WindowAlign = SL_WindowAlign.NONE
    if mode == SL_LayoutMode.SINGLE:   alignment = _sl_options.align_single
    elif mode == SL_LayoutMode.DOUBLE: alignment = _sl_options.align_double

    rect = win32gui.GetWindowRect(_sl_hwnd)
    x:int = rect[0]
    y:int = rect[1]
    height:int = rect[3] - y
    if height < desktop_height:
        height = desktop_height
    if alignment == SL_WindowAlign.RIGHT or x + width > desktop_rect[2]:
        x = desktop_rect[2] - width
    if alignment == SL_WindowAlign.CENTER:
        x = desktop_x + (desktop_width - width)/2
    if alignment == SL_WindowAlign.LEFT:
        x = desktop_x
    win32gui.MoveWindow(_sl_hwnd, int(x), y, width, height, True)

def SL_SwitchSingle():
    Editor.ExecuteCommand("SetColumnCount1")
    _SL_SetWindowWidth(1100, SL_LayoutMode.SINGLE)

def SL_SwitchDouble():
    Editor.ExecuteCommand("SetColumnCount2")
    _SL_SetWindowWidth(2000, SL_LayoutMode.DOUBLE)

def _SL_SettingsChanged():
    global _sl_options
    _sl_options = SL_Options()

def _SL_WorkspaceOpened():
    global _sl_hwnd
    _sl_hwnd = win32gui.GetActiveWindow()

Editor.AddOnSettingsChangedFunction(_SL_SettingsChanged)
Editor.AddOnWorkspaceOpenedFunction(_SL_WorkspaceOpened)



