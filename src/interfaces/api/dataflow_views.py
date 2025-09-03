from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from typing import Dict, Any
from uuid import UUID

from ...application.use_cases.dataflow_use_cases import (
    CreateDataFlowUseCase,
    UpdateDataFlowUseCase,
    DeleteDataFlowUseCase,
    GetDataFlowsUseCase
)
from ...application.dtos.information_system_dto import (
    CreateDataFlowRequest, UpdateDataFlowRequest
)
from ...infrastructure.persistence.sqlite_information_system_repository import SQLiteInformationSystemRepository


class DataFlowAPIView(APIView):
    """API view for data flow operations"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = SQLiteInformationSystemRepository()
    
    def get(self, request):
        """Get data flows with optional filtering"""
        try:
            system_id = request.GET.get('system_id')
            
            if system_id:
                # Get dataflows for a specific system (both incoming and outgoing)
                use_case = GetDataFlowsUseCase(self.repository)
                dataflows = use_case.execute_for_system(UUID(system_id))
                
                return Response([
                    self._dataflow_to_dict(df) for df in dataflows
                ])
            else:
                # Get all dataflows from all systems
                all_systems = self.repository.get_all()
                all_dataflows = []
                
                for system in all_systems:
                    if system.dataflows:
                        all_dataflows.extend(system.dataflows)
                
                return Response([
                    self._dataflow_to_dict(df) for df in all_dataflows
                ])
                
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
    
    def post(self, request):
        """Create new data flow"""
        try:
            # Validate required fields
            required_fields = ['source_system_id', 'target_system_id', 'data_objects', 'integration_technology']
            
            for field in required_fields:
                if field not in request.data:
                    return Response(
                        {'error': f'Missing required field: {field}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Create request DTO
            create_request = CreateDataFlowRequest(
                source_system_id=UUID(request.data['source_system_id']),
                target_system_id=UUID(request.data['target_system_id']),
                data_objects=request.data['data_objects'],
                integration_technology=request.data['integration_technology'],
                description=request.data.get('description'),
                frequency=request.data.get('frequency', 'real-time')
            )
            
            # Execute use case
            use_case = CreateDataFlowUseCase(self.repository)
            created_dataflow = use_case.execute(create_request)
            
            # Convert to DTO for response
            return Response(
                self._dataflow_to_dict(created_dataflow),
                status=status.HTTP_201_CREATED
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
    
    def put(self, request, dataflow_id):
        """Update existing data flow"""
        try:
            # Create request DTO
            update_request = UpdateDataFlowRequest(
                data_objects=request.data.get('data_objects'),
                integration_technology=request.data.get('integration_technology'),
                description=request.data.get('description'),
                frequency=request.data.get('frequency')
            )
            
            # Execute use case
            use_case = UpdateDataFlowUseCase(self.repository)
            updated_dataflow = use_case.execute(UUID(dataflow_id), update_request)
            
            # Convert to DTO for response
            return Response(
                self._dataflow_to_dict(updated_dataflow),
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
    
    def delete(self, request, dataflow_id):
        """Delete data flow"""
        try:
            # Execute use case
            use_case = DeleteDataFlowUseCase(self.repository)
            deleted = use_case.execute(UUID(dataflow_id))
            
            if deleted:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {'error': 'Data flow not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except Exception as e:
            return Response(
                {'error': f'Internal server error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _dataflow_to_dict(self, dataflow) -> Dict[str, Any]:
        """Convert dataflow domain entity to dictionary for JSON response"""
        return {
            "id": str(dataflow.id),
            "source_system_id": str(dataflow.source_system_id),
            "target_system_id": str(dataflow.target_system_id),
            "data_objects": dataflow.data_objects,
            "integration_technology": dataflow.integration_technology,
            "description": dataflow.description,
            "frequency": dataflow.frequency,
            "created_at": dataflow.created_at.isoformat(),
            "updated_at": dataflow.updated_at.isoformat()
        }
