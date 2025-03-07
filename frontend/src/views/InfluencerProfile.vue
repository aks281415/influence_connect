<template>
  <div>
    <!-- Include InfluencerBar for navigation -->
    <InfluencerBar :username="username" />

    <div class="profile-container">
      <h3>{{ isEditing ? 'Edit Your Profile' : `${username}'s Profile` }}</h3>

      <!-- If editing, show form inputs, otherwise show static profile details -->
      <div v-if="isEditing" class="edit-section">
        <div class="form-group">
          <label for="username"><i class="fas fa-user"></i> Username:</label>
          <input type="text" v-model="editUsername" id="username" class="form-control" />
        </div>

        <div class="form-group">
          <label for="category"><i class="fas fa-tag"></i> Category:</label>
          <select v-model="selectedCategory" id="category" class="form-control" @change="handleCategoryChange">
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

        <div class="form-group" v-if="selectedCategory === 'Other'">
          <label for="manualCategory"><i class="fas fa-pencil-alt"></i> Custom Category:</label>
          <input type="text" v-model="manualCategory" id="manualCategory" class="form-control" placeholder="Enter custom category" />
        </div>

        <div class="form-group">
          <label for="expertise"><i class="fas fa-user-tie"></i> Expertise:</label>
          <input type="text" v-model="expertise" id="expertise" class="form-control" />
        </div>

        <div class="form-group">
          <label for="reach"><i class="fas fa-users"></i> Reach:</label>
          <input type="number" v-model="reach" id="reach" class="form-control" />
        </div>

        <div class="btn-group">
          <button @click="saveProfile" class="btn btn-success">Save Changes</button>
          <button @click="toggleEdit" class="btn btn-secondary">Cancel</button>
        </div>
      </div>

      <!-- If not editing, show static profile details -->
      <div v-else class="profile-section">
        <p><i class="fas fa-user"></i> <strong>Username:</strong> {{ username }}</p>
        <p><i class="fas fa-tag"></i> <strong>Category:</strong> {{ category }}</p>
        <p><i class="fas fa-user-tie"></i> <strong>Expertise:</strong> {{ expertise }}</p>
        <p><i class="fas fa-users"></i> <strong>Reach:</strong> {{ reach }} followers</p>
        
        <button @click="toggleEdit" class="btn btn-primary">Edit Profile</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import InfluencerBar from '@/components/InfluencerBar.vue';

export default {
  components: {
    InfluencerBar // Register InfluencerBar component
  },
  data() {
    return {
      username: '',
      editUsername: '', // Store the editable username
      category: '',
      expertise: '',
      reach: 0,
      isEditing: false, // Toggle edit mode
      selectedCategory: '',
      manualCategory: ''
    };
  },
  created() {
    this.fetchProfileData();
  },
  methods: {
    async fetchProfileData() {
      try {
        const response = await axios.get('http://localhost:5000/influencer/profile', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        const profile = response.data;
        this.username = profile.username;
        this.editUsername = profile.username; // Initialize editable username
        this.category = profile.category;
        this.expertise = profile.expertise;
        this.reach = profile.reach;

        // Check if the category is predefined or custom
        if (!this.predefinedCategories.includes(this.category)) {
          this.selectedCategory = 'Other';
          this.manualCategory = this.category;
        } else {
          this.selectedCategory = this.category;
        }
      } catch (error) {
        console.error('Error fetching profile data:', error);
      }
    },
    toggleEdit() {
      this.isEditing = !this.isEditing;
    },
    handleCategoryChange() {
      if (this.selectedCategory !== 'Other') {
        this.manualCategory = '';
      }
    },
    async saveProfile() {
      try {
        const finalCategory = this.selectedCategory === 'Other' ? this.manualCategory : this.selectedCategory;

        await axios.put('http://localhost:5000/influencer/profile', {
          username: this.editUsername, // Update username
          category: finalCategory,
          expertise: this.expertise,
          reach: this.reach
        }, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });

        // Update local state after saving
        this.username = this.editUsername;
        this.category = finalCategory;
        this.isEditing = false; // Exit edit mode after saving
      } catch (error) {
        console.error('Error updating profile:', error);
      }
    }
  },
  computed: {
    predefinedCategories() {
      return [
        'Tech & Gadgets',
        'Fashion & Beauty',
        'Lifestyle',
        'Fitness & Health',
        'Travel & Adventure',
        'Food & Beverages',
        'Gaming',
        'Entertainment & Movies',
        'Music',
        'Parenting & Family',
      ];
    }
  }
};
</script>

<style scoped>
/* Styling for the profile page and InfluencerBar */
.profile-container {
  max-width: 600px;
  margin: 40px auto;
  padding: 30px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}

h3 {
  text-align: center;
  font-weight: bold;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  font-weight: bold;
  margin-bottom: 10px;
  display: block;
  color: #333;
}

.form-group input, .form-group select {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.btn-group {
  display: flex;
  justify-content: center;
  gap: 10px;
}

button {
  padding: 10px 20px;
  font-size: 1rem;
  border-radius: 5px;
  cursor: pointer;
}

.btn-primary {
  background-color: #007bff;
  border: none;
  color: white;
}

.btn-success {
  background-color: #28a745;
  border: none;
  color: white;
}

.btn-secondary {
  background-color: #6c757d;
  border: none;
  color: white;
}

.profile-section p {
  margin: 15px 0;
  font-size: 1.2rem;
  color: #555;
}

.profile-section i {
  margin-right: 10px;
}

.edit-section i {
  margin-right: 5px;
}

button:hover {
  opacity: 0.9;
}
</style>
