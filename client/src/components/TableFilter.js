import React from 'react';
import { useAsyncDebounce } from 'react-table';
import { Form, Row, Col } from 'react-bootstrap';

function TableFilter({
    preGlobalFilteredRows,
    globalFilter,
    setGlobalFilter,
    sWidth,
    hasMoreTableData,
    dataLength
  }) {
    const count = preGlobalFilteredRows.length
    const [value, setValue] = React.useState(globalFilter)
    const onChange = useAsyncDebounce(value => {
      setGlobalFilter(value || undefined)
    }, 200)
    let countDisplay = count
    if(dataLength){
      countDisplay = dataLength
    }
    return (
      <Row className="mb-3">
        <Col md={sWidth}>
        <Form.Control
            type="text"
            name="searchTerm"
            value={value || ""}
            placeholder={hasMoreTableData ? `${countDisplay} records loaded for search` : `Search ${countDisplay} records`}
            onChange={e => {
              setValue(e.target.value);
              onChange(e.target.value);
            }}
        />
        </Col>
      </Row>
    )
  }

export default TableFilter
