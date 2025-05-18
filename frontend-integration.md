# Frontend Integration Guide

This document outlines how the frontend team should connect to the backend API.

## API Endpoints

The backend exposes several endpoints that the frontend will need to interact with:

### Base URL

- Production: `https://drivex.uz/api/`
- Development: `http://localhost:8000/api/`

### Authentication

- Login: `POST /api/v1/token/`
  ```json
  {
    "username": "user@example.com",
    "password": "password"
  }
  ```
  Response:
  ```json
  {
    "access": "access_token_here",
    "refresh": "refresh_token_here"
  }
  ```

- Refresh Token: `POST /api/v1/token/refresh/`
  ```json
  {
    "refresh": "refresh_token_here"
  }
  ```

- Verify Token: `POST /api/v1/token/verify/`
  ```json
  {
    "token": "token_here"
  }
  ```

- Get User Data: `GET /api/v1/request-user-data/`
  Headers: `Authorization: Bearer <access_token>`

### API Documentation

For the complete API documentation, refer to:
- Swagger UI: `https://drivex.uz/swagger/`
- ReDoc: `https://your-domain.com/redoc/`

## CORS Configuration

The backend is configured to accept requests from the following origins:
- `http://localhost:3000` (development)
- `https://app.tpm.house` (production)
- `https://xsoftt.vercel.app` (additional frontend)

If you need to add additional origins, please let the backend team know so we can update the CORS configuration.

## Connection Setup in Frontend

### Example using Axios

```javascript
import axios from 'axios';

// Create an axios instance
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'https://drivex.uz/api/',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  }
});

// Add a request interceptor for authentication
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

// Add a response interceptor for token refresh
api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;
    
    // If the error is 401 and hasn't been retried yet
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        // Try to refresh the token
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post('https://drivex.uz/api/v1/token/refresh/', {
          refresh: refreshToken
        });
        
        // If token refresh is successful
        if (response.status === 200) {
          // Update tokens in storage
          localStorage.setItem('access_token', response.data.access);
          
          // Update authorization header
          api.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;
          originalRequest.headers['Authorization'] = `Bearer ${response.data.access}`;
          
          // Retry the original request
          return api(originalRequest);
        }
      } catch (err) {
        // If refresh fails, redirect to login
        console.error('Token refresh failed:', err);
        // Redirect to login page
        window.location.href = '/login';
      }
    }
    
    return Promise.reject(error);
  }
);

export default api;
```

## Health Check

You can use the backend health check endpoint to verify connectivity:

```javascript
// Check if backend is available
async function checkBackendHealth() {
  try {
    const response = await fetch('https://drivex.uz/api/health/');
    return response.ok; // Returns true if status is 200-299
  } catch (error) {
    console.error('Backend health check failed:', error);
    return false;
  }
}
```

## Deployment Notes

- The backend API is deployed to the same server as your frontend
- The backend runs on port 8000 and is proxied through Nginx
- Your frontend should be deployed to port 3000
- Both applications share the same domain with different paths

## Environment Variables

Your frontend application should have the following environment variables:

```
REACT_APP_API_URL=https://drivex.uz/api/
```

For local development:

```
REACT_APP_API_URL=http://localhost:8000/api/
```
