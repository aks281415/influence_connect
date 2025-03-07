<template>
  <div>
    <InfluencerBar :username="username" />

    <div class="container mt-5">
      <h2>Ad Request Management</h2>

      <!-- Ad Requests List -->
      <div v-if="adRequests.length > 0">
        <div class="card mb-3" v-for="(adRequest, index) in adRequests" :key="index">
          <div class="card-body">
            <h5 class="card-title">Campaign name - {{ adRequest.campaign_name }}</h5>
            <h5 class="card-title">Sponsor name - {{ adRequest.sponsor_name }}</h5>
            <h5 class="card-title">Major Requirements - {{ adRequest.requirements }}</h5>

            <!-- Check if negotiation was accepted or rejected -->
            <!-- <p v-if="adRequest.payment_amount === adRequest.negotiated_payment_amount">
              <strong>Payment:</strong> ${{ adRequest.payment_amount }} (Negotiation Rejected)
            </p>
            <p v-else-if ="adRequest.is_negotiated !=1 && adRequest.payment_amount < adRequest.negotiated_payment_amount">
              <strong>Payment:</strong> ${{ adRequest.negotiated_payment_amount }} (Negotiation Accepted)
            </p> -->

            <!-- View Campaign Button -->
            <button class="btn btn-info me-2" @click="viewCampaign(adRequest.campaign_id)">
              <i class="fas fa-eye"></i> View Campaign
            </button>

            <!-- Status and Buttons Based on Ad Request Status -->
            <div v-if="adRequest.status === 'Pending'">
              <!-- Accept Button -->
              <button class="btn btn-success me-2" @click="updateStatus(adRequest.id, 'Accepted')">
                <i class="fas fa-check"></i> Accept
              </button>

              <!-- Reject Button -->
              <button class="btn btn-danger me-2" @click="updateStatus(adRequest.id, 'Rejected')">
                <i class="fas fa-times"></i> Reject
              </button>

              <!-- Negotiate Button -->
              <button class="btn btn-warning" @click="openNegotiateModal(adRequest)">
                <i class="fas fa-comment-dollar"></i> Negotiate
              </button>
            </div>

            <!-- Show Accepted/Rejected Button Based on Status -->
            <div v-else-if="adRequest.status === 'Accepted'">
              <button class="btn btn-success" disabled>
                <i class="fas fa-check"></i> Status: Accepted
              </button>
            </div>

            <div v-else-if="adRequest.status === 'Rejected'">
              <button class="btn btn-danger" disabled>
                <i class="fas fa-times"></i> Status: Rejected
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- No Requests Message -->
      <p v-else>No ad requests available yet.</p>
    </div>

    <!-- Negotiate Modal -->
    <div class="modal fade show" tabindex="-1" v-if="showNegotiateModal" style="display: block;">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Negotiate Ad Request</h5>
            <button type="button" class="btn-close" @click="closeNegotiateModal"></button>
          </div>
          <div class="modal-body">
            <p><strong>Current Payment Offer:</strong> ${{ currentAdRequest.payment_amount }}</p>

            <!-- Input for Payment Negotiation -->
            <div class="mb-3">
              <label for="payment" class="form-label">Your Payment Offer</label>
              <input v-model="negotiatedPayment" type="number" class="form-control" placeholder="Enter your payment offer" />
            </div>

            <!-- Messages Input -->
            <div class="mb-3">
              <label for="message" class="form-label">Your Negotiation Message</label>
              <textarea v-model="negotiationMessage" class="form-control" rows="3" placeholder="Enter your message"></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeNegotiateModal">Cancel</button>
            <button class="btn btn-primary" @click="submitNegotiation">Submit Negotiation</button>
          </div>
        </div>
      </div>
    </div>

    <!-- View Campaign Modal -->
    <div class="modal fade show" tabindex="-1" v-if="showCampaignModal" style="display: block;">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Campaign Details</h5>
            <button type="button" class="btn-close" @click="closeCampaignModal"></button>
          </div>
          <div class="modal-body">
            <p><strong>Campaign Name:</strong> {{ campaignDetails.name }}</p>
            <p><strong>Description:</strong> {{ campaignDetails.description }}</p>
            <p><strong>Start Date:</strong> {{ campaignDetails.start_date }}</p>
            <p><strong>End Date:</strong> {{ campaignDetails.end_date }}</p>
            <p><strong>Budget:</strong> ${{ campaignDetails.budget }}</p>
            <p><strong>Visibility:</strong> {{ campaignDetails.visibility }}</p>
            <p><strong>Category:</strong> {{ campaignDetails.category }}</p>
            
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeCampaignModal">Close</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Backdrop for the overlay -->
    <div class="modal-backdrop fade show" v-if="showCampaignModal || showNegotiateModal"></div>
  </div>
