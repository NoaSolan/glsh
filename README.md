# Feature Selection and Processing with ArcPy

This Python script uses the ArcPy library to perform feature selection and processing on spatial data within a Geographic Information System (GIS). It contains various classes and methods for finding, selecting, and creating new feature classes based on different criteria.

## Requirements

- ArcPy: Ensure that you have ArcPy installed, which is a Python library that provides access to various geoprocessing tools in ArcGIS.

## Code Structure

The code is structured into several classes, each with specific functionality:

### Params Class

The `Params` class is responsible for storing the paths to input feature classes and workspace directories. It is used to define the source and target paths for various GIS operations.

### FindFeatures Class

- This is an abstract base class (`ABC`) that other feature-finding classes inherit from.
- It initializes feature class names, selection, and feature layers for input datasets.
- Contains an abstract method `find_features()` that must be implemented in subclasses.
- Provides a `create_feature_class()` method to create new feature classes based on feature selection.

### FindRenewingFeatures Class

- Subclass of `FindFeatures`.
- Finds and selects features that need to be renewed by performing a location-based selection.
- Defines the feature class name as 'renewing_features'.

### FindFeaturesWithOverlapPercentage Class

- Subclass of `FindFeatures`.
- Takes a bilateral overlap feature class as input and performs selection based on a query.
- Initializes the bilateral overlap feature layer.
- Provides a method to select features based on overlap percentage criteria.
- Subclasses `FindReplacingFeatures` and `FindDeletingFeatures` use this class as a base for their functionality.

### FindReplacingFeatures Class

- Subclass of `FindFeaturesWithOverlapPercentage`.
- Implements a specific query to select features that meet replacement criteria.
- Defines the feature class name as 'replacing_features'.

### FindDeletingFeatures Class

- Subclass of `FindFeaturesWithOverlapPercentage`.
- Implements a specific query to select features that meet deletion criteria.
- Defines the feature class name as 'deleting_features'.

## Running the Script

1. Ensure that ArcPy is available and properly configured.
2. Define the paths to your input feature classes and the workspace in the `Params` class.
3. Run the script to perform the following operations:
   - Find bilateral overlap features by calling the `find_bilateral_overlap` function.
   - Find and create 'renewing_features' based on location-based selection.
   - Find and create 'replacing_features' based on overlap percentage criteria.
   - Find and create 'deleting_features' based on overlap percentage criteria.

## Additional Notes

- Make sure to customize the paths, queries, and criteria as per your specific GIS data and requirements.
- The script demonstrates how to use ArcPy geoprocessing tools to select, create, and manage feature classes within the ArcGIS environment.

Happy geospatial analysis!
