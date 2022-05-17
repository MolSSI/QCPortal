from typing import Union, Any

import pydantic

from .models import (
    BaseDataset,
    DatasetQueryModel,
    DatasetFetchEntryBody,
    DatasetFetchRecordItemsBody,
    DatasetSubmitBody,
    DatasetDeleteStrBody,
    DatasetDeleteRecordItemsBody,
    DatasetRecordModifyBody,
    DatasetRecordRevertBody,
    DatasetModifyMetadata,
    DatasetQueryRecords,
    DatasetDeleteParams,
    DatasetDeleteEntryBody,
    DatasetDeleteSpecificationBody,
)

# All possible datasets we can get from the server
from .singlepoint.models import SinglepointDataset
from .optimization.models import OptimizationDataset
from .torsiondrive.models import TorsiondriveDataset
from .gridoptimization import GridoptimizationDataset
from .manybody import ManybodyDataset
from .reaction import ReactionDataset

AllDatasetTypes = Union[
    SinglepointDataset,
    OptimizationDataset,
    TorsiondriveDataset,
    GridoptimizationDataset,
    ManybodyDataset,
    ReactionDataset,
]
AllDatasetDataModelTypes = Union[
    SinglepointDataset._DataModel,
    OptimizationDataset._DataModel,
    TorsiondriveDataset._DataModel,
    GridoptimizationDataset._DataModel,
    ManybodyDataset._DataModel,
    ReactionDataset._DataModel,
]


def dataset_from_datamodel(data: AllDatasetDataModelTypes, client: Any) -> AllDatasetTypes:
    dataset_init = {"client": client, "dataset_type": data.collection_type, "raw_data": data}
    return pydantic.parse_obj_as(AllDatasetTypes, dataset_init)
