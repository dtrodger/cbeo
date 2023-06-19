import { Row, Col, Spinner } from 'react-bootstrap';

const Loading = props => {
  const { message } = props;
  return (
    <Row>
      <Col className="text-center">
        <Spinner animation="border" />
        {message
          ? (
              <p>{message}</p>
            )
          : null
        }
      </Col>
    </Row>
  );
};

export default Loading;