// Assuming Axios is available in your environment

// Import axios if you're using a module system (e.g., in a Node.js environment)
// If you're in a browser environment with Axios loaded via <script> tag, you can skip this line
const axios = require('axios');

const baseURL = "http://localhost:5000";

// const problem_name = 'two-sum';

function fetchGptHints(problem_name) {
    axios.get(baseURL + '/gpt/hints', {
        params: {
            problem_name: problem_name
        }
    })
    .then(function (response) {
        // Handle success
        console.log('Data:', response.data);
    })
    .catch(function (error) {
        // Handle error
        console.log('Error:', error);
    })
    .then(function () {
        // Always executed
        console.log('GET request to /gpt/hints completed');
    });
}

// Call the function to make the GET request
fetchGptHints('two-sum');
