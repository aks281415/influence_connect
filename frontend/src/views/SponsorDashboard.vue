<template>
  <div>
    <!-- Pass the username prop to SponsorBar -->
    <SponsorBar :username="username" />

    <div class="container mt-5">
      <!-- Flexbox layout for the welcome message, Add Campaign button, and Search Sidebar -->
      <div class="row">
        <div class="col-md-9 text-center">
          <!-- Styled Welcome Message -->
          <h2 class="welcome-text me-3">Welcome, {{ username }}!</h2>
          
          <!-- Add Campaign and Download Report Buttons -->
          <div class="d-flex justify-content-center gap-3 mb-4">
            <button class="btn btn-primary" @click="openModal('add')">
              <i class="fas fa-plus"></i> Add Campaign
            </button>
            <button class="btn btn-success" @click="downloadReport">
              <i class="fas fa-download"></i> Download Report
            </button>
          </div>

          <!-- Display Filtered Influencers -->
          <div class="row">
            <div class="col-lg-4 col-md-6 mb-4" v-for="influencer in influencers" :key="influencer.id">
              <div class="card h-100 shadow-lg">
                <div class="card-header bg-primary text-white">
                  <h5 class="card-title">{{ influencer.username }}</h5>
                </div>
                <div class="card-body">
                  <p><strong>Category:</strong> {{ influencer.category }}</p>
                  <p><strong>Expertise:</strong> {{ influencer.expertise }}</p>
                  <p><strong>Reach:</strong> {{ influencer.reach }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Add Campaign Modal -->
          <AddCampaignModal v-if="showModal && modalMode !== 'view'" :visible="showModal" :mode="modalMode"
            :campaign="currentCampaign" @close="closeModal" @campaignAdded="fetchCampaigns" />

          <!-- View Campaign Modal -->
          <ViewCampaignModal v-if="showViewModal" :campaign="currentCampaign" @close="closeViewModal" />

          <!-- Campaigns List in Box Layout -->
          <div class="row" v-if="campaigns.length > 0">
            <div class="col-lg-4 col-md-6 mb-4" v-for="(campaign, index) in campaigns" :key="index">
              <div class="card h-100 shadow-lg">
                <div class="card-header bg-primary text-white">
                  <h5 class="card-title"><i class="fas fa-bullhorn"></i> {{ campaign.name }}</h5>
                </div>
                <div class="card-body">
                  <p class="card-text"><i class="fas fa-align-left"></i> <strong>Description:</strong> {{ campaign.description }}</p>
                  <p class="card-text"><i class="fas fa-calendar-alt"></i> <strong>Start Date:</strong> {{ campaign.start_date }}</p>
                  <p class="card-text"><i class="fas fa-calendar-check"></i> <strong>End Date:</strong> {{ campaign.end_date }}</p>
                  <p class="card-text"><i class="fas fa-dollar-sign"></i> <strong>Budget:</strong> ${{ campaign.budget }}</p>
                  <p class="card-text"><i class="fas fa-eye"></i> <strong>Visibility:</strong> {{ campaign.visibility }}</p>
                  <p class="card-text"><i class="fas fa-tags"></i> <strong>Category:</strong> {{ campaign.category }}</p>
                </div>
                <div class="card-footer bg-light">
                  <button class="btn btn-sm btn-warning me-2" @click="openModal('edit', campaign)"><i class="fas fa-edit"></i> Edit</button>
                  <button class="btn btn-sm btn-info me-2" @click="openViewModal(campaign)"><i class="fas fa-eye"></i> View</button>
                  <button class="btn btn-sm btn-danger" @click="deleteCampaign(campaign.id)"><i class="fas fa-trash"></i> Delete</button>
                </div>
              </div>
            </div>
          </div>
          <p v-else class="text-center">No campaigns added yet.</p>
        </div>

        <!-- Right Sidebar for Search Filters -->
        <div class="col-md-3">
          <div class="search-sidebar bg-light p-3 rounded">
            <h5>Search Influencers</h5>

            <!-- Category Filter Dropdown -->
            <select v-model="selectedCategory" class="form-control mb-2">
              <option disabled value="">Select a category</option>
              <option value="Tech & Gadgets">Tech & Gadgets</option>
              <option value="Fashion & Beauty">Fashion & Beauty</option>
              <option value="Lifestyle">Lifestyle</option>
              <option value="Fitness & Health">Fitness & Health</option>
              <option value="Travel & Adventure">Travel & Adventure</option>
              <option value="Food & Beverages">Food & Beverages</option>
              <option value="Gaming">Gaming</option>
              <option value="Entertainment & Movies">Entertainment & Movies</option>
              <option value="Music">Music</option>
              <option value="Parenting & Family">Parenting & Family</option>
              <option value="Other">Other</option>
            </select>

            <!-- Expertise Filter Input -->
            <input type="text" v-model="expertiseFilter" placeholder="Enter Expertise" class="form-control mb-2" />

            <!-- Reach Filter Input -->
            <input type="number" v-model="reachFilter" placeholder="Minimum Reach" class="form-control mb-2" />

            <!-- Search Button -->
            <button class="btn btn-primary w-100" @click="fetchInfluencers"><i class="fas fa-search"></i> Search</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SponsorBar from '@/components/SponsorBar.vue';
import AddCampaignModal from '@/components/AddCampaignModal.vue';
import ViewCampaignModal from '@/components/ViewCampaignModal.vue'; 
import axios from 'axios';

export default {
  name: 'SponsorDashboard',
  components: {
    SponsorBar,
    AddCampaignModal,
    ViewCampaignModal
  },
  data() {
    return {
      showModal: false,
      showViewModal: false,
      modalMode: 'add',
      currentCampaign: null,
      campaigns: [],
      username: '',
      selectedCategory: '',
      expertiseFilter: '',
      reachFilter: null,
      influencers: []
    };
  },
  created() {
    this.fetchUsername();
    this.fetchCampaigns();
  },
  methods: {
    async fetchUsername() {
      try {
        const response = await axios.get('http://localhost:5000/sponsor/details', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        this.username = response.data.username;
      } catch (error) {
        console.error('Error fetching username:', error);
      }
    },
    async fetchCampaigns() {
      try {
        const response = await axios.get('http://localhost:5000/sponsor/campaigns', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        this.campaigns = response.data;
      } catch (error) {
        if (error.response && error.response.status === 403) {
          alert('Profile incomplete. Please complete your profile first.');
          this.$router.push('/complete-profile');
        } else {
          console.error('Error fetching campaigns:', error);
        }
      }
    },
    async fetchInfluencers() {
      try {
        const response = await axios.get('http://localhost:5000/sponsor/influencers', {
          params: {
            category: this.selectedCategory,
            expertise: this.expertiseFilter,
            reach: this.reachFilter
          },
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        this.influencers = response.data;
      } catch (error) {
        console.error('Error fetching influencers:', error);
      }
    },
    openModal(mode, campaign = null) {
      this.modalMode = mode;
      this.currentCampaign = campaign ? { ...campaign } : null;
      this.showModal = true;
    },
    openViewModal(campaign) {
      this.currentCampaign = { ...campaign };
      this.showViewModal = true;
    },
    closeModal() {
      this.showModal = false;
    },
    closeViewModal() {
      this.showViewModal = false;
    },
    async deleteCampaign(campaignId) {
      try {
        await axios.delete(`http://localhost:5000/sponsor/campaigns/${campaignId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        this.fetchCampaigns();
      } catch (error) {
        console.error('Error deleting campaign:', error);
      }
    },
    async downloadReport() {
      try {
        const response = await axios.get('http://localhost:5000/sponsor/export-campaigns', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          },
          responseType: 'blob'  // Important for handling file download
        });

        // Create a blob from the response data
        const blob = new Blob([response.data], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        
        // Create a temporary link and trigger the download
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'campaign_report.csv');
        document.body.appendChild(link);
        link.click();
        
        // Clean up
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
      } catch (error) {
        console.error('Error downloading report:', error);
        alert('Error downloading report. Please try again.');
      }
    }
  }
};
</script>

<style scoped>
.search-sidebar {
  position: relative;
  max-width: 300px;
}
.card {
  border-radius: 10px;
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
  transition: transform 0.2s;
}

.card:hover {
  transform: scale(1.02);
}

.card-title {
  font-size: 1.4rem;
  font-weight: bold;
}

.card-text {
  font-size: 1rem;
  color: #333;
}

.card-header {
  border-bottom: 1px solid #ddd;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f8f9fa;
}

.container {
  padding-top: 20px;
}

.welcome-text {
  font-size: 2rem;
  font-weight: bold;
  color: #4a90e2;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

button {
  margin-left: 10px;
}
</style>