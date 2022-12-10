
const routes = [
  {
    path: '/',
    component: () => import('layouts/LoginLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') }
    ]
  },
  {
    path: '/login/',
      component: () => import('layouts/LoginLayout.vue'),
      children: [
	  { path: '/login/', component: () => import('pages/IndexPage.vue') }
      ]
  },
   {
      path: '/account/:username',
      component: () => import('layouts/AccountLayout.vue'),
      children: [
	  { path: '/account/', component: () => import('pages/IndexPage.vue') }
      ]
  },
   {
      path: '/followers/:username',
      component: () => import('layouts/FollowersLayout.vue'),
      children: [
	  { path: '/followers/', component: () => import('pages/IndexPage.vue') }
      ]
  },
   {
      path: '/feed',
      component: () => import('layouts/FeedLayout.vue'),
      children: [
	  { path: '/feed/', component: () => import('pages/IndexPage.vue') }
      ]
  },
   {
       path: '/message/:chatroom',
      component: () => import('layouts/MessagingLayout.vue'),
      children: [
	  { path: '/message/:chatroom/', component: () => import('pages/IndexPage.vue') }
      ]
  },
   {
       path: '/chatrooms',
      component: () => import('layouts/ChatroomsLayout.vue'),
      children: [
	  { path: '/chatrooms', component: () => import('pages/IndexPage.vue') }
      ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
