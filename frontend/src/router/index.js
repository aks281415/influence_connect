import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import Signup from '../views/Signup.vue';
import AdminDashboard from '../views/AdminDashboard.vue';
import CompleteProfile from '@/views/CompleteProfile.vue';
import SponsorDashboard from '@/views/SponsorDashboard.vue';
import ProfileSetup from '@/views/ProfileSetup.vue';
import InfluencerDashboard from '@/views/InfluencerDashboard.vue';
import InfluencerProfile from '@/views/InfluencerProfile.vue';
// import AdRequestPage from '@/views/AdRequestPage.vue';
import SponsorAdRequests from '@/views/SponsorAdRequests.vue';
import CreateAdRequest from '@/views/CreateAdRequest.vue';
import InfluencerAdRequests from '@/views/InfluencerAdRequests.vue';
import Sponsors from '@/views/Sponsors.vue';
import Influencers from '@/views/Influencers.vue'
import Campaigns from '@/views/Campaigns.vue';

const routes = [
  {
    path: '/login',   // The URL path
    name: 'Login',    // The name of the route
    component: Login  // The component to render
  },
  {
    path: '/signup',
    name: 'Signup',
    component: Signup
  },
  {
    path: '/',  // Redirect root path to login by default
    redirect: '/login'
  },
  {
    path: '/complete-profile',
    name: 'CompleteProfile',
    component: CompleteProfile,
  },

  {
    path: '/admin',
    name : 'AdminDashboard',
    component : AdminDashboard
  },
  {
    path: '/sponsor',    // Sponsor Dashboard route
    name: 'SponsorDashboard',
    component: SponsorDashboard
  },
  {
    path: '/profile-setup',    
    name: 'ProfileSetup',
    component: ProfileSetup
  },
  {
    path: '/influencer',
    name: 'InfluencerDashboard',
    component: InfluencerDashboard
  },
  {
  path: '/influencer/profile',
  name: 'InfluencerProfile',
  component: InfluencerProfile
  },
  // {
  //   path: '/create-ad-request',
  //   name: 'AdRequestPage',
  //   component: AdRequestPage
  // },
  {
    path: '/ad-request',
    name: 'SponsorAdRequests',
    component: SponsorAdRequests
  },
  {
    path: '/create-ad-request',
    name: 'CreateAdRequest',
    component: CreateAdRequest
  },
  {
    path: '/influencer/ad-requests',
    name: 'InfluencerAdRequests',
    component: InfluencerAdRequests
  },
  {
    path: '/sponsors',
    name: 'Sponsors',
    component: Sponsors,
  },
  {
    path: '/influencers',
    name:'Influencers',
    component: Influencers
  },

  {
    path: '/Campaigns',
    name:'Campaigns',
    component: Campaigns
  }

];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
