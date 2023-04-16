from N10X import Editor

g_FsCurScroll:int = -1
g_FsTargetScroll:int = -1
g_FsScrollSpeed:int = 0
FASTSCROLL_PAGE_SIZE:int = 15
FASTSCROLL_SCROLL_SPEED:int = 4

def FastScrollDown():
    global g_FsCurScroll, g_FsTargetScroll, g_FsScrollSpeed
    if g_FsScrollSpeed == 0:
        col, line = Editor.GetCursorPos()
        g_FsCurScroll = line
        g_FsTargetScroll = g_FsCurScroll + FASTSCROLL_PAGE_SIZE
        g_FsScrollSpeed = FASTSCROLL_SCROLL_SPEED

def FastScrollUp():
    global g_FsCurScroll, g_FsTargetScroll, g_FsScrollSpeed
    if g_FsScrollSpeed == 0:
        col, line = Editor.GetCursorPos()
        g_FsCurScroll = line
        g_FsTargetScroll = g_FsCurScroll - FASTSCROLL_PAGE_SIZE
        g_FsScrollSpeed = -FASTSCROLL_SCROLL_SPEED


def _FastScrollUpdate():
    global g_FsCurScroll, g_FsTargetScroll, g_FsScrollSpeed
    if g_FsScrollSpeed != 0:
        g_FsCurScroll = g_FsCurScroll + g_FsScrollSpeed
        if g_FsScrollSpeed > 0:
            g_FsCurScroll = g_FsTargetScroll if g_FsCurScroll > g_FsTargetScroll else g_FsCurScroll
        elif g_FsScrollSpeed < 0:
            g_FsCurScroll = g_FsTargetScroll if g_FsCurScroll < g_FsTargetScroll else g_FsCurScroll

        Editor.SetScrollLine(g_FsCurScroll)
        if g_FsCurScroll == g_FsTargetScroll:
            Editor.CenterViewAtLinePos(g_FsTargetScroll)
            Editor.SetCursorPos((0, g_FsTargetScroll))
            g_FsScrollSpeed = 0
    
Editor.AddUpdateFunction(_FastScrollUpdate)
