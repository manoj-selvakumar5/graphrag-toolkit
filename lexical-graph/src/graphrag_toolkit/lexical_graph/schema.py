from dataclasses import dataclass
from typing import List

@dataclass
class EntityType:
    """
    Represents a type of entity in the knowledge graph.

    Attributes:
        name (str): The name of the entity type
        description (str): A description of what this entity type represents
        examples (List[str]): Example values for this entity type
    """
    name: str
    description: str
    examples: List[str]

@dataclass
class RelationType:
    """
    Represents a type of relation in the knowledge graph.

    Attributes:
        name (str): The name of the relation type
        description (str): A description of what this relation type represents
        examples (List[str]): Example statements showing how this relation is used
    """
    name: str
    description: str
    examples: List[str] 