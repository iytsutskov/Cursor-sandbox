from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
import json
from typing import Dict, Any
from uuid import UUID

from ...application.use_cases.information_system_use_cases import (
    CreateInformationSystemUseCase,
    UpdateInformationSystemUseCase,
    GetInformationSystemUseCase,
    ListInformationSystemsUseCase,
    SearchInformationSystemsUseCase,
    GetSystemStatisticsUseCase
)
from ...application.dtos.information_system_dto import (
    CreateInformationSystemRequest,
    SearchRequest,
    SystemOwnerDTO,
    TechnicalSpecificationDTO,
    BusinessFunctionDTO
)
from ...infrastructure.persistence.sqlite_information_system_repository import SQLiteInformationSystemRepository


class InformationSystemAPIView(APIView):
    """API view for information system operations"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = SQLiteInformationSystemRepository()
    
    def get(self, request, system_id=None):
        """Get information system(s)"""
        if system_id:
            # Get specific system
            use_case = GetInformationSystemUseCase(self.repository)
            system = use_case.execute(system_id)
            
            if not system:
                return Response(
                    {"error": "Information system not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            return Response(self._system_to_dict(system))
        else:
            # Get all systems
            use_case = ListInformationSystemsUseCase(self.repository)
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 20))
            
            result = use_case.execute(page=page, page_size=page_size)
            
            return Response({
                "systems": [self._system_to_dict(system) for system in result.systems],
                "pagination": {
                    "total_count": result.total_count,
                    "page": result.page,
                    "page_size": result.page_size,
                    "total_pages": result.total_pages
                }
            })
    
    def post(self, request):
        """Create new information system"""
        try:
            # Validate required fields
            required_fields = ['name', 'code', 'description', 'owner', 'status']
            
            for field in required_fields:
                if field not in request.data:
                    return Response(
                        {"error": f"Missing required field: {field}"}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Construct owner DTO
            owner_data = request.data.get('owner', {})
            department = request.data.get('department', 'IT')
            if isinstance(owner_data, str):
                # If owner is just a string, create a default owner object
                owner_dto = SystemOwnerDTO(
                    name=owner_data,
                    email=f"{str(owner_data).lower().replace(' ', '.')}@company.com",
                    department=department
                )
            else:
                owner_dto = SystemOwnerDTO(
                    name=owner_data.get('name', 'Unknown'),
                    email=owner_data.get('email', 'unknown@company.com'),
                    department=owner_data.get('department', department),
                    phone=owner_data.get('phone')
                )
            
            # Construct technical spec DTO
            tech_spec_data = request.data.get('technical_spec', {})
            tech_spec_dto = TechnicalSpecificationDTO(
                technology_stack=tech_spec_data.get('technology_stack', []),
                programming_languages=tech_spec_data.get('programming_languages', []),
                databases=tech_spec_data.get('databases', []),
                frameworks=tech_spec_data.get('frameworks', []),
                deployment_model=tech_spec_data.get('deployment_model', 'On-premise'),
                hosting_provider=tech_spec_data.get('hosting_provider')
            )
            
            # Construct business functions DTOs
            business_functions_data = request.data.get('business_functions', [])
            criticality_class = request.data.get('criticality_class', 'Business operational')
            business_functions_dtos = []
            for bf_data in business_functions_data:
                bf_dto = BusinessFunctionDTO(
                    name=bf_data.get('name', 'Unknown'),
                    description=bf_data.get('description', ''),
                    criticality=bf_data.get('criticality', 'high' if criticality_class in ['Mission critical', 'Business critical'] else 'medium'),
                    business_processes=bf_data.get('business_processes', [])
                )
                business_functions_dtos.append(bf_dto)
            
            # Create request DTO
            create_request = CreateInformationSystemRequest(
                name=request.data['name'],
                code=request.data['code'],
                description=request.data['description'],
                purpose=request.data.get('purpose', 'Internal system management'),
                owner=owner_dto,
                technical_spec=tech_spec_dto,
                business_functions=business_functions_dtos,
                business_value=request.data.get('business_value', 'High'),
                cost_center=request.data.get('cost_center', 'IT-001'),
                system_type=request.data.get('system_type', 'internal'),
                status=request.data.get('status', 'development'),
                criticality_class=request.data.get('criticality_class', 'Business operational')
            )
            
            # Execute use case
            use_case = CreateInformationSystemUseCase(self.repository)
            created_system = use_case.execute(create_request)
            
            return Response(
                self._system_to_dict(created_system), 
                status=status.HTTP_201_CREATED
            )
            
        except ValueError as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"Internal server error: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def put(self, request, system_id):
        """Update existing information system"""
        try:
            # Get the existing system (system_id is already a UUID from URL pattern)
            system = self.repository.get_by_id(system_id)
            if not system:
                return Response(
                    {'error': 'Information system not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Validate required fields
            required_fields = ['name', 'code', 'description', 'owner', 'status']
            
            for field in required_fields:
                if field not in request.data:
                    return Response(
                        {'error': f'Field "{field}" is required'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Construct owner DTO
            owner_data = request.data.get('owner', {})
            department = request.data.get('department', 'IT')
            if isinstance(owner_data, str):
                # If owner is just a string, create a default owner object
                owner_dto = SystemOwnerDTO(
                    name=owner_data,
                    email=f"{str(owner_data).lower().replace(' ', '.')}@company.com",
                    department=department
                )
            else:
                owner_dto = SystemOwnerDTO(
                    name=owner_data.get('name', 'Unknown'),
                    email=owner_data.get('email', 'unknown@company.com'),
                    department=owner_data.get('department', department),
                    phone=owner_data.get('phone')
                )
            
            # Construct technical spec DTO
            tech_spec_data = request.data.get('technical_spec', {})
            tech_spec_dto = TechnicalSpecificationDTO(
                technology_stack=tech_spec_data.get('technology_stack', []),
                programming_languages=tech_spec_data.get('programming_languages', []),
                databases=tech_spec_data.get('databases', []),
                frameworks=tech_spec_data.get('frameworks', []),
                deployment_model=tech_spec_data.get('deployment_model', 'On-premise'),
                hosting_provider=tech_spec_data.get('hosting_provider')
            )
            
            # Construct business functions DTOs
            business_functions_data = request.data.get('business_functions', [])
            criticality_class = request.data.get('criticality_class', 'Business operational')
            business_functions_dtos = []
            for bf_data in business_functions_data:
                bf_dto = BusinessFunctionDTO(
                    name=bf_data.get('name', 'Unknown'),
                    description=bf_data.get('description', ''),
                    criticality=bf_data.get('criticality', 'high' if criticality_class in ['Mission critical', 'Business critical'] else 'medium'),
                    business_processes=bf_data.get('business_processes', [])
                )
                business_functions_dtos.append(bf_dto)
            
            # Create request DTO
            update_request = CreateInformationSystemRequest(
                name=request.data['name'],
                code=request.data['code'],
                description=request.data['description'],
                purpose=request.data.get('purpose', 'Internal system management'),
                owner=owner_dto,
                technical_spec=tech_spec_dto,
                business_functions=business_functions_dtos,
                business_value=request.data.get('business_value', 'High'),
                cost_center=request.data.get('cost_center', 'IT-001'),
                system_type=request.data.get('system_type', 'internal'),
                status=request.data.get('status', 'development'),
                criticality_class=request.data.get('criticality_class', 'Business operational')
            )
            
            # Execute use case to update the system
            use_case = UpdateInformationSystemUseCase(self.repository)
            updated_system = use_case.execute(system_id, update_request)
            
            # Convert to DTO for response
            return Response(
                self._system_to_dict(updated_system), 
                status=status.HTTP_200_OK
            )
            
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Internal server error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _system_to_dict(self, system) -> Dict[str, Any]:
        """Convert system DTO to dictionary for JSON response"""
        return {
            "id": str(system.id),
            "name": system.name,
            "code": system.code,
            "description": system.description,
            "purpose": system.purpose,
            "status": system.status,
            "system_type": system.system_type,
            "owner": {
                "name": system.owner.name,
                "email": system.owner.email,
                "department": system.owner.department,
                "phone": system.owner.phone
            },
            "technical_spec": {
                "technology_stack": system.technical_spec.technology_stack,
                "programming_languages": system.technical_spec.programming_languages,
                "databases": system.technical_spec.databases,
                "frameworks": system.technical_spec.frameworks,
                "deployment_model": system.technical_spec.deployment_model,
                "hosting_provider": system.technical_spec.hosting_provider
            },
            "business_functions": [
                {
                    "name": func.name,
                    "description": func.description,
                    "criticality": func.criticality,
                    "business_processes": func.business_processes
                }
                for func in system.business_functions
            ],
            "business_value": system.business_value,
            "cost_center": system.cost_center,
            "created_at": system.created_at.isoformat(),
            "updated_at": system.updated_at.isoformat(),
            "version": system.version,
            "parent_system_id": str(system.parent_system_id) if system.parent_system_id else None,
            "dependent_systems": [str(sid) for sid in system.dependent_systems],
            "is_critical": system.is_critical,
            "criticality_class": system.criticality_class,
            "dataflows": [
                {
                    "id": str(df.id),
                    "source_system_id": str(df.source_system_id),
                    "target_system_id": str(df.target_system_id),
                    "data_objects": df.data_objects,
                    "integration_technology": df.integration_technology,
                    "description": df.description,
                    "frequency": df.frequency,
                    "created_at": df.created_at.isoformat(),
                    "updated_at": df.updated_at.isoformat()
                }
                for df in (system.dataflows or [])
            ]
        }


class SearchInformationSystemsAPIView(APIView):
    """API view for searching information systems"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = SQLiteInformationSystemRepository()
    
    def get(self, request):
        """Search information systems"""
        try:
            # Get search parameters
            query = request.GET.get('q', '')
            status_filter = request.GET.get('status')
            system_type = request.GET.get('system_type')
            department = request.GET.get('department')
            technology = request.GET.get('technology')
            criticality = request.GET.get('criticality')
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 20))
            
            # Create search request
            search_request = SearchRequest(
                query=query,
                status=status_filter,
                system_type=system_type,
                department=department,
                technology=technology,
                criticality=criticality,
                page=page,
                page_size=page_size
            )
            
            # Execute use case
            use_case = SearchInformationSystemsUseCase(self.repository)
            result = use_case.execute(search_request)
            
            return Response({
                "systems": [self._system_to_dict(system) for system in result.systems],
                "pagination": {
                    "total_count": result.total_count,
                    "page": result.page,
                    "page_size": result.page_size,
                    "total_pages": result.total_pages
                }
            })
            
        except Exception as e:
            return Response(
                {"error": f"Internal server error: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _system_to_dict(self, system) -> Dict[str, Any]:
        """Convert system DTO to dictionary for JSON response"""
        return {
            "id": str(system.id),
            "name": system.name,
            "code": system.code,
            "description": system.description,
            "purpose": system.purpose,
            "status": system.status,
            "system_type": system.system_type,
            "owner": {
                "name": system.owner.name,
                "email": system.owner.email,
                "department": system.owner.department,
                "phone": system.owner.phone
            },
            "technical_spec": {
                "technology_stack": system.technical_spec.technology_stack,
                "programming_languages": system.technical_spec.programming_languages,
                "databases": system.technical_spec.databases,
                "frameworks": system.technical_spec.frameworks,
                "deployment_model": system.technical_spec.deployment_model,
                "hosting_provider": system.technical_spec.hosting_provider
            },
            "business_functions": [
                {
                    "name": func.name,
                    "description": func.description,
                    "criticality": func.criticality,
                    "business_processes": func.business_processes
                }
                for func in system.business_functions
            ],
            "business_value": system.business_value,
            "cost_center": system.cost_center,
            "created_at": system.created_at.isoformat(),
            "updated_at": system.updated_at.isoformat(),
            "version": system.version,
            "parent_system_id": str(system.parent_system_id) if system.parent_system_id else None,
            "dependent_systems": [str(sid) for sid in system.dependent_systems],
            "is_critical": system.is_critical,
            "criticality_class": system.criticality_class,
            "dataflows": [
                {
                    "id": str(df.id),
                    "source_system_id": str(df.source_system_id),
                    "target_system_id": str(df.target_system_id),
                    "data_objects": df.data_objects,
                    "integration_technology": df.integration_technology,
                    "description": df.description,
                    "frequency": df.frequency,
                    "created_at": df.created_at.isoformat(),
                    "updated_at": df.updated_at.isoformat()
                }
                for df in (system.dataflows or [])
            ]
        }


class SystemStatisticsAPIView(APIView):
    """API view for system statistics"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = SQLiteInformationSystemRepository()
    
    def get(self, request):
        """Get system statistics"""
        try:
            use_case = GetSystemStatisticsUseCase(self.repository)
            stats = use_case.execute()
            
            return Response({
                "total_systems": stats.total_systems,
                "development_systems": stats.development_systems,
                "production_systems": stats.production_systems or 0,
                "deprecated_systems": stats.deprecated_systems,
                "critical_systems": stats.critical_systems,
                "systems_by_type": stats.systems_by_type,
                "systems_by_department": stats.systems_by_department,
                "top_technologies": stats.top_technologies
            })
            
        except Exception as e:
            return Response(
                {"error": f"Internal server error: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# Legacy function-based views for compatibility
@api_view(['GET'])
def get_system_statistics(request):
    """Get system statistics (legacy function-based view)"""
    try:
        repository = SQLiteInformationSystemRepository()
        use_case = GetSystemStatisticsUseCase(repository)
        stats = use_case.execute()
        
        return JsonResponse({
            "total_systems": stats.total_systems,
            "development_systems": stats.development_systems,
            "production_systems": stats.production_systems or 0,
            "deprecated_systems": stats.deprecated_systems,
            "critical_systems": stats.critical_systems,
            "systems_by_type": stats.systems_by_type,
            "systems_by_department": stats.systems_by_department,
            "top_technologies": stats.top_technologies
        })
        
    except Exception as e:
        return JsonResponse(
            {"error": f"Internal server error: {str(e)}"}, 
            status=500
        )
