import { Badge, Col, Container, Row } from "react-bootstrap";

function HomePage() {
  return (
    <div className="py-5">
      <Container className="text-center">
        <Row className="gx-5 align-items-center">
          <Col className="xxl-5">
            <Badge className="gradient-linear">
              <span className="text-uppercase">
                Universidad Tecnológica de San Juan del Río
              </span>
            </Badge>
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default HomePage;
