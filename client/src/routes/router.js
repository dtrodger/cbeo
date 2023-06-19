import {
  createBrowserRouter,
} from "react-router-dom";
import PublicRoute from './PublicRoute';
import Homepage from "../views/Homepage";
import NotFound from '../views/NotFound';

const router = createBrowserRouter([
  {
    path: "/",
    element: <PublicRoute path="*" component={Homepage} />,
  },
  {
    path: "*",
    element: <PublicRoute path="*" component={NotFound} />,
  },
]);

export default router;