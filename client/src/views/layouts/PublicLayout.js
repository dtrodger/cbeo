import React from "react"
import Header from '../../components/Header';

const PublicLayout = props => {
  return (
    <>
      <div className="openLayout">
        <Header/>
        <div className="container mb-5">
          {props.children}
        </div>
      </div>
    </>
  )
};

export default PublicLayout;