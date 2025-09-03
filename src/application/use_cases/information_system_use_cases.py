from typing import List, Optional
from uuid import UUID
from datetime import datetime

from ...domain.entities.information_system import (
    InformationSystem, SystemStatus, SystemType, SystemOwner, 
    TechnicalSpecification, BusinessFunction, DataFlow
)
from ...domain.repositories.information_system_repository import InformationSystemRepository
from ..dtos.information_system_dto import (
    CreateInformationSystemRequest, UpdateInformationSystemRequest,
    InformationSystemDTO, InformationSystemListResponse, SearchRequest,
    SystemStatisticsResponse, SystemOwnerDTO, TechnicalSpecificationDTO, BusinessFunctionDTO,
    DataFlowDTO
)


class CreateInformationSystemUseCase:
    """Use case for creating a new information system"""
    
    def __init__(self, repository: InformationSystemRepository):
        self.repository = repository
    
    def execute(self, request: CreateInformationSystemRequest) -> InformationSystemDTO:
        """Execute the create information system use case"""
        
        # Validate business code uniqueness
        existing_system = self.repository.get_by_code(request.code)
        if existing_system:
            raise ValueError(f"Information system with code '{request.code}' already exists")
        
        # Convert DTOs to domain objects
        owner = SystemOwner(
            name=request.owner.name,
            email=request.owner.email,
            department=request.owner.department,
            phone=request.owner.phone
        )
        
        technical_spec = TechnicalSpecification(
            technology_stack=request.technical_spec.technology_stack,
            programming_languages=request.technical_spec.programming_languages,
            databases=request.technical_spec.databases,
            frameworks=request.technical_spec.frameworks,
            deployment_model=request.technical_spec.deployment_model,
            hosting_provider=request.technical_spec.hosting_provider
        )
        
        business_functions = [
            BusinessFunction(
                name=func.name,
                description=func.description,
                criticality=func.criticality,
                business_processes=func.business_processes
            )
            for func in request.business_functions
        ]
        
        # Create domain entity
        information_system = InformationSystem.create(
            name=request.name,
            code=request.code,
            description=request.description,
            purpose=request.purpose,
            owner=owner,
            technical_spec=technical_spec,
            business_functions=business_functions,
            business_value=request.business_value,
            system_type=SystemType(request.system_type),
            status=SystemStatus(request.status),
            criticality_class=request.criticality_class
        )
        
        if request.cost_center:
            information_system.cost_center = request.cost_center
        
        # Save to repository
        saved_system = self.repository.save(information_system)
        
        # Return DTO
        return self._to_dto(saved_system)
    
    def _to_dto(self, system: InformationSystem) -> InformationSystemDTO:
        """Convert domain entity to DTO"""
        return InformationSystemDTO(
            id=system.id,
            name=system.name,
            code=system.code,
            description=system.description,
            purpose=system.purpose,
            status=system.status.value,
            system_type=system.system_type.value,
            owner=SystemOwnerDTO(
                name=system.owner.name,
                email=system.owner.email,
                department=system.owner.department,
                phone=system.owner.phone
            ),
            technical_spec=TechnicalSpecificationDTO(
                technology_stack=system.technical_spec.technology_stack,
                programming_languages=system.technical_spec.programming_languages,
                databases=system.technical_spec.databases,
                frameworks=system.technical_spec.frameworks,
                deployment_model=system.technical_spec.deployment_model,
                hosting_provider=system.technical_spec.hosting_provider
            ),
            business_functions=[
                BusinessFunctionDTO(
                    name=func.name,
                    description=func.description,
                    criticality=func.criticality,
                    business_processes=func.business_processes
                )
                for func in system.business_functions
            ],
            business_value=system.business_value,
            cost_center=system.cost_center,
            created_at=system.created_at,
            updated_at=system.updated_at,
            version=system.version,
            parent_system_id=system.parent_system_id,
            dependent_systems=system.dependent_systems,
            is_critical=system.is_critical(),
            criticality_class=getattr(system, 'criticality_class', 'Business operational'),
            dataflows=[
                DataFlowDTO(
                    id=df.id,
                    source_system_id=df.source_system_id,
                    target_system_id=df.target_system_id,
                    data_objects=df.data_objects,
                    integration_technology=df.integration_technology,
                    description=df.description,
                    frequency=df.frequency,
                    created_at=df.created_at,
                    updated_at=df.updated_at
                )
                for df in (system.dataflows or [])
            ]
        )


