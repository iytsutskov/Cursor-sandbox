import React, { useState, useEffect, useCallback } from 'react';
import { Form, Button, Card, Alert, Row, Col, Tabs, Tab } from 'react-bootstrap';
import { useNavigate, useParams } from 'react-router-dom';
import { FaSave, FaTimes, FaPlus, FaEdit, FaExchangeAlt } from 'react-icons/fa';
import axios from 'axios';
import DataFlowList from '../components/DataFlowList';

const SystemForm = () => {
  console.log('SystemForm component mounting...');
  const navigate = useNavigate();
  const { id } = useParams();
  const isEditMode = Boolean(id);
  console.log('URL params:', { id });
  console.log('isEditMode:', isEditMode);
  
  const [formData, setFormData] = useState({
    name: '',
    code: '',
    description: '',
    owner: '',
    status: 'development',
    department: 'IT',
    criticality_class: 'Business operational'
  });
  
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [systems, setSystems] = useState([]);
  const [dataflows, setDataflows] = useState([]);

  // Debug: Log when systems state changes
  useEffect(() => {
    console.log('Systems state changed:', systems?.length || 0, 'systems');
  }, [systems]);

  const statusOptions = [
    { value: 'development', label: 'Development' },
    { value: 'production', label: 'Production' },
    { value: 'deprecated', label: 'Deprecated' }
  ];

  const criticalityClassOptions = [
    { value: 'Mission critical', label: 'Mission Critical' },
    { value: 'Business critical', label: 'Business Critical' },
    { value: 'Business operational', label: 'Business Operational' },
    { value: 'Office productivity', label: 'Office Productivity' }
  ];

  // Fetch all systems for dataflow creation
  const fetchSystems = useCallback(async () => {
    try {
      console.log('Fetching systems...');
      const response = await axios.get('/api/systems/');
      console.log('Systems response:', response.data);
      console.log('Systems response type:', typeof response.data);
      console.log('Systems response keys:', Object.keys(response.data || {}));
      setSystems(response.data.systems || []);
      console.log('Systems state updated:', response.data.systems?.length || 0, 'systems');
    } catch (error) {
      console.error('Error fetching systems:', error);
      console.error('Error details:', error.response?.data, error.response?.status);
    }
  }, []);

  // Fetch dataflows for the current system
  const fetchDataflows = useCallback(async () => {
    if (!id) return;
    try {
      // Use the dedicated dataflows API endpoint
      const response = await axios.get(`/api/dataflows/?system_id=${id}`);
      setDataflows(response.data || []);
    } catch (error) {
      console.error('Error fetching dataflows:', error);
      // Fallback to getting dataflows from system endpoint
      try {
        const systemResponse = await axios.get(`/api/systems/${id}/`);
        setDataflows(systemResponse.data.dataflows || []);
      } catch (fallbackError) {
        console.error('Error fetching system dataflows:', fallbackError);
        setDataflows([]);
      }
    }
  }, [id]);

  const fetchSystemData = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await axios.get(`/api/systems/${id}/`);
      const system = response.data;
      
      setFormData({
        name: system.name || '',
        code: system.code || '',
        description: system.description || '',
        owner: system.owner?.name || system.owner || '',
        status: system.status || 'development',
        department: system.owner?.department || 'IT',
        criticality_class: system.criticality_class || 'Business operational'
      });
      
      // Also fetch dataflows for this system
      setDataflows(system.dataflows || []);
    } catch (error) {
      console.error('Error fetching system data:', error);
      setSubmitError('Failed to load system data. Please try again.');
    } finally {
      setIsLoading(false);
    }
  }, [id]);

  // Fetch existing system data when in edit mode
  useEffect(() => {
    console.log('useEffect triggered - isEditMode:', isEditMode, 'id:', id);
    if (isEditMode && id) {
      console.log('Calling fetchSystemData...');
      fetchSystemData();
    }
    console.log('Calling fetchSystems...');
    fetchSystems();
  }, [isEditMode, id]);

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
    
    if (!formData.name.trim()) {
      newErrors.name = 'System name is required';
    }
    
    if (!formData.code.trim()) {
      newErrors.code = 'System code is required';
    }
    
    if (!formData.owner.trim()) {
      newErrors.owner = 'System owner is required';
    }
    
    if (!formData.status) {
      newErrors.status = 'System status is required';
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
      const systemData = {
        name: formData.name.trim(),
        code: formData.code.trim(),
        description: formData.description.trim() || '',
        owner: formData.owner.trim(),
        status: formData.status,
        department: formData.department,
        criticality_class: formData.criticality_class,
        system_type: 'internal', // Default value
        purpose: 'Enterprise system management', // Default value
        business_value: 'High', // Default value
        cost_center: 'IT-001', // Default value
        version: '1.0.0', // Default value
        technical_spec: {
          technology_stack: ['Python', 'Django', 'React'],
          programming_languages: ['Python', 'JavaScript'],
          databases: ['SQLite'],
          frameworks: ['Django', 'React'],
          deployment_model: 'On-premise',
          hosting_provider: 'Internal'
        },
        business_functions: [
          {
            name: 'System Management',
            description: 'Core system management functionality',
            criticality: formData.criticality_class === 'Mission critical' || formData.criticality_class === 'Business critical' ? 'high' : 'medium'
          }
        ],
        dependent_systems: [],
        parent_system_id: null
      };
      

      
      let response;
      if (isEditMode) {
        // Update existing system
        response = await axios.put(`/api/systems/${id}/`, systemData);
        if (response.status === 200) {
          navigate('/systems', { 
            state: { 
              message: `System "${formData.name}" updated successfully!`,
              type: 'success'
            }
          });
        }
      } else {
        // Create new system
        response = await axios.post('/api/systems/', systemData);
        if (response.status === 201) {
          navigate('/systems', { 
            state: { 
              message: `System "${formData.name}" created successfully!`,
              type: 'success'
          }
        });
        }
      }
    } catch (error) {
      console.error(`Error ${isEditMode ? 'updating' : 'creating'} system:`, error);
      if (error.response?.data) {
        setSubmitError(error.response.data.message || `Failed to ${isEditMode ? 'update' : 'create'} system`);
      } else {
        setSubmitError('Network error. Please try again.');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCancel = () => {
    navigate('/systems');
  };

  const handleDataFlowChange = useCallback(() => {
    fetchDataflows();
  }, [fetchDataflows]);

  return (
    <div className="container mt-4">
      <Row className="justify-content-center">
        <Col md={8} lg={6}>
          <Card>
                      <Card.Header className="bg-primary text-white">
            <h4 className="mb-0">
              {isEditMode ? (
                <>
                  <FaEdit className="me-2" />
                  Edit Information System
                </>
              ) : (
                <>
                  <FaPlus className="me-2" />
                  Add New Information System
                </>
              )}
            </h4>
          </Card.Header>
            <Card.Body>
              {isLoading && (
                <div className="text-center py-4">
                  <div className="spinner-border text-primary" role="status">
                    <span className="visually-hidden">Loading...</span>
                  </div>
                  <p className="mt-2">Loading system data...</p>
                </div>
              )}
              
              {submitError && (
                <Alert variant="danger" dismissible onClose={() => setSubmitError('')}>
                  {submitError}
                </Alert>
              )}
              
                            {!isLoading && (
                <Tabs defaultActiveKey="details" className="mb-3">
                  <Tab eventKey="details" title="System Details">
                    <Form onSubmit={handleSubmit}>
                      <Row>
                        <Col md={6}>
                          <Form.Group className="mb-3">
                            <Form.Label>System Name *</Form.Label>
                            <Form.Control
                              type="text"
                              name="name"
                              value={formData.name}
                              onChange={handleInputChange}
                              isInvalid={!!errors.name}
                              placeholder="Enter system name"
                            />
                            <Form.Control.Feedback type="invalid">
                              {errors.name}
                            </Form.Control.Feedback>
                          </Form.Group>
                        </Col>
                        
                        <Col md={6}>
                          <Form.Group className="mb-3">
                            <Form.Label>System Code *</Form.Label>
                            <Form.Control
                              type="text"
                              name="code"
                              value={formData.code}
                              onChange={handleInputChange}
                              isInvalid={!!errors.code}
                              placeholder="Enter system code"
                            />
                            <Form.Control.Feedback type="invalid">
                              {errors.code}
                            </Form.Control.Feedback>
                          </Form.Group>
                        </Col>
                      </Row>

                      <Form.Group className="mb-3">
                        <Form.Label>Description</Form.Label>
                        <Form.Control
                          as="textarea"
                          rows={3}
                          name="description"
                          value={formData.description}
                          onChange={handleInputChange}
                          placeholder="Enter system description (optional)"
                        />
                      </Form.Group>

                      <Row>
                        <Col md={6}>
                          <Form.Group className="mb-3">
                            <Form.Label>System Owner *</Form.Label>
                            <Form.Control
                              type="text"
                              name="owner"
                              value={formData.owner}
                              onChange={handleInputChange}
                              isInvalid={!!errors.owner}
                              placeholder="Enter system owner"
                            />
                            <Form.Control.Feedback type="invalid">
                              {errors.owner}
                            </Form.Control.Feedback>
                          </Form.Group>
                        </Col>
                        
                        <Col md={6}>
                          <Form.Group className="mb-3">
                            <Form.Label>System Status *</Form.Label>
                            <Form.Select
                              name="status"
                              value={formData.status}
                              onChange={handleInputChange}
                              isInvalid={!!errors.status}
                            >
                              {statusOptions.map(option => (
                                <option key={option.value} value={option.value}>
                                  {option.label}
                                </option>
                              ))}
                            </Form.Select>
                            <Form.Control.Feedback type="invalid">
                              {errors.status}
                            </Form.Control.Feedback>
                          </Form.Group>
                        </Col>
                      </Row>

                      <Row>
                        <Col md={6}>
                          <Form.Group className="mb-3">
                            <Form.Label>Department</Form.Label>
                            <Form.Select
                              name="department"
                              value={formData.department}
                              onChange={handleInputChange}
                            >
                              <option value="IT">IT</option>
                              <option value="Finance">Finance</option>
                              <option value="HR">HR</option>
                              <option value="Operations">Operations</option>
                              <option value="Sales">Sales</option>
                              <option value="Marketing">Marketing</option>
                              <option value="Legal">Legal</option>
                              <option value="Other">Other</option>
                            </Form.Select>
                          </Form.Group>
                        </Col>
                        
                        <Col md={6}>
                          <Form.Group className="mb-3">
                            <Form.Label>Criticality Class</Form.Label>
                            <Form.Select
                              name="criticality_class"
                              value={formData.criticality_class}
                              onChange={handleInputChange}
                            >
                              {criticalityClassOptions.map(option => (
                                <option key={option.value} value={option.value}>
                                  {option.label}
                                </option>
                              ))}
                            </Form.Select>
                            <small className="text-muted d-block mt-1">
                              Defines the business impact level of the system
                            </small>
                          </Form.Group>
                        </Col>
                      </Row>

                      <div className="d-flex justify-content-end gap-2 mt-4">
                        <Button 
                          variant="secondary" 
                          onClick={handleCancel}
                          disabled={isSubmitting}
                        >
                          <FaTimes className="me-2" />
                          Cancel
                        </Button>
                        <Button
                          type="submit"
                          variant="primary"
                          disabled={isSubmitting}
                        >
                          {isSubmitting ? (
                            <>
                              <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                              {isEditMode ? 'Updating...' : 'Creating...'}
                            </>
                          ) : (
                            <>
                              <FaSave className="me-2" />
                              {isEditMode ? 'Update System' : 'Create System'}
                            </>
                          )}
                        </Button>
                      </div>
                    </Form>
                  </Tab>
                  
                  {isEditMode && (
                    <Tab eventKey="dataflows" title="Data Flows">
                      <DataFlowList
                        dataflows={dataflows}
                        systems={systems}
                        onDataFlowChange={handleDataFlowChange}
                        currentSystemId={id}
                      />
                    </Tab>
                  )}
                </Tabs>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default SystemForm;
