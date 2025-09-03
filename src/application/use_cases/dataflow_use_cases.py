from typing import List, Optional
from uuid import UUID
from datetime import datetime

from ...domain.entities.information_system import DataFlow
from ...domain.repositories.information_system_repository import InformationSystemRepository
from ..dtos.information_system_dto import (
    CreateDataFlowRequest, UpdateDataFlowRequest, DataFlowDTO
)


class CreateDataFlowUseCase:
    """Use case for creating a new data flow"""
    
    def __init__(self, repository: InformationSystemRepository):
        self.repository = repository
    
    def execute(self, request: CreateDataFlowRequest) -> DataFlow:
        """Execute the create data flow use case"""
        
        # Validate that both systems exist
        source_system = self.repository.get_by_id(request.source_system_id)
        if not source_system:
            raise ValueError(f"Source system with id '{request.source_system_id}' not found")
        
        target_system = self.repository.get_by_id(request.target_system_id)
        if not target_system:
            raise ValueError(f"Target system with id '{request.target_system_id}' not found")
        
        # Create the data flow
        dataflow = DataFlow.create(
            source_system_id=request.source_system_id,
            target_system_id=request.target_system_id,
            data_objects=request.data_objects,
            integration_technology=request.integration_technology,
            description=request.description,
            frequency=request.frequency
        )
        
        # Add dataflow to both systems (for in-memory consistency)
        source_system.add_dataflow(dataflow)
        target_system.add_dataflow(dataflow)
        
        # Save the dataflow directly to avoid duplication
        self.repository.save_dataflow(dataflow)
        
        return dataflow


class UpdateDataFlowUseCase:
    """Use case for updating an existing data flow"""
    
    def __init__(self, repository: InformationSystemRepository):
        self.repository = repository
    
    def execute(self, dataflow_id: UUID, request: UpdateDataFlowRequest) -> DataFlow:
        """Execute the update data flow use case"""
        
        # Find the dataflow in one of the systems
        all_systems = self.repository.get_all()
        dataflow = None
        source_system = None
        target_system = None
        
        for system in all_systems:
            if system.dataflows:
                for df in system.dataflows:
                    if df.id == dataflow_id:
                        dataflow = df
                        if df.source_system_id == system.id:
                            source_system = system
                        elif df.target_system_id == system.id:
                            target_system = system
                        break
                if dataflow:
                    break
        
        if not dataflow:
            raise ValueError(f"Data flow with id '{dataflow_id}' not found")
        
        # Update the dataflow
        if request.data_objects is not None:
            dataflow.update_data_objects(request.data_objects)
        
        if request.integration_technology is not None:
            dataflow.update_integration_technology(request.integration_technology)
        
        if request.description is not None:
            dataflow.update_description(request.description)
        
        if request.frequency is not None:
            dataflow.update_frequency(request.frequency)
        
        # Save both systems
        if source_system:
            self.repository.save(source_system)
        if target_system:
            self.repository.save(target_system)
        
        return dataflow


class DeleteDataFlowUseCase:
    """Use case for deleting a data flow"""
    
    def __init__(self, repository: InformationSystemRepository):
        self.repository = repository
    
    def execute(self, dataflow_id: UUID) -> bool:
        """Execute the delete data flow use case"""
        
        all_systems = self.repository.get_all()
        deleted = False
        
        for system in all_systems:
            if system.dataflows:
                if system.remove_dataflow(dataflow_id):
                    self.repository.save(system)
                    deleted = True
        
        return deleted


class GetDataFlowsUseCase:
    """Use case for getting data flows for a system"""
    
    def __init__(self, repository: InformationSystemRepository):
        self.repository = repository
    
    def execute(self, system_id: UUID) -> List[DataFlowDTO]:
        """Execute the get data flows use case for a specific system"""
        
        system = self.repository.get_by_id(system_id)
        if not system:
            raise ValueError(f"System with id '{system_id}' not found")
        
        if not system.dataflows:
            return []
        
        # Convert to DTOs
        dataflow_dtos = []
        for dataflow in system.dataflows:
            dto = DataFlowDTO(
                id=dataflow.id,
                source_system_id=dataflow.source_system_id,
                target_system_id=dataflow.target_system_id,
                data_objects=dataflow.data_objects,
                integration_technology=dataflow.integration_technology,
                description=dataflow.description,
                frequency=dataflow.frequency,
                created_at=dataflow.created_at,
                updated_at=dataflow.updated_at
            )
            dataflow_dtos.append(dto)
        
        return dataflow_dtos
    
    def execute_for_system(self, system_id: UUID) -> List[DataFlow]:
        """Execute the get data flows use case for a specific system (both incoming and outgoing)"""
        
        # Use the repository's direct dataflow loading method to avoid duplicates
        return self.repository._load_dataflows(system_id)
    
    def execute_all(self) -> List[DataFlow]:
        """Execute the get all data flows use case across all systems"""
        
        all_systems = self.repository.get_all()
        all_dataflows = []
        
        for system in all_systems:
            if system.dataflows:
                all_dataflows.extend(system.dataflows)
        
        # Remove duplicates based on dataflow ID
        unique_dataflows = {}
        for dataflow in all_dataflows:
            unique_dataflows[str(dataflow.id)] = dataflow
        
        return list(unique_dataflows.values())
