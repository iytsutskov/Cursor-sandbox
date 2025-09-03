from django.http import JsonResponse
from django.views import View
from rest_framework import status
from rest_framework.response import Response
import json

from src.application.use_cases.information_system_use_cases import ListInformationSystemsUseCase
from src.application.use_cases.dataflow_use_cases import GetDataFlowsUseCase
from src.infrastructure.persistence.sqlite_information_system_repository import SQLiteInformationSystemRepository


class DataflowDiagramView(View):
    """View for providing dataflow diagram data"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = SQLiteInformationSystemRepository()
    
    def get(self, request):
        """Get dataflow diagram data for visualization"""
        try:
            # Get all systems
            systems_use_case = ListInformationSystemsUseCase(self.repository)
            systems_response = systems_use_case.execute()
            systems = systems_response.systems
            
            # Get all dataflows
            dataflows_use_case = GetDataFlowsUseCase(self.repository)
            all_dataflows = dataflows_use_case.execute_all()
            
            # Prepare nodes (systems)
            nodes = []
            for system in systems:
                # Determine node color based on criticality class
                node_color = self._get_node_color(system.criticality_class)
                
                node = {
                    'id': str(system.id),
                    'type': 'system',
                    'data': {
                        'label': system.name,
                        'code': system.code,
                        'description': system.description,
                        'status': system.status,
                        'system_type': system.system_type,
                        'criticality_class': system.criticality_class,
                        'owner': system.owner.name,
                        'department': system.owner.department
                    },
                    'position': self._calculate_node_position(len(nodes)),  # Simple positioning for now
                    'style': {
                        'background': node_color,
                        'color': 'white',
                        'border': '2px solid #333',
                        'borderRadius': '8px',
                        'padding': '10px',
                        'fontWeight': 'bold',
                        'minWidth': '150px',
                        'textAlign': 'center'
                    }
                }
                nodes.append(node)
            
            # Prepare edges (dataflows)
            edges = []
            for dataflow in all_dataflows:
                edge = {
                    'id': str(dataflow.id),
                    'source': str(dataflow.source_system_id),
                    'target': str(dataflow.target_system_id),
                    'type': 'smoothstep',
                    'animated': True,
                    'style': {
                        'stroke': '#2563eb',
                        'strokeWidth': 2,
                        'strokeDasharray': '5,5'
                    },
                    'data': {
                        'label': f"{dataflow.data_objects} via {dataflow.integration_technology}",
                        'frequency': dataflow.frequency,
                        'description': dataflow.description or ''
                    },
                    'labelStyle': {
                        'fill': '#1f2937',
                        'fontWeight': 500,
                        'fontSize': '12px'
                    }
                }
                edges.append(edge)
            
            # Prepare diagram metadata
            diagram_data = {
                'nodes': nodes,
                'edges': edges,
                'metadata': {
                    'total_systems': len(systems),
                    'total_dataflows': len(all_dataflows),
                    'connected_systems': len(set([edge['source'] for edge in edges] + [edge['target'] for edge in edges])),
                    'isolated_systems': len([node for node in nodes if not any(edge['source'] == node['id'] or edge['target'] == node['id'] for edge in edges)])
                }
            }
            
            return JsonResponse(diagram_data)
            
        except Exception as e:
            return JsonResponse(
                {'error': f'Failed to generate dataflow diagram: {str(e)}'},
                status=500
            )
    
    def _get_node_color(self, criticality_class):
        """Get node color based on criticality class"""
        color_map = {
            'Mission critical': '#dc2626',      # Red
            'Business critical': '#ea580c',     # Orange
            'Business operational': '#2563eb',  # Blue
            'Office productivity': '#059669'    # Green
        }
        return color_map.get(criticality_class, '#6b7280')  # Default gray
    
    def _calculate_node_position(self, index):
        """Calculate node position in a grid layout"""
        # Simple grid layout: 3 columns, auto rows
        cols = 3
        row = index // cols
        col = index % cols
        
        # Spacing between nodes
        x_spacing = 250
        y_spacing = 150
        
        return {
            'x': col * x_spacing + 100,
            'y': row * y_spacing + 100
        }
