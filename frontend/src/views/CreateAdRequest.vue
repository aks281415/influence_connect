<template>
    <div>
      <!-- SponsorBar at the top -->
      <SponsorBar :username="username" />
  
      <div class="container mt-5">
        <h2>Create Ad Request</h2>
  
        <!-- Form to create ad request -->
        <form @submit.prevent="createAdRequest">
          <!-- Campaign Selection -->
          <div class="mb-3">
            <label for="campaign" class="form-label"><i class="fas fa-bullhorn"></i> Select Private Campaign</label>
            <select v-model="selectedCampaign" id="campaign" class="form-select" required>
              <!-- Only show private campaigns -->
              <option v-for="campaign in privateCampaigns" :key="campaign.id" :value="campaign.id">
                {{ campaign.name }} ({{ campaign.visibility }})
              </option>
            </select>
          </div>
  
          <!-- Influencer Selection -->
          <div class="mb-3">
            <label for="influencer" class="form-label"><i class="fas fa-user"></i> Select Influencer</label>
            <select v-model="selectedInfluencer" id="influencer" class="form-select" required>
              <option v-for="influencer in influencers" :key="influencer.id" :value="influencer.id">
                {{ influencer.username }} (Category: {{ influencer.category }}, Reach: {{ influencer.reach }})
              </option>
            </select>
          </div>
  
          <!-- Requirements -->
          <div class="mb-3">
            <label for="requirements" class="form-label"><i class="fas fa-tasks"></i> Requirements</label>
            <textarea v-model="requirements" id="requirements" class="form-control" placeholder="Enter the requirements" required></textarea>
          </div>
  
          <!-- Payment Amount -->
          <div class="mb-3">
            <label for="payment" class="form-label"><i class="fas fa-dollar-sign"></i> Payment Amount</label>
            <input v-model="paymentAmount" type="number" id="payment" class="form-control" placeholder="Enter the payment amount" required />
          </div>
  
          <!-- Submit Button -->
          <button type="submit" class="btn btn-success">Submit Ad Request</button>
        </form>
  
        <!-- Error Message -->
        <p v-if="errorMessage" class="text-danger mt-3">{{ errorMessage }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import SponsorBar from '@/components/SponsorBar.vue';  // Ensure this is the correct path to SponsorBar.vue
  
  export default {
    components: {
      SponsorBar   // Register the SponsorBar component
    },
    data() {
      return {
        campaigns: [],            // Store list of campaigns
        privateCampaigns: [],     // Store filtered list of private campaigns
        influencers: [],          // Store list of influencers
        selectedCampaign: null,   // Selected campaign ID
        selectedInfluencer: null, // Selected influencer ID
        requirements: '',         // Requirements for the ad request
        paymentAmount: 0,         // Payment amount for the ad request
        errorMessage: '',         // Error message for validation or API issues
        username: ''              // Store the sponsor's username
      };
    },
    created() {
      this.fetchCampaigns();    // Fetch available campaigns
      this.fetchInfluencers();  // Fetch available influencers
      this.fetchUsername();     // Fetch sponsor's username for SponsorBar
    },
    methods: {
      async fetchCampaigns() {
        try {
          const response = await axios.get('http://localhost:5000/sponsor/campaigns', {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`
            }
          });
          this.campaigns = response.data; // Store fetched campaigns
          
          // Filter private campaigns
          this.privateCampaigns = this.campaigns.filter(campaign => campaign.visibility === 'private');
        } catch (error) {
          this.errorMessage = 'Error fetching campaigns. Please try again later.';
          console.error('Error fetching campaigns:', error);
        }
      },
      async fetchInfluencers() {
        try {
          const response = await axios.get('http://localhost:5000/sponsor/influencers', {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`
            }
          });
          this.influencers = response.data; // Store fetched influencers
        } catch (error) {
          this.errorMessage = 'Error fetching influencers. Please try again later.';
          console.error('Error fetching influencers:', error);
        }
      },
      async fetchUsername() {
        try {
          const response = await axios.get('http://localhost:5000/sponsor/details', {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`
            }
          });
          this.username = response.data.username; // Store the sponsor's username
        } catch (error) {
          console.error('Error fetching username:', error);
        }
      },
      async createAdRequest() {
        // Reset error message
        this.errorMessage = '';
  
        // Ensure all fields are filled
        if (!this.selectedCampaign || !this.selectedInfluencer || !this.requirements || !this.paymentAmount) {
          this.errorMessage = 'Please fill in all fields.';
          return;
        }
  
        try {
          const response = await axios.post('http://localhost:5000/sponsor/ad-requests', {
            campaign_id: this.selectedCampaign,
            influencer_id: this.selectedInfluencer,
            requirements: this.requirements,
            payment_amount: this.paymentAmount
          }, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`
            }
          });
  
          alert('Ad Request created successfully!');
          this.$router.push('/ad-request'); // Redirect back to ad request management
  
          // Reset form fields after successful submission
          this.selectedCampaign = null;
          this.selectedInfluencer = null;
          this.requirements = '';
          this.paymentAmount = 0;
        } catch (error) {
          this.errorMessage = 'Error creating ad request. Please try again later.';
          console.error('Error creating ad request:', error);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .container {
    max-width: 600px;
  }
  
  button {
    margin-top: 20px;
  }
  </style>
  