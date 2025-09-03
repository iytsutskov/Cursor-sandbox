import React, { useState, useEffect } from 'react';
import { Table, Button, Card, Badge, Row, Col, Alert } from 'react-bootstrap';
import { FaPlus, FaEdit, FaTrash, FaArrowRight, FaDatabase, FaExchangeAlt } from 'react-icons/fa';
import DataFlowForm from './DataFlowForm';

const DataFlowList = ({ dataflows, systems, onDataFlowChange, currentSystemId }) => {
  console.log('DataFlowList component rendering...');
  console.log('DataFlowList props:', { dataflows, systems: systems?.length, currentSystemId });
  console.log('Systems array:', systems);
  const [showForm, setShowForm] = useState(false);
  const [editingDataFlow, setEditingDataFlow] = useState(null);
  const [formMode, setFormMode] = useState('create');
  const [deleteConfirm, setDeleteConfirm] = useState(null);
  const [formData, setFormData] = useState({
    connected_system_id: '',
    data_objects: '',
    integration_technology: '',
    frequency: '',
    description: ''
  });
  console.log('showForm state:', showForm);
  console.log('Modal should be visible:', showForm);

  // Monitor showForm state changes and refresh dataflows when modal closes
  useEffect(() => {
    console.log('showForm state changed to:', showForm);
    
    // If the modal just closed and we're not in edit mode, refresh the dataflows
    if (!showForm && formMode === 'create' && onDataFlowChange) {
      console.log('Modal closed, refreshing dataflows...');
      // Add a small delay to ensure the backend state is consistent
      setTimeout(() => {
        onDataFlowChange();
      }, 200);
    }
  }, [showForm, formMode, onDataFlowChange]);

  const handleAddDataFlow = () => {
    console.log('Add Data Flow button clicked!');
    console.log('Current state:', { showForm, editingDataFlow, formMode });
    console.log('Systems available:', systems?.length || 0);
    console.log('Systems data:', systems);
    setEditingDataFlow(null);
    setFormMode('create');
    setFormData({
      connected_system_id: '',
      data_objects: '',
      integration_technology: '',
      frequency: '',
      description: ''
    });
    setShowForm(true);
    console.log('State after update:', { showForm: true, editingDataFlow: null, formMode: 'create' });
  };

  const handleEditDataFlow = (dataflow) => {
    setEditingDataFlow(dataflow);
    setFormMode('edit');
    setShowForm(true);
  };

  const handleDeleteDataFlow = async (dataflowId) => {
    try {
      const response = await fetch(`/api/dataflows/${dataflowId}/`, {
        method: 'DELETE',
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      console.log('Dataflow deleted successfully');
      onDataFlowChange(); // Refresh the data
      setDeleteConfirm(null);
    } catch (error) {
      console.error('Error deleting dataflow:', error);
      alert('Failed to delete dataflow. Please try again.');
    }
  };

  const handleSaveDataFlow = () => {
    if (!formData.connected_system_id || !formData.data_objects || !formData.integration_technology) {
      alert('Please fill in all required fields');
      return;
    }

    const newDataFlow = {
      source_system_id: currentSystemId,
      target_system_id: formData.connected_system_id,
      data_objects: formData.data_objects,
      integration_technology: formData.integration_technology,
      frequency: formData.frequency || 'batch',
      description: formData.description || ''
    };

    console.log('Creating new dataflow:', newDataFlow);
    
    // Make API call to create dataflow
    fetch('/api/dataflows/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newDataFlow),
    })
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      console.log('Dataflow created successfully:', data);
      
      // Close modal and reset form
      setShowForm(false);
      setFormData({
        connected_system_id: '',
        data_objects: '',
        integration_technology: '',
        frequency: '',
        description: ''
      });
      
      // Don't call onDataFlowChange here - let the parent component handle the refresh
      // This prevents duplicate dataflow entries
    })
    .catch(error => {
      console.error('Error creating dataflow:', error);
      alert('Failed to create dataflow. Please try again.');
    });
  };

  const getSystemName = (systemId) => {
    // Convert both to strings for comparison since systemId might be a UUID object
    const systemIdStr = String(systemId);
    const system = systems.find(s => String(s.id) === systemIdStr);
    return system ? `${system.name} (${system.code})` : 'Unknown System';
  };

  const getDirectionBadge = (sourceId, targetId) => {
    // Convert both to strings for comparison since currentSystemId might be a string from URL params
    const currentIdStr = String(currentSystemId);
    const sourceIdStr = String(sourceId);
    const targetIdStr = String(targetId);
    
    if (sourceIdStr === currentIdStr) {
      return <Badge bg="outgoing" className="text-dark">Outgoing</Badge>;
    } else if (targetIdStr === currentIdStr) {
      return <Badge bg="incoming" className="text-dark">Incoming</Badge>;
    }
    return <Badge bg="secondary">Bidirectional</Badge>;
  };

  const getTechnologyBadge = (technology) => {
    const variants = {
      'REST API': 'primary',
      'SOAP API': 'info',
      'Message Queue (RabbitMQ, Kafka)': 'warning',
      'Database Replication': 'success',
      'ETL/Data Pipeline': 'secondary',
      'File Transfer (SFTP, S3)': 'dark',
      'Event Streaming': 'danger',
      'Direct Database Connection': 'primary',
      'Webhook': 'info',
      'Other': 'secondary'
    };
    return <Badge bg={variants[technology] || 'secondary'}>{technology}</Badge>;
  };

  const getFrequencyBadge = (frequency) => {
    const variants = {
      'real-time': 'success',
      'near-real-time': 'warning',
      'batch': 'info',
      'on-demand': 'secondary'
    };
    return <Badge bg={variants[frequency] || 'secondary'}>{frequency}</Badge>;
  };

  // Always render the main content, but conditionally show the table or "no dataflows" message

  return (
    <>
      <Card>
        <Card.Header>
          <div className="d-flex justify-content-between align-items-center">
            <h5 className="mb-0">
              <FaExchangeAlt className="me-2" />
              Data Flows ({dataflows.length})
            </h5>
            <Button variant="primary" size="sm" onClick={handleAddDataFlow}>
              <FaPlus className="me-2" />
              Add Data Flow
            </Button>
          </div>
        </Card.Header>
        <Card.Body className={!dataflows || dataflows.length === 0 ? "text-center py-4" : "p-0"}>
          {!dataflows || dataflows.length === 0 ? (
            <>
              <FaDatabase size={48} className="text-muted mb-3" />
              <p className="text-muted">No data flows configured for this system.</p>
              <p className="text-muted">Click "Add Data Flow" to establish connections with other systems.</p>
            </>
          ) : (
            <Table responsive hover className="mb-0">
              <thead className="table-light">
                <tr>
                  <th>Direction</th>
                  <th>Connected System</th>
                  <th>Data Objects</th>
                  <th>Technology</th>
                  <th>Frequency</th>
                  <th>Description</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {dataflows.map((dataflow) => (
                  <tr key={dataflow.id}>
                    <td>
                      <div className="d-flex align-items-center">
                        {String(dataflow.source_system_id) === String(currentSystemId) ? (
                          <>
                            <span className="fw-bold text-primary">→</span>
                            <span className="ms-2">{getSystemName(dataflow.target_system_id)}</span>
                          </>
                        ) : (
                          <>
                            <span className="fw-bold text-success">←</span>
                            <span className="ms-2">{getSystemName(dataflow.source_system_id)}</span>
                          </>
                        )}
                        <div className="ms-2">
                          {getDirectionBadge(dataflow.source_system_id, dataflow.target_system_id)}
                        </div>
                      </div>
                    </td>
                    <td>
                      <div>
                        <div className="fw-bold">
                          {String(dataflow.source_system_id) === String(currentSystemId)
                            ? getSystemName(dataflow.target_system_id)
                            : getSystemName(dataflow.source_system_id)
                          }
                        </div>
                        <small className="text-muted">
                          {String(dataflow.source_system_id) === String(currentSystemId) ? 'Target' : 'Source'}
                        </small>
                      </div>
                    </td>
                    <td>
                      <div>
                        {Array.isArray(dataflow.data_objects) ? (
                          dataflow.data_objects.map((obj, index) => (
                            <Badge key={index} bg="light" className="text-dark me-1 mb-1">
                              {obj}
                            </Badge>
                          ))
                        ) : (
                          <Badge bg="light" className="text-dark">
                            {dataflow.data_objects}
                          </Badge>
                        )}
                      </div>
                    </td>
                    <td>{getTechnologyBadge(dataflow.integration_technology)}</td>
                    <td>{getFrequencyBadge(dataflow.frequency)}</td>
                    <td>
                      <small className="text-muted">
                        {dataflow.description || 'No description'}
                      </small>
                    </td>
                    <td>
                      <div className="d-flex gap-1">
                        <Button
                          variant="outline-secondary"
                          size="sm"
                          onClick={() => handleEditDataFlow(dataflow)}
                          title="Edit Data Flow"
                        >
                          <FaEdit />
                        </Button>
                        <Button
                          variant="outline-danger"
                          size="sm"
                          onClick={() => setDeleteConfirm(dataflow.id)}
                          title="Delete Data Flow"
                        >
                          <FaTrash />
                        </Button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </Table>
          )}
        </Card.Body>
      </Card>

      {/* Delete Confirmation Modal */}
      {deleteConfirm && (
        <div className="modal fade show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Confirm Delete</h5>
                <button
                  type="button"
                  className="btn-close"
                  onClick={() => setDeleteConfirm(null)}
                ></button>
              </div>
              <div className="modal-body">
                <p>Are you sure you want to delete this data flow? This action cannot be undone.</p>
              </div>
              <div className="modal-footer">
                <Button variant="secondary" onClick={() => setDeleteConfirm(null)}>
                  Cancel
                </Button>
                <Button
                  variant="danger"
                  onClick={() => handleDeleteDataFlow(deleteConfirm)}
                >
                  Delete
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Data Flow Form Modal */}
      {showForm && (
        <div 
          className="modal show d-block" 
          style={{ 
            position: 'fixed',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            backgroundColor: 'rgba(0,0,0,0.5)', 
            zIndex: 9999,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}
        >
          <div className="modal-dialog modal-lg" style={{ margin: 'auto' }}>
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">
                  {formMode === 'edit' ? 'Edit Data Flow' : 'Add New Data Flow'}
                </h5>
                <button type="button" className="btn-close" onClick={() => setShowForm(false)}></button>
              </div>
              <div className="modal-body">
                <form>
                  <div className="mb-3">
                    <label htmlFor="connectedSystem" className="form-label">Connected System *</label>
                    <select 
                      id="connectedSystem" 
                      className="form-select"
                      onChange={(e) => setFormData({...formData, connected_system_id: e.target.value})}
                      value={formData.connected_system_id || ''}
                      required
                    >
                      <option value="">Select a system...</option>
                      {systems?.filter(sys => sys.id !== currentSystemId).map(system => (
                        <option key={system.id} value={system.id}>
                          {system.name} ({system.code})
                        </option>
                      ))}
                    </select>
                  </div>
                  
                  <div className="mb-3">
                    <label htmlFor="dataObjects" className="form-label">Data Objects *</label>
                    <input
                      type="text"
                      id="dataObjects"
                      className="form-control"
                      placeholder="e.g., Customer data, Orders, Inventory"
                      value={formData.data_objects || ''}
                      onChange={(e) => setFormData({...formData, data_objects: e.target.value})}
                      required
                    />
                    <div className="form-text">Describe what data is being transferred between systems</div>
                  </div>
                  
                  <div className="mb-3">
                    <label htmlFor="integrationTechnology" className="form-label">Integration Technology *</label>
                    <select 
                      id="integrationTechnology" 
                      className="form-select"
                      onChange={(e) => setFormData({...formData, integration_technology: e.target.value})}
                      value={formData.integration_technology || ''}
                      required
                    >
                      <option value="">Select technology...</option>
                      <option value="API (REST, GraphQL)">API (REST, GraphQL)</option>
                      <option value="Message Queue (RabbitMQ, Kafka)">Message Queue (RabbitMQ, Kafka)</option>
                      <option value="Database Replication">Database Replication</option>
                      <option value="ETL/Data Pipeline">ETL/Data Pipeline</option>
                      <option value="File Transfer (SFTP, S3)">File Transfer (SFTP, S3)</option>
                      <option value="Event Streaming">Event Streaming</option>
                      <option value="Direct Database Connection">Direct Database Connection</option>
                      <option value="Webhook">Webhook</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>
                  
                  <div className="mb-3">
                    <label htmlFor="frequency" className="form-label">Data Transfer Frequency</label>
                    <select 
                      id="frequency" 
                      className="form-select"
                      onChange={(e) => setFormData({...formData, frequency: e.target.value})}
                      value={formData.frequency || ''}
                    >
                      <option value="">Select frequency...</option>
                      <option value="real-time">Real-time</option>
                      <option value="near-real-time">Near Real-time</option>
                      <option value="batch">Batch</option>
                      <option value="on-demand">On-demand</option>
                    </select>
                  </div>
                  
                  <div className="mb-3">
                    <label htmlFor="description" className="form-label">Description</label>
                    <textarea
                      id="description"
                      className="form-control"
                      rows="3"
                      placeholder="Additional details about this data flow..."
                      value={formData.description || ''}
                      onChange={(e) => setFormData({...formData, description: e.target.value})}
                    />
                  </div>
                </form>
              </div>
              <div className="modal-footer">
                <button className="btn btn-secondary" onClick={() => setShowForm(false)}>
                  Cancel
                </button>
                <button 
                  className="btn btn-primary" 
                  onClick={handleSaveDataFlow}
                  disabled={!formData.connected_system_id || !formData.data_objects || !formData.integration_technology}
                >
                  {formMode === 'edit' ? 'Update Data Flow' : 'Create Data Flow'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default DataFlowList;
