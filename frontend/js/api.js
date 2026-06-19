const API_BASE = window.API_BASE_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
    baseURL: API_BASE,
    headers: { 'Content-Type': 'application/json' },
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            const path = window.location.pathname;
            if (!path.includes('login') && !path.includes('register')) {
                localStorage.removeItem('access_token');
                localStorage.removeItem('user');
            }
        }
        return Promise.reject(error);
    }
);

window.api = api;
