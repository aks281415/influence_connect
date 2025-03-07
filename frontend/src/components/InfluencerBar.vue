<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <!-- Replace username with 'Visit Profile' -->
      <a class="navbar-brand" href="#" @click.prevent="goToProfile">Visit Profile</a>

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
          <!-- Ad Requests button -->
          <li class="nav-item">
            <button @click="goToAdRequests" class="btn btn-outline-light me-3">
              <i class="fas fa-envelope"></i> Ad Requests
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
  methods: {
    goToProfile() {
      // Navigate to the profile page when 'Visit Profile' is clicked
      this.$router.push('/influencer/profile'); // Make sure this route is set up in your router
    },
    goToAdRequests() {
      // Navigate to the Ad Requests page where private ad requests will be shown
      this.$router.push('/influencer/ad-requests'); // Add this route to your router configuration
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
  cursor: pointer; /* Make it look clickable */
}

button {
  margin-left: 20px;
}
</style>
