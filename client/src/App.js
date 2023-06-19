import React from "react"
import {
  RouterProvider,
} from "react-router-dom";
import "filepond-plugin-image-preview/dist/filepond-plugin-image-preview.css";
import "filepond/dist/filepond.min.css";
import { configureSentry } from './libs/sentry';
import { configureFilepond } from './libs/filepond';
import { Toaster, ToastBar, toast } from 'react-hot-toast';
import { XCircle } from "react-bootstrap-icons";
import router from "./routes/router"
import './App.css';

configureSentry()
configureFilepond()

function App() {
  return (
    <div className="App">
      <Toaster
          toastOptions={{
            duration: 5000,
            style: {
              fontSize: '16px',
            },
            success: {
              style: {
                backgroundColor: '#e6ffe6',
              },
            },
            error: {
              style: {
                backgroundColor: '#ffcccb',
              },
            },
          }}
        >
          {(t) => (
              <ToastBar toast={t}>
                {({ icon, message }) => (
                  <>
                    {icon}
                    {message}
                    {t.type !== 'loading' && (
                      <XCircle onClick={() => toast.dismiss(t.id)}
                    />
                    )}
                  </>
                )}
              </ToastBar>
            )}
          </Toaster>
          <RouterProvider router={router} />
    </div>
  );
}

export default App;
