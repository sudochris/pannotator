import PySimpleGUI as sg
import ui_keys as uk
from input_output.api_facade import ManagerFacade
from ui_components.class_list import ClassList
from ui_components.events_list import EventsList
from ui_components.image_display import ImageDisplay
from ui_components.menus import MainMenu
from ui_components.toolbar import Toolbar
from input_output.argument_parser import StringOption, application_settings_from_args, ApplicationSettings


if __name__ == '__main__':
    # Define application arguments
    argument_options = [
        StringOption("project_folder", "Project Folder (default: ./)", "./"),
    ]
    # Set the applications theme
    # sg.theme('Material2')
    sg.theme('Default1')

    # Load command line parameters
    app_settings = application_settings_from_args(argument_options)

    # Setup all application managers
    api = ManagerFacade(app_settings)

    # Create UI components
    main_menu = MainMenu(api)
    toolbar = Toolbar(api)
    image_display = ImageDisplay(api)
    class_list = ClassList(api)
    events_list = EventsList(api)

    # Build window layout
    main_menu_layout = main_menu.get_layout()
    toolbar_layout = toolbar.get_layout()
    image_display_layout = image_display.get_layout()
    class_list_layout = class_list.get_layout()
    events_list_layout = events_list.get_layout()

    right_column_layout = [
        [sg.TabGroup([[sg.Tab("Classes", class_list_layout), sg.Tab("Events", events_list_layout)]])]]

    layout = [[sg.Menu(main_menu_layout)],
        [sg.Column(toolbar_layout), sg.VerticalSeparator(), sg.Column(image_display_layout), sg.VerticalSeparator(), sg.Column(right_column_layout)]]

    # Create window with layout
    window = sg.Window("PANNotator",
                       layout,
                       size=(1800, 900),font=32,
                       return_keyboard_events=True,
                       finalize=True)

    image_graph: sg.Graph = window[uk.IMAGE_GRAPH]
    image_display.process_event(window, uk.NEXT_IMAGE, {})

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event.endswith(uk.MENU_FILE_EXIT):
            break

        main_menu.process_event(window, event, values)
        toolbar.process_event(window, event, values)
        image_display.process_event(window, event, values)

        class_list.process_event(window, event, values)
        events_list.process_event(window, event, values)

        toolbar.selected_tool.draw(image_graph)

    window.close()
