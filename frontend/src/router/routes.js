
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
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
    path: '/account/',
      component: () => import('layouts/AccountLayout.vue'),
      children: [
	  { path: '/account/', component: () => import('pages/IndexPage.vue') }
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
