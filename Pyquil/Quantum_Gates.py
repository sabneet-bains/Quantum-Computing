from warnings import warn
from typing import Callable, Mapping, Optional, Tuple, Union

import numpy

from pyquil.quilatom import (
    Addr,
    Expression,
    MemoryReference,
    MemoryReferenceDesignator,
    ParameterDesignator,
    QubitDesignator,
    unpack_classical_reg,
    unpack_qubit,
)