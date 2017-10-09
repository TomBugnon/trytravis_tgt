#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __init__.py

"""Spiking VisNet."""

import logging
import os

from .parameters import Params
from .simulation import Simulation
from .network.network import Network
from .save import load_yaml


__all__ = ['load_params', 'run', 'Simulation', 'Network']

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
        }
    },
    'handlers': {
        'stdout': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        }
    },
    'loggers': {
        'spiking_visnet': {
            'level': 'INFO',
            'handlers': ['stdout'],
        }
    }
})
log = logging.getLogger(__name__)  # pylint: disable=invalid-name


def load_params(path, overrides=None):
    """Load a list of parameter files, optionally overriding some values.

    Args:
        path (str): The filepath to load.

    Keyword Args:
        overrides (tree or list of trees): A dictionary or list/tuple of
            dictionaries containing parameters that will take precedence over
            those in the file. If the argument is a list of trees, the
            overrides will be applied in turn starting from the end of the list.

    Returns:
        Params: The loaded parameters with overrides applied.
    """
    if not isinstance(overrides, (list, tuple)):
        overrides = [overrides]
    directory = os.path.dirname(os.path.abspath(path))
    return Params.merge(
        *[Params(overrides_dict)
          for overrides_dict in overrides],
        *[Params.load(directory, relative_path)
        for relative_path in load_yaml(path)]
    )


def run(path, overrides=None, output_dir=None, input_dir=None):
    """Run the simulation described by the params at ``path``.

    Args:
        path (str): The filepath of a parameter file specifying the simulation.

    Keyword Arguments:
        overrides (dict or list): Parameters that should override those from
            the path. Either provided as a dictionary or as a list of dict.
    """
    print(f'Loading parameters: `{path}`... ', end='', flush=True)
    params = load_params(path, overrides=overrides)
    # Incorporate kwargs in params
    if output_dir is not None:
        params.c['simulation']['output_dir'] = output_dir
    if output_dir is not None:
        params.c['simulation']['input_dir'] = input_dir
    print('done.', flush=True)
    # Initialize simulation
    sim = Simulation(params)
    # Simulate and save
    if not params.c['simulation'].get('dry_run', False):
        sim.run()
    if params.c['simulation'].get('save_simulation', True):
        sim.save()
    # Dump network's connections
    if params.c['simulation'].get('dump_connections', False):
        sim.dump_connections()
    # Plot network's connections
    if params.c['simulation'].get('plot_connections', False):
        sim.plot_connections()
