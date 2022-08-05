import json
from dataclasses import dataclass
from typing import List, Optional, Literal, Union

from pydalle.functional.assumptions import OPENAI_LABS_SHARE_URL_TEMPLATE


@dataclass
class TaskList:
    object: Literal["list"]
    data: List['Task']

    @classmethod
    def from_dict(cls, d: dict) -> 'TaskList':
        return cls(object=d["object"],
                   data=[Task.from_dict(t) for t in d["data"]])

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]


TaskType = Union[Literal["inpainting"], Literal["text2im"], Literal["variations"]]


@dataclass
class Task:
    object: Literal["task"]
    id: str
    created: int
    task_type: TaskType
    status: Union[Literal["succeeded"], Literal["pending"], Literal["rejected"]]
    status_information: 'StatusInformation'
    prompt_id: str
    generations: Optional["GenerationList"]
    prompt: "Prompt"

    @classmethod
    def from_dict(cls, d: dict) -> 'Task':
        return cls(object=d["object"],
                   id=d["id"],
                   created=d["created"],
                   task_type=d["task_type"],
                   status=d["status"],
                   status_information=StatusInformation.from_dict(d["status_information"]),
                   prompt_id=d["prompt_id"],
                   generations=GenerationList.from_dict(d["generations"]) if "generations" in d else None,
                   prompt=Prompt.from_dict(d["prompt"]), )

    def __str__(self):
        return f"Task(id={self.id}, task_type={self.task_type}, status={self.status})"


@dataclass
class StatusInformation:
    type: Optional[Literal["error"]] = None
    message: Optional[Literal["Your task failed as a result of our safety system."]] = None
    code: Optional[Literal["task_failed_text_safety_system"]] = None

    @classmethod
    def from_dict(cls, d: dict) -> 'StatusInformation':
        return cls(type=d.get("type"),
                   message=d.get("message"),
                   code=d.get("code"))


@dataclass
class Prompt:
    id: str
    object: Literal["prompt"]
    created: int
    prompt_type: Union[Literal["CaptionlessImagePrompt"],
                       Literal["CaptionImagePrompt"],
                       Literal["CaptionPrompt"]]
    prompt: "PromptData"
    parent_generation_id: Optional[str] = None

    @classmethod
    def from_dict(cls, d: dict) -> 'Prompt':
        return cls(id=d["id"],
                   object=d["object"],
                   created=d["created"],
                   prompt_type=d["prompt_type"],
                   prompt=PromptData.from_dict(d["prompt"]),
                   parent_generation_id=d.get("parent_generation_id"))


@dataclass
class PromptData:
    caption: Optional[str] = None
    image_path: Optional[str] = None
    masked_image_path: Optional[str] = None

    @classmethod
    def from_dict(cls, d: dict) -> 'PromptData':
        return cls(caption=d.get("caption"),
                   image_path=d.get("image_path"),
                   masked_image_path=d.get("masked_image_path"))


@dataclass
class GenerationList:
    object: Literal["list"]
    data: List["Generation"]

    @classmethod
    def from_dict(cls, d: dict) -> 'GenerationList':
        return cls(object=d["object"],
                   data=[Generation.from_dict(g) for g in d["data"]])

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]


@dataclass
class Generation:
    id: str
    object: Literal["generation"]
    created: int
    generation_type: Literal["ImageGeneration"]
    generation: "GenerationData"
    task_id: str
    prompt_id: str
    is_public: bool

    @classmethod
    def from_dict(cls, d: dict) -> 'Generation':
        return cls(id=d["id"],
                   object=d["object"],
                   created=d["created"],
                   generation_type=d["generation_type"],
                   generation=GenerationData.from_dict(d["generation"]),
                   task_id=d["task_id"],
                   prompt_id=d["prompt_id"],
                   is_public=d["is_public"])

    @property
    def share_url(self):
        # The generation must be public for the share url to be available
        return OPENAI_LABS_SHARE_URL_TEMPLATE % (self.id.replace("generation-", "", 1))


@dataclass
class GenerationData:
    image_path: str

    @classmethod
    def from_dict(cls, d: dict) -> 'GenerationData':
        return cls(image_path=d["image_path"])


@dataclass
class Collection:
    object: Literal["collection"]
    id: str
    created: int
    name: str
    description: str
    is_public: bool
    alias: str

    @classmethod
    def from_dict(cls, d: dict) -> 'Collection':
        return cls(object=d["object"],
                   id=d["id"],
                   created=d["created"],
                   name=d["name"],
                   description=d["description"],
                   is_public=d["is_public"],
                   alias=d["alias"])
