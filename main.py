import abc
from abc import ABC
import arcpy

from bilateral_overlap import find_bilateral_overlap


# Class to store parameter values
class Params:
    def __init__(self):
        # Set the paths to input feature classes and workspace
        self.moria_buildings = r'C:\Users\amitv\Desktop\TONOA\bordered_data.gdb\B_BUILDINGS_A'
        self.bs_buildings = r'C:\Users\amitv\Desktop\TONOA\bordered_data.gdb\no_dupes_leb_new_new'
        self.workspace_source = r'C:\Users\amitv\Desktop\TONOA\workspace.gdb'
        self.target_source = r'C:\Users\amitv\Desktop\TONOA\target.gdb'


# Abstract base class for finding features
class FindFeatures(Params):
    def __init__(self):
        super().__init()
        self.fc_name = None
        self.selection = None
        # Create feature layers for the input feature classes
        self.bs_buildings_layer = arcpy.MakeFeatureLayer_management(self.bs_buildings, "bs_buildings_lyr")
        self.moria_buildings_layer = arcpy.MakeFeatureLayer_management(self.moria_buildings, "moria_buildings_lyr")

    @abc.abstractmethod
    def find_features(self):
        pass

    def create_feature_class(self):
        match_count = int(arcpy.management.GetCount(self.selection)[0])
        if not match_count:
            print(f'There aren\'t any {self.fc_name}')
        else:
            # Create a new feature class based on the selected features
            arcpy.FeatureClassToFeatureClass_conversion(self.bs_buildings_layer,
                                                        self.target_source, self.fc_name)


# Class for finding renewing features
class FindRenewingFeatures(FindFeatures, ABC):
    def __init__(self):
        super().__init()
        self.fc_name = 'renewing_features'

    def find_features(self):
        # Select features that intersect with another feature layer
        self.selection = arcpy.management.SelectLayerByLocation(self.bs_buildings_layer, "INTERSECT",
                                                                self.moria_buildings_layer, None, "NEW_SELECTION",
                                                                "INVERT")


# Class for finding features with overlap percentage
class FindFeaturesWithOverlapPercentage(FindFeatures, ABC):
    def __init__(self, bilateral_overlap):
        super().__init()
        self.query = None
        self.bilateral_overlap = bilateral_overlap
        # Create a feature layer for bilateral overlap data
        self.bilateral_overlap_layer = arcpy.MakeFeatureLayer_management(self.bilateral_overlap,
                                                                         "bilateral_overlap_lyr")

    def find_features(self):
        arcpy.env.overwriteOutput = True

        # Select features based on a query and create a new feature class
        selection = arcpy.management.SelectLayerByAttribute(self.bilateral_overlap_layer, "NEW_SELECTION", self.query)
        match_count = int(arcpy.management.GetCount(selection)[0])
        if match_count:
            selection_layer = arcpy.FeatureClassToFeatureClass_conversion(self.bilateral_overlap_layer,
                                                                          self.workspace_source,
                                                                          'bilateral_overlap_selection_lyr')
            # Select features that intersect with the newly created selection layer
            self.selection = arcpy.management.SelectLayerByLocation(self.bs_buildings_layer,
                                                                    "INTERSECT", selection_layer)


# Class for finding replacing features
class FindReplacingFeatures(FindFeaturesWithOverlapPercentage, ABC):
    def __init__(self, bilateral_overlap):
        super().__init__(bilateral_overlap)
        self.fc_name = 'replacing_features'
        self.query = "PERCENTAGE_1 >= 70 And PERCENTAGE_2 >= 70"


# Class for finding deleting features
class FindDeletingFeatures(FindFeaturesWithOverlapPercentage, ABC):
    def __init__(self, bilateral_overlap):
        super().__init__(bilateral_overlap)
        self.fc_name = 'deleting_features'
        self.query = "PERCENTAGE_1 <= 10 And PERCENTAGE_2 <= 10"


if __name__ == '__main':
    params = Params()

    # Find bilateral overlap features by calling the `find_bilateral_overlap` function
    bilateral_overlap = find_bilateral_overlap(params.moria_buildings,
                                               params.bs_buildings, params.workspace_source)

    # Renewing features
    renewing_features = FindRenewingFeatures()
    renewing_features.find_features()
    renewing_features.create_feature_class()

    # Replacing features
    replacing_features = FindReplacingFeatures(bilateral_overlap)
    replacing_features.find_features()
    replacing_features.create_feature_class()

    # Deleting features
    deleting_features = FindDeletingFeatures(bilateral_overlap)
    deleting_features.find_features()
    deleting_features.create_feature_class()
