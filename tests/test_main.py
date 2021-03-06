from os.path import join

import pytest
from hdx.hdx_configuration import Configuration
from hdx.hdx_locations import Locations
from hdx.location.country import Country
from hdx.utilities.compare import assert_files_same
from hdx.utilities.downloader import Download
from hdx.utilities.path import temp_dir

from model.main import get_indicators
from utilities.jsonoutput import jsonoutput
from utilities.nooutput import nooutput


class TestCovid:
    @pytest.fixture(scope='function')
    def configuration(self):
        Configuration._create(hdx_read_only=True, hdx_site='prod', user_agent='test',
                              project_config_yaml=join('tests', 'config', 'project_configuration.yml'))
        Locations.set_validlocations([{'name': 'afg', 'title': 'Afghanistan'}, {'name': 'pse', 'title': 'State of Palestine'}])
        Country.countriesdata(use_live=False)
        return Configuration.read()

    @pytest.fixture(scope='function')
    def folder(self):
        return join('tests', 'fixtures')

    def test_get_indicators(self, configuration, folder):
        with temp_dir('TestCovidViz') as tempdir:
            with Download(user_agent='test') as downloader:
                tabs = configuration['tabs']
                noout = nooutput(tabs)
                jsonout = jsonoutput(configuration, tabs)
                outputs = {'gsheets': noout, 'excel': noout, 'json': jsonout}
                get_indicators(configuration, downloader, outputs, tabs, scrapers=['ifi', 'who', 'covid_trend'])
                filepath = jsonout.save(tempdir)
                assert_files_same(filepath, join(folder, 'test_tabular.json'))
