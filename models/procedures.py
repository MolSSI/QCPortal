"""
A model for TorsionDrive
"""

import copy
import json
from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel

from .common_models import (Molecule, ObjectId, OptimizationSpecification, Provenance, QCSpecification, hash_dictionary,
                            json_encoders)

from qcelemental.models import Optimization

__all__ = ["OptimizationDocument"]


class OptimizationDocument(Optimization):
    """
    A TorsionDrive Input base class
    """

    # Client and local data
    client: Any = None
    cache: Dict[str, Any] = {}

    id: ObjectId = None
    procedure: str
    program: str
    initial_molecule: ObjectId
    hash_index: Optional[str] = None

    qc_spec: QCSpecification
    input_specification: Any = None # Deprecated

    # Results
    final_molecule: ObjectId = None
    trajectory: List[ObjectId] = None

    class Config:
        allow_mutation = False
        json_encoders = json_encoders
        extra = "forbid"

    def __init__(self, **data):
        data["procedure"] = "optimization"
        super().__init__(**data)

        # Set hash index if not present
        if self.hash_index is None:
            self.__values__["hash_index"] = self.get_hash_index()

    def __str__(self):
        """
        Simplified optimization string representation.

        Returns
        -------
        ret : str
            A representation of the current Optimization status.

        Examples
        --------

        >>> repr(optimization_obj)
        Optimization(id='5b7f1fd57b87872d2c5d0a6d', status='FINISHED', molecule_id='5b7f1fd57b87872d2c5d0a6c', molecule_name='HOOH')
        """

        ret = "Optimization("
        ret += "id='{}', ".format(self.id)
        ret += "success='{}', ".format(self.success)
        ret += "initial_molecule='{}') ".format(self.initial_molecule)
        return ret

    def dict(self, *args, **kwargs):
        kwargs["exclude"] = (kwargs.pop("exclude", None) or set()) | {"client", "cache"}
        kwargs["skip_defaults"] = True
        return super().dict(*args, **kwargs)

    def json_dict(self, *args, **kwargs):
        return json.loads(self.json(*args, **kwargs))

    def get_hash_index(self):

        data = self.dict(
            include={"initial_molecule", "program", "procedure", "keywords", "qc_spec"})

        return hash_dictionary(data)
