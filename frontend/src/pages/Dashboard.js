import React, { useState, useEffect } from 'react';
import { Row, Col, Card, Badge, Alert } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { FaDatabase, FaServer, FaCloud, FaExclamationTriangle, FaCheckCircle, FaClock, FaCode, FaPlus, FaSearch } from 'react-icons/fa';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import axios from 'axios';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStatistics();
  }, []);

  const fetchStatistics = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/statistics/');
      setStats(response.data);
    } catch (err) {
      setError('Failed to fetch statistics');
      console.error('Error fetching statistics:', err);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      'active': 'success',
      'inactive': 'secondary',
      'deprecated': 'danger',
      'planned': 'info',
      'development': 'warning'
    };
    return colors[status] || 'secondary';
  };

  const getStatusIcon = (status) => {
    const icons = {
      'active': <FaCheckCircle />,
      'inactive': <FaClock />,
      'deprecated': <FaExclamationTriangle />,
      'planned': <FaClock />,
      'development': <FaCode />
    };
    return icons[status] || <FaClock />;
  };

  if (loading) {
    return (
      <div className="text-center py-5">
        <div className="spinner-border" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <Alert variant="danger">
        <Alert.Heading>Error</Alert.Heading>
        <p>{error}</p>
      </Alert>
    );
  }

  if (!stats) {
    return null;
  }

  // Prepare chart data
  const statusData = [
    { name: 'Development', value: stats.development_systems, color: '#ffc107' },
    { name: 'Production', value: stats.production_systems || 0, color: '#28a745' },
    { name: 'Deprecated', value: stats.deprecated_systems, color: '#dc3545' }
  ];

  const typeData = Object.entries(stats.systems_by_type).map(([type, count]) => ({
    name: type.charAt(0).toUpperCase() + type.slice(1),
    count: count
  }));

  const departmentData = Object.entries(stats.systems_by_department).map(([dept, count]) => ({
    name: dept,
    count: count
  }));

  return (
    <div>
      <h1 className="mb-4">Enterprise Architecture Dashboard</h1>
      
      {/* Summary Cards */}
      <Row className="mb-4">
        <Col md={3}>
          <Card className="text-center h-100">
            <Card.Body>
              <FaDatabase className="text-primary mb-2" size={30} />
              <Card.Title>{stats.total_systems}</Card.Title>
              <Card.Text>Total Systems</Card.Text>
            </Card.Body>
          </Card>
        </Col>
        
        <Col md={3}>
          <Card className="text-center h-100">
            <Card.Body>
              <FaCheckCircle className="text-success mb-2" size={30} />
              <Card.Title>{stats.production_systems || 0}</Card.Title>
              <Card.Text>Production Systems</Card.Text>
            </Card.Body>
          </Card>
        </Col>
        
        <Col md={3}>
          <Card className="text-center h-100">
            <Card.Body>
              <FaExclamationTriangle className="text-warning mb-2" size={30} />
              <Card.Title>{stats.critical_systems}</Card.Title>
              <Card.Text>Critical Systems</Card.Text>
            </Card.Body>
          </Card>
        </Col>
        
        <Col md={3}>
          <Card className="text-center h-100">
            <Card.Body>
              <FaCode className="text-info mb-2" size={30} />
              <Card.Title>{stats.development_systems}</Card.Title>
              <Card.Text>In Development</Card.Text>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Charts Row */}
      <Row className="mb-4">
        <Col md={6}>
          <Card>
            <Card.Header>
              <h5>System Status Distribution</h5>
            </Card.Header>
            <Card.Body>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={statusData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {statusData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </Card.Body>
          </Card>
        </Col>
        
        <Col md={6}>
          <Card>
            <Card.Header>
              <h5>Systems by Type</h5>
            </Card.Header>
            <Card.Body>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={typeData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="count" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Top Technologies */}
      <Row className="mb-4">
        <Col md={12}>
          <Card>
            <Card.Header>
              <h5>Top Technologies</h5>
            </Card.Header>
            <Card.Body>
              <Row>
                {stats.top_technologies.slice(0, 8).map((tech, index) => (
                  <Col md={3} key={index} className="mb-2">
                    <div className="d-flex justify-content-between align-items-center p-2 border rounded">
                      <span className="fw-bold">{tech.technology}</span>
                      <Badge bg="primary">{tech.count}</Badge>
                    </div>
                  </Col>
                ))}
              </Row>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Quick Actions */}
      <Row>
        <Col md={12}>
          <Card>
            <Card.Header>
              <h5>Quick Actions</h5>
            </Card.Header>
            <Card.Body>
              <div className="d-flex gap-2 flex-wrap">
                <Link to="/systems/new" className="btn btn-primary">
                  <FaPlus className="me-2" />
                  Add New System
                </Link>
                <Link to="/systems" className="btn btn-outline-primary">
                  <FaDatabase className="me-2" />
                  View All Systems
                </Link>
                <Link to="/search" className="btn btn-outline-secondary">
                  <FaSearch className="me-2" />
                  Search Systems
                </Link>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;
