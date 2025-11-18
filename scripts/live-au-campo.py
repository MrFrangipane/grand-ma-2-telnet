import logging
import os.path
import sys

from grandma2telnet.lib import MAConsole, MAConsoleSelectionInfo, MAInstallationStore


def import_xml_from_capture(console_selection_info):
    installation_store = MAInstallationStore()
    installations = installation_store.list_installations()

    with MAConsole(console_selection_info) as ma_console:
        ma_console.set_installation(installations[-1])
        ma_console.delete_all_layers()
        ma_console.import_fixtures(filepath=os.path.join(root, "live-au-campo.xml"))


def export_xml_for_capture(console_selection_info):
    installation_store = MAInstallationStore()
    installations = installation_store.list_installations()

    with MAConsole(console_selection_info) as ma_console:
        ma_console.set_installation(installations[-1])
        ma_console.export_fixtures(filepath=os.path.join(root, "live-au-campo-for-capture.xml"))


def import_fixtures_types(console_selection_info):
    installation_store = MAInstallationStore()
    installations = installation_store.list_installations()

    with MAConsole(console_selection_info) as ma_console:
        ma_console.set_installation(installations[-1])
        ma_console.import_fixture_type(os.path.join(root, "beamz@nereid380b_outdoor@18_channels.xml"))
        ma_console.import_fixture_type(os.path.join(root, "beamz@sb220ip_stage@4_channels.xml"))
        ma_console.import_fixture_type(os.path.join(root, "beamz_professional@nuke3@25ch_mode.xml"))


if __name__ == '__main__':
    root = sys.argv[1]
    logging.basicConfig(level=logging.INFO)

    local_console = MAConsoleSelectionInfo(host='127.0.0.1', username='administrator', password='admin')

    # import_fixtures_types(local_console)
    # import_xml_from_capture(local_console)
    export_xml_for_capture(local_console)
