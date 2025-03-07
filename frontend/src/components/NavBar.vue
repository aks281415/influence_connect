<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <!-- Brand Logo -->
      <span class="navbar-brand" to="/">InfluenceConnect</span>

      <!-- Toggler for mobile view -->
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Navigation Links -->
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item" :class="{ active: isActive('/admin') }">
            <router-link class="nav-link" to="/admin">Dashboard</router-link>
          </li>
          <li class="nav-item" :class="{ active: isActive('/sponsors') }">
            <router-link class="nav-link" to="/sponsors">Sponsors</router-link>
          </li>
          <li class="nav-item" :class="{ active: isActive('/influencers') }">
            <router-link class="nav-link" to="/influencers">Influencers</router-link>
          </li>
          <li class="nav-item" :class="{ active: isActive('/campaigns') }">
            <router-link class="nav-link" to="/campaigns">Campaigns</router-link>
          </li>
        </ul>

        <!-- Logout Button -->
        <button class="btn btn-danger" @click="logout">Logout</button>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBar',
  methods: {
    // Logout method
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/login');
    },
    // Method to check the active route
    isActive(route) {
      return this.$route.path === route;
    }
  }
};
</script>

<style scoped>
/* Optional styling adjustments can go here */
</style>
