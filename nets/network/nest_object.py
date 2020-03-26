#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# network/nest_object.py
"""Base class for representations of NEST objects."""

import copy as cp
import functools
from pprint import pformat

from ..utils.validation import validate


class ParamObject:
    """Base class for a named object with parameters.

    Supports "validation" of parameters.
    """

    RESERVED_PARAMS = None
    MANDATORY_PARAMS = None
    OPTIONAL_PARAMS = None
    
    def __init__(self, name, params):
        self.name = name
        self.params = cp.deepcopy(params)
        self.validate_params()

    def validate_params(self):
        """Validate and update params with default values."""
        # Validate params:
        self.params = validate(
            self.name, self.params, param_type='params',
            reserved=self.RESERVED_PARAMS,
            mandatory=self.MANDATORY_PARAMS,
            optional=self.OPTIONAL_PARAMS,
        )

@functools.total_ordering
class NestObject:
    """Base class for a named NEST object, with params and nest_params

    Args:
        name (str): The name of the object.
        params (Params): The object parameters. Interpreted by NETS.
        nest_params (Params): The object parameters passed to NEST.

    Objects are ordered and hashed by name.
    """

    # Validation of `params`
    RESERVED_PARAMS = None
    MANDATORY_PARAMS = None
    OPTIONAL_PARAMS = None
    # Validation of `nest_params`
    RESERVED_NEST_PARAMS = None
    MANDATORY_NEST_PARAMS = None
    OPTIONAL_NEST_PARAMS = None

    # pylint: disable=too-few-public-methods

    def __init__(self, name, params, nest_params):
        self.name = name
        # Flatten the parameters to a dictionary (and make a copy)
        self.params = cp.deepcopy(params)
        self.nest_params = cp.deepcopy(nest_params)
        # Validate self.params and self.nest_params
        self.validate_params()
        # Whether the object has been created in NEST
        self._created = False

    def validate_params(self):
        """Validate and update params and nest_params with default values."""
        # Validate params:
        self.params = validate(
            self.name, self.params, param_type='params',
            reserved=self.RESERVED_PARAMS,
            mandatory=self.MANDATORY_PARAMS,
            optional=self.OPTIONAL_PARAMS,
        )
        self.nest_params = validate(
            self.name, self.nest_params, param_type='nest_params',
            reserved=self.RESERVED_NEST_PARAMS,
            mandatory=self.MANDATORY_NEST_PARAMS,
            optional=self.OPTIONAL_NEST_PARAMS,
        )

    # pylint: disable=unused-argument,invalid-name
    def _repr_pretty_(self, p, cycle):
        opener = '{classname}({name}, '.format(
            classname=type(self).__name__, name=self.name)
        closer = ')'
        with p.group(p.indentation, opener, closer):
            p.breakable()
            p.pretty(self.params)
            p.pretty(self.nest_params)

    # pylint: enable=unused-argument,invalid-name

    def __repr__(self):
        return '{classname}({name}, {params}, {nest_params})'.format(
            classname=type(self).__name__, name=self.name,
            params=pformat(self.params), nest_params=pformat(self.nest_params)
        )

    def __lt__(self, other):
        return self.name < other.name

    def __hash__(self):
        return hash(self.name)
