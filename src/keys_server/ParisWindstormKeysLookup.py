__all__ = [
    'ParisWindstormKeysLookup'
]

import logging
import os
from typing import Dict, Any, Optional

import pandas as pd

from oasislmf.lookup.interface import KeyLookupInterface
from oasislmf.utils.log import oasis_log
from oasislmf.utils.status import OASIS_KEYS_STATUS
from pandas import DataFrame

logger = logging.getLogger()


class ParisWindstormKeysLookup(KeyLookupInterface):
    """
    This class is responsible for Model-specific keys lookup logic.

    Attributes:
        config_dict (Dict[str, str]): parameters for the model parameters and data paths
        config_dir (str): the directory to the configuration file
        output_dir (str): the directory for output data
        user_data_dir (Optional[str]): the directory pointing to the user data
        df_ap_dict (DataFrame): Data marrying up the area peril id, latitude and longitude
        df_vuln_dict (DataFrame): Data marrying up the vulnerability id with the construction code
    """
    @oasis_log()
    def __init__(self, config_dict: Dict[str, str], config_dir: str, output_dir: str,
                 user_data_dir: Optional[str] = None) -> None:
        """
        The constructor for the ParisWindstormKeysLookup class.

        @param config_dict: (Dict[str, str]) configuration for model parameters such as data paths and model meta data
        @param config_dir: (str) the directory pointing to the configuration file
        @param output_dir: (str) the directory for output data
        @param user_data_dir: (Optional[str])
        """
        self.config_dict: Dict[str, str] = config_dict
        self.config_dir: str = config_dir
        self.output_dir: str = output_dir
        self.user_data_dir: Optional[str] = user_data_dir
        self.df_ap_dict: DataFrame = pd.read_csv(self.area_peril_data_dir)
        self.df_vuln_dict: DataFrame = pd.read_csv(self.vulnerability_data_dir)

    @property
    def area_peril_data_dir(self) -> str:
        data_path: str = str(os.path.join(self.config_dict["keys_data_path"], 'areaperil_dict.csv'))
        if not os.path.isfile(data_path):
            raise FileExistsError(f"data file {data_path} does not exist")
        return data_path

    @property
    def vulnerability_data_dir(self) -> str:
        data_path: str = str(os.path.join(self.config_dict["keys_data_path"], 'vulnerability_dict.csv'))
        if not os.path.isfile(data_path):
            raise FileExistsError(f"data file {data_path} does not exist")
        return data_path

    def get_areaperil(self, loc_df: DataFrame) -> DataFrame:
        """
        Processes the 'latitude' and 'longitude' before merging the area peril data.

        @param loc_df: (DataFrame) the data frame to be processed and returned
        @return: (DataFrame) data with processed 'latitude' and 'longitude' and merged area peril data
        """
        loc_df['lat_join'] = (loc_df['latitude']*1000000).astype('int')
        loc_df['lon_join'] = (loc_df['longitude']*1000000).astype('int')
        loc_df = loc_df.merge(self.df_ap_dict, how='left')
        loc_df['areaperil_id'].fillna(0)
        loc_df['ap_status'] = OASIS_KEYS_STATUS['success']['id']
        loc_df['ap_message'] = ''
        return loc_df

    def get_vulnerbaility(self, loc_df: DataFrame) -> DataFrame:
        """
        Fills in the null 'vulnerability_id' data and merge vulnerability data with data frame.

        @param loc_df: (DataFrame) the data frame to be processed
        @return: (DataFrame) the processed data frame
        """
        loc_df = loc_df.merge(self.df_vuln_dict, how='left')
        loc_df['vulnerability_id'].fillna(0)
        loc_df['v_status'] = OASIS_KEYS_STATUS['success']['id']
        loc_df['v_message'] = ''
        return loc_df

    @oasis_log()
    def process_locations(self, loc_df: DataFrame) -> Dict[str, Any]:
        """
        A generator that produces a row from the area peril data and vulnerabilities.

        @param loc_df: (DataFrame) the data frame to processed and returned
        @return: (Dict[str, Any]) row of the processed data frame produced by a yield
        """
        loc_df.columns = map(str.lower, loc_df.columns)
        loc_df: DataFrame = self.get_areaperil(loc_df)
        loc_df: DataFrame = self.get_vulnerbaility(loc_df)

        for _, loc in loc_df.iterrows():

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
                    "status": status,
                    "message": ''
                }
            else:
                yield {
                    "loc_id": loc_id,
                    "peril_id": peril,
                    "coverage_type": coverage,
                    "message": message,
                    "status": status
                }

