<template>
    <div>
      <!-- Include NavBar at the top -->
      <NavBar />
  
      <!-- Page Content for Campaigns -->
      <div class="container mt-5">
        <h1 class="text-center mb-4">Manage Campaigns</h1>
        
        <!-- Campaigns List Table -->
        <table class="table table-striped">
          <thead>
            <tr>
              <th>S.No</th>
              <th>Campaign Name</th>
              <th>Description</th>
              <th>Visibility</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(campaign, index) in campaigns" :key="campaign.id">
              <td>{{ index + 1 }}</td>
              <td>{{ campaign.name }}</td>
              <td>{{ campaign.description }}</td>
              <td>{{ campaign.visibility }}</td>
              <td>
                <!-- Flag/Unflag Button based on current flagged status -->
                <button 
                  v-if="campaign.flagged === 'Active'" 
                  class="btn btn-danger" 
                  @click="toggleFlag(campaign.id, 'Flagged')">
                  Flag
                </button>
                <button 
                  v-else 
                  class="btn btn-success" 
                  @click="toggleFlag(campaign.id, 'Active')">
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
    name: 'Campaigns',
    components: {
      NavBar
    },
    data() {
      return {
        campaigns: []
      };
    },
    created() {
      this.fetchCampaigns();
    },
    methods: {
      async fetchCampaigns() {
        try {
          const response = await axios.get('http://localhost:5000/admin/campaigns', {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
          });
          this.campaigns = response.data;
        } catch (error) {
          console.error('Error fetching campaigns:', error);
        }
      },
      async toggleFlag(campaignId, status) {
        try {
          const endpoint = status === 'Flagged' 
            ? `http://localhost:5000/admin/flag-campaign/${campaignId}`
            : `http://localhost:5000/admin/unflag-campaign/${campaignId}`;
            
          await axios.put(endpoint, null, {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
          });
          this.fetchCampaigns(); // Refresh the list to update flagged status
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
  