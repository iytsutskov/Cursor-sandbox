import React, { useState, useEffect, useCallback } from 'react';
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  Panel
} from 'reactflow';
import 'reactflow/dist/style.css';
import { Card, Badge, Spinner, Alert } from 'react-bootstrap';
import { FaNetworkWired, FaInfoCircle, FaDownload } from 'react-icons/fa';
import axios from 'axios';

const DataflowDiagram = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [metadata, setMetadata] = useState(null);
  const [selectedNode, setSelectedNode] = useState(null);

  // Fetch diagram data
  const fetchDiagramData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await axios.get('/api/diagram/dataflow/');
      const data = response.data;
      
      setNodes(data.nodes);
      setEdges(data.edges);
      setMetadata(data.metadata);
      
    } catch (err) {
      setError('Failed to load dataflow diagram');
      console.error('Error fetching diagram data:', err);
    } finally {
      setLoading(false);
    }
  }, [setNodes, setEdges]);

  useEffect(() => {
    fetchDiagramData();
  }, [fetchDiagramData]);

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  const onNodeClick = useCallback((event, node) => {
    setSelectedNode(node);
  }, []);

  const onPaneClick = useCallback(() => {
    setSelectedNode(null);
  }, []);

  const getStatusBadge = (status) => {
    const variants = {
      'development': 'warning',
      'production': 'success',
      'deprecated': 'danger'
    };
    return <Badge bg={variants[status] || 'secondary'}>{status}</Badge>;
  };

  const getTypeBadge = (type) => {
    const variants = {
      'internal': 'primary',
      'external': 'info',
      'cloud': 'secondary'
    };
    return <Badge bg={variants[type] || 'secondary'}>{type}</Badge>;
  };

  if (loading) {
    return (
      <div className="text-center py-5">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
        <p className="mt-3">Loading dataflow diagram...</p>
      </div>
    );
  }

  if (error) {
    return (
      <Alert variant="danger" dismissible onClose={() => setError(null)}>
        {error}
        <div className="mt-2">
          <button className="btn btn-outline-danger btn-sm" onClick={fetchDiagramData}>
            Try Again
          </button>
        </div>
      </Alert>
    );
  }

  return (
    <div style={{ height: '80vh', width: '100%' }}>
      <Card className="mb-3">
        <Card.Header>
          <div className="d-flex justify-content-between align-items-center">
            <div>
              <FaNetworkWired className="me-2" />
              <strong>Dataflow Diagram</strong>
            </div>
            <div className="d-flex gap-2">
              <Badge bg="info" className="d-flex align-items-center">
                <FaInfoCircle className="me-1" />
                {metadata?.total_systems || 0} Systems
              </Badge>
              <Badge bg="primary" className="d-flex align-items-center">
                <FaDownload className="me-1" />
                {metadata?.total_dataflows || 0} Dataflows
              </Badge>
              <Badge bg="success" className="d-flex align-items-center">
                Connected: {metadata?.connected_systems || 0}
              </Badge>
              <Badge bg="warning" className="d-flex align-items-center">
                Isolated: {metadata?.isolated_systems || 0}
              </Badge>
            </div>
          </div>
        </Card.Header>
      </Card>

      <div style={{ height: 'calc(80vh - 80px)', border: '1px solid #dee2e6', borderRadius: '0.375rem' }}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onNodeClick={onNodeClick}
          onPaneClick={onPaneClick}
          fitView
          attributionPosition="bottom-left"
        >
          <Controls />
          <MiniMap />
          <Background variant="dots" gap={12} size={1} />
          
          {/* Legend */}
          <Panel position="top-right" className="bg-white p-3 rounded shadow-sm">
            <h6 className="mb-2">Legend</h6>
            <div className="d-flex flex-column gap-1">
              <div className="d-flex align-items-center gap-2">
                <div style={{ width: '20px', height: '20px', backgroundColor: '#dc2626', borderRadius: '4px' }}></div>
                <small>Mission Critical</small>
              </div>
              <div className="d-flex align-items-center gap-2">
                <div style={{ width: '20px', height: '20px', backgroundColor: '#ea580c', borderRadius: '4px' }}></div>
                <small>Business Critical</small>
              </div>
              <div className="d-flex align-items-center gap-2">
                <div style={{ width: '20px', height: '20px', backgroundColor: '#2563eb', borderRadius: '4px' }}></div>
                <small>Business Operational</small>
              </div>
              <div className="d-flex align-items-center gap-2">
                <div style={{ width: '20px', height: '20px', backgroundColor: '#059669', borderRadius: '4px' }}></div>
                <small>Office Productivity</small>
              </div>
            </div>
          </Panel>

          {/* Node Details Panel */}
          {selectedNode && (
            <Panel position="bottom-left" className="bg-white p-3 rounded shadow-sm" style={{ maxWidth: '300px' }}>
              <h6 className="mb-2">{selectedNode.data.label}</h6>
              <div className="small">
                <p><strong>Code:</strong> {selectedNode.data.code}</p>
                <p><strong>Status:</strong> {getStatusBadge(selectedNode.data.status)}</p>
                <p><strong>Type:</strong> {getTypeBadge(selectedNode.data.system_type)}</p>
                <p><strong>Criticality:</strong> {selectedNode.data.criticality_class}</p>
                <p><strong>Owner:</strong> {selectedNode.data.owner}</p>
                <p><strong>Department:</strong> {selectedNode.data.department}</p>
                {selectedNode.data.description && (
                  <p><strong>Description:</strong> {selectedNode.data.description}</p>
                )}
              </div>
            </Panel>
          )}
        </ReactFlow>
      </div>
    </div>
  );
};

export default DataflowDiagram;
