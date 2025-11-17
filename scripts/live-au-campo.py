from pprint import pprint
import logging
import os.path
import sys

from grandma2telnet.lib import MA


if __name__ == '__main__':
    root = sys.argv[1]

    logging.basicConfig(level=logging.INFO)

    with MA(host='127.0.0.1', username='administrator', password='admin') as ma_console:

        ma_console.set_installation(ma_console.installations[-1])
        #
        # ma_console.import_fixture_type(os.path.join(root, "beamz@nereid380b_outdoor@18_channels.xml"))
        # ma_console.import_fixture_type(os.path.join(root, "beamz@sb220ip_stage@4_channels.xml"))
        # ma_console.import_fixture_type(os.path.join(root, "beamz_professional@nuke3@25ch_mode.xml"))
        #
        ma_console.delete_all_layers()
        ma_console.import_fixtures(filepath=os.path.join(root, "live-au-campo.xml"))

        # TODO make a Layer object with fixtures() method ?
        layers = ma_console.list_layers()
        pprint(ma_console.list_fixtures(layer_id=1))
        #
        # fixtures = ma_console.list_fixtures(layer_id=2)
        # pprint(fixtures)
        #
        # ma_console.set_fixture_type(
        #     layer_id=2,
        #     fixture_type_id=3,
        #     fixture_first=1,
        #     fixture_last=len(fixtures)
        # )
        #
        # fixtures = ma_console.list_fixtures(layer_id=2)
        # pprint(fixtures)
