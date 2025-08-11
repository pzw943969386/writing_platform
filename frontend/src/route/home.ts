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
    path: '/splite',
    name: 'splite',
    component: () => import('../views/article/Splite.vue'),
},
// {
//     path: '/get_content',
//     name: 'getContent',
//     component: () => import('../views/article/GetContent.vue'),
// },
{
    path: '/write',
    name: 'write',
    component: () => import('../views/article/Write.vue'),
},
{
    path: '/think',
    name: 'think',
    component: () => import('../views/article/Thinking.vue'),
}
]

export default homeRoute