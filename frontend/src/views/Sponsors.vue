<template>
  <div>
    <!-- Include NavBar at the top -->
    <NavBar />

    <!-- Page Content for Sponsors -->
    <div class="container mt-5">
      <h1 class="text-center mb-4">Manage Sponsors</h1>
      
      <!-- Sponsors List Table -->
      <table class="table table-striped">
        <thead>
          <tr>
            <th>S.No</th>
            <th>Name</th>
            <th>Email</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(sponsor, index) in sponsors" :key="sponsor.id">
            <td>{{ index + 1 }}</td>
            <td>{{ sponsor.username }}</td>
            <td>{{ sponsor.email }}</td>
            <td>
              <!-- Flag/Unflag Button based on current flagged status -->
              <button 
                v-if="sponsor.flagged === 'Active'" 
                class="btn btn-danger" 
                @click="toggleFlag(sponsor.id, 'Flagged')">
                Flag
              </button>
              <button 
                v-else 
                class="btn btn-success" 
                @click="toggleFlag(sponsor.id, 'Active')">
                Unflag
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import NavBar from '@/components/NavBar.vue';

export default {
  name: 'Sponsors',
  components: {
    NavBar
  },
  data() {
    return {
      sponsors: []
    };
  },
  created() {
    this.fetchSponsors();
  },
  methods: {
    async fetchSponsors() {
      try {
        const response = await axios.get('http://localhost:5000/admin/sponsors', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        this.sponsors = response.data;
      } catch (error) {
        console.error('Error fetching sponsors:', error);
      }
    },
    async toggleFlag(sponsorId, status) {
      try {
        const endpoint = status === 'Flagged' 
          ? `http://localhost:5000/admin/flag-sponsor/${sponsorId}`
          : `http://localhost:5000/admin/unflag-sponsor/${sponsorId}`;
          
        await axios.put(endpoint, null, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        this.fetchSponsors(); // Refresh the list to update flagged status
      } catch (error) {
        console.error('Error toggling flag status:', error);
      }
    }
  }
};
</script>

<style scoped>
.table {
  margin-top: 20px;
}
</style>
