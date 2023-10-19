from os.path import basename, join

import arcpy


def find_bilateral_overlap(fc1, fc2, output_source):
    # Enable overwriting of output data
    arcpy.env.overwriteOutput = True

    # Step 1: Perform an intersection of two input feature classes (fc1 and fc2)
    intersect_features = arcpy.Intersect_analysis([fc1, fc2], join(output_source, 'intersect_features'), "ONLY_FID")

    # Create a list of feature classes (fc1 and fc2)
    feature_classes = [fc1, fc2]

    # Step 2: Loop through the feature classes and create tables for each
    for fc in feature_classes:
        # Create a table for the intersection of each feature class
        table = arcpy.analysis.TabulateIntersection(fc, "OBJECTID", intersect_features,
                                                    join(output_source, f"{fc1.lower()}_table"), "OBJECTID")

        # Step 3: Join and rename fields
        # Join the table with the intersection results based on OBJECTID
        arcpy.management.JoinField(intersect_features, "OBJECTID", table, "OBJECTID_12", ["PERCENTAGE"])

        # Rename the PERCENTAGE field to distinguish between feature classes
        arcpy.management.AlterField(intersect_features, "PERCENTAGE", f"PERCENTAGE_{feature_classes.index(fc) + 1}",
                                    f"PERCENTAGE_{feature_classes.index(fc) + 1}")

    # Step 4: Return the intersected features
    return intersect_features
