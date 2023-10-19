import abc
from abc import ABC

import arcpy


class CreateTheLayers:
    def __init__(self):
        self.moria_buildings = r'C:\Users\amitv\Desktop\TONOA\bordered_data.gdb\B_BUILDINGS_A'
        self.bs_buildings = r'C:\Users\amitv\Desktop\TONOA\bordered_data.gdb\no_dupes_leb_new_new'
        self.workspace_source = r'C:\Users\amitv\Desktop\TONOA\workspace.gdb'
        self.target_source = r'C:\Users\amitv\Desktop\TONOA\target.gdb'

    @abc.abstractmethod
    def find_features(self):
        pass

    @abc.abstractmethod
    def create_feature_class(self):
        pass


class FindRenewingFeatures(CreateTheLayers, ABC):
    def __init__(self):
        super().__init__()
        self.selection = None
        self.bs_buildings_layer = arcpy.MakeFeatureLayer_management(self.bs_buildings, "bs_buildings_lyr")
        self.moria_buildings_layer = arcpy.MakeFeatureLayer_management(self.moria_buildings, "moria_buildings_lyr")

    def find_features(self):
        self.selection = arcpy.management.SelectLayerByLocation(self.bs_buildings_layer, "INTERSECT",
                                                                self.moria_buildings_layer, None, "NEW_SELECTION",
                                                                "INVERT")

    def create_feature_class(self):
        match_count = int(arcpy.management.GetCount(self.selection)[0])
        if not match_count:
            print('There aren\'t any renewing features')
        else:
            arcpy.FeatureClassToFeatureClass_conversion(self.bs_buildings_layer,
                                                        self.target_source, "renewing_buildings")




if __name__ == '__main__':
    renewing_features = FindRenewingFeatures()
    renewing_features.find_features()
    renewing_features.create_feature_class()
