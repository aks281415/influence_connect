<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <!-- Display the username from the passed prop -->
      <a class="navbar-brand" href="#">{{ username }}</a>
      
      <!-- Toggle button for mobile view -->
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Navigation Links -->
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <!-- Ad Request Button -->
          <li class="nav-item">
            <button @click="goToAdRequestPage" class="btn btn-outline-light me-3">
              <i class="fas fa-paper-plane"></i> Ad Request
            </button>
          </li>
          <!-- Logout button -->
          <li class="nav-item">
            <button @click="logout" class="btn btn-outline-danger">Logout</button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  props: ['username'],  // Accept the username as a prop from parent
  methods: {
    goToAdRequestPage() {
      // Navigate to the Ad Request management page
      this.$router.push('/ad-request'); // This assumes you have the route set up in Vue Router
    },
    logout() {
      localStorage.removeItem('token'); // Remove token from localStorage
      this.$router.push('/login'); // Redirect to login page
    }
  }
};
</script>

<style scoped>
.navbar-brand {
  font-size: 1.5rem;
  font-weight: bold;
  color: #ffffff;
}

button {
  margin-left: 20px;
}
</style>
