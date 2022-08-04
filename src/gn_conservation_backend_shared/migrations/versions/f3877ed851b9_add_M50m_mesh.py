"""Add nomenclatures shared in conservation modules

Revision ID: f3877ed851b9
Revises: None
Create Date: 2022-08-04 11:30:26.775634

"""
import importlib
from csv import DictReader
from io import TextIOWrapper

from alembic import op
import sqlalchemy as sa

from utils_flask_sqla.migrations.utils import logger


# revision identifiers, used by Alembic.
revision = 'f3877ed851b9'
down_revision = None
branch_labels = "add_M50m_mesh"
depends_on = (
    "6afe74833ed0",  # ref_geo
)


def upgrade():

    op.execute(
        """
        INSERT INTO ref_geo.bib_areas_types (
            type_code,
            type_name,
            type_desc
        ) VALUES (
            'M50m',
            'Mailles50*50m',
            'Maille INPN redécoupé en 50m'
        ) ;
        """
    )

def downgrade():
    delete_mesh("M50m")


def delete_mesh(mesh_code):
    operation = sa.sql.text(
        """
        DELETE FROM ref_geo.l_areas
        WHERE id_type = (
            SELECT id_type
            FROM ref_nomenclatures.bib_areas_types
            WHERE type_code = :meshCode
        );

        DELETE FROM ref_geo.bib_areas_types
        WHERE type_code = :meshCode
        ;
        """
    )
    op.get_bind().execute(operation, {"meshCode": mesh_code})

