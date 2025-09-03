from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from uuid import UUID

from ..entities.information_system import InformationSystem, SystemStatus, SystemType


class InformationSystemRepository(ABC):
    """Abstract repository interface for Information System persistence operations"""
    
    @abstractmethod
    def save(self, information_system: InformationSystem) -> InformationSystem:
        """Save or update an information system"""
        pass
    
    @abstractmethod
    def get_by_id(self, system_id: UUID) -> Optional[InformationSystem]:
        """Get information system by ID"""
        pass
    
    @abstractmethod
    def get_by_code(self, code: str) -> Optional[InformationSystem]:
        """Get information system by business code"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[InformationSystem]:
        """Get all information systems"""
        pass
    
    @abstractmethod
    def get_by_status(self, status: SystemStatus) -> List[InformationSystem]:
        """Get information systems by status"""
        pass
    
    @abstractmethod
    def get_by_type(self, system_type: SystemType) -> List[InformationSystem]:
        """Get information systems by type"""
        pass
    
    @abstractmethod
    def get_by_owner_department(self, department: str) -> List[InformationSystem]:
        """Get information systems by owner department"""
        pass
    
    @abstractmethod
    def get_critical_systems(self) -> List[InformationSystem]:
        """Get all critical information systems"""
        pass
    
    @abstractmethod
    def search(self, query: str) -> List[InformationSystem]:
        """Search information systems by name, description, or code"""
        pass
    
    @abstractmethod
    def get_dependent_systems(self, system_id: UUID) -> List[InformationSystem]:
        """Get all systems that depend on the specified system"""
        pass
    
    @abstractmethod
    def get_parent_system(self, system_id: UUID) -> Optional[InformationSystem]:
        """Get the parent system of the specified system"""
        pass
    
    @abstractmethod
    def delete(self, system_id: UUID) -> bool:
        """Delete an information system"""
        pass
    
    @abstractmethod
    def exists(self, system_id: UUID) -> bool:
        """Check if an information system exists"""
        pass
    
    @abstractmethod
    def count(self) -> int:
        """Get total count of information systems"""
        pass
    
    @abstractmethod
    def get_systems_by_technology(self, technology: str) -> List[InformationSystem]:
        """Get information systems that use a specific technology"""
        pass
    
    @abstractmethod
    def get_systems_by_business_function(self, function_name: str) -> List[InformationSystem]:
        """Get information systems that support a specific business function"""
        pass
    
    @abstractmethod
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about information systems"""
        pass
