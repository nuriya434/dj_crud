document.getElementById('login-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('/api/token/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        if (!response.ok) {
            throw new Error('Invalid username or password');
        }

        const saveSuccess = await saveUserData(username, password);
        if (saveSuccess) {
            alert('User data saved in the database!');
        } else {
            alert('Failed to save user data in the database');
        }

        localStorage.setItem('token', data.access);
        window.location.href = '/';
    } catch (error) {
        document.getElementById('login-error').style.display = 'block';
        console.error('Login error:', error);
    }
});

async function saveUserData(username, password) {
    try {
        const response = await fetch('/save-user-data/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        if (!response.ok) {
            throw new Error('Failed to save user data to the database');
        }

        return true;
    } catch (error) {
        console.error('Failed to save user data to the database:', error);
        return false;
    }
}
