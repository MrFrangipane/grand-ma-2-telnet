from grandma2telnet.lib import MA


if __name__ == '__main__':
    ma_console = MA(host='127.0.0.1')
    ma_console.connect(username='administrator', password='admin')
    ma_console.set_version(ma_console.versions[-1])

    ma_console.import_fixture_type("C:\\Users\\Ourson\\PROJETS\\live-au-campo\\beamz@nereid380b_outdoor@18_channels.xml")
    ma_console.import_fixture_type("C:\\Users\\Ourson\\PROJETS\\live-au-campo\\beamz@sb220ip_stage@4_channels.xml")
    ma_console.import_fixture_type("C:\\Users\\Ourson\\PROJETS\\live-au-campo\\beamz_professional@nuke3@25ch_mode.xml")

    ma_console.import_fixtures(filepath="C:\\Users\\Ourson\\PROJETS\\live-au-campo\\live-au-campo.xml")

    ma_console.disconnect()
