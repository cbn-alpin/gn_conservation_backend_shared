"""Add nomenclatures shared in conservation modules

Revision ID: 0a97fffb151c
Revises: None
Create Date: 2022-06-14 11:30:26.775634

"""
import importlib

from utils_flask_sqla.migrations.utils import logger

from gn_conservation_backend_shared.migrations.utils import csv, nomenclatures


# revision identifiers, used by Alembic.
revision = "0a97fffb151c"
down_revision = None
branch_labels = "nomenclatures_shared_in_conservation_modules"
depends_on = ("96a713739fdd",)  # nomenclatures_inpn_data


def upgrade():
    nomenclatures.add_nomenclature_type(
        mnemonic="TYPE_PERTURBATION",
        label="Type de perturbations",
        definition="Nomenclatures des perturbations des milieux naturels.",
        source="CBNA",
    )
    # WARNING: do not add "TYPE_SITE" it's already imported by nomenclatures_inpn_data branch.

    with importlib.resources.open_text(
        "gn_conservation_backend_shared.migrations.data", "nomenclatures.csv"
    ) as csvfile:
        logger.info("Inserting perturbations and others Conservation nomenclatures…")
        csv.copy_from_csv(
            csvfile,
            "ref_nomenclatures",
            "t_nomenclatures",
            dest_cols=(
                "id_type",
                "cd_nomenclature",
                "mnemonique",
                "label_default",
                "definition_default",
                "label_fr",
                "definition_fr",
                "id_broader",
                "hierarchy",
            ),
            source_cols=(
                "ref_nomenclatures.get_id_nomenclature_type(type_nomenclature_code)",
                "cd_nomenclature",
                "mnemonique",
                "label_default",
                "definition_default",
                "label_fr",
                "definition_fr",
                "ref_nomenclatures.get_id_nomenclature(type_nomenclature_code, cd_nomenclature_broader)",
                "hierarchy",
            ),
            header=True,
            encoding="UTF-8",
            delimiter=",",
        )


def downgrade():
    nomenclatures.delete_nomenclatures_by_type("TYPE_PERTURBATION")
    nomenclatures.delete_nomenclatures("TYPE_SITE", ("HAB", "ZP"))
