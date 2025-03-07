<template>
    <div>
      <!-- Include NavBar at the top -->
      <NavBar />
  
      <!-- Page Content for Influencers -->
      <div class="container mt-5">
        <h1 class="text-center mb-4">Manage Influencers</h1>
        
        <!-- Influencers List Table -->
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
            <tr v-for="(influencer, index) in influencers" :key="influencer.id">
              <td>{{ index + 1 }}</td>
              <td>{{ influencer.username }}</td>
              <td>{{ influencer.email }}</td>
              <td>
                <!-- Flag/Unflag Button based on current flagged status -->
                <button 
                  v-if="influencer.flagged === 'Active'" 
                  class="btn btn-danger" 
                  @click="toggleFlag(influencer.id, 'Flagged')">
                  Flag
                </button>
                <button 
                  v-else 
                  class="btn btn-success" 
                  @click="toggleFlag(influencer.id, 'Active')">
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
    name: 'Influencers',
    components: {
      NavBar
    },
    data() {
      return {
        influencers: []
      };
    },
    created() {
      this.fetchInfluencers();
    },
    methods: {
      // Fetch the list of all influencers along with their flag statuses
      async fetchInfluencers() {
        try {
          const response = await axios.get('http://localhost:5000/admin/influencers', {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
          });
          this.influencers = response.data;
        } catch (error) {
          console.error('Error fetching influencers:', error);
        }
      },
      // Toggle flag status based on the current status
      async toggleFlag(influencerId, status) {
        try {
          const endpoint = status === 'Flagged' 
            ? `http://localhost:5000/admin/flag-influencer/${influencerId}`
            : `http://localhost:5000/admin/unflag-influencer/${influencerId}`;
            
          await axios.put(endpoint, null, {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
          });
          this.fetchInfluencers(); // Refresh the list to update flagged status
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
  