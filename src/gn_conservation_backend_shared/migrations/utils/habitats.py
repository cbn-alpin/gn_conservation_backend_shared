from alembic import op
import sqlalchemy.sql as text


def add_habitats_list(habitat_list_name: str):
    operation = text(
        """
        INSERT INTO ref_habitats.bib_list_habitat (list_name)
        VALUES (:habitatListName) ;
        """
    )
    op.get_bind().execute(operation, {"habitatListName": habitat_list_name})


def delete_habitats_list(habitat_list_name: str):
    operation = text(
        """
        DELETE FROM ref_habitats.cor_list_habitat WHERE id_list IN (
            SELECT id_list
            FROM ref_habitats.bib_list_habitat
            WHERE list_name = :habitatListName
        ) ;

        DELETE FROM ref_habitats.bib_list_habitat
            WHERE list_name = :habitatListName ;
        """
    )
    op.get_bind().execute(operation, {"habitatListName": habitat_list_name})
