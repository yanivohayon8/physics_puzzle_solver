from shapely import Polygon,unary_union
from shapely import errors as shapely_errors

def semi_dice_overlapping(polygons:list[Polygon]):
    dice_sum = 0

    for i in range(len(polygons)):
        other_polygons = [polygons[j] for j in range(len(polygons)) if i!=j]    
        other_union = unary_union(other_polygons)
        try:
            curr_intersect_with_other = polygons[i].intersection(other_union)
        except shapely_errors.GEOSException as e:
            curr_intersect_with_other = polygons[i].buffer(0).intersection(other_union.buffer(0))
        dice_sum+= curr_intersect_with_other.area/polygons[i].area

    return dice_sum