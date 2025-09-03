import sqlite3
import json
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from ...domain.entities.information_system import (
    InformationSystem, SystemStatus, SystemType, SystemOwner, 
    TechnicalSpecification, BusinessFunction
)
from ...domain.repositories.information_system_repository import InformationSystemRepository


class SQLiteInformationSystemRepository(InformationSystemRepository):
    """SQLite implementation of Information System Repository"""
    
    def __init__(self, db_path: str = "db.sqlite3"):
        self.db_path = db_path
        self._init_database()
        self._upgrade_database_schema()
    
    def _init_database(self):
        """Initialize the database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create information_systems table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS information_systems (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    code TEXT UNIQUE NOT NULL,
                    description TEXT,
                    purpose TEXT,
                    status TEXT NOT NULL,
                    system_type TEXT NOT NULL,
                    owner_name TEXT NOT NULL,
                    owner_email TEXT NOT NULL,
                    owner_department TEXT NOT NULL,
                    owner_phone TEXT,
                    technology_stack TEXT,
                    programming_languages TEXT,
                    databases TEXT,
                    frameworks TEXT,
                    deployment_model TEXT,
                    hosting_provider TEXT,
                    business_functions TEXT,
                    business_value TEXT,
                    cost_center TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    version TEXT NOT NULL,
                    parent_system_id TEXT,
                    dependent_systems TEXT,
                    criticality_class TEXT DEFAULT 'Business operational'
                )
            ''')
            
            # Create dataflows table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dataflows (
                    id TEXT PRIMARY KEY,
                    source_system_id TEXT NOT NULL,
                    target_system_id TEXT NOT NULL,
                    data_objects TEXT NOT NULL,
                    integration_technology TEXT NOT NULL,
                    description TEXT,
                    frequency TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY (source_system_id) REFERENCES information_systems (id),
                    FOREIGN KEY (target_system_id) REFERENCES information_systems (id)
                )
            ''')
            
            conn.commit()
    
    def save(self, information_system: InformationSystem) -> InformationSystem:
        """Save or update an information system"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Check if system exists
            cursor.execute("SELECT id FROM information_systems WHERE id = ?", (str(information_system.id),))
            exists = cursor.fetchone()
            
            if exists:
                # Update existing system
                cursor.execute('''
                    UPDATE information_systems SET
                        name = ?, code = ?, description = ?, purpose = ?, status = ?, system_type = ?,
                        owner_name = ?, owner_email = ?, owner_department = ?, owner_phone = ?,
                        technology_stack = ?, programming_languages = ?, databases = ?, frameworks = ?,
                        deployment_model = ?, hosting_provider = ?, business_functions = ?,
                        business_value = ?, cost_center = ?, updated_at = ?, version = ?,
                        parent_system_id = ?, dependent_systems = ?, criticality_class = ?
                    WHERE id = ?
                ''', (
                    information_system.name,
                    information_system.code,
                    information_system.description,
                    information_system.purpose,
                    information_system.status.value,
                    information_system.system_type.value,
                    information_system.owner.name,
                    information_system.owner.email,
                    information_system.owner.department,
                    information_system.owner.phone,
                    json.dumps(information_system.technical_spec.technology_stack),
                    json.dumps(information_system.technical_spec.programming_languages),
                    json.dumps(information_system.technical_spec.databases),
                    json.dumps(information_system.technical_spec.frameworks),
                    information_system.technical_spec.deployment_model,
                    information_system.technical_spec.hosting_provider,
                    json.dumps([self._business_function_to_dict(bf) for bf in information_system.business_functions]),
                    information_system.business_value,
                    information_system.cost_center,
                    information_system.updated_at.isoformat(),
                    information_system.version,
                    str(information_system.parent_system_id) if information_system.parent_system_id else None,
                    json.dumps([str(sid) for sid in information_system.dependent_systems]),
                    information_system.criticality_class,
                    str(information_system.id)
                ))
            else:
                # Insert new system
                cursor.execute('''
                    INSERT INTO information_systems (
                        id, name, code, description, purpose, status, system_type,
                        owner_name, owner_email, owner_department, owner_phone,
                        technology_stack, programming_languages, databases, frameworks,
                        deployment_model, hosting_provider, business_functions,
                        business_value, cost_center, created_at, updated_at, version,
                        parent_system_id, dependent_systems, criticality_class
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    str(information_system.id),
                    information_system.name,
                    information_system.code,
                    information_system.description,
                    information_system.purpose,
                    information_system.status.value,
                    information_system.system_type.value,
                    information_system.owner.name,
                    information_system.owner.email,
                    information_system.owner.department,
                    information_system.owner.phone,
                    json.dumps(information_system.technical_spec.technology_stack),
                    json.dumps(information_system.technical_spec.programming_languages),
                    json.dumps(information_system.technical_spec.databases),
                    json.dumps(information_system.technical_spec.frameworks),
                    information_system.technical_spec.deployment_model,
                    information_system.technical_spec.hosting_provider,
                    json.dumps([self._business_function_to_dict(bf) for bf in information_system.business_functions]),
                    information_system.business_value,
                    information_system.cost_center,
                    information_system.created_at.isoformat(),
                    information_system.updated_at.isoformat(),
                    information_system.version,
                    str(information_system.parent_system_id) if information_system.parent_system_id else None,
                    json.dumps([str(sid) for sid in information_system.dependent_systems]),
                    information_system.criticality_class
                ))
            
            # Save dataflows for this system
            self._save_dataflows(cursor, information_system)
            
            conn.commit()
            return information_system
    
    def _upgrade_database_schema(self):
        """Upgrade database schema to add missing columns"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if criticality_class column exists
                cursor.execute("PRAGMA table_info(information_systems)")
                columns = [column[1] for column in cursor.fetchall()]
                
                if 'criticality_class' not in columns:
                    print("Adding criticality_class column to existing database...")
                    cursor.execute('''
                        ALTER TABLE information_systems 
                        ADD COLUMN criticality_class TEXT DEFAULT 'Business operational'
                    ''')
                    conn.commit()
                    print("Database schema upgraded successfully!")
                    
        except Exception as e:
            print(f"Error upgrading database schema: {e}")
            import traceback
            traceback.print_exc()
    
    def get_by_id(self, system_id: UUID) -> Optional[InformationSystem]:
        """Get information system by ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM information_systems WHERE id = ?", (str(system_id),))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_entity(row)
            return None
    
    def get_by_code(self, code: str) -> Optional[InformationSystem]:
        """Get information system by business code"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM information_systems WHERE code = ?", (code,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_entity(row)
            return None
    
    def get_all(self) -> List[InformationSystem]:
        """Get all information systems"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM information_systems ORDER BY name")
            rows = cursor.fetchall()
            
            return [self._row_to_entity(row) for row in rows]
    
    def get_by_status(self, status: SystemStatus) -> List[InformationSystem]:
        """Get information systems by status"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM information_systems WHERE status = ? ORDER BY name", (status.value,))
            rows = cursor.fetchall()
            
            return [self._row_to_entity(row) for row in rows]
    
    def get_by_type(self, system_type: SystemType) -> List[InformationSystem]:
        """Get information systems by type"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM information_systems WHERE system_type = ? ORDER BY name", (system_type.value,))
            rows = cursor.fetchall()
            
            return [self._row_to_entity(row) for row in rows]
    
    def get_by_owner_department(self, department: str) -> List[InformationSystem]:
        """Get information systems by owner department"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM information_systems WHERE owner_department = ? ORDER BY name", (department,))
            rows = cursor.fetchall()
            
            return [self._row_to_entity(row) for row in rows]
    
    def get_critical_systems(self) -> List[InformationSystem]:
        """Get all critical information systems"""
        all_systems = self.get_all()
        return [system for system in all_systems if system.is_critical()]
    
    def search(self, query: str) -> List[InformationSystem]:
        """Search information systems by name, description, or code"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            search_pattern = f"%{query}%"
            cursor.execute('''
                SELECT * FROM information_systems 
                WHERE name LIKE ? OR description LIKE ? OR code LIKE ?
                ORDER BY name
            ''', (search_pattern, search_pattern, search_pattern))
            rows = cursor.fetchall()
            
            return [self._row_to_entity(row) for row in rows]
    
    def get_dependent_systems(self, system_id: UUID) -> List[InformationSystem]:
        """Get all systems that depend on the specified system"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM information_systems WHERE dependent_systems LIKE ? ORDER BY name", (f"%{str(system_id)}%",))
            rows = cursor.fetchall()
            
            return [self._row_to_entity(row) for row in rows]
    
    def get_parent_system(self, system_id: UUID) -> Optional[InformationSystem]:
        """Get the parent system of the specified system"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM information_systems WHERE id = ?", (str(system_id),))
            row = cursor.fetchone()
            
            if row and row[23]:  # parent_system_id column
                parent_id = UUID(row[23])
                return self.get_by_id(parent_id)
            return None
    
    def delete(self, system_id: UUID) -> bool:
        """Delete an information system"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM information_systems WHERE id = ?", (str(system_id),))
            conn.commit()
            return cursor.rowcount > 0
    
    def exists(self, system_id: UUID) -> bool:
        """Check if an information system exists"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM information_systems WHERE id = ?", (str(system_id),))
            return cursor.fetchone() is not None
    
    def count(self) -> int:
        """Get total count of information systems"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM information_systems")
            return cursor.fetchone()[0]
    
    def get_systems_by_technology(self, technology: str) -> List[InformationSystem]:
        """Get information systems that use a specific technology"""
        all_systems = self.get_all()
        return [
            system for system in all_systems 
            if technology in system.technical_spec.technology_stack
        ]
    
    def get_systems_by_business_function(self, function_name: str) -> List[InformationSystem]:
        """Get information systems that support a specific business function"""
        all_systems = self.get_all()
        return [
            system for system in all_systems 
            if any(bf.name == function_name for bf in system.business_functions)
        ]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about information systems"""
        all_systems = self.get_all()
        
        stats = {
            "total_systems": len(all_systems),
            "active_systems": len([s for s in all_systems if s.status == SystemStatus.ACTIVE]),
            "inactive_systems": len([s for s in all_systems if s.status == SystemStatus.INACTIVE]),
            "deprecated_systems": len([s for s in all_systems if s.status == SystemStatus.DEPRECATED]),
            "production_systems": len([s for s in all_systems if s.status == SystemStatus.PRODUCTION]),
            "development_systems": len([s for s in all_systems if s.status == SystemStatus.DEVELOPMENT]),
            "critical_systems": len([s for s in all_systems if s.is_critical()])
        }
        
        return stats
    
    def _row_to_entity(self, row) -> InformationSystem:
        """Convert database row to domain entity"""
        # Parse JSON fields
        technology_stack = json.loads(row[11]) if row[11] else []
        programming_languages = json.loads(row[12]) if row[12] else []
        databases = json.loads(row[13]) if row[13] else []
        frameworks = json.loads(row[14]) if row[14] else []
        business_functions_data = json.loads(row[17]) if row[17] else []
        dependent_systems_data = json.loads(row[24]) if row[24] else []
        
        # Create value objects
        owner = SystemOwner(
            name=row[7],
            email=row[8],
            department=row[9],
            phone=row[10]
        )
        
        technical_spec = TechnicalSpecification(
            technology_stack=technology_stack,
            programming_languages=programming_languages,
            databases=databases,
            frameworks=frameworks,
            deployment_model=row[15],
            hosting_provider=row[16]
        )
        
        business_functions = [
            BusinessFunction(
                name=bf["name"],
                description=bf["description"],
                criticality=bf["criticality"],
                business_processes=bf["business_processes"]
            )
            for bf in business_functions_data
        ]
        
        # Create entity
        system = InformationSystem(
            id=UUID(row[0]),
            name=row[1],
            code=row[2],
            description=row[3],
            purpose=row[4],
            status=SystemStatus(row[5]),
            system_type=SystemType(row[6]),
            owner=owner,
            technical_spec=technical_spec,
            business_functions=business_functions,
            business_value=row[18],
            cost_center=row[19],
            created_at=datetime.fromisoformat(row[20]),
            updated_at=datetime.fromisoformat(row[21]),
            version=row[22],
            parent_system_id=UUID(row[23]) if row[23] else None,
            dependent_systems=[UUID(sid) for sid in dependent_systems_data],
            criticality_class=row[25] if len(row) > 25 and row[25] else 'Business operational'
        )
        
        # Load dataflows for this system
        system.dataflows = self._load_dataflows(system.id)
        
        return system
    
    def _business_function_to_dict(self, bf: BusinessFunction) -> dict:
        """Convert BusinessFunction to dictionary for JSON serialization"""
        return {
            "name": bf.name,
            "description": bf.description,
            "criticality": bf.criticality,
            "business_processes": bf.business_processes
        }
    
    def _save_dataflows(self, cursor, information_system: InformationSystem):
        """Save dataflows for a system"""
        # First, delete existing dataflows for this system
        cursor.execute("DELETE FROM dataflows WHERE source_system_id = ? OR target_system_id = ?", 
                      (str(information_system.id), str(information_system.id)))
        
        # Then insert current dataflows
        if information_system.dataflows:
            for dataflow in information_system.dataflows:
                cursor.execute('''
                    INSERT INTO dataflows (
                        id, source_system_id, target_system_id, data_objects, 
                        integration_technology, description, frequency, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    str(dataflow.id),
                    str(dataflow.source_system_id),
                    str(dataflow.target_system_id),
                    dataflow.data_objects,
                    dataflow.integration_technology,
                    dataflow.description or '',
                    dataflow.frequency,
                    dataflow.created_at.isoformat(),
                    dataflow.updated_at.isoformat()
                ))
    
    def save_dataflow(self, dataflow: 'DataFlow') -> 'DataFlow':
        """Save a single dataflow directly to the dataflows table"""
        from ...domain.entities.information_system import DataFlow
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Check if dataflow exists
            cursor.execute("SELECT id FROM dataflows WHERE id = ?", (str(dataflow.id),))
            exists = cursor.fetchone()
            
            if exists:
                # Update existing dataflow
                cursor.execute('''
                    UPDATE dataflows SET
                        source_system_id = ?, target_system_id = ?, data_objects = ?,
                        integration_technology = ?, description = ?, frequency = ?, updated_at = ?
                    WHERE id = ?
                ''', (
                    str(dataflow.source_system_id),
                    str(dataflow.target_system_id),
                    dataflow.data_objects,
                    dataflow.integration_technology,
                    dataflow.description or '',
                    dataflow.frequency,
                    dataflow.updated_at.isoformat(),
                    str(dataflow.id)
                ))
            else:
                # Insert new dataflow
                cursor.execute('''
                    INSERT INTO dataflows (
                        id, source_system_id, target_system_id, data_objects, 
                        integration_technology, description, frequency, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    str(dataflow.id),
                    str(dataflow.source_system_id),
                    str(dataflow.target_system_id),
                    dataflow.data_objects,
                    dataflow.integration_technology,
                    dataflow.description or '',
                    dataflow.frequency,
                    dataflow.created_at.isoformat(),
                    dataflow.updated_at.isoformat()
                ))
            
            conn.commit()
            return dataflow
    
    def _load_dataflows(self, system_id: UUID) -> List['DataFlow']:
        """Load dataflows for a system from database"""
        from ...domain.entities.information_system import DataFlow
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, source_system_id, target_system_id, data_objects, 
                       integration_technology, description, frequency, created_at, updated_at
                FROM dataflows 
                WHERE source_system_id = ? OR target_system_id = ?
            ''', (str(system_id), str(system_id)))
            
            dataflows = []
            for row in cursor.fetchall():
                dataflow = DataFlow.create(
                    source_system_id=UUID(row[1]),
                    target_system_id=UUID(row[2]),
                    data_objects=row[3],
                    integration_technology=row[4],
                    description=row[5] if row[5] else None,
                    frequency=row[6]
                )
                # Set the ID and timestamps from database
                dataflow.id = UUID(row[0])
                dataflow.created_at = datetime.fromisoformat(row[7])
                dataflow.updated_at = datetime.fromisoformat(row[8])
                dataflows.append(dataflow)
            
            return dataflows
