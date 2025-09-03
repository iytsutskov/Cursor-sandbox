from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from ...domain.entities.information_system import SystemStatus, SystemType


@dataclass
class SystemOwnerDTO:
    """DTO for system owner information"""
    name: str
    email: str
    department: str
    phone: Optional[str] = None


@dataclass
class TechnicalSpecificationDTO:
    """DTO for technical specifications"""
    technology_stack: List[str]
    programming_languages: List[str]
    databases: List[str]
    frameworks: List[str]
    deployment_model: str
    hosting_provider: Optional[str] = None


@dataclass
class BusinessFunctionDTO:
    """DTO for business functions"""
    name: str
    description: str
    criticality: str
    business_processes: List[str]


@dataclass
class InformationSystemDTO:
    """DTO for information system data transfer"""
    id: UUID
    name: str
    code: str
    description: str
    purpose: str
    status: str
    system_type: str
    owner: SystemOwnerDTO
    technical_spec: TechnicalSpecificationDTO
    business_functions: List[BusinessFunctionDTO]
    business_value: str
    created_at: datetime
    updated_at: datetime
    version: str
    dependent_systems: List[UUID]
    is_critical: bool
    criticality_class: str
    parent_system_id: Optional[UUID] = None
    cost_center: Optional[str] = None
    dataflows: List['DataFlowDTO'] = field(default_factory=list)


@dataclass
class CreateInformationSystemRequest:
    """Request DTO for creating a new information system"""
    name: str
    code: str
    description: str
    purpose: str
    owner: SystemOwnerDTO
    technical_spec: TechnicalSpecificationDTO
    business_functions: List[BusinessFunctionDTO]
    business_value: str
    cost_center: Optional[str] = None
    system_type: str = "internal"
    status: str = "development"
    criticality_class: str = "Business operational"


@dataclass
class UpdateInformationSystemRequest:
    """Request DTO for updating an information system"""
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    purpose: Optional[str] = None
    owner: Optional[SystemOwnerDTO] = None
    technical_spec: Optional[TechnicalSpecificationDTO] = None
    business_functions: Optional[List[BusinessFunctionDTO]] = None
    business_value: Optional[str] = None
    cost_center: Optional[str] = None
    system_type: Optional[str] = None
    status: Optional[str] = None
    version: Optional[str] = None
    criticality_class: Optional[str] = None


@dataclass
class InformationSystemListResponse:
    """Response DTO for information system list"""
    systems: List[InformationSystemDTO]
    total_count: int
    page: int
    page_size: int
    total_pages: int


@dataclass
class SearchRequest:
    """Request DTO for searching information systems"""
    query: str
    status: Optional[str] = None
    system_type: Optional[str] = None
    department: Optional[str] = None
    technology: Optional[str] = None
    criticality: Optional[str] = None
    page: int = 1
    page_size: int = 20


@dataclass
class DataFlowDTO:
    """DTO for data flow information"""
    id: UUID
    source_system_id: UUID
    target_system_id: UUID
    data_objects: List[str]
    integration_technology: str
    created_at: datetime
    updated_at: datetime
    description: Optional[str] = None
    frequency: str = "real-time"


@dataclass
class CreateDataFlowRequest:
    """Request DTO for creating a new data flow"""
    source_system_id: UUID
    target_system_id: UUID
    data_objects: List[str]
    integration_technology: str
    description: Optional[str] = None
    frequency: str = "real-time"


@dataclass
class UpdateDataFlowRequest:
    """Request DTO for updating a data flow"""
    data_objects: Optional[List[str]] = None
    integration_technology: Optional[str] = None
    description: Optional[str] = None
    frequency: Optional[str] = None


@dataclass
class SystemStatisticsResponse:
    """Response DTO for system statistics"""
    total_systems: int
    development_systems: int
    production_systems: int
    deprecated_systems: int
    critical_systems: int
    systems_by_type: dict
    systems_by_department: dict
    top_technologies: List[dict]
