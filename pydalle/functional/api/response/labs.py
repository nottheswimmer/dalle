"""
This module contains dataclasses which represent the Labs API's response objects.
"""

from dataclasses import dataclass
from typing import List, Optional, Literal, Union, Any

from pydalle.functional.assumptions import OPENAI_LABS_SHARE_URL_TEMPLATE


@dataclass
class TaskList:
    raw: dict
    object: Literal["list"]
    data: List['Task']

    @classmethod
    def from_dict(cls, d: dict) -> 'TaskList':
        return cls(object=d["object"],
                   data=[Task.from_dict(t) for t in d["data"]],
                   raw=d)

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]


TaskType = Union[Literal["inpainting"], Literal["text2im"], Literal["variations"]]


@dataclass
class Task:
    raw: dict
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
                   prompt=Prompt.from_dict(d["prompt"]),
                   raw=d)

    def __str__(self):
        return f"Task(id={self.id}, task_type={self.task_type}, status={self.status})"


@dataclass
class StatusInformation:
    raw: dict
    type: Optional[Literal["error"]] = None
    message: Optional[Literal["Your task failed as a result of our safety system."]] = None
    code: Optional[Literal["task_failed_text_safety_system"]] = None

    @classmethod
    def from_dict(cls, d: dict) -> 'StatusInformation':
        return cls(type=d.get("type"),
                   message=d.get("message"),
                   code=d.get("code"),
                   raw=d)


@dataclass
class Prompt:
    raw: dict
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
                   parent_generation_id=d.get("parent_generation_id"),
                   raw=d)


@dataclass
class PromptData:
    raw: dict
    caption: Optional[str] = None
    image_path: Optional[str] = None
    masked_image_path: Optional[str] = None

    @classmethod
    def from_dict(cls, d: dict) -> 'PromptData':
        return cls(caption=d.get("caption"),
                   image_path=d.get("image_path"),
                   masked_image_path=d.get("masked_image_path"),
                   raw=d)


@dataclass
class GenerationList:
    raw: dict
    object: Literal["list"]
    data: List["Generation"]

    @classmethod
    def from_dict(cls, d: dict) -> 'GenerationList':
        return cls(object=d["object"],
                   data=[Generation.from_dict(g) for g in d["data"]],
                   raw=d)

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]


@dataclass
class Generation:
    raw: dict
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
                   is_public=d["is_public"],
                   raw=d)

    @property
    def share_url(self):
        # The generation must be public for the share url to be available
        return OPENAI_LABS_SHARE_URL_TEMPLATE % (self.id.replace("generation-", "", 1))


@dataclass
class GenerationData:
    raw: dict
    image_path: str

    @classmethod
    def from_dict(cls, d: dict) -> 'GenerationData':
        return cls(image_path=d["image_path"],
                   raw=d)


@dataclass
class Collection:
    raw: dict
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
                   alias=d["alias"],
                   raw=d)


@dataclass
class Breakdown:
    raw: dict
    free: int

    @classmethod
    def from_dict(cls, d: dict) -> 'Breakdown':
        return cls(free=d["free"],
                   raw=d)


@dataclass
class BillingInfo:
    raw: dict
    aggregate_credits: int
    next_grant_ts: int
    breakdown: Breakdown

    @classmethod
    def from_dict(cls, d: dict) -> 'BillingInfo':
        return cls(aggregate_credits=d["aggregate_credits"],
                   next_grant_ts=d["next_grant_ts"],
                   breakdown=Breakdown.from_dict(d["breakdown"]),
                   raw=d)


@dataclass
class Features:
    raw: dict
    public_endpoints: bool
    image_uploads: bool

    @classmethod
    def from_dict(cls, d: dict) -> 'Features':
        return cls(public_endpoints=d["public_endpoints"],
                   image_uploads=d["image_uploads"],
                   raw=d)


@dataclass
class Organization:
    raw: dict
    object: Literal["organization"]
    id: str
    created: int
    title: str
    name: str
    description: str
    personal: bool
    is_default: bool
    role: str
    groups: List[str]

    @classmethod
    def from_dict(cls, d: dict) -> 'Organization':
        return cls(object=d["object"],
                   id=d["id"],
                   created=d["created"],
                   title=d["title"],
                   name=d["name"],
                   description=d["description"],
                   personal=d["personal"],
                   is_default=d["is_default"],
                   role=d["role"],
                   groups=d["groups"],
                   raw=d)


@dataclass
class OrganizationList:
    raw: dict
    object: Literal["list"]
    data: List[Organization]

    @classmethod
    def from_dict(cls, d: dict) -> 'OrganizationList':
        return cls(object=d["object"],
                   data=[Organization.from_dict(o) for o in d["data"]],
                   raw=d)


@dataclass
class Session:
    raw: dict
    sensitive_id: str
    object: Literal["session"]
    created: int
    last_use: int
    publishable: bool

    @classmethod
    def from_dict(cls, d: dict) -> 'Session':
        return cls(sensitive_id=d["sensitive_id"],
                   object=d["object"],
                   created=d["created"],
                   last_use=d["last_use"],
                   publishable=d["publishable"],
                   raw=d)


@dataclass
class User:
    raw: dict
    object: Literal["user"]
    id: str
    email: str
    name: str
    picture: str
    created: int
    accepted_terms_at: int
    session: Session
    groups: List[str]
    orgs: OrganizationList
    intercom_hash: str
    accepted_terms: int
    seen_upload_guidelines: int
    seen_billing_onboarding: int

    @classmethod
    def from_dict(cls, d: dict) -> 'User':
        return cls(object=d["object"],
                   id=d["id"],
                   email=d["email"],
                   name=d["name"],
                   picture=d["picture"],
                   created=d["created"],
                   accepted_terms_at=d["accepted_terms_at"],
                   session=Session.from_dict(d["session"]),
                   groups=d["groups"],
                   orgs=OrganizationList.from_dict(d["orgs"]),
                   intercom_hash=d["intercom_hash"],
                   accepted_terms=d["accepted_terms"],
                   seen_upload_guidelines=d["seen_upload_guidelines"],
                   seen_billing_onboarding=d["seen_billing_onboarding"],
                   raw=d)


@dataclass
class Login:
    raw: dict
    object: Literal["login"]
    user: User
    invites: List[Any]
    features: Features
    billing_info: BillingInfo

    @classmethod
    def from_dict(cls, d: dict) -> 'Login':
        return cls(object=d["object"],
                   user=User.from_dict(d["user"]),
                   invites=d["invites"],
                   features=Features.from_dict(d["features"]),
                   billing_info=BillingInfo.from_dict(d["billing_info"]),
                   raw=d)


@dataclass
class UserFlag:
    raw: dict
    object: Literal["user_flag"]
    id: str
    created: int
    generation_id: str
    description: str

    @classmethod
    def from_dict(cls, d: dict) -> 'UserFlag':
        return cls(object=d["object"],
                   id=d["id"],
                   created=d["created"],
                   generation_id=d["generation_id"],
                   description=d["description"],
                   raw=d)
