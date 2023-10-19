from os.path import basename, join
import arcpy


def find_bilateral_overlap(fc1, fc2, output_source):
    arcpy.env.overwriteOutput = True

    intersect_features = arcpy.Intersect_analysis([fc1, fc2], join(output_source, 'intersect_features'),
                                                  "ONLY_FID")
    feature_classes = [fc1, fc2]
    for fc in feature_classes:
        table = arcpy.analysis.TabulateIntersection(fc, "OBJECTID", intersect_features,
                                                    join(output_source, f"{fc1.lower()}_table"), "OBJECTID")

        # Join and rename fields
        arcpy.management.JoinField(intersect_features, "OBJECTID", table, "OBJECTID_12", ["PERCENTAGE"])
        arcpy.management.AlterField(intersect_features, "PERCENTAGE", f"PERCENTAGE_{feature_classes.index(fc)+1}",
                                    f"PERCENTAGE_{feature_classes.index(fc)+1}")

    return intersect_features


