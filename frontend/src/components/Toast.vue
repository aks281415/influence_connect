<template>
    <div v-if="visible" class="toast-notification">
      <p>{{ message }}</p>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      message: {
        type: String,
        required: true
      }
    },
    data() {
      return {
        visible: false
      };
    },
    methods: {
      show() {
        this.visible = true;
        // Hide the toast after 3 seconds
        setTimeout(() => {
          this.visible = false;
        }, 3000);
      }
    },
    mounted() {
      this.show();
    }
  };
  </script>
  
  <style scoped>
  .toast-notification {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background-color: #ff6b6b;
    color: white;
    padding: 15px 20px;
    border-radius: 5px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    animation: fadeIn 0.5s ease-in-out;
  }
  
  @keyframes fadeIn {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }
  </style>
  