class UpdateInformationSystemUseCase:
    """Use case for updating an existing information system"""
    
    def __init__(self, repository: InformationSystemRepository):
        self.repository = repository
    
    def execute(self, system_id: UUID, request: CreateInformationSystemRequest) -> InformationSystemDTO:
        """Execute the update information system use case"""
        
        # Get the existing system
        existing_system = self.repository.get_by_id(system_id)
        if not existing_system:
            raise ValueError(f"Information system with id '{system_id}' not found")
        
        # Validate business code uniqueness (if code changed)
        if existing_system.code != request.code:
            code_exists = self.repository.get_by_code(request.code)
            if code_exists and str(code_exists.id) != str(system_id):
                raise ValueError(f"Information system with code '{request.code}' already exists")
        
        # Convert DTOs to domain objects
        owner = SystemOwner(
            name=request.owner.name,
            email=request.owner.email,
            department=request.owner.department,
            phone=request.owner.phone
        )
        
        technical_spec = TechnicalSpecification(
            technology_stack=request.technical_spec.technology_stack,
            programming_languages=request.technical_spec.programming_languages,
            databases=request.technical_spec.databases,
            frameworks=request.technical_spec.frameworks,
            deployment_model=request.technical_spec.deployment_model,
            hosting_provider=request.technical_spec.hosting_provider
        )
        
        business_functions = [
            BusinessFunction(
                name=func.name,
                description=func.description,
                criticality=func.criticality,
                business_processes=func.business_processes
            )
            for func in request.business_functions
        ]
        
        # Update the existing system
        existing_system.name = request.name
        existing_system.code = request.code
        existing_system.description = request.description
        existing_system.purpose = request.purpose
        existing_system.status = SystemStatus(request.status)
        existing_system.system_type = SystemType(request.system_type)
        existing_system.owner = owner
        existing_system.technical_spec = technical_spec
        existing_system.business_functions = business_functions
        existing_system.business_value = request.business_value
        existing_system.cost_center = request.cost_center
        existing_system.criticality_class = request.criticality_class
        existing_system.updated_at = datetime.utcnow()
        
        # Save to repository
        saved_system = self.repository.save(existing_system)
        
        # Return DTO
        return self._to_dto(saved_system)
    
    def _to_dto(self, system: InformationSystem) -> InformationSystemDTO:
        """Convert domain entity to DTO"""
        return InformationSystemDTO(
            id=system.id,
            name=system.name,
            code=system.code,
            description=system.description,
            purpose=system.purpose,
            status=system.status.value,
            system_type=system.system_type.value,
            owner=SystemOwnerDTO(
                name=system.owner.name,
                email=system.owner.email,
                department=system.owner.department,
                phone=system.owner.phone
            ),
            technical_spec=TechnicalSpecificationDTO(
                technology_stack=system.technical_spec.technology_stack,
                programming_languages=system.technical_spec.programming_languages,
                databases=system.technical_spec.databases,
                frameworks=system.technical_spec.frameworks,
                deployment_model=system.technical_spec.deployment_model,
                hosting_provider=system.technical_spec.hosting_provider
            ),
            business_functions=[
                BusinessFunctionDTO(
                    name=func.name,
                    description=func.description,
                    criticality=func.criticality,
                    business_processes=func.business_processes
                )
                for func in system.business_functions
            ],
            business_value=system.business_value,
            cost_center=system.cost_center,
            created_at=system.created_at,
            updated_at=system.updated_at,
            version=system.version,
            parent_system_id=system.parent_system_id,
            dependent_systems=system.dependent_systems,
            is_critical=system.is_critical(),
            criticality_class=getattr(system, 'criticality_class', 'Business operational'),
            dataflows=[
                DataFlowDTO(
                    id=df.id,
                    source_system_id=df.source_system_id,
                    target_system_id=df.target_system_id,
                    data_objects=df.data_objects,
                    integration_technology=df.integration_technology,
                    description=df.description,
                    frequency=df.frequency,
                    created_at=df.created_at,
                    updated_at=df.updated_at
                )
                for df in (system.dataflows or [])
            ]
        )


