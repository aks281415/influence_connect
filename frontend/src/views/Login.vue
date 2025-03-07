<template>
  <div class="login-container">
    <h2>Login to Your Account</h2>
    <form @submit.prevent="handleLogin">
      <!-- Email -->
      <div class="input-group mb-3">
        <span class="input-group-text"><i class="fas fa-envelope"></i></span>
        <input
          v-model="email"
          type="email"
          class="form-control"
          placeholder="Enter your email"
          required
        />
      </div>

      <!-- Password -->
      <div class="input-group mb-3">
        <span class="input-group-text"><i class="fas fa-lock"></i></span>
        <input
          v-model="password"
          type="password"
          class="form-control"
          placeholder="Enter your password"
          required
        />
      </div>

      <!-- Select Role (Admin, Sponsor, Influencer) -->
      <div class="input-group mb-3">
        <span class="input-group-text"><i class="fas fa-user-tag"></i></span>
        <select v-model="role" class="form-control" required>
          <option disabled value="">Select Role</option>
          <option value="Admin">Admin</option>
          <option value="Sponsor">Sponsor</option>
          <option value="Influencer">Influencer</option>
        </select>
      </div>

      <!-- Submit Button -->
      <button type="submit" class="btn btn-primary w-100">Login</button>
    </form>

    <p class="text-center mt-3">
      Don't have an account?
      <router-link to="/signup">Register here</router-link>
    </p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      email: '',
      password: '',
      role: ''
    };
  },
  methods: {
    async handleLogin() {
      try {
        const response = await axios.post('http://localhost:5000/auth/login', {
          email: this.email,
          password: this.password,
          role: this.role
        });

        // Check if the response contains an error message for unapproved sponsors
        if (response.data.error === 'Your account is pending approval by the admin.') {
          alert('Your account is pending approval by the admin. Please wait until your account is approved.');
          return;
        }

        // Store the JWT token in localStorage
        localStorage.setItem('token', response.data.access_token);

        // Redirect based on user role
        if (this.role === 'Sponsor') {
          if (response.data.message === 'Profile incomplete.') {
            this.$router.push('/complete-profile');  // Redirect to the "Complete Profile" page
          } else {
            this.$router.push('/sponsor'); // Redirect to sponsor dashboard
          }
        } else if (this.role === 'Influencer') {
          if (response.data.message === 'Profile incomplete.') {
            this.$router.push('/profile-setup');  // Redirect to profile setup page
          } else {
            this.$router.push('/influencer'); // Redirect to influencer dashboard
          }
        } else if (this.role === 'Admin') {
          this.$router.push('/admin'); // Redirect to admin dashboard
        }
      } catch (error) {
        // Display specific error messages
        if (error.response && error.response.data && error.response.data.error) {
          alert(error.response.data.error);
        } else {
          alert('Login failed. Please check your credentials.');
        }
      }
    }
  }
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #007bff;
}

.input-group-text {
  background-color: #007bff;
  color: white;
}

.input-group input,
.input-group select {
  padding: 10px;
}

button {
  padding: 10px;
  font-size: 16px;
}

p {
  margin-top: 15px;
}

p a {
  color: #007bff;
  text-decoration: none;
}

p a:hover {
  text-decoration: underline;
}
</style>
