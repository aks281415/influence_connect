<template>
  <div class="modal fade show" style="display: block;" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title"><i class="fas fa-info-circle"></i> {{ campaign.name }} - Details</h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>
        <div class="modal-body">
          <p><i class="fas fa-align-left"></i> <strong>Description:</strong> {{ campaign.description }}</p>
          <p><i class="fas fa-calendar-alt"></i> <strong>Start Date:</strong> {{ campaign.start_date }}</p>
          <p><i class="fas fa-calendar-check"></i> <strong>End Date:</strong> {{ campaign.end_date }}</p>
          <p><i class="fas fa-dollar-sign"></i> <strong>Budget:</strong> ${{ campaign.budget }}</p>
          <p><i class="fas fa-eye"></i> <strong>Visibility:</strong> {{ campaign.visibility }}</p>
          <p><i class="fas fa-bullseye"></i> <strong>Goals:</strong> {{ campaign.goals }}</p>
          <p><i class="fas fa-tags"></i> <strong>Category:</strong> {{ campaign.category }}</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="$emit('close')">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    campaign: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
.modal {
  background-color: rgba(0, 0, 0, 0.5);
}
.modal-dialog {
  max-width: 600px;
}
.modal-header {
  background-color: #343a40;
  color: white;
}
</style>
