from alembic import op
import sqlalchemy.sql as text


def update_module(code: str, label: str, description: str, doc_url: str):
    operation = text(
        """
        UPDATE gn_commons.t_modules
        SET
            module_label = :label,
            module_desc = :description,
            module_doc_url = :docUrl
        WHERE module_code = :code ;
        """
    )
    op.get_bind().execute(
        operation,
        {
            "code": code,
            "label": label,
            "description": description,
            "docUrl": doc_url,
        },
    )


def delete_module(code: str):
    operation = text(
        """
        -- Unlink module from dataset
        DELETE FROM gn_commons.cor_module_dataset
            WHERE id_module = (
                SELECT id_module
                FROM gn_commons.t_modules
                WHERE module_code = :code
            ) ;

        -- Uninstall module (unlink this module of GeoNature)
        DELETE FROM gn_commons.t_modules
            WHERE module_code = :code ;
        """
    )
    op.get_bind().execute(operation, {"code": code})
