import PySimpleGUI as sg
import json as json

import ui_keys as uk
from input_output.api_facade import ManagerFacade
from ui_components.component import UIComponent
import utils.utils as utils


class EventsList(UIComponent):

    def __init__(self, api: ManagerFacade) -> None:
        super().__init__()
        self.api = api
        self.event_list_path = self.api.event_list_path()

        self.eventgroup_data = self._load_events_list_from_file(self.api.event_list_path())

        groups = list(self.eventgroup_data.keys())
        selected_group = ""
        if len(groups) > 0:
            selected_group = groups[0]

        events_list = self.eventgroup_data.get(selected_group, [])

        self.eventgroup_combo = sg.InputCombo(groups, selected_group, size=(80, 1),
                                              enable_events=True,
                                              key=uk.EVENTS_GROUPCOMBO)
        self.eventlist_list = sg.Listbox(events_list,
                                         bind_return_key=True,
                                         select_mode=sg.SELECT_MODE_SINGLE, size=(80, 20),
                                         key=uk.EVENTS_EVENT_LIST)

        table_data = [["", ""]]

        self.event_table = sg.Table(table_data, ["Eventgroup", "Event"],
                                    justification="left",
                                    bind_return_key=True,
                                    num_rows=8,
                                    col_widths=[15, 15],
                                    auto_size_columns=False,
                                    key=uk.EVENTS_EVENT_TABLE)

    def _load_events_list_from_file(self, file_path):
        with open(file_path, 'r') as file:
            result: dict = json.load(file)
        return result.get("eventList", {})

    def _save_events_list_to_file(self, file_path, event_list):
        with open(file_path, 'w') as file:
            json.dump({"eventList": event_list}, file)

    def get_layout(self):

        layout = [
            [self.eventgroup_combo],
            [sg.T("Groupname:"), sg.In(key=uk.EVENTS_INPUT_GROUP)],
            [sg.B("+", size=(1,1), key=uk.EVENTS_ADD_GROUP), sg.B("-", size=(1,1), key=uk.EVENTS_REMOVE_GROUP)],
            [self.eventlist_list],
            [sg.T("Eventname:"), sg.In(key=uk.EVENTS_INPUT_EVENT)],
            [sg.B("+", size=(1, 1), key=uk.EVENTS_ADD_EVENT), sg.B("-", size=(1, 1), key=uk.EVENTS_REMOVE_EVENT)],
            [self.event_table]]

        return layout

    def _update_ui(self, selected_group):
        groups = list(self.eventgroup_data.keys())
        self.eventgroup_combo.update(value=selected_group, values=groups)

        events_list = self.eventgroup_data.get(selected_group, [])
        self.eventlist_list.update(events_list)




    def process_event(self, window, event, values):
        changed = False

        selected_groupname = values[uk.EVENTS_GROUPCOMBO]
        selected_event_name = utils.get_or_default(values[uk.EVENTS_EVENT_LIST], 0, "")
        selected_table_event = utils.get_or_default(values[uk.EVENTS_EVENT_TABLE], 0, None)

        if event == uk.EVENTS_GROUPCOMBO:
            changed = True

        if event == uk.EVENTS_ADD_GROUP:
            new_eventgroup_name = values[uk.EVENTS_INPUT_GROUP]
            if not new_eventgroup_name in self.eventgroup_data and not utils.is_emtpy(new_eventgroup_name):
                self.eventgroup_data.update({new_eventgroup_name: []})
                changed = True

        if event == uk.EVENTS_REMOVE_GROUP:
            if selected_groupname in self.eventgroup_data:
                self.eventgroup_data = {k:v for k, v in self.eventgroup_data.items() if k != selected_groupname}
                changed = True

        if event == uk.EVENTS_ADD_EVENT:
            event_name:str = values[uk.EVENTS_INPUT_EVENT]
            if not utils.is_emtpy(event_name):
                if selected_groupname in self.eventgroup_data:
                    if event_name not in self.eventgroup_data[selected_groupname]:
                        actual_group = self.eventgroup_data.get(selected_groupname, [])
                        actual_group.append(event_name)
                        changed = True

        if event == uk.EVENTS_REMOVE_EVENT:
            if selected_groupname in self.eventgroup_data:
                if selected_event_name in self.eventgroup_data[selected_groupname]:
                    actual_group = self.eventgroup_data.get(selected_groupname, [])
                    actual_group.remove(selected_event_name)
                    changed = True

        if event == uk.EVENTS_EVENT_LIST:
            if selected_event_name in self.eventgroup_data[selected_groupname]:
                success = self.api.insert_event(selected_groupname, selected_event_name)
                print(f"{success=}")
                if success:
                    changed = True # redraw

        if event == uk.EVENTS_EVENT_TABLE:
            if selected_table_event is not None:
                table_event_group, table_event = self.api.get_event_table()[selected_table_event]
                self.api.remove_event(table_event_group, table_event)

        if changed:
            self._update_ui(selected_groupname)
            self._save_events_list_to_file(self.event_list_path, self.eventgroup_data)


        event_table_data = self.api.get_event_table()
        self.event_table.update(event_table_data)

        pass
