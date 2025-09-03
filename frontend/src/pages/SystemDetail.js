import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Card, Row, Col, Badge, Alert, Spinner, Button } from 'react-bootstrap';
import { FaArrowLeft, FaEdit, FaTrash } from 'react-icons/fa';
import axios from 'axios';

const SystemDetail = () => {
  const { id } = useParams();
  const [system, setSystem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchSystem();
  }, [id]);

  const fetchSystem = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`/api/systems/${id}/`);
      setSystem(response.data);
    } catch (err) {
      setError('Failed to fetch system details');
      console.error('Error fetching system:', err);
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status) => {
    const variants = {
      'active': 'success',
      'inactive': 'secondary',
      'deprecated': 'danger',
      'planned': 'info',
      'development': 'warning'
    };
    return <Badge bg={variants[status] || 'secondary'}>{status}</Badge>;
  };

  const getTypeBadge = (type) => {
    const variants = {
      'enterprise': 'primary',
      'departmental': 'info',
      'project': 'warning',
      'legacy': 'secondary',
      'cloud': 'success'
    };
    return <Badge bg={variants[type] || 'secondary'}>{type}</Badge>;
  };

  if (loading) {
    return (
      <div className="text-center py-5">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
      </div>
    );
  }

  if (error) {
    return (
      <Alert variant="danger">
        <Alert.Heading>Error</Alert.Heading>
        <p>{error}</p>
        <Link to="/systems" className="btn btn-primary">
          Back to Systems
        </Link>
      </Alert>
    );
  }

  if (!system) {
    return (
      <Alert variant="warning">
        <Alert.Heading>System Not Found</Alert.Heading>
        <p>The requested system could not be found.</p>
        <Link to="/systems" className="btn btn-primary">
          Back to Systems
        </Link>
      </Alert>
    );
  }

  return (
    <div>
      {/* Header */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <Link to="/systems" className="btn btn-outline-secondary me-3">
            <FaArrowLeft className="me-2" />
            Back to Systems
          </Link>
          <h1 className="d-inline">{system.name}</h1>
        </div>
        <div>
          <Link to={`/systems/edit/${system.id}`} className="btn btn-primary me-2">
            <FaEdit className="me-2" />
            Edit
          </Link>
          <Button variant="danger">
            <FaTrash className="me-2" />
            Delete
          </Button>
        </div>
      </div>

      <Row>
        {/* Main Information */}
        <Col md={8}>
          <Card className="mb-4">
            <Card.Header>
              <h4>System Information</h4>
            </Card.Header>
            <Card.Body>
              <Row>
                <Col md={6}>
                  <p><strong>Code:</strong> <code>{system.code}</code></p>
                  <p><strong>Status:</strong> {getStatusBadge(system.status)}</p>
                  <p><strong>Type:</strong> {getTypeBadge(system.system_type)}</p>
                  <p><strong>Version:</strong> {system.version}</p>
                </Col>
                <Col md={6}>
                  <p><strong>Created:</strong> {new Date(system.created_at).toLocaleDateString()}</p>
                  <p><strong>Updated:</strong> {new Date(system.updated_at).toLocaleDateString()}</p>
                  <p><strong>Critical:</strong> {system.is_critical ? 'Yes' : 'No'}</p>
                  {system.cost_center && (
                    <p><strong>Cost Center:</strong> {system.cost_center}</p>
                  )}
                </Col>
              </Row>
              
              <hr />
              
              <div>
                <h5>Description</h5>
                <p>{system.description}</p>
              </div>
              
              <div>
                <h5>Purpose</h5>
                <p>{system.purpose}</p>
              </div>
              
              <div>
                <h5>Business Value</h5>
                <p>{system.business_value}</p>
              </div>
            </Card.Body>
          </Card>

          {/* Business Functions */}
          <Card className="mb-4">
            <Card.Header>
              <h4>Business Functions</h4>
            </Card.Header>
            <Card.Body>
              {system.business_functions.map((func, index) => (
                <div key={index} className="mb-3 p-3 border rounded">
                  <div className="d-flex justify-content-between align-items-start">
                    <div>
                      <h6 className="mb-1">{func.name}</h6>
                      <p className="mb-2">{func.description}</p>
                      <div className="mb-2">
                        <strong>Criticality:</strong> 
                        <Badge bg={func.criticality === 'high' ? 'danger' : func.criticality === 'medium' ? 'warning' : 'secondary'} className="ms-2">
                          {func.criticality}
                        </Badge>
                      </div>
                      <div>
                        <strong>Business Processes:</strong>
                        <div className="mt-1">
                          {func.business_processes.map((process, pIndex) => (
                            <Badge key={pIndex} bg="info" className="me-1">{process}</Badge>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </Card.Body>
          </Card>
        </Col>

        {/* Sidebar */}
        <Col md={4}>
          {/* Owner Information */}
          <Card className="mb-4">
            <Card.Header>
              <h5>System Owner</h5>
            </Card.Header>
            <Card.Body>
              <p><strong>Name:</strong> {system.owner.name}</p>
              <p><strong>Email:</strong> {system.owner.email}</p>
              <p><strong>Department:</strong> {system.owner.department}</p>
              {system.owner.phone && (
                <p><strong>Phone:</strong> {system.owner.phone}</p>
              )}
            </Card.Body>
          </Card>

          {/* Technical Specifications */}
          <Card className="mb-4">
            <Card.Header>
              <h5>Technical Specifications</h5>
            </Card.Header>
            <Card.Body>
              <div className="mb-3">
                <strong>Technology Stack:</strong>
                <div className="mt-1">
                  {system.technical_spec.technology_stack.map((tech, index) => (
                    <Badge key={index} bg="primary" className="me-1 mb-1">{tech}</Badge>
                  ))}
                </div>
              </div>
              
              <div className="mb-3">
                <strong>Programming Languages:</strong>
                <div className="mt-1">
                  {system.technical_spec.programming_languages.map((lang, index) => (
                    <Badge key={index} bg="success" className="me-1 mb-1">{lang}</Badge>
                  ))}
                </div>
              </div>
              
              <div className="mb-3">
                <strong>Databases:</strong>
                <div className="mt-1">
                  {system.technical_spec.databases.map((db, index) => (
                    <Badge key={index} bg="warning" className="me-1 mb-1">{db}</Badge>
                  ))}
                </div>
              </div>
              
              <div className="mb-3">
                <strong>Frameworks:</strong>
                <div className="mt-1">
                  {system.technical_spec.frameworks.map((framework, index) => (
                    <Badge key={index} bg="info" className="me-1 mb-1">{framework}</Badge>
                  ))}
                </div>
              </div>
              
              <p><strong>Deployment Model:</strong> {system.technical_spec.deployment_model}</p>
              {system.technical_spec.hosting_provider && (
                <p><strong>Hosting Provider:</strong> {system.technical_spec.hosting_provider}</p>
              )}
            </Card.Body>
          </Card>

          {/* Relationships */}
          <Card>
            <Card.Header>
              <h5>Relationships</h5>
            </Card.Header>
            <Card.Body>
              {system.parent_system_id && (
                <p><strong>Parent System:</strong> {system.parent_system_id}</p>
              )}
              
              <div>
                <strong>Dependent Systems:</strong>
                {system.dependent_systems.length > 0 ? (
                  <div className="mt-1">
                    {system.dependent_systems.map((depId, index) => (
                      <Badge key={index} bg="secondary" className="me-1">{depId}</Badge>
                    ))}
                  </div>
                ) : (
                  <p className="text-muted mt-1">No dependent systems</p>
                )}
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default SystemDetail;
