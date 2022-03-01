import numpy as np
from typing import Union

import redback.get_data.directory
from redback.transient.transient import OpticalTransient


class TDE(OpticalTransient):
    DATA_MODES = ['flux', 'flux_density', 'photometry', 'luminosity']

    def __init__(
            self, name: str, data_mode: str = 'photometry', time: np.ndarray = None, time_err: np.ndarray = None,
            time_mjd: np.ndarray = None, time_mjd_err: np.ndarray = None, time_rest_frame: np.ndarray = None,
            time_rest_frame_err: np.ndarray = None, Lum50: np.ndarray = None, Lum50_err: np.ndarray = None,
            flux_density: np.ndarray = None, flux_density_err: np.ndarray = None, magnitude: np.ndarray = None,
            magnitude_err: np.ndarray = None, bands: np.ndarray = None, system: np.ndarray = None,
            active_bands: Union[np.ndarray, str] = 'all', use_phase_model: bool = False, **kwargs: dict) -> None:
        """

        Parameters
        ----------
        name
        data_mode
        time
        time_err
        time_mjd
        time_mjd_err
        time_rest_frame
        time_rest_frame_err
        Lum50
        Lum50_err
        flux_density
        flux_density_err
        magnitude
        magnitude_err
        bands
        system
        active_bands
        use_phase_model
        kwargs
        """
        super().__init__(time=time, time_err=time_err, time_rest_frame=time_rest_frame, time_mjd=time_mjd,
                         time_mjd_err=time_mjd_err, time_rest_frame_err=time_rest_frame_err, Lum50=Lum50,
                         Lum50_err=Lum50_err, flux_density=flux_density, flux_density_err=flux_density_err,
                         magnitude=magnitude, magnitude_err=magnitude_err, data_mode=data_mode, name=name,
                         use_phase_model=use_phase_model, bands=bands, system=system, active_bands=active_bands,
                         **kwargs)
        self.directory_structure = redback.get_data.directory.transient_directory_structure(
            transient=self.name, transient_type="tidal_disruption_event", data_mode=self.data_mode)
        self._set_data()
