const axios = require('axios');

const API_URL = 'http://localhost:5000/api/auth';

const testAuth = async () => {
    try {
        console.log('--- Testing User Registration ---');
        const regRes = await axios.post(`${API_URL}/register`, {
            full_name: 'Test User',
            email: 'test@example.com',
            password: 'password123',
            role: 'customer'
        });
        console.log('Registration Success:', regRes.data);

        console.log('\n--- Testing User Login ---');
        const loginRes = await axios.post(`${API_URL}/login`, {
            email: 'test@example.com',
            password: 'password123'
        });
        console.log('Login Success:', loginRes.data);
        console.log('Token received:', loginRes.data.token);

    } catch (error) {
        console.error('Error:', error.response ? error.response.data : error.message);
    }
};

testAuth();
