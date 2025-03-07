<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h3 class="modal-title">{{ mode === 'edit' ? 'Edit Campaign' : 'Add Campaign' }}</h3>

      <div class="form-group">
        <label for="name"><i class="fas fa-pen"></i> Campaign Name</label>
        <input v-model="formData.name" type="text" id="name" class="form-control" placeholder="Enter campaign name" />
      </div>

      <div class="form-group">
        <label for="description"><i class="fas fa-align-left"></i> Campaign Description</label>
        <input v-model="formData.description" type="text" id="description" class="form-control" placeholder="Enter campaign description" />
      </div>

      <div class="form-group">
        <label for="start_date"><i class="fas fa-calendar-alt"></i> Start Date</label>
        <input v-model="formData.start_date" type="date" id="start_date" class="form-control" />
      </div>

      <div class="form-group">
        <label for="end_date"><i class="fas fa-calendar-check"></i> End Date</label>
        <input v-model="formData.end_date" type="date" id="end_date" class="form-control" />
      </div>

      <div class="form-group">
        <label for="budget"><i class="fas fa-dollar-sign"></i> Budget</label>
        <input v-model="formData.budget" type="number" id="budget" class="form-control" placeholder="Enter budget" />
      </div>

      <div class="form-group">
        <label for="visibility"><i class="fas fa-eye"></i> Visibility</label>
        <select v-model="formData.visibility" id="visibility" class="form-control">
          <option value="public">Public</option>
          <option value="private">Private</option>
        </select>
      </div>

      <div class="form-group">
        <label for="category"><i class="fas fa-tags"></i> Campaign Category</label>
        <select v-model="selectedCategory" id="category" @change="handleCategoryChange" class="form-control">
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

      <!-- Manual Category Input if 'Other' is selected -->
      <div class="form-group" v-if="selectedCategory === 'Other'">
        <label for="manualCategory"><i class="fas fa-pencil-alt"></i> Enter Your Category</label>
        <input v-model="manualCategory" type="text" id="manualCategory" class="form-control" placeholder="Enter your category" />
      </div>

      <div class="form-group">
        <label for="goals"><i class="fas fa-bullseye"></i> Campaign Goals</label>
        <textarea v-model="formData.goals" id="goals" class="form-control" placeholder="Enter campaign goals"></textarea>
      </div>

      <div class="modal-footer">
        <button @click="handleSubmit" class="btn btn-primary">{{ mode === 'edit' ? 'Save Changes' : 'Save' }}</button>
        <button @click="$emit('close')" class="btn btn-secondary">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    mode: {
      type: String,
      default: 'add',
    },
    campaign: {
      type: Object,
      default: () => ({}),
    },
  },
  data() {
    return {
      formData: this.getDefaultFormData(),
      selectedCategory: '',
      manualCategory: '',
    };
  },
  watch: {
    campaign: {
      immediate: true,
      handler(newCampaign) {
        if (this.mode === 'edit' && newCampaign) {
          this.formData = { ...newCampaign };
          this.selectedCategory = newCampaign.category || '';
        } else {
          this.formData = this.getDefaultFormData();
          this.selectedCategory = '';
        }
      },
    },
  },
  methods: {
    getDefaultFormData() {
      return {
        name: '',
        description: '',
        start_date: '',
        end_date: '',
        budget: '',
        visibility: 'public',
        goals: '',
      };
    },
    handleCategoryChange() {
      if (this.selectedCategory !== 'Other') {
        this.manualCategory = '';
      }
    },
    async handleSubmit() {
      const finalCategory = this.selectedCategory === 'Other' ? this.manualCategory : this.selectedCategory;

      const url = this.mode === 'edit'
        ? `http://localhost:5000/sponsor/campaigns/${this.campaign.id}`
        : 'http://localhost:5000/sponsor/campaigns';

      const method = this.mode === 'edit' ? 'put' : 'post';

      try {
        await axios({
          method: method,
          url: url,
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
          data: {
            ...this.formData,
            category: finalCategory,
          },
        });

        this.$emit('campaignAdded');
        this.$emit('close');
      } catch (error) {
        console.error('Error saving campaign:', error);
      }
    },
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 5px;
  width: 400px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 15px;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 15px;
  text-align: center;
}

.modal-footer {
  text-align: right;
}

button {
  margin-left: 10px;
}
</style>
