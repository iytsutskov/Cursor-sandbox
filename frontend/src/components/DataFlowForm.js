import React, { useState, useEffect } from 'react';
import { Form, Button, Modal, Alert, Row, Col } from 'react-bootstrap';
import { FaSave, FaTimes, FaPlus, FaEdit } from 'react-icons/fa';
import axios from 'axios';

const DataFlowForm = ({ show, onHide, dataflow, systems, onSave, mode = 'create' }) => {
  console.log('DataFlowForm component mounting with props:', { show, onHide, dataflow, systems: systems?.length, onSave, mode });
  const [formData, setFormData] = useState({
    source_system_id: '',
    target_system_id: '',
    data_objects: '',
    integration_technology: '',
    description: '',
    frequency: 'real-time'
  });
  
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState('');

  const frequencyOptions = [
    { value: 'real-time', label: 'Real-time' },
    { value: 'near-real-time', label: 'Near Real-time' },
    { value: 'batch', label: 'Batch' },
    { value: 'on-demand', label: 'On-demand' }
  ];

  const integrationTechnologyOptions = [
    'REST API',
    'SOAP API',
    'Message Queue (RabbitMQ, Kafka)',
    'Database Replication',
    'ETL/Data Pipeline',
    'File Transfer (SFTP, S3)',
    'Event Streaming',
    'Direct Database Connection',
    'Webhook',
    'Other'
  ];

  useEffect(() => {
    if (dataflow && mode === 'edit') {
      setFormData({
        source_system_id: dataflow.source_system_id,
        target_system_id: dataflow.target_system_id,
        data_objects: Array.isArray(dataflow.data_objects) ? dataflow.data_objects.join(', ') : dataflow.data_objects || '',
        integration_technology: dataflow.integration_technology || '',
        description: dataflow.description || '',
        frequency: dataflow.frequency || 'real-time'
      });
    } else if (mode === 'create') {
      setFormData({
        source_system_id: '',
        target_system_id: '',
        data_objects: '',
        integration_technology: '',
        description: '',
        frequency: 'real-time'
      });
    }
  }, [dataflow, mode]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.source_system_id) {
      newErrors.source_system_id = 'Source system is required';
    }
    
    if (!formData.target_system_id) {
      newErrors.target_system_id = 'Target system is required';
    }
    
    if (formData.source_system_id === formData.target_system_id) {
      newErrors.target_system_id = 'Source and target systems must be different';
    }
    
    if (!formData.data_objects.trim()) {
      newErrors.data_objects = 'Data objects are required';
    }
    
    if (!formData.integration_technology) {
      newErrors.integration_technology = 'Integration technology is required';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    setIsSubmitting(true);
    setSubmitError('');
    
    try {
      // Prepare the data for the API
      const dataflowData = {
        source_system_id: formData.source_system_id,
        target_system_id: formData.target_system_id,
        data_objects: formData.data_objects.split(',').map(obj => obj.trim()).filter(obj => obj),
        integration_technology: formData.integration_technology,
        description: formData.description.trim() || null,
        frequency: formData.frequency
      };
      
      let response;
      if (mode === 'edit') {
        response = await axios.put(`/api/dataflows/${dataflow.id}/`, dataflowData);
      } else {
        response = await axios.post('/api/dataflows/', dataflowData);
      }
      
      if (response.status === 200 || response.status === 201) {
        onSave(response.data);
        onHide();
      }
    } catch (error) {
      console.error(`Error ${mode === 'edit' ? 'updating' : 'creating'} dataflow:`, error);
      if (error.response?.data) {
        setSubmitError(error.response.data.error || `Failed to ${mode === 'edit' ? 'update' : 'create'} dataflow`);
      } else {
        setSubmitError('Network error. Please try again.');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const getSystemName = (systemId) => {
    const system = systems.find(s => s.id === systemId);
    return system ? `${system.name} (${system.code})` : 'Unknown System';
  };

  // Show loading state if systems data is not available
  const isSystemsLoading = !systems || systems.length === 0;

  console.log('DataFlowForm render - show:', show, 'isSystemsLoading:', isSystemsLoading, 'systems count:', systems?.length);

  if (!show) {
    console.log('DataFlowForm: show is false, returning null');
    return null;
  }

  console.log('DataFlowForm: show is true, rendering modal');

  return (
    <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 1050 }}>
      <div className="modal-dialog modal-lg">
        <div className="modal-content">
                <div className="modal-header">
            <h5 className="modal-title">
              {mode === 'edit' ? (
                <>
                  <FaEdit className="me-2" />
                  Edit Data Flow
                </>
              ) : (
                <>
                  <FaPlus className="me-2" />
                  Add New Data Flow
                </>
              )}
            </h5>
            <button type="button" className="btn-close" onClick={onHide}></button>
          </div>
      
                <div className="modal-body">
        {submitError && (
          <Alert variant="danger" dismissible onClose={() => setSubmitError('')}>
            {submitError}
          </Alert>
        )}
        
        {isSystemsLoading ? (
          <div className="text-center py-4">
            <div className="spinner-border text-primary" role="status">
              <span className="visually-hidden">Loading systems...</span>
            </div>
            <p className="mt-2">Loading systems data...</p>
          </div>
        ) : (
          <Form onSubmit={handleSubmit}>
            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Source System *</Form.Label>
                  <Form.Select
                    name="source_system_id"
                    value={formData.source_system_id}
                    onChange={handleInputChange}
                    isInvalid={!!errors.source_system_id}
                  >
                    <option value="">Select source system</option>
                    {systems.map(system => (
                      <option key={system.id} value={system.id}>
                        {system.name} ({system.code})
                      </option>
                    ))}
                  </Form.Select>
                  <Form.Control.Feedback type="invalid">
                    {errors.source_system_id}
                  </Form.Control.Feedback>
                </Form.Group>
              </Col>
            
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Target System *</Form.Label>
                <Form.Select
                  name="target_system_id"
                  value={formData.target_system_id}
                  onChange={handleInputChange}
                  isInvalid={!!errors.target_system_id}
                >
                  <option value="">Select target system</option>
                  {systems.map(system => (
                    <option key={system.id} value={system.id}>
                      {system.name} ({system.code})
                    </option>
                  ))}
                </Form.Select>
                <Form.Control.Feedback type="invalid">
                  {errors.target_system_id}
                </Form.Control.Feedback>
              </Form.Group>
            </Col>
          </Row>

          <Form.Group className="mb-3">
            <Form.Label>Data Objects *</Form.Label>
            <Form.Control
              as="textarea"
              rows={3}
              name="data_objects"
              value={formData.data_objects}
              onChange={handleInputChange}
              isInvalid={!!errors.data_objects}
              placeholder="Enter data objects (comma-separated)"
            />
            <Form.Control.Feedback type="invalid">
              {errors.data_objects}
            </Form.Control.Feedback>
            <small className="text-muted">
              Separate multiple data objects with commas (e.g., Customer, Order, Product)
            </small>
          </Form.Group>

          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Integration Technology *</Form.Label>
                <Form.Select
                  name="integration_technology"
                  value={formData.integration_technology}
                  onChange={handleInputChange}
                  isInvalid={!!errors.integration_technology}
                >
                  <option value="">Select technology</option>
                  {integrationTechnologyOptions.map(tech => (
                    <option key={tech} value={tech}>
                      {tech}
                    </option>
                  ))}
                </Form.Select>
                <Form.Control.Feedback type="invalid">
                  {errors.integration_technology}
                </Form.Control.Feedback>
              </Form.Group>
            </Col>
            
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Frequency</Form.Label>
                <Form.Select
                  name="frequency"
                  value={formData.frequency}
                  onChange={handleInputChange}
                >
                  {frequencyOptions.map(option => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </Form.Select>
              </Form.Group>
            </Col>
          </Row>

          <Form.Group className="mb-3">
            <Form.Label>Description</Form.Label>
            <Form.Control
              as="textarea"
              rows={2}
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              placeholder="Optional description of the data flow"
            />
          </Form.Group>

          {mode === 'edit' && dataflow && (
            <div className="mb-3 p-3 bg-light rounded">
              <small className="text-muted">
                <strong>Current Flow:</strong> {getSystemName(dataflow.source_system_id)} → {getSystemName(dataflow.target_system_id)}
              </small>
            </div>
          )}
          </Form>
        )}
          </div>
          
          <div className="modal-footer">
            <Button variant="secondary" onClick={onHide} disabled={isSubmitting}>
              <FaTimes className="me-2" />
              Cancel
            </Button>
            {!isSystemsLoading && (
              <Button
                type="submit"
                variant="primary"
                disabled={isSubmitting}
                onClick={handleSubmit}
              >
                {isSubmitting ? (
                  <>
                    <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    {mode === 'edit' ? 'Updating...' : 'Creating...'}
                  </>
                ) : (
                  <>
                    <FaSave className="me-2" />
                    {mode === 'edit' ? 'Update Data Flow' : 'Create Data Flow'}
                  </>
                )}
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default DataFlowForm;
