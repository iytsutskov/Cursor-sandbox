from django.urls import path
from . import views
from . import dataflow_views
from . import excel_export_views
from . import dataflow_diagram_views

app_name = 'api'

urlpatterns = [
    # Information Systems
    path('systems/', views.InformationSystemAPIView.as_view(), name='systems'),
    path('systems/<uuid:system_id>/', views.InformationSystemAPIView.as_view(), name='system-detail'),
    
    # Search
    path('search/', views.SearchInformationSystemsAPIView.as_view(), name='search'),
    
    # Statistics
    path('statistics/', views.SystemStatisticsAPIView.as_view(), name='statistics'),
    
    # Data Flows
    path('dataflows/', dataflow_views.DataFlowAPIView.as_view(), name='dataflows'),
    path('dataflows/<uuid:dataflow_id>/', dataflow_views.DataFlowAPIView.as_view(), name='dataflow-detail'),
    
    # Excel Export
    path('export/excel/', excel_export_views.ExcelExportView.as_view(), name='export-excel'),
    
    # Dataflow Diagram
    path('diagram/dataflow/', dataflow_diagram_views.DataflowDiagramView.as_view(), name='dataflow-diagram'),
    
    # Legacy endpoints
    path('stats/', views.get_system_statistics, name='legacy-stats'),
]
