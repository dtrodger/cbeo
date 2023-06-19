import axios from 'axios';
import config from '../config'

console.log()
const apiClient = axios.create({
    baseURL: config.API_BASE_URL
});

export default apiClient;