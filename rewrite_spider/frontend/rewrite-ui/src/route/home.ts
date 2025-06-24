const homeRoute = [{
    path: '/',
    name: 'home',
    component: () => import('../views/Home.vue')
}, {
    path: '/article',
    name: 'article',
    component: () => import('../views/article/Home.vue'),
}, {
    path: '/article/content',
    name: 'articleContent',
    component: () => import('../views/article/Content.vue')
}, {
    path: '/other',
    name: 'other',
    component: () => import('../views/other/Other.vue'),
}
]

export default homeRoute