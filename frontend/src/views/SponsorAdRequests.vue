<template>
  <div>
    <!-- Pass the username prop to SponsorBar -->
    <SponsorBar :username="username" />
    <div class="container mt-5">
      <h2>Sponsor Ad Request Management</h2>

      <!-- Button to add new Ad Request -->
      <div class="text-end mb-3">
        <button @click="goToCreateAdRequest" class="btn btn-primary">
          <i class="fas fa-plus"></i> Create Ad Request
        </button>
      </div>

      <!-- List of Ad Requests (created by Sponsor) -->
      <h3 class="mt-4">Ad Requests</h3>
      <div v-if="adRequests.length > 0">
        <div class="card mb-3" v-for="(adRequest, index) in adRequests" :key="index">
          <div class="card-body">
            <h5 class="card-title">Campaign: {{ adRequest.campaign_name }}</h5>
            <p><strong>Influencer:</strong> {{ adRequest.influencer_name }}</p>
            <p><strong>Requirements:</strong> {{ adRequest.requirements }}</p>
            <p><strong>Original Payment:</strong> ${{ adRequest.payment_amount }}</p>
            <p><strong>Negotiated Payment:</strong> ${{ adRequest.negotiated_payment_amount ?? 0 }}</p>

            <!-- Display negotiation details if there is a negotiation -->
            <div v-if="adRequest.is_negotiated && adRequest.negotiated_payment_amount">
              <p>
                <strong>Negotiated Amount:</strong> ${{ adRequest.negotiated_payment_amount }}
                (Pending approval)
              </p>
              
              <!-- Add negotiation action buttons -->
              <div class="mt-3">
                <button class="btn btn-success me-2" @click="acceptNegotiation(adRequest.id)">
                  <i class="fas fa-check"></i> Accept Negotiation
                </button>
                <button class="btn btn-danger" @click="rejectNegotiation(adRequest.id)">
                  <i class="fas fa-times"></i> Reject Negotiation
                </button>
              </div>
            </div>

            <!-- Display messages if available -->
            <div v-if="adRequest.negotiated_payment_amount && adRequest.messages">
              <strong>Messages:</strong>
              <ul>
                <li v-for="(message, index) in adRequest.messages.split('\n')" :key="index">
                  {{ message }}
                </li>
              </ul>
            </div>

            <!-- Display status based on 'status' field -->
            <p><strong>Status:</strong> {{ adRequest.status }}</p>

            <!-- Edit button visible only if status is Pending -->
            <div v-if="adRequest.status === 'Pending'">
              <button class="btn btn-primary me-2" @click="editAdRequest(adRequest)">Edit</button>
            </div>

            <button class="btn btn-danger" @click="deleteAdRequest(adRequest.id)">Delete</button>
          </div>
        </div>
      </div>
      <p v-else>No ad requests found. Create a new one!</p>

      <!-- Incoming Requests Section -->
      <h3 class="mt-5">Incoming Requests from Influencers</h3>
      <div v-if="incomingRequests.length > 0">
        <div class="card mb-3" v-for="(request, index) in incomingRequests" :key="index">
          <div class="card-body">
            <h5 class="card-title">Campaign: {{ request.campaign_name }}</h5>
            <p><strong>Influencer:</strong> {{ request.influencer_name }}</p>
            <p><strong>Payment Offer:</strong> ${{ request.payment_amount }}</p>
            <p><strong>Category:</strong> {{ request.category }}</p>
            <p><strong>Reach:</strong> {{ request.reach }}</p>

            <!-- Accept/Reject Buttons -->
            <div v-if="request.status === 'Pending'">
              <button class="btn btn-success me-2" @click="acceptIncomingRequest(request.id)">
                <i class="fas fa-check"></i> Accept Request
              </button>
              <button class="btn btn-danger" @click="rejectIncomingRequest(request.id)">
                <i class="fas fa-times"></i> Reject Request
              </button>
            </div>
          </div>
        </div>
      </div>
      <p v-else>No incoming requests at the moment.</p>
    </div>

    <!-- Edit Modal -->
    <EditAdRequestModal
      v-if="showEditModal"
      :adRequest="adRequestToEdit"
      @update="fetchAdRequests"
      @close="closeEditModal"
    />
  </div>
