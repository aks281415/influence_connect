<template>
    <div>
      <!-- Include NavBar at the top -->
      <NavBar />
  
      <div class="container mt-5">
        <h1 class="text-center mb-4">Admin Dashboard</h1>
  
        <!-- Statistics Grid -->
        <div class="row">
          <div class="col-md-4 mb-4" v-for="(stat, index) in statistics" :key="index">
            <div class="card h-100 shadow-sm stat-card">
              <div class="card-body text-center">
                <h3 class="card-title">{{ stat.label }}</h3>
                <p class="card-text display-6">{{ stat.value }}</p>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Flagged Sponsors for Approval -->
        <div class="container mt-4">
          <h3>To Approve Sponsors</h3>
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
              <tr v-for="(sponsor, index) in flaggedSponsors" :key="sponsor.id">
                <td>{{ index + 1 }}</td>
                <td>{{ sponsor.username }}</td>
                <td>{{ sponsor.email }}</td>
                <td>
                  <button class="btn btn-success" @click="approveSponsor(sponsor.id)">
                    Approve
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
  
        <!-- Flagged Influencers for Approval -->
        <div class="container mt-4">
          <h3>To Approve Influencers</h3>
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
              <tr v-for="(influencer, index) in flaggedInfluencers" :key="influencer.id">
                <td>{{ index + 1 }}</td>
                <td>{{ influencer.username }}</td>
                <td>{{ influencer.email }}</td>
                <td>
                  <button class="btn btn-success" @click="approveInfluencer(influencer.id)">
                    Approve
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
  
        <!-- Recent Ad Requests -->
        <div class="container mt-4">
          <h3>Recent Ad Requests</h3>
          <table class="table table-striped">
            <thead>
              <tr>
                <th>S.No</th>
                <th>Campaign Name</th>
                <th>Sponsor Name</th>
                <th>Influencer Name</th>
                <th>Requirements</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(request, index) in recentAdRequests" :key="request.id">
                <td>{{ index + 1 }}</td>
                <td>{{ request.campaign_name }}</td>
                <td>{{ request.sponsor_name }}</td>
                <td>{{ request.influencer_name }}</td>
                <td>{{ request.requirements }}</td>
                <td>{{ request.status }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import NavBar from '@/components/NavBar.vue';
  
  export default {
    name: 'AdminDashboard',
    components: {
      NavBar,
    },
    data() {
      return {
        statistics: [],
        flaggedSponsors: [],
        flaggedInfluencers: [],
        recentAdRequests: [],
      };
    },
    created() {
      this.fetchDashboardStats();
      this.fetchFlaggedSponsors();
      this.fetchFlaggedInfluencers(); // Fetch flagged influencers
      this.fetchRecentAdRequests();
    },
    methods: {
      async fetchDashboardStats() {
        try {
          const response = await axios.get('http://localhost:5000/admin/dashboard', {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
          });
          this.statistics = [
            { label: 'Total Sponsors', value: response.data.total_sponsors },
            { label: 'Flagged Sponsors', value: response.data.flagged_sponsors },
            { label: 'Total Influencers', value: response.data.total_influencers },
            { label: 'Flagged Influencers', value: response.data.flagged_influencers },
            { label: 'Total Campaigns', value: response.data.total_campaigns },
            { label: 'Public Campaigns', value: response.data.public_campaigns },
            { label: 'Private Campaigns', value: response.data.private_campaigns },
            { label: 'Flagged Campaigns', value: response.data.flagged_campaigns },
            { label: 'Total Ad Requests', value: response.data.total_ad_requests },
            { label: 'Pending Ad Requests', value: response.data.pending_ad_requests },
            { label: 'Accepted Ad Requests', value: response.data.accepted_ad_requests },
            { label: 'Rejected Ad Requests', value: response.data.rejected_ad_requests },
          ];
        } catch (error) {
          console.error('Error fetching admin dashboard statistics', error);
        }
      },
      async fetchFlaggedSponsors() {
        try {
          const response = await axios.get('http://localhost:5000/admin/flagged-sponsors', {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
          });
          this.flaggedSponsors = response.data;
        } catch (error) {
          console.error('Error fetching flagged sponsors', error);
        }
      },
      async fetchFlaggedInfluencers() {
        try {
          const response = await axios.get('http://localhost:5000/admin/influencers', {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
          });
          this.flaggedInfluencers = response.data.filter(influencer => influencer.flagged === 'Flagged');
        } catch (error) {
          console.error('Error fetching flagged influencers', error);
        }
      },
      async fetchRecentAdRequests() {
        try {
          const response = await axios.get('http://localhost:5000/admin/recent-ad-requests', {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
          });
          this.recentAdRequests = response.data;
        } catch (error) {
          console.error('Error fetching recent ad requests', error);
        }
      },
      async approveSponsor(sponsorId) {
        try {
          await axios.post(`http://localhost:5000/admin/approve-sponsor/${sponsorId}`, null, {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
          });
          this.fetchFlaggedSponsors();
        } catch (error) {
          console.error('Error approving sponsor:', error);
        }
      },
      async approveInfluencer(influencerId) {
        try {
          await axios.post(`http://localhost:5000/admin/approve-influencer/${influencerId}`, null, {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
          });
          this.fetchFlaggedInfluencers(); // Refresh the flagged influencers list
        } catch (error) {
          console.error('Error approving influencer:', error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .card {
    border-radius: 10px;
  }
  
  .stat-card:hover {
    animation: blink 0.8s linear infinite;
    cursor: pointer;
  }
  
  @keyframes blink {
    0% {
      opacity: 1;
    }
    50% {
      opacity: 0.5;
    }
    100% {
      opacity: 1;
    }
  }
  </style>
  