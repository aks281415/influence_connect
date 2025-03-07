<template>
  <div class="signup-container">
    <h2>Create an Account</h2>
    <form @submit.prevent="registerUser">
      <!-- Username -->
      <div class="input-group mb-3">
        <span class="input-group-text"><i class="fas fa-user"></i></span>
        <input
          v-model="username"
          type="text"
          class="form-control"
          placeholder="Enter your username"
          required
        />
      </div>

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

      <!-- Select Role -->
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
      <button type="submit" class="btn btn-primary w-100">Sign Up</button>
    </form>

    <p class="text-center mt-3">
      Already have an account?
      <router-link to="/login">Login here</router-link>
    </p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      username: "",
      email: "",
      password: "",
      role: "",
    };
  },
  methods: {
    async registerUser() {
      if (!this.role) {
        alert("Please select a role.");
        return;
      }

      try {
        const response = await axios.post("http://localhost:5000/auth/signup", {
          username: this.username,
          email: this.email,
          password: this.password,
          role: this.role,
        });
        alert("Signup successful! Please login.");
        this.$router.push("/login"); // Redirect to login page after successful signup
      } catch (error) {
        alert(error.response.data.error || "Signup failed, please try again.");
      }
    },
  },
};
</script>

<style scoped>
.signup-container {
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