</template>

<script>
import axios from "axios";
import SponsorBar from "@/components/SponsorBar.vue";
import EditAdRequestModal from "@/components/EditAdRequestModal.vue";

export default {
  name: "SponsorAdRequests",
  components: {
    SponsorBar,
    EditAdRequestModal,
  },
  data() {
    return {
      username: "", // Store the username
      adRequests: [], // Store ad requests created by sponsor
      incomingRequests: [], // Store incoming requests from influencers
      adRequestToEdit: null, // Ad request to be edited
      showEditModal: false, // Control the edit modal visibility
    };
  },
  created() {
    this.fetchUsername();
    this.fetchAdRequests(); // Fetch sponsor-created ad requests
    this.fetchIncomingRequests(); // Fetch incoming ad requests from influencers
  },
  methods: {
    async fetchAdRequests() {
      try {
        const response = await axios.get("http://localhost:5000/sponsor/ad-requests", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        this.adRequests = response.data; // Store fetched ad requests
      } catch (error) {
        console.error("Error fetching ad requests:", error);
      }
    },
    async fetchIncomingRequests() {
      try {
        const response = await axios.get("http://localhost:5000/sponsor/incoming-requests", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        this.incomingRequests = response.data; // Store fetched incoming requests
      } catch (error) {
        console.error("Error fetching incoming requests:", error);
      }
    },
    async fetchUsername() {
      try {
        const response = await axios.get("http://localhost:5000/sponsor/details", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        this.username = response.data.username;
      } catch (error) {
        console.error("Error fetching username:", error);
      }
    },
    async acceptNegotiation(adRequestId) {
      try {
        await axios.put(`http://localhost:5000/sponsor/ad-requests/${adRequestId}/accept`, {}, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        await this.fetchAdRequests(); // Refresh the list
        alert("Negotiation accepted successfully.");
      } catch (error) {
        console.error("Error accepting negotiation:", error);
        alert("Error accepting negotiation. Please try again.");
      }
    },
    async rejectNegotiation(adRequestId) {
      try {
        await axios.put(`http://localhost:5000/sponsor/ad-requests/${adRequestId}/reject`, {}, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        await this.fetchAdRequests(); // Refresh the list
        alert("Negotiation rejected successfully.");
      } catch (error) {
        console.error("Error rejecting negotiation:", error);
        alert("Error rejecting negotiation. Please try again.");
      }
    },
    goToCreateAdRequest() {
      this.$router.push("/create-ad-request"); // Navigate to create ad request page
    },
    async editAdRequest(adRequest) {
      this.adRequestToEdit = adRequest;
      this.showEditModal = true;
    },
    async deleteAdRequest(adRequestId) {
      try {
        await axios.delete(`http://localhost:5000/sponsor/ad-requests/${adRequestId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        this.fetchAdRequests(); // Refresh the list after deletion
        alert("Ad Request deleted successfully.");
      } catch (error) {
        console.error("Error deleting ad request:", error);
      }
    },
    closeEditModal() {
      this.showEditModal = false;
    },
    async acceptIncomingRequest(requestId) {
      try {
        await axios.put(`http://localhost:5000/sponsor/incoming-requests/${requestId}/accept`, {}, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        this.fetchIncomingRequests(); // Refresh incoming requests after accepting
        alert("Request Accepted.");
      } catch (error) {
        console.error("Error accepting the incoming request:", error);
      }
    },
    async rejectIncomingRequest(requestId) {
      try {
        await axios.put(`http://localhost:5000/sponsor/incoming-requests/${requestId}/reject`, {}, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        this.fetchIncomingRequests(); // Refresh incoming requests after rejecting
        alert("Request Rejected.");
      } catch (error) {
        console.error("Error rejecting the incoming request:", error);
      }
    },
  },
};
</script>

<style scoped>
.card {
  border-radius: 10px;
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.1);
  padding: 15px;
  margin-bottom: 20px;
}
</style>