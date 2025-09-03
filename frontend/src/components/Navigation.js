import React from 'react';
import { Navbar, Nav, Container, NavDropdown } from 'react-bootstrap';
import { Link, useLocation } from 'react-router-dom';
import { FaDatabase, FaChartBar, FaSearch, FaPlus } from 'react-icons/fa';

const Navigation = () => {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <Navbar bg="dark" variant="dark" expand="lg" className="mb-4">
      <Container>
        <Navbar.Brand as={Link} to="/" className="fw-bold">
          <FaDatabase className="me-2" />
          Enterprise Architecture Repository
        </Navbar.Brand>
        
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link 
              as={Link} 
              to="/" 
              active={isActive('/')}
            >
              Dashboard
            </Nav.Link>
            
            <Nav.Link 
              as={Link} 
              to="/systems" 
              active={isActive('/systems')}
            >
              Information Systems
            </Nav.Link>
            
            <Nav.Link 
              as={Link} 
              to="/diagram" 
              active={isActive('/diagram')}
            >
              <FaChartBar className="me-1" />
              Dataflow Diagram
            </Nav.Link>
            
            <Nav.Link 
              as={Link} 
              to="/search" 
              active={isActive('/search')}
            >
              <FaSearch className="me-1" />
              Search
            </Nav.Link>
          </Nav>
          
          <Nav>
            <Nav.Link 
              as={Link} 
              to="/systems/new" 
              className="btn btn-primary btn-sm"
            >
              <FaPlus className="me-1" />
              Add System
            </Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default Navigation;
