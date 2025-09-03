from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4
from enum import Enum


class SystemStatus(Enum):
    """Information System Status enumeration"""
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    DEPRECATED = "deprecated"


class SystemType(Enum):
    """Information System Type enumeration"""
    INTERNAL = "internal"
    EXTERNAL = "external"
    CLOUD = "cloud"


@dataclass
class SystemOwner:
    """Value object for system ownership information"""
    name: str
    email: str
    department: str
    phone: Optional[str] = None


@dataclass
class TechnicalSpecification:
    """Value object for technical specifications"""
    technology_stack: List[str]
    programming_languages: List[str]
    databases: List[str]
    frameworks: List[str]
    deployment_model: str
    hosting_provider: Optional[str] = None


@dataclass
class BusinessFunction:
    """Value object for business functions supported by the system"""
    name: str
    description: str
    criticality: str  # high, medium, low
    business_processes: List[str]


@dataclass
class InformationSystem:
    """Core domain entity for Information System"""
    
    # Identity
    id: UUID
    name: str
    code: str  # Unique business code
    
    # Basic Information
    description: str
    purpose: str
    status: SystemStatus
    system_type: SystemType
    
    # Ownership
    owner: SystemOwner
    
    # Technical Details
    technical_spec: TechnicalSpecification
    
    # Business Context
    business_functions: List[BusinessFunction]
    business_value: str
    
    # Metadata
    created_at: datetime
    updated_at: datetime
    
    # Relationships
    parent_system_id: Optional[UUID] = None
    dependent_systems: List[UUID] = None
    
    # Optional fields with defaults
    cost_center: Optional[str] = None
    version: str = "1.0.0"
    criticality_class: str = "Business operational"
    dataflows: List['DataFlow'] = field(default_factory=list)
    
    def __post_init__(self):
        if self.dependent_systems is None:
            self.dependent_systems = []
    
    def activate(self) -> None:
        """Activate the system (move to production)"""
        if self.status != SystemStatus.PRODUCTION:
            self.status = SystemStatus.PRODUCTION
            self.updated_at = datetime.utcnow()
    
    def deactivate(self) -> None:
        """Deactivate the system (move to deprecated)"""
        if self.status != SystemStatus.DEPRECATED:
            self.status = SystemStatus.DEPRECATED
            self.updated_at = datetime.utcnow()
    
    def deprecate(self) -> None:
        """Mark system as deprecated"""
        if self.status != SystemStatus.DEPRECATED:
            self.status = SystemStatus.DEPRECATED
            self.updated_at = datetime.utcnow()
    
    def update_version(self, new_version: str) -> None:
        """Update system version"""
        self.version = new_version
        self.updated_at = datetime.utcnow()
    
    def add_business_function(self, business_function: BusinessFunction) -> None:
        """Add a new business function"""
        self.business_functions.append(business_function)
        self.updated_at = datetime.utcnow()
    
    def remove_business_function(self, function_name: str) -> bool:
        """Remove a business function by name"""
        initial_count = len(self.business_functions)
        self.business_functions = [f for f in self.business_functions if f.name != function_name]
        if len(self.business_functions) < initial_count:
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def add_dependent_system(self, system_id: UUID) -> None:
        """Add a dependent system"""
        if system_id not in self.dependent_systems:
            self.dependent_systems.append(system_id)
            self.updated_at = datetime.utcnow()
    
    def remove_dependent_system(self, system_id: UUID) -> bool:
        """Remove a dependent system"""
        if system_id in self.dependent_systems:
            self.dependent_systems.remove(system_id)
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def add_dataflow(self, dataflow: 'DataFlow') -> None:
        """Add a new dataflow"""
        if self.dataflows is None:
            self.dataflows = []
        self.dataflows.append(dataflow)
        self.updated_at = datetime.utcnow()
    
    def remove_dataflow(self, dataflow_id: UUID) -> bool:
        """Remove a dataflow by ID"""
        if self.dataflows is None:
            return False
        initial_count = len(self.dataflows)
        self.dataflows = [df for df in self.dataflows if df.id != dataflow_id]
        if len(self.dataflows) < initial_count:
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def get_incoming_dataflows(self) -> List['DataFlow']:
        """Get dataflows where this system is the target"""
        if self.dataflows is None:
            return []
        return [df for df in self.dataflows if df.target_system_id == self.id]
    
    def get_outgoing_dataflows(self) -> List['DataFlow']:
        """Get dataflows where this system is the source"""
        if self.dataflows is None:
            return []
        return [df for df in self.dataflows if df.source_system_id == self.id]
    
    def is_critical(self) -> bool:
        """Check if system has any critical business functions"""
        return any(func.criticality == "high" for func in self.business_functions)
    
    def get_technology_summary(self) -> str:
        """Get a summary of technologies used"""
        return f"{', '.join(self.technical_spec.technology_stack)} | {', '.join(self.technical_spec.programming_languages)}"
    
    @classmethod
    def create(
        cls,
        name: str,
        code: str,
        description: str,
        purpose: str,
        owner: SystemOwner,
        technical_spec: TechnicalSpecification,
        business_functions: List[BusinessFunction],
        business_value: str,
        system_type: SystemType = SystemType.INTERNAL,
        status: SystemStatus = SystemStatus.DEVELOPMENT,
        criticality_class: str = "Business operational"
    ) -> 'InformationSystem':
        """Factory method to create a new Information System"""
        now = datetime.utcnow()
        return cls(
            id=uuid4(),
            name=name,
            code=code,
            description=description,
            purpose=purpose,
            status=status,
            system_type=system_type,
            owner=owner,
            technical_spec=technical_spec,
            business_functions=business_functions,
            business_value=business_value,
            criticality_class=criticality_class,
            created_at=now,
            updated_at=now
        )


@dataclass
class DataFlow:
    """Data flow between information systems"""
    id: UUID
    source_system_id: UUID
    target_system_id: UUID
    data_objects: List[str]
    integration_technology: str
    description: Optional[str] = None
    frequency: str = "real-time"
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        if self.id is None:
            self.id = uuid4()
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()
    
    def update_data_objects(self, new_data_objects: List[str]) -> None:
        """Update data objects"""
        self.data_objects = new_data_objects
        self.updated_at = datetime.utcnow()
    
    def update_integration_technology(self, new_technology: str) -> None:
        """Update integration technology"""
        self.integration_technology = new_technology
        self.updated_at = datetime.utcnow()
    
    def update_description(self, new_description: str) -> None:
        """Update description"""
        self.description = new_description
        self.updated_at = datetime.utcnow()
    
    def update_frequency(self, new_frequency: str) -> None:
        """Update frequency"""
        self.frequency = new_frequency
        self.updated_at = datetime.utcnow()
    
    @classmethod
    def create(
        cls,
        source_system_id: UUID,
        target_system_id: UUID,
        data_objects: List[str],
        integration_technology: str,
        description: Optional[str] = None,
        frequency: str = "real-time"
    ) -> 'DataFlow':
        """Factory method to create a new Data Flow"""
        now = datetime.utcnow()
        return cls(
            id=uuid4(),
            source_system_id=source_system_id,
            target_system_id=target_system_id,
            data_objects=data_objects,
            integration_technology=integration_technology,
            description=description,
            frequency=frequency,
            created_at=now,
            updated_at=now
        )
