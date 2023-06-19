import React from "react"
import PublicLayout from '../views/layouts/PublicLayout';

const PublicRoute = ({ component: Component, ...rest }) => {
  return (
    <PublicLayout>
        <Component {...rest} />
    </PublicLayout>
  )
};

export default PublicRoute;