</template>

<script>
import axios from 'axios';
import InfluencerBar from '@/components/InfluencerBar.vue';

export default {
  name: 'InfluencerDashboard',
  components: {
    InfluencerBar
  },
  data() {
    return {
      adRequests: [],
      username: '',
      showNegotiateModal: false,
      showCampaignModal: false,
      currentAdRequest: {},
      campaignDetails: {},  // For storing campaign details
      negotiatedPayment: 0,
      negotiationMessage: ''
    };
  },
  created() {
    this.fetchAdRequests();
    this.fetchUsername();
  },
  methods: {
    async fetchAdRequests() {
      try {
        const response = await axios.get('http://localhost:5000/influencer/ad-requests', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        this.adRequests = response.data;
      } catch (error) {
        console.error('Error fetching ad requests:', error);
      }
    },
    async fetchUsername() {
      try {
        const response = await axios.get('http://localhost:5000/influencer/profile', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        this.username = response.data.username;
      } catch (error) {
        console.error('Error fetching username:', error);
      }
    },
    async viewCampaign(campaignId) {
      try {
        const response = await axios.get(`http://localhost:5000/influencer/campaign/${campaignId}`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        this.campaignDetails = response.data;  // Store the campaign details
        this.showCampaignModal = true;  // Open the modal
      } catch (error) {
        console.error('Error fetching campaign details:', error);
      }
    },
    closeCampaignModal() {
      this.showCampaignModal = false;
    },
    openNegotiateModal(adRequest) {
      this.currentAdRequest = adRequest;
      this.negotiatedPayment = adRequest.payment_amount; // Set initial payment amount
      this.showNegotiateModal = true;
    },
    closeNegotiateModal() {
      this.showNegotiateModal = false;
    },
    async submitNegotiation() {
      try {
        await axios.put(`http://localhost:5000/influencer/ad-request/${this.currentAdRequest.id}/negotiate`, {
          payment_amount: this.negotiatedPayment,
          message: this.negotiationMessage
        }, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });

        alert('Negotiation submitted successfully!');
        this.closeNegotiateModal();
        this.fetchAdRequests(); // Refresh the ad request list after negotiation
      } catch (error) {
        console.error('Error submitting negotiation:', error);
      }
    },
    async updateStatus(adRequestId, status) {
      try {
        await axios.put(`http://localhost:5000/influencer/ad-request/${adRequestId}/status`, {
          status: status
        }, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        alert(`Ad request ${status}`);
        this.fetchAdRequests(); // Refresh the ad requests after updating the status
      } catch (error) {
        console.error(`Error updating ad request to ${status}:`, error);
      }
    }
  }
};
</script>

<style scoped>
.card {
  border-radius: 10px;
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.1);
  padding: 15px;
  margin-bottom: 20px;
}

.modal-dialog {
  margin-top: 100px;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1040;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-content {
  border-radius: 10px;
  padding: 20px;
}

.modal-header {
  border-bottom: 1px solid #ddd;
}

.modal-footer {
  border-top: 1px solid #ddd;
}

.modal-body p {
  margin-bottom: 10px;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: bold;
}
</style>
