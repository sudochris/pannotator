import PySimpleGUI as sg
def get_or_default(lst, index, default = None):
    return lst[index] if index < len(lst) else default

def strip_all(value:str):
    return value.replace(" ", "")

def is_emtpy(value:str):
    return strip_all(value) == ""


def draw_rectangle(overlay: sg.Graph, top_left, bottom_right, line_color="#000000", line_width=1):
    overlay.draw_rectangle(top_left, bottom_right, line_color=line_color, line_width=line_width)

def draw_oval(overlay: sg.Graph, top_left, bottom_right, line_color="#000000", line_width=1):
    overlay.draw_oval(top_left, bottom_right, line_color=line_color, line_width=line_width)


def draw_cross(overlay: sg.Graph, center, size, line_color="#000000", line_width=1):
    overlay.draw_line([center[0] - size[0], center[1] - size[1]],
                      [center[0] + size[0], center[1] + size[1]],
                      color=line_color, width=line_width)
    overlay.draw_line([center[0] - size[0], center[1] + size[1]],
                      [center[0] + size[0], center[1] - size[1]],
                      color=line_color, width=line_width)

    pass