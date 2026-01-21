from pydantic import Field

from vgd.shared.models.model_cards import ModelCard
from vgd.shared.types.api import ChatCompletionTaskParams
from vgd.shared.types.common import CommandId, NodeId
from vgd.shared.types.worker.instances import Instance, InstanceId, InstanceMeta
from vgd.shared.types.worker.shards import Sharding
from vgd.utils.pydantic_ext import CamelCaseModel, TaggedModel


class BaseCommand(TaggedModel):
    command_id: CommandId = Field(default_factory=CommandId)


class TestCommand(BaseCommand):
    __test__ = False


class ChatCompletion(BaseCommand):
    request_params: ChatCompletionTaskParams


class PlaceInstance(BaseCommand):
    model_card: ModelCard
    sharding: Sharding
    instance_meta: InstanceMeta
    min_nodes: int


class CreateInstance(BaseCommand):
    instance: Instance


class DeleteInstance(BaseCommand):
    instance_id: InstanceId


class TaskFinished(BaseCommand):
    finished_command_id: CommandId


class RequestEventLog(BaseCommand):
    since_idx: int


Command = (
    TestCommand
    | RequestEventLog
    | ChatCompletion
    | PlaceInstance
    | CreateInstance
    | DeleteInstance
    | TaskFinished
)


class ForwarderCommand(CamelCaseModel):
    origin: NodeId
    command: Command
