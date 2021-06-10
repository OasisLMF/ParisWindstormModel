__all__ = [
    'ParisWindstormKeysLookup'
]

from oasislmf.lookup.builtin import Lookup


class ParisWindStormKeysLookup(Lookup):
    """
    Model-specific keys lookup logic.
    """
    @staticmethod
    def set_geoloc_join(locations):
        locations['lat_join'] = (locations['latitude']*1000000).astype('int')
        locations['lon_join'] = (locations['longitude']*1000000).astype('int')
        return locations