class GetInformationSystemUseCase:
    """Use case for retrieving an information system"""
    
    def __init__(self, repository: InformationSystemRepository):
        self.repository = repository
    
    def execute(self, system_id: UUID) -> Optional[InformationSystemDTO]:
        """Execute the get information system use case"""
        system = self.repository.get_by_id(system_id)
        if not system:
            return None
        
        return self._to_dto(system)
    
    def _to_dto(self, system: InformationSystem) -> InformationSystemDTO:
        """Convert domain entity to DTO"""
        return InformationSystemDTO(
            id=system.id,
            name=system.name,
            code=system.code,
            description=system.description,
            purpose=system.purpose,
            status=system.status.value,
            system_type=system.system_type.value,
            owner=SystemOwnerDTO(
                name=system.owner.name,
                email=system.owner.email,
                department=system.owner.department,
                phone=system.owner.phone
            ),
            technical_spec=TechnicalSpecificationDTO(
                technology_stack=system.technical_spec.technology_stack,
                programming_languages=system.technical_spec.programming_languages,
                databases=system.technical_spec.databases,
                frameworks=system.technical_spec.frameworks,
                deployment_model=system.technical_spec.deployment_model,
                hosting_provider=system.technical_spec.hosting_provider
            ),
            business_functions=[
                BusinessFunctionDTO(
                    name=func.name,
                    description=func.description,
                    criticality=func.criticality,
                    business_processes=func.business_processes
                )
                for func in system.business_functions
            ],
            business_value=system.business_value,
            cost_center=system.cost_center,
            created_at=system.created_at,
            updated_at=system.updated_at,
            version=system.version,
            parent_system_id=system.parent_system_id,
            dependent_systems=system.dependent_systems,
            is_critical=system.is_critical(),
            criticality_class=getattr(system, 'criticality_class', 'Business operational'),
            dataflows=[
                DataFlowDTO(
                    id=df.id,
                    source_system_id=df.source_system_id,
                    target_system_id=df.target_system_id,
                    data_objects=df.data_objects,
                    integration_technology=df.integration_technology,
                    description=df.description,
                    frequency=df.frequency,
                    created_at=df.created_at,
                    updated_at=df.updated_at
                )
                for df in (system.dataflows or [])
            ]
        )


