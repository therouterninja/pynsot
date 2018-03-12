# -*- coding: utf-8 -*-

"""
Test Circuits in the CLI app.
"""

from __future__ import absolute_import, unicode_literals
import logging

import pytest

from tests.fixtures import (attribute, attributes, client, config, device,
                            interface, network, protocol, protocol_type, site, site_client)

from tests.fixtures.circuits import circuit

from tests.util import CliRunner, assert_output

log = logging.getLogger(__name__)


def test_protocol_types_add(site_client):
    """Test ``nsot protocol_types add``."""

    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        # Add a protocol_type by name.
        result = runner.run(
            "protocol_types add -n bgp"
        )
        assert result.exit_code == 0
        assert 'Added protocol_type!' in result.output

        # Verify addition.
        result = runner.run('protocol_types list')
        assert result.exit_code == 0
        assert 'bgp' in result.output
        assert '1' in result.output

        # Add a protocol with same name and fail.
        result = runner.run(
            "protocol_types add -n bgp"
        )
        expected_output = 'The fields site, name must make a unique set.'
        assert result.exit_code != 0
        assert expected_output in result.output

        # Add second protocol_type by name.
        result = runner.run(
            "protocol_types add -n ospf -e 'OSPF is the best'"
        )
        assert result.exit_code == 0
        assert 'Added protocol_type!' in result.output

        # Verify default site is assigned and verify description..
        result = runner.run('protocol_types list -I 2')
        assert result.exit_code == 0
        assert '1' in result.output
        assert 'OSPF is the best' in result.output


def test_protocol_types_list(site_client, protocol_type):
    """Test ``nsot protocol_types list``"""

    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        # Basic List.
        result = runner.run('protocol_types list')
        assert result.exit_code == 0
        assert protocol_type['name'] in result.output

        # Test -n/--name
        result = runner.run('protocol_types list -n %s' % protocol_type['name'])
        assert result.exit_code == 0
        assert protocol_type['name'] in result.output

        # Test -s/--site
        result = runner.run('protocol_types list -s %s' % protocol_type['site'])
        assert result.exit_code == 0
        assert protocol_type['name'] in result.output

        # Test -I/--id
        result = runner.run('protocol_types list -I %s' % protocol_type['id'])
        assert result.exit_code == 0
        assert protocol_type['name'] in result.output

def test_protocol_types_update(site_client, protocol_type):
    """Test ``nsot protocol_types update``"""

    pt_id = protocol_type['id']
    pt_site = protocol_type['site']

    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        # Try to change the name
        result = runner.run(
            'protocol_types update -n Cake -I %s -s %s' % (pt_id, str(pt_site))
        )
        assert result.exit_code == 0
        assert 'Updated protocol_type!' in result.output

        # Update the description
        result = runner.run(
            'protocol_types update -e Rise -I %s -s %s' % (pt_id, str(pt_site))
        )
        assert result.exit_code == 0
        assert 'Updated protocol_type!' in result.output

        # Assert the Cake Rises
        result = runner.run('protocol_types list -I %s' % pt_id)
        assert result.exit_code == 0
        assert 'Cake'  in result.output
        assert 'Rise' in result.output


def test_protocol_types_remove(site_client, protocol_type):
    """Test ``nsot protocol_types remove``"""

    runner = CliRunner(site_client.config)
    with runner.isolated_filesystem():
        result = runner.run(
            'protocol_types remove -I %s -s %s' % (protocol_type['id'], protocol_type['site'])
        )
        assert result.exit_code == 0
        assert 'Removed protocol_type!' in result.output
