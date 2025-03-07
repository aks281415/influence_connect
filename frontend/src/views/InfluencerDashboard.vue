<template>
  <div>
    <!-- InfluencerBar at the top -->
    <InfluencerBar :username="username" />

    <div class="dashboard-container">
      <!-- Main Content Area for Campaigns -->
      <div class="main-content">
        <h2 class="welcome-text">Welcome, {{ username }}!</h2>

        <div class="campaigns-container">
          <div class="row" v-if="filteredCampaigns.length > 0">
            <div class="col-lg-4 col-md-6 mb-4" v-for="(campaign, index) in filteredCampaigns" :key="index">
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
                  <p class="card-text"><i class="fas fa-user-tie"></i> <strong>Sponsor:</strong> {{ campaign.sponsor_name }}</p>
                  <p class="card-text"><i class="fas fa-tag"></i> <strong>Category:</strong> {{ campaign.category }}</p>

                  <!-- Apply Button -->
                  <button class="btn btn-success mt-3" @click="applyForCampaign(campaign.id)">
                    <i class="fas fa-paper-plane"></i> Apply
                  </button>
                </div>
              </div>
            </div>
          </div>
          <p v-else class="text-center">No campaigns found matching your criteria.</p>
        </div>
      </div>

      <!-- Sidebar for Search Filters (moved to the right side) -->
      <div class="sidebar">
        <h3 class="sidebar-title"><i class="fas fa-search"></i> Search Campaigns</h3>

        <!-- Category Dropdown with Icon -->
        <div class="form-group">
          <label for="category"><i class="fas fa-filter"></i> Category</label>
          <select v-model="selectedCategory" class="form-control">
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
        </div>

        <!-- Budget Range Inputs with Icons -->
        <div class="form-group">
          <label><i class="fas fa-dollar-sign"></i> Budget Range</label>
          <div class="d-flex">
            <input v-model.number="minBudget" type="number" placeholder="Min" class="form-control me-2" />
            <input v-model.number="maxBudget" type="number" placeholder="Max" class="form-control" />
          </div>
        </div>

        <!-- Search Button -->
        <button class="btn btn-primary w-100 mt-3" @click="fetchFilteredCampaigns">
          <i class="fas fa-search"></i> Search
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import InfluencerBar from '@/components/InfluencerBar.vue';
import axios from 'axios';

export default {
  name: 'InfluencerDashboard',
  components: {
    InfluencerBar
  },
  data() {
    return {
      username: '',  // Store the username
      campaigns: [],  // Store all campaigns
      filteredCampaigns: [],  // Store filtered campaigns based on search criteria
      selectedCategory: '',  // Store selected category
      minBudget: null,  // Minimum budget
      maxBudget: null  // Maximum budget
    };
  },
  created() {
    this.fetchUsername();   // Fetch username when component is created
    this.fetchCampaigns();  // Fetch campaigns when component is created
  },
  methods: {
    async fetchUsername() {
      try {
        const response = await axios.get('http://localhost:5000/influencer/profile', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        this.username = response.data.username;  // Store the username
      } catch (error) {
        console.error('Error fetching username:', error);
      }
    },

    async fetchCampaigns() {
      try {
        const response = await axios.get('http://localhost:5000/influencer/dashboard', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        this.campaigns = response.data;  // Store all campaigns
        this.filteredCampaigns = this.campaigns;  // Set filtered campaigns to all initially
      } catch (error) {
        if (error.response && error.response.status === 403) {
          alert('Profile incomplete. Please complete your profile first.');
          this.$router.push('/profile-setup');  // Redirect to profile setup page
        } else {
          console.error('Error fetching campaigns:', error);
        }
      }
    },

    async fetchFilteredCampaigns() {
      try {
        const response = await axios.get('http://localhost:5000/influencer/dashboard', {
          params: {
            category: this.selectedCategory,
            min_budget: this.minBudget,
            max_budget: this.maxBudget
          },
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        this.filteredCampaigns = response.data;
      } catch (error) {
        console.error('Error fetching filtered campaigns:', error);
      }
    },

    async applyForCampaign(campaignId) {
      try {
        await axios.post('http://localhost:5000/influencer/apply', {
          campaign_id: campaignId
        }, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        alert('Application sent successfully!');
      } catch (error) {
        console.error('Error applying for the campaign:', error);
      }
    }
  }
};
</script>

<style scoped>
.dashboard-container {
  display: flex;
  justify-content: space-between;
}

.main-content {
  flex-grow: 1;
  padding: 20px;
}

.sidebar {
  width: 250px;
  padding: 20px;
  background-color: #f8f9fa;
  border-left: 1px solid #ddd;
}

.sidebar-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #4a90e2;
}

.form-group {
  margin-bottom: 1rem;
}

.welcome-text {
  font-size: 1.8rem;
  font-weight: bold;
  color: #4a90e2;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.campaigns-container {
  padding-top: 20px;
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
</style>
