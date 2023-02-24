from alembic import op
import sqlalchemy.sql as text


def delete_sites(module_code):
    operation = text(
        """
        -- Unlink sites from module
        DELETE FROM gn_monitoring.cor_site_module
            WHERE id_module = (
                SELECT id_module
                FROM gn_commons.t_modules
                WHERE module_code = :moduleCode
            ) ;

        -- Delete sites
        DELETE from gn_monitoring.t_base_sites WHERE id_base_site IN (
            SELECT id_base_site
            FROM pr_monitoring_habitat_station.t_transects
        ) ;
        """
    )
    op.get_bind().execute(operation, {"moduleCode": module_code})


def delete_visits_by_dataset(dataset_code):
    operation = text(
        """
        DELETE from gn_monitoring.t_base_visits WHERE id_dataset = (
            SELECT id_dataset
            FROM gn_meta.t_datasets
            WHERE dataset_shortname = :metadataCode
            LIMIT 1
        );
        """
    )
    op.get_bind().execute(operation, {"metadataCode": dataset_code})