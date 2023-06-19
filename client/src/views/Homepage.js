import React, { useState, useEffect } from 'react';
import {
  Form, Row, Col, Button
} from 'react-bootstrap';
import * as Yup from 'yup';
import { useFormik } from 'formik';
import { FilePond } from 'react-filepond';
import toast from 'react-hot-toast';
import Loading from '../components/Loading';
import apiClient from '../libs/apiClient';
import SortableTable from '../components/SortableTable';

const Homepage = () => {
  const [ isSubmitting, setIsSubmitting ] = useState(false);
  const [ pitches, setPitches ] = useState([])

  useEffect(() => {
    getPitches()
  }, [])

  const getPitches = async () => {
    const response = await apiClient.get("pitch")
    if (response.status === 200){
      setPitches(response.data)
    }
  }

  const formik = useFormik({
    initialValues: {
      pitchFile: [],
    },
    validationSchema: Yup.object().shape({
      pitchFile: Yup.array().length(1, 'Please select one file').required('File is required')
    }),
    validateOnChange: false,
    onSubmit: async (values, { setFieldValue }) => {
      setIsSubmitting(true)
      const formData = new FormData();
      const pitchFile = values.pitchFile[0]
      formData.append('file', pitchFile.file);
      formData.append('file_name', pitchFile.filename)
      const response = await apiClient.post("pitch-upload/", formData)
      if (response.status === 200){
        await getPitches()
        toast.success("File Processed")
        setFieldValue('pitchFile', [])
      } else {
        toast.success("Error Processing File")
      }
      setIsSubmitting(false);
    }
  });

  return (
      <>
        <div id="homepage" className="mt-5">
          <Row className="mb-3">
            <Col>
              <h3>New Upload</h3>
            </Col>
          </Row>
          <Row>
            <Col>
              <Form
                onSubmit={formik.handleSubmit}
              >
                  <Form.Group>
                  <Row>
                    <Col xs={{span: 10, offset: 1}}>
                      <FilePond
                        files={formik.values.pitchFile}
                        onupdatefiles={pitchFile => {
                          formik.setFieldValue("pitchFile", pitchFile)
                        }}
                        allowMultiple={false}
                        allowFileSizeValidation
                        maxFileSize="1000MB"
                        labelMaxFileSize="Maximum preview image size is {filesize}"
                        maxFiles={1}
                        name="files"
                        labelIdle='Drag and drop a PITCH file or <span class="filepond--label-action">Browse</span>'
                      />
                    </Col>
                  </Row>
                </Form.Group>
                {isSubmitting
                    ? (
                        <Row className="mt-2">
                          <Col>
                            <Loading/>
                          </Col>
                        </Row>
                      )
                    : null
                  }
                {formik.values.pitchFile?.length === 1 &&
                  <Button type="submit" variant="outline-primary" disabled={isSubmitting}>
                    Upload
                  </Button>
                }
              </Form>
            </Col>
          </Row>
          <Row className="mt-5">
            <Col>
              <h3>Preivous Uploads</h3>
            </Col>
          </Row>
          <Row className="mb-5 pb-5">
            <Col>
              <SortableTable
                columns={[
                  {
                    Header: 'File Name',
                    accessor: 'file_name',
                  },
                  {
                    Header: 'Symbol Clear Messages',
                    accessor: 'symbol_clear_message_count',
                  },
                  {
                    Header: 'Add Order Messages',
                    accessor: 'add_order_message_count',
                  },
                  {
                    Header: 'Modify Order Messages',
                    accessor: 'modify_order_message_count',
                  },
                  {
                    Header: 'Execute Order Messages',
                    accessor: 'execute_order_message_count',
                  },
                  {
                    Header: 'Trade Messages',
                    accessor: 'trade_message_count',
                  },
                  {
                    Header: 'Trade Break Messages',
                    accessor: 'trade_break_message_count',
                  },
                  {
                    Header: 'Cancel Order Messages',
                    accessor: 'cancel_order_message_count',
                  },
                  {
                    Header: 'Trading Status Messages',
                    accessor: 'trading_status_message_count',
                  },
                  {
                    Header: 'Auction Update Messages',
                    accessor: 'auction_update_message_count',
                  },
                  {
                    Header: 'Auction Summary Messages',
                    accessor: 'auction_summary_message_count',
                  },
                  {
                    Header: 'Retail Price Improvement Messages',
                    accessor: 'retail_price_improvement_message_count',
                  },
                ]}
                data={pitches}
                trStyle={{margin: 0, padding: 0, fontSize: "14px"}}
                thStyle={{margin: 0, fontSize: "14px"}}
                searchWidth={12}
                hideGlobalFilter
              />
            </Col>
          </Row>
        </div>
      </>
    );
};

export default Homepage;