// src/layout/Navbar.jsx

import React from "react";
import { Navbar, Container, Nav } from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";

function LayoutNavbar() {
  return (
    <Navbar bg="dark" variant="dark">
      <Container>
        <Navbar.Brand href="/">Navbar</Navbar.Brand>
        <Nav className="me-auto">
          <LinkContainer to="/">
            <Nav.Link>Home</Nav.Link>
          </LinkContainer>
          {/* Agrega más enlaces según sea necesario */}
        </Nav>
      </Container>
    </Navbar>
  );
}

export default LayoutNavbar;