class ListInformationSystemsUseCase:
    """Use case for listing information systems"""
    
    def __init__(self, repository: InformationSystemRepository):
        self.repository = repository
    
    def execute(self, page: int = 1, page_size: int = 20) -> InformationSystemListResponse:
        """Execute the list information systems use case"""
        all_systems = self.repository.get_all()
        
        # Simple pagination (in production, use database-level pagination)
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        paginated_systems = all_systems[start_index:end_index]
        
        total_count = len(all_systems)
        total_pages = (total_count + page_size - 1) // page_size
        
        return InformationSystemListResponse(
            systems=[self._to_dto(system) for system in paginated_systems],
            total_count=total_count,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    
    def _to_dto(self, system: InformationSystem) -> InformationSystemDTO:
        """Convert domain entity to DTO"""
        return InformationSystemDTO(
            id=system.id,
            name=system.name,
            code=system.code,
            description=system.description,
            purpose=system.purpose,
            status=system.status.value,
            system_type=system.system_type.value,
            owner=SystemOwnerDTO(
                name=system.owner.name,
                email=system.owner.email,
                department=system.owner.department,
                phone=system.owner.phone
            ),
            technical_spec=TechnicalSpecificationDTO(
                technology_stack=system.technical_spec.technology_stack,
                programming_languages=system.technical_spec.programming_languages,
                databases=system.technical_spec.databases,
                frameworks=system.technical_spec.frameworks,
                deployment_model=system.technical_spec.deployment_model,
                hosting_provider=system.technical_spec.hosting_provider
            ),
            business_functions=[
                BusinessFunctionDTO(
                    name=func.name,
                    description=func.description,
                    criticality=func.criticality,
                    business_processes=func.business_processes
                )
                for func in system.business_functions
            ],
            business_value=system.business_value,
            cost_center=system.cost_center,
            created_at=system.created_at,
            updated_at=system.updated_at,
            version=system.version,
            parent_system_id=system.parent_system_id,
            dependent_systems=system.dependent_systems,
            is_critical=system.is_critical(),
            criticality_class=getattr(system, 'criticality_class', 'Business operational'),
            dataflows=[
                DataFlowDTO(
                    id=df.id,
                    source_system_id=df.source_system_id,
                    target_system_id=df.target_system_id,
                    data_objects=df.data_objects,
                    integration_technology=df.integration_technology,
                    description=df.description,
                    frequency=df.frequency,
                    created_at=df.created_at,
                    updated_at=df.updated_at
                )
                for df in (system.dataflows or [])
            ]
        )


class SearchInformationSystemsUseCase:
    """Use case for searching information systems"""
    
    def __init__(self, repository: InformationSystemRepository):
        self.repository = repository
    
    def execute(self, request: SearchRequest) -> InformationSystemListResponse:
        """Execute the search information systems use case"""
        # For now, use simple search. In production, implement advanced search logic
        all_systems = self.repository.get_all()
        
        # Apply filters
        filtered_systems = all_systems
        
        if request.status:
            filtered_systems = [s for s in filtered_systems if s.status.value == request.status]
        
        if request.system_type:
            filtered_systems = [s for s in filtered_systems if s.system_type.value == request.system_type]
        
        if request.department:
            filtered_systems = [s for s in filtered_systems if s.owner.department == request.department]
        
        if request.technology:
            filtered_systems = [
                s for s in filtered_systems 
                if request.technology in s.technical_spec.technology_stack
            ]
        
        if request.criticality:
            filtered_systems = [
                s for s in filtered_systems 
                if any(func.criticality == request.criticality for func in s.business_functions)
            ]
        
        # Apply text search
        if request.query:
            query_lower = request.query.lower()
            filtered_systems = [
                s for s in filtered_systems
                if (query_lower in s.name.lower() or 
                    query_lower in s.description.lower() or 
                    query_lower in s.code.lower())
            ]
        
        # Pagination
        total_count = len(filtered_systems)
        start_index = (request.page - 1) * request.page_size
        end_index = start_index + request.page_size
        paginated_systems = filtered_systems[start_index:end_index]
        
        total_pages = (total_count + request.page_size - 1) // request.page_size
        
        return InformationSystemListResponse(
            systems=[self._to_dto(system) for system in paginated_systems],
            total_count=total_count,
            page=request.page,
            page_size=request.page_size,
            total_pages=total_pages
        )
    
    def _to_dto(self, system: InformationSystem) -> InformationSystemDTO:
        """Convert domain entity to DTO"""
        return InformationSystemDTO(
            id=system.id,
            name=system.name,
            code=system.code,
            description=system.description,
            purpose=system.purpose,
            status=system.status.value,
            system_type=system.system_type.value,
            owner=SystemOwnerDTO(
                name=system.owner.name,
                email=system.owner.email,
                department=system.owner.department,
                phone=system.owner.phone
            ),
            technical_spec=TechnicalSpecificationDTO(
                technology_stack=system.technical_spec.technology_stack,
                programming_languages=system.technical_spec.programming_languages,
                databases=system.technical_spec.databases,
                frameworks=system.technical_spec.frameworks,
                deployment_model=system.technical_spec.deployment_model,
                hosting_provider=system.technical_spec.hosting_provider
            ),
            business_functions=[
                BusinessFunctionDTO(
                    name=func.name,
                    description=func.description,
                    criticality=func.criticality,
                    business_processes=func.business_processes
                )
                for func in system.business_functions
            ],
            business_value=system.business_value,
            cost_center=system.cost_center,
            created_at=system.created_at,
            updated_at=system.updated_at,
            version=system.version,
            parent_system_id=system.parent_system_id,
            dependent_systems=system.dependent_systems,
            is_critical=system.is_critical(),
            criticality_class=getattr(system, 'criticality_class', 'Business operational'),
            dataflows=[
                DataFlowDTO(
                    id=df.id,
                    source_system_id=df.source_system_id,
                    target_system_id=df.target_system_id,
                    data_objects=df.data_objects,
                    integration_technology=df.integration_technology,
                    description=df.description,
                    frequency=df.frequency,
                    created_at=df.created_at,
                    updated_at=df.updated_at
                )
                for df in (system.dataflows or [])
            ]
        )


class GetSystemStatisticsUseCase:
    """Use case for getting system statistics"""
    
    def __init__(self, repository: InformationSystemRepository):
        self.repository = repository
    
    def execute(self) -> SystemStatisticsResponse:
        """Execute the get system statistics use case"""
        all_systems = self.repository.get_all()
        
        # Calculate statistics
        total_systems = len(all_systems)
        development_systems = len([s for s in all_systems if s.status == SystemStatus.DEVELOPMENT])
        production_systems = len([s for s in all_systems if s.status == SystemStatus.PRODUCTION])
        deprecated_systems = len([s for s in all_systems if s.status == SystemStatus.DEPRECATED])
        critical_systems = len([s for s in all_systems if s.is_critical()])
        
        # Systems by type
        systems_by_type = {}
        for system in all_systems:
            system_type = system.system_type.value
            systems_by_type[system_type] = systems_by_type.get(system_type, 0) + 1
        
        # Systems by department
        systems_by_department = {}
        for system in all_systems:
            department = system.owner.department
            systems_by_department[department] = systems_by_department.get(department, 0) + 1
        
        # Top technologies
        technology_count = {}
        for system in all_systems:
            for tech in system.technical_spec.technology_stack:
                technology_count[tech] = technology_count.get(tech, 0) + 1
        
        top_technologies = [
            {"technology": tech, "count": count}
            for tech, count in sorted(technology_count.items(), key=lambda x: x[1], reverse=True)[:10]
        ]
        
        return SystemStatisticsResponse(
            total_systems=total_systems,
            development_systems=development_systems,
            production_systems=production_systems,
            deprecated_systems=deprecated_systems,
            critical_systems=critical_systems,
            systems_by_type=systems_by_type,
            systems_by_department=systems_by_department,
            top_technologies=top_technologies
        )
