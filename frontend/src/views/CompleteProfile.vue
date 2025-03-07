<template>
  <div class="complete-profile-container">
    <h2>Complete Your Profile</h2>
    <form @submit.prevent="submitProfile">
      <div class="form-group">
        <label for="sponsor_type">Sponsor Type</label>
        <select v-model="sponsor_type" id="sponsor_type" required>
          <option value="" disabled>Select sponsor type</option>
          <option value="Individual">Individual</option>
          <option value="Organisation">Organisation</option>
        </select>
      </div>

      <div class="form-group">
        <label for="industry">Industry</label>
        <input v-model="industry" type="text" id="industry" placeholder="Enter your industry" required />
      </div>

      <button type="submit" class="submit-btn">Save Profile</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      sponsor_type: '', // Replace company_name with sponsor_type
      industry: '',
    };
  },
  methods: {
    async submitProfile() {
      try {
        const response = await axios.post('http://localhost:5000/sponsor/complete-profile', {
          sponsor_type: this.sponsor_type,
          industry: this.industry,
        }, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });

        if (response.data.message === 'Profile completed successfully!') {
          this.$router.push('/sponsor'); // Redirect to sponsor dashboard after profile completion
        }
      } catch (error) {
        console.error('Error updating profile:', error);
        alert('Failed to update profile. Please try again.');
      }
    }
  }
};
</script>

<style scoped>
.complete-profile-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

h2 {
  text-align: center;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input, select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.submit-btn {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.submit-btn:hover {
  background-color: #0056b3;
}
</style>
