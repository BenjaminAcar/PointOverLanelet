import lanelet2
from lanelet2.projection import MercatorProjector

class Lanelet2Map:
    def __init__(self):
        osm_file = "./lanelet2_map.osm"
        lat = 52.51354954806
        lon = 13.31962097419
        self.myProjector = MercatorProjector(lanelet2.io.Origin(lat=lat, lon=lon))
        self.lanelet_map = lanelet2.io.load(osm_file, lanelet2.io.Origin(lat=lat, lon=lon))

    def is_over_lanelet(self, x, y):
        gpsPoint = lanelet2.core.GPSPoint(x,y)
        plocal = lanelet2.geometry.to2D(self.myProjector.forward(gpsPoint))
        nearest_lanelet = lanelet2.geometry.findNearest(self.lanelet_map.laneletLayer, plocal, 1)
        if not nearest_lanelet:
            # no nearest lanelet, shouldn't happen, just a sanity check
            return None

        # If this lanelet contains the point return the id of the lanelet, otherwise None
        if lanelet2.geometry.inside(nearest_lanelet[0][1],plocal):
            return nearest_lanelet[0][1].id
        else:
            return None
