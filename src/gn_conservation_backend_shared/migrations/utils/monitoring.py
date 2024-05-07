from alembic import op
import sqlalchemy.sql as text


def delete_sites(module_code):
    operation = text(
        """
        -- Create temporary table to keep in memory all the sites linked to module
        CREATE TEMPORARY TABLE sites_module(
        gid serial4 NOT NULL,
        id_base_site int4 NOT NULL,
        id_module int4 NOT NULL
        );

        -- Insert all sites linked to module
        INSERT INTO sites_module(id_base_site, id_module)
        SELECT 
            csm.id_base_site,
            csm.id_module
        FROM gn_monitoring.cor_site_module csm
        JOIN gn_commons.t_modules tm
            ON tm.id_module = csm.id_module
        WHERE tm.module_code = :moduleCode
        ;

        -- Unlink sites from module
        DELETE FROM gn_monitoring.cor_site_module
            WHERE id_module = (
                SELECT id_module
                FROM gn_commons.t_modules
                WHERE module_code = :moduleCode
            ) ;

        -- Delete sites
        DELETE from gn_monitoring.t_base_sites WHERE id_base_site IN (
            SELECT sm.id_base_site
            FROM gn_monitoring.cor_site_module  csm
            LEFT JOIN sites_module sm
                ON csm.id_base_site = sm.id_base_site
            WHERE csm.id_base_site = sm.id_base_site
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