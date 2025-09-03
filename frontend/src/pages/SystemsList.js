import React, { useState, useEffect } from 'react';
import { Table, Card, Badge, Button, Row, Col, Form, Alert, Spinner } from 'react-bootstrap';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { FaEye, FaEdit, FaPlus, FaSearch, FaFilter, FaFileExcel } from 'react-icons/fa';
import axios from 'axios';

const SystemsList = () => {
  const [systems, setSystems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [typeFilter, setTypeFilter] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const [successMessage, setSuccessMessage] = useState('');
  
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    fetchSystems();
  }, [currentPage, statusFilter, typeFilter]);

  useEffect(() => {
    // Check for success message from navigation state
    if (location.state?.message) {
      setSuccessMessage(location.state.message);
      // Clear the location state to prevent showing the message again on refresh
      navigate(location.pathname, { replace: true });
    }
  }, [location.state, navigate, location.pathname]);

  const fetchSystems = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams({
        page: currentPage,
        page_size: 20
      });

      if (statusFilter) params.append('status', statusFilter);
      if (typeFilter) params.append('system_type', typeFilter);

      const response = await axios.get(`/api/systems/?${params}`);
      setSystems(response.data.systems);
      setTotalPages(response.data.pagination.total_pages);
      setTotalCount(response.data.pagination.total_count);
    } catch (err) {
      setError('Failed to fetch systems');
      console.error('Error fetching systems:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchTerm.trim()) {
      fetchSystems();
      return;
    }

    try {
      setLoading(true);
      const params = new URLSearchParams({
        q: searchTerm,
        page: 1,
        page_size: 20
      });

      if (statusFilter) params.append('status', statusFilter);
      if (typeFilter) params.append('system_type', typeFilter);

      const response = await axios.get(`/api/search/?${params}`);
      setSystems(response.data.systems);
      setTotalPages(response.data.pagination.total_pages);
      setTotalCount(response.data.pagination.total_count);
      setCurrentPage(1);
    } catch (err) {
      setError('Search failed');
      console.error('Search error:', err);
    } finally {
      setLoading(false);
    }
  };

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
      'cloud': 'success'
    };
    return <Badge bg={variants[type] || 'secondary'}>{type}</Badge>;
  };

  const getCriticalityBadgeColor = (criticalityClass) => {
    const variants = {
      'Mission critical': 'danger',
      'Business critical': 'warning',
      'Business operational': 'info',
      'Office productivity': 'secondary'
    };
    return variants[criticalityClass] || 'secondary';
  };

  const clearFilters = () => {
    setSearchTerm('');
    setStatusFilter('');
    setTypeFilter('');
    setCurrentPage(1);
    fetchSystems();
  };

  const handleExportToExcel = async () => {
    try {
      const response = await axios.get('/api/export/excel/', {
        responseType: 'blob'
      });
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `information_systems_export_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.xlsx`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError('Failed to export to Excel');
      console.error('Export error:', err);
    }
  };

  if (loading && systems.length === 0) {
    return (
      <div className="text-center py-5">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
      </div>
    );
  }

  return (
    <div>
      <Row className="mb-4 align-items-center">
        <Col>
          <h1>Information Systems</h1>
        </Col>
        <Col xs="auto">
          <div className="d-flex gap-2">
            <Button onClick={handleExportToExcel} variant="success">
              <FaFileExcel className="me-2" />
              Export to Excel
            </Button>
            <Button as={Link} to="/systems/new" variant="primary">
              <FaPlus className="me-2" />
              Add System
            </Button>
          </div>
        </Col>
      </Row>

      {/* Search and Filters */}
      <Card className="mb-4">
        <Card.Body>
          <Row>
            <Col md={4}>
              <Form.Group>
                <Form.Label>Search</Form.Label>
                <div className="d-flex">
                  <Form.Control
                    type="text"
                    placeholder="Search systems..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                  />
                  <Button 
                    variant="outline-secondary" 
                    onClick={handleSearch}
                    className="ms-2"
                  >
                    <FaSearch />
                  </Button>
                </div>
              </Form.Group>
            </Col>
            
            <Col md={3}>
              <Form.Group>
                <Form.Label>Status</Form.Label>
                <Form.Select
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                >
                  <option value="">All Statuses</option>
                  <option value="development">Development</option>
                  <option value="production">Production</option>
                  <option value="deprecated">Deprecated</option>
                </Form.Select>
              </Form.Group>
            </Col>
            
            <Col md={3}>
              <Form.Group>
                <Form.Label>Type</Form.Label>
                <Form.Select
                  value={typeFilter}
                  onChange={(e) => setTypeFilter(e.target.value)}
                >
                  <option value="">All Types</option>
                  <option value="internal">Internal</option>
                  <option value="external">External</option>
                  <option value="cloud">Cloud</option>
                </Form.Select>
              </Form.Group>
            </Col>
            
            <Col md={2} className="d-flex align-items-end">
              <Button variant="outline-secondary" onClick={clearFilters}>
                <FaFilter className="me-2" />
                Clear
              </Button>
            </Col>
          </Row>
        </Card.Body>
      </Card>

      {error && (
        <Alert variant="danger" dismissible onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {successMessage && (
        <Alert variant="success" dismissible onClose={() => setSuccessMessage('')}>
          {successMessage}
        </Alert>
      )}

      {/* Systems Table */}
      <Card>
        <Card.Header>
          <div className="d-flex justify-content-between align-items-center">
            <span>Systems ({totalCount})</span>
            {loading && <Spinner animation="border" size="sm" />}
          </div>
        </Card.Header>
        <Card.Body className="p-0">
          <Table responsive hover className="mb-0">
            <thead className="table-light">
              <tr>
                <th>Name</th>
                <th>System Code</th>
                <th>Status</th>
                <th>Type</th>
                <th>Owner</th>
                <th>Department</th>
                <th>Criticality Class</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {systems.map((system) => (
                <tr key={system.id}>
                  <td>
                    <div>
                      <div className="fw-bold">{system.name}</div>
                      <small className="text-muted">
                        {system.description ? system.description.substring(0, 60) + '...' : 'No description'}
                      </small>
                    </div>
                  </td>
                  <td>
                    <code>{system.code}</code>
                  </td>
                  <td>{getStatusBadge(system.status)}</td>
                  <td>{getTypeBadge(system.system_type)}</td>
                  <td>{system.owner?.name || system.owner || 'N/A'}</td>
                  <td>{system.owner?.department || 'N/A'}</td>
                  <td>
                    {system.criticality_class ? (
                      <Badge bg={getCriticalityBadgeColor(system.criticality_class)}>
                        {system.criticality_class}
                      </Badge>
                    ) : (
                      <Badge bg="secondary">Unknown</Badge>
                    )}
                  </td>
                  <td>
                    <div className="d-flex gap-1">
                      <Button
                        as={Link}
                        to={`/systems/${system.id}`}
                        variant="outline-primary"
                        size="sm"
                        title="View Details"
                      >
                        <FaEye />
                      </Button>
                      <Button
                        as={Link}
                        to={`/systems/edit/${system.id}`}
                        variant="outline-secondary"
                        size="sm"
                        title="Edit"
                      >
                        <FaEdit />
                      </Button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
          
          {systems.length === 0 && !loading && (
            <div className="text-center py-4">
              <p className="text-muted">No systems found</p>
            </div>
          )}
        </Card.Body>
      </Card>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="d-flex justify-content-center mt-4">
          <nav>
            <ul className="pagination">
              <li className={`page-item ${currentPage === 1 ? 'disabled' : ''}`}>
                <Button
                  className="page-link"
                  variant="outline-primary"
                  onClick={() => setCurrentPage(currentPage - 1)}
                  disabled={currentPage === 1}
                >
                  Previous
                </Button>
              </li>
              
              {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                <li key={page} className={`page-item ${page === currentPage ? 'active' : ''}`}>
                  <Button
                    className="page-link"
                    variant={page === currentPage ? 'primary' : 'outline-primary'}
                    onClick={() => setCurrentPage(page)}
                  >
                    {page}
                  </Button>
                </li>
              ))}
              
              <li className={`page-item ${currentPage === totalPages ? 'disabled' : ''}`}>
                <Button
                  className="page-link"
                  variant="outline-primary"
                  onClick={() => setCurrentPage(currentPage + 1)}
                  disabled={currentPage === totalPages}
                >
                  Next
                </Button>
              </li>
            </ul>
          </nav>
        </div>
      )}
    </div>
  );
};

export default SystemsList;
