from typing import List

from alembic import op
import sqlalchemy as sa


def add_nomenclature_type(mnemonic: str, label: str, definition: str, source: str):
    operation = sa.sql.text(
        """
        INSERT INTO ref_nomenclatures.bib_nomenclatures_types (
            mnemonique,
            label_default,
            definition_default,
            label_fr,
            definition_fr,
            source
        ) VALUES (
            :mnemonic,
            :label,
            :definition,
            :label,
            :definition,
            :source
        );
        """
    )
    op.get_bind().execute(
        operation,
        {
            "mnemonic": mnemonic,
            "label": label,
            "definition": definition,
            "source": source,
        },
    )


def delete_nomenclatures_by_type(mnemonique: str):
    operation = sa.sql.text(
        """
        DELETE FROM ref_nomenclatures.t_nomenclatures
        WHERE id_type = (
            SELECT id_type
            FROM ref_nomenclatures.bib_nomenclatures_types
            WHERE mnemonique = :mnemonique
        );

        DELETE FROM ref_nomenclatures.bib_nomenclatures_types
        WHERE mnemonique = :mnemonique
        """
    )
    op.get_bind().execute(operation, {"mnemonique": mnemonique})


def delete_nomenclatures(type_mnemonique: str, cd_nomenclature_list: List[str]):
    operation = sa.sql.text(
        """
        DELETE FROM ref_nomenclatures.t_nomenclatures
        WHERE id_type = (
            SELECT id_type
            FROM ref_nomenclatures.bib_nomenclatures_types
            WHERE mnemonique = :typeMnemonique
        )
            AND cd_nomenclature IN :cdNomenclatureList;
        """
    )
    op.get_bind().execute(
        operation,
        {
            "typeMnemonique": type_mnemonique,
            "cdNomenclatureList": cd_nomenclature_list,
        },
    )
