__all__ = [
    'ParisWindstormKeysLookup'
]

# Python library imports
import io
import logging
import os
import pandas as pd

# oasislmf imports
from oasislmf.preparation.lookup import OasisBaseKeysLookup
from oasislmf.utils.log import oasis_log
from oasislmf.utils.status import OASIS_KEYS_STATUS

logger = logging.getLogger()

class ParisWindstormKeysLookup(OasisBaseKeysLookup):
    """
    Model-specific keys lookup logic.
    """

    @oasis_log()

    def __init__(self, keys_data_directory=None, supplier='OasisLMF', model_name='ParisWindstorm', model_version=None,
            complex_lookup_config_fp=None,output_directory=None):
        """
        Initialise the static data required for the lookup.
        """
        super(self.__class__, self).__init__(
            keys_data_directory,
            supplier,
            model_name,
            model_version,
            complex_lookup_config_fp,
            output_directory
        )

    def get_areaperil(self,loc_df):
        loc_df['areaperil_id'] = 1
        loc_df['ap_status'] = OASIS_KEYS_STATUS['success']['id']
        loc_df['ap_message'] = ''
        return loc_df

    def get_vulnerbaility(self,loc_df):
        loc_df['vulnerability_id'] = 1
        loc_df['v_status'] = OASIS_KEYS_STATUS['success']['id']
        loc_df['v_message'] = ''
        return loc_df

    @oasis_log()
    def process_locations(self,loc_df):

        loc_df.columns = map(str.lower, loc_df.columns)
        loc_df = self.get_areaperil(loc_df)
        loc_df = self.get_vulnerbaility(loc_df)

        for _,loc in loc_df.iterrows():

            loc_id = int(loc['loc_id'])
            peril = 'WTC'
            coverage = 1
            ap_id = int(loc['areaperil_id'])
            v_id = int(loc['vulnerability_id'])
            status = OASIS_KEYS_STATUS['success']['id']
            message = ''

            if status == OASIS_KEYS_STATUS['success']['id']:
                yield {
                    "loc_id": loc_id,
                    "peril_id": peril,
                    "coverage_type": coverage,
                    "area_peril_id": ap_id,
                    "vulnerability_id": v_id,
                    "status": status
                }
            else:
                yield {
                    "loc_id": loc_id,
                    "peril_id": peril,
                    "coverage_type": coverage,
                    "message": message,
                    "status": status
                }

