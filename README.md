## CBOE Pitch Data File Processor
### Components
- Django REST API that saves processed pitch files to a PostgreSQL database
- React UI that support uploading of pitch files, and retreving previously uploaded pitch file stastics
### Set up and Run  
1. Install [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/)
2. Build the API and UI Docker images, then run API, UI, PostgreSQL and Redis containers  
`$ make demo`  
3. Open [http://localhost:3000](http://localhost:3000) to view the upload interface  
