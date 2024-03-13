# CHANGELOG

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.5.1] - 2024-03-13

### Changed

- Minimum version of sqlalchemy (v2.0)

## [0.5.0] - 2023-02-24

### Added

- Added utility functions for webservices: debug, prepare output and input.
- Added utility functions to migrate data to module, habitat, monitoring and nomenclatures.
- Added utility functions to use CSV files to import data into the database.

### Changed

- Using utility functions in migration revision files.

### Remove

- Remove `STRATE_PLACETTE` and `POSITION_PLACETTE` nomenclatures. Move directly to Monitoring Habitat Station.

## [0.4.0] - 2022-08-10

### Added

- Add `STRATE_PLACETTE` and `POSITION_PLACETTE` nomenclatures.

## [0.3.1] - 2022-08-08

### Fixed

- Use correct schema name (`ref_geo`) in "`add_M25m_mesh`", "`add_M50m_mesh`" and
  "`add_M100m_mesh`" branches.

## [0.3.0] - 2022-08-05

### Changed

- Set values for the `cd_nomenclature_broader` and `hierarchy` fields to the `HAB` and `ZP`
  values of the `TYPE_SITE` nomenclature.

## [0.2.0] - 2022-08-04

### Added

- Add Alembic branches "`add_M25m_mesh`", "`add_M50m_mesh`", "`add_M100m_mesh`" to GeoNature.

## [0.1.0] - 2022-08-03

### Added

- First release.
- Add Alembic branche "`nomenclatures_shared_in_conservation_modules`" to GeoNature.
- Add `TYPE_PERTURBATION` nomenclatures shared by GeoNature conservation modules.
- Add 2 values (`HAB`, `ZP`) to `TYPE_SITE` nomenclature.
  ]
