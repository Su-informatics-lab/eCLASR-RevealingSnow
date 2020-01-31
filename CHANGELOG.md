# Revealing Snow Change Log

## [Unreleased]

### Added

* Added a filter indicating whether a patient was in a previous export batch.

### Changed

* Updated the data version in the model.
* Corrected the vitals item description to remove BMI.


## [2019.5.1] - 2020-01-09

### Added

* Added the Thomasville site.

### Changed

* Updated descriptions in the data model to reflect POINTER Protocol v2.0.

## [2019.5.0] - 2019-12-31

### Changed

* Relabeled "Unfiltered" and "Filtered" to "Overall" and "Eligible."
* Added support for data files without the redundant "_date" columns, such
  as those produced by v4 of the phenotyping algorithm.

### Fixed

* Icons in the filter legend popover appear again.

## [2019.4.0] - 2019-09-26

### Added

* Added the High Point Medical Center fitness center.

## [2019.3.0] - 2019-08-28

### Added

* Added the Lexington J. Smith Young YMCA.

## [2019.2.0] - 2019-06-06

### Changed

* Updated the model to use the v3 screening criteria.
* Default dates are now relative to the 2019-04-01 reference date.
* Range filters (e.g. age) now support non-integer values.
* Exclusion filters now specifically exclude patients with condition = 1
  rather than requiring condition = 0. This ensures empty/unknown condition
  values are not excluded.

## [2019.1.0] - 2019-02-15

### Added

* The YMCA site distance filters now support specifying a minimum distance.

## [2018.6.2] - 2019-01-03

### Added

* The download and export payload now includes the data version string.

### Changed

* Changed distance cutoffs to use <= instead of <.
* Updated the data model to allow newer versions of the screening data to be used.

## [2018.6] - 2018-12-28

### Added

* The export dialog now has a field for user name.
* The app can now be built and distributed as a standalone Windows app.

### Changed

* Exporting to remote tracking is now a toggleable feature. It defaults to being turned off.

### Fixed

* Removed the artificial max of 1000 from the limit field in the filter bar.


## [2018.5] - 2018-12-14

### Added

* Metadata from previous exports can now be re-imported.
* Added age to the available filter criteria.

### Fixed

* Sequential load and unload of chart data results in incorrect chart appearance.


## [2018.4] - 2018-10-17

### Added

* Value tooltips now include percentages.
* Data exports now support labels and descriptions.
* Patient subsetting also supports ordering by YMCA distance.

### Changed

* Charts have more complete annotations.


## [2018.3] - 2018-10-03

### Added

* Data can now be exported to the remote mail tracking system in addition to downloading locally.
* The set of patients downloaded/exported can now be limited and sorted by last visit date.

### Fixed

* Inconsistent color scheme when groups are different between charts.
* Demographic charts don't update when categories are empty.


## [2018.2] - 2018-09-07

### Added

* Metadata and YMCA site cutoffs are included in exported data.
* Added a legend to explain inclusion/exclusion/ignore icons.
* Demographic data are now included among the YMCA site charts.

### Changed

* Modifications to filter or site criteria are now applied automatically.
* Filter criteria are now three-way checkboxes.
* Cutoff dates can now be entered by keyboard.

### Fixed

* Distances are now rounded correctly.
* Filter controls are no longer unclickable on narrow screens.


## [2018.1] - 2018-05-18

* Initial Release
