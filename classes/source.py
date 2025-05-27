
from typing_extensions import Any, deprecated
from dataclasses       import dataclass, field

@dataclass(frozen=True, slots=True)
class GaiaSource(object):

    """
    GaiaSource
    _
    A data container representing a single star entry from the Gaia EDR3 (Early Data Release 3) catalog.

    This class uses positional argument unpacking (*args) to initialize all 95 parameters in order.
    Each field corresponds to a specific property observed or calculated for a star, including:
    - Astrometric parameters (position, proper motion, parallax, etc.)
    - Photometric measurements (fluxes and magnitudes in G, BP, and RP bands)
    - Observation metadata (number of transits, goodness of fit, etc.)
    - Derived statistics (errors, correlations, RUWE, etc.)

    Usage:
    _
    ```
        row = [...]  # A list or tuple with 95 ordered values from the Gaia dataset
        star = GaiaSource(*row)

        print(star.ra, star.dec, star.phot_g_mean_mag)
    ```

    Notes:
    _
    - The order of input values must match the Gaia EDR3 column order exactly.
    - All fields are set as frozen (immutable) after initialization.
    - Slots are used to reduce memory overhead.
    """


    solution_id:                     Any = field(init=False)
    designation:                     Any = field(init=False)
    source_id:                       Any = field(init=False)
    random_index:                    Any = field(init=False)
    ref_epoch:                       Any = field(init=False)
    ra:                              Any = field(init=False)
    ra_error:                        Any = field(init=False)
    dec:                             Any = field(init=False)
    dec_error:                       Any = field(init=False)
    parallax:                        Any = field(init=False)
    parallax_error:                  Any = field(init=False)
    parallax_over_error:             Any = field(init=False)
    pm:                              Any = field(init=False)
    pmra:                            Any = field(init=False)
    pmra_error:                      Any = field(init=False)
    pmdec:                           Any = field(init=False)
    pmdec_error:                     Any = field(init=False)
    ra_dec_corr:                     Any = field(init=False)
    ra_parallax_corr:                Any = field(init=False)
    ra_pmra_corr:                    Any = field(init=False)
    ra_pmdec_corr:                   Any = field(init=False)
    dec_parallax_corr:               Any = field(init=False)
    dec_pmra_corr:                   Any = field(init=False)
    dec_pmdec_corr:                  Any = field(init=False)
    parallax_pmra_corr:              Any = field(init=False)
    parallax_pmdec_corr:             Any = field(init=False)
    pmra_pmdec_corr:                 Any = field(init=False)
    astrometric_n_obs_al:            Any = field(init=False)
    astrometric_n_obs_ac:            Any = field(init=False)
    astrometric_n_good_obs_al:       Any = field(init=False)
    astrometric_n_bad_obs_al:        Any = field(init=False)
    astrometric_gof_al:              Any = field(init=False)
    astrometric_chi2_al:             Any = field(init=False)
    astrometric_excess_noise:        Any = field(init=False)
    astrometric_excess_noise_sig:    Any = field(init=False)
    astrometric_params_solved:       Any = field(init=False)
    astrometric_primary_flag:        Any = field(init=False)
    nu_eff_used_in_astrometry:       Any = field(init=False)
    pseudocolour:                    Any = field(init=False)
    pseudocolour_error:              Any = field(init=False)
    ra_pseudocolour_corr:            Any = field(init=False)
    dec_pseudocolour_corr:           Any = field(init=False)
    parallax_pseudocolour_corr:      Any = field(init=False)
    pmra_pseudocolour_corr:          Any = field(init=False)
    pmdec_pseudocolour_corr:         Any = field(init=False)
    astrometric_matched_transits:    Any = field(init=False)
    visibility_periods_used:         Any = field(init=False)
    astrometric_sigma5d_max:         Any = field(init=False)
    matched_transits:                Any = field(init=False)
    new_matched_transits:            Any = field(init=False)
    matched_transits_removed:        Any = field(init=False)
    ipd_gof_harmonic_amplitude:      Any = field(init=False)
    ipd_gof_harmonic_phase:          Any = field(init=False)
    ipd_frac_multi_peak:             Any = field(init=False)
    ipd_frac_odd_win:                Any = field(init=False)
    ruwe:                            Any = field(init=False)
    scan_direction_strength_k1:      Any = field(init=False)
    scan_direction_strength_k2:      Any = field(init=False)
    scan_direction_strength_k3:      Any = field(init=False)
    scan_direction_strength_k4:      Any = field(init=False)
    scan_direction_mean_k1:          Any = field(init=False)
    scan_direction_mean_k2:          Any = field(init=False)
    scan_direction_mean_k3:          Any = field(init=False)
    scan_direction_mean_k4:          Any = field(init=False)
    duplicated_source:               Any = field(init=False)
    phot_g_n_obs:                    Any = field(init=False)
    phot_g_mean_flux:                Any = field(init=False)
    phot_g_mean_flux_error:          Any = field(init=False)
    phot_g_mean_flux_over_error:     Any = field(init=False)
    phot_g_mean_mag:                 Any = field(init=False)
    phot_bp_n_obs:                   Any = field(init=False)
    phot_bp_mean_flux:               Any = field(init=False)
    phot_bp_mean_flux_error:         Any = field(init=False)
    phot_bp_mean_flux_over_error:    Any = field(init=False)
    phot_bp_mean_mag:                Any = field(init=False)
    phot_rp_n_obs:                   Any = field(init=False)
    phot_rp_mean_flux:               Any = field(init=False)
    phot_rp_mean_flux_error:         Any = field(init=False)
    phot_rp_mean_flux_over_error:    Any = field(init=False)
    phot_rp_mean_mag:                Any = field(init=False)
    phot_bp_n_contaminated_transits: Any = field(init=False)
    phot_bp_n_blended_transits:      Any = field(init=False)
    phot_rp_n_contaminated_transits: Any = field(init=False)
    phot_rp_n_blended_transits:      Any = field(init=False)
    phot_proc_mode:                  Any = field(init=False)
    phot_bp_rp_excess_factor:        Any = field(init=False)
    bp_rp:                           Any = field(init=False)
    bp_g:                            Any = field(init=False)
    g_rp:                            Any = field(init=False)
    dr2_radial_velocity:             Any = field(init=False)
    dr2_radial_velocity_error:       Any = field(init=False)
    dr2_rv_nb_transits:              Any = field(init=False)
    dr2_rv_template_teff:            Any = field(init=False)
    dr2_rv_template_logg:            Any = field(init=False)
    dr2_rv_template_fe_h:            Any = field(init=False)
    l:                               Any = field(init=False)
    b:                               Any = field(init=False)
    ecl_lon:                         Any = field(init=False)
    ecl_lat:                         Any = field(init=False)

    def __init__(self, *args: Any) -> None:
        fields: list = list(self.__dataclass_fields__)
        if len(args) != len(fields):
            raise ValueError(f"Expected {len(fields)} values, got {len(args)}")
        for name, value in zip(fields, args):
            object.__setattr__(self, name, value)

__all__: list = ['GaiaSource']