# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2013 OpenStack Foundation
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
# @author Sean M. Collins (Comcast)

"""Add subnet_mode property

Revision ID: 2447ad0e9585
Revises: e197124d4b9
Create Date: 2013-10-23 16:36:44.188904

"""

# revision identifiers, used by Alembic.
revision = '2447ad0e9585'
down_revision = '50e86cb2637a'

# Change to ['*'] if this migration applies to all plugins

migration_for_plugins = [
    '*'
]

from alembic import op
import sqlalchemy as sa


from neutron.common import constants
from neutron.db import migration


def upgrade(active_plugins=None, options=None):
    if not migration.should_run(active_plugins, migration_for_plugins):
        return

    op.create_table('dhcp_modes',
                    sa.Column('id', sa.String(36), primary_key=True),
                    sa.Column('subnet_id', sa.String(36),
                              sa.ForeignKey('subnets.id', ondelete='CASCADE')),
                    sa.Column('mode',
                              sa.Enum(constants.DHCP_V6_MODE_SLAAC,
                                      constants.DHCP_V6_MODE_RANAME,
                                      constants.DHCP_V6_MODE_RAONLY,
                                      constants.DHCP_MODE_STATIC,
                                      constants.DHCP_V6_MODE_RASTATELESS,
                                      name='dhcp_mode_choices'))

                    )
    ## Insert rows into dhcp_modes for existing subnets
    op.execute("INSERT INTO dhcp_modes SELECT id, id as subnet_id,"
               "'static' as mode FROM subnets")
    pass


def downgrade(active_plugins=None, options=None):
    if not migration.should_run(active_plugins, migration_for_plugins):
        return

    op.drop_table('dhcp_modes')
    pass
