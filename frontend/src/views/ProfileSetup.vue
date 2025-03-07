<template>
    <div class="profile-setup-container">
      <h2>Complete Your Profile</h2>
      <form @submit.prevent="submitProfile">
        <!-- Predefined Category Dropdown -->
        <div class="form-group">
          <label for="category">Category</label>
          <select v-model="category" id="category" @change="handleCategoryChange" required>
            <option disabled value="">Select a category</option>
            <!-- Top 10 in-demand categories -->
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
            <option value="Other">Other</option> <!-- Option for manual entry -->
          </select>
        </div>
  
        <!-- Show manual category input if 'Other' is selected -->
        <div class="form-group" v-if="category === 'Other'">
          <label for="manualCategory">Enter Your Category</label>
          <input v-model="manualCategory" type="text" id="manualCategory" placeholder="Enter your category" required />
        </div>
  
        <div class="form-group">
          <label for="expertise">Expertise</label>
          <input v-model="expertise" type="text" id="expertise" placeholder="Enter your expertise" required />
        </div>
  
        <div class="form-group">
          <label for="reach">Reach</label>
          <input v-model="reach" type="number" id="reach" placeholder="Enter your reach" required />
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
        category: '',        // Selected value from dropdown
        manualCategory: '',  // For manual category input if "Other" is selected
        expertise: '',
        reach: ''
      };
    },
    methods: {
      handleCategoryChange() {
        if (this.category !== 'Other') {
          this.manualCategory = '';  // Reset manual input if category changes from 'Other'
        }
      },
      async submitProfile() {
        try {
          // Send finalCategory based on user selection
          const finalCategory = this.category === 'Other' ? this.manualCategory : this.category;
  
          const response = await axios.post('http://localhost:5000/influencer/profile-setup', {
            category: finalCategory,
            expertise: this.expertise,
            reach: this.reach
          }, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`
            }
          });
  
          if (response.data.message === 'Profile completed successfully!') {
            this.$router.push('/influencer'); // Redirect to dashboard after profile completion
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
  .profile-setup-container {
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
  
  input {
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
  