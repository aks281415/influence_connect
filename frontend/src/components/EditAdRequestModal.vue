<template>
    <div class="modal-backdrop">
      <div class="modal-container">
        <h3>Edit Ad Request</h3>
        <form @submit.prevent="submitEdit">
          <div class="form-group">
            <label for="influencerId">Influencer</label>
            <select
              id="influencerId"
              v-model="formData.influencer_id"
              class="form-control"
              required
            >
              <option v-for="influencer in influencers" :key="influencer.id" :value="influencer.id">
                {{ influencer.username }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label for="requirements">Requirements</label>
            <textarea
              id="requirements"
              v-model="formData.requirements"
              class="form-control"
              required
            ></textarea>
          </div>
          <div class="form-group">
            <label for="paymentAmount">Payment Amount</label>
            <input
              type="number"
              id="paymentAmount"
              v-model="formData.payment_amount"
              class="form-control"
              required
            />
          </div>
          <div class="mt-3">
            <button type="submit" class="btn btn-success">Save Changes</button>
            <button type="button" class="btn btn-secondary" @click="closeModal">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    props: {
      adRequest: {
        type: Object,
        required: true,
      },
    },
    data() {
      return {
        formData: {
          influencer_id: this.adRequest.influencer_id,
          requirements: this.adRequest.requirements,
          payment_amount: this.adRequest.payment_amount,
        },
        influencers: [], // List of available influencers
      };
    },
    created() {
      this.fetchInfluencers();
    },
    methods: {
      async fetchInfluencers() {
        try {
          const response = await axios.get("http://localhost:5000/sponsor/influencers", {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
          });
          this.influencers = response.data;
        } catch (error) {
          console.error("Error fetching influencers:", error);
        }
      },
      async submitEdit() {
        try {
          await axios.put(
            `http://localhost:5000/sponsor/ad-requests/${this.adRequest.id}`,
            this.formData,
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`,
              },
            }
          );
          this.$emit("update"); // Notify parent to refresh data
          this.closeModal();
          alert("Ad Request updated successfully.");
        } catch (error) {
          console.error("Error updating ad request:", error);
          alert("Failed to update the ad request.");
        }
      },
      closeModal() {
        this.$emit("close"); // Notify parent to close modal
      },
    },
  };
  </script>
  
  <style scoped>
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .modal-container {
    background: white;
    padding: 20px;
    border-radius: 10px;
    width: 400px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  }
  </style>
  