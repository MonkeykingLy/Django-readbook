import Vue from 'vue'
import Router from 'vue-router'
import login from './pages/login.vue'
import register from './pages/register.vue'
import homepage from './pages/homepage.vue'
import search_result from './pages/search_result'
import person from './pages/person.vue'
import one_book from './pages/one_book'
import my_bookspage from './pages/my_bookspage'
import recommendation from './pages/recommendation'
Vue.use(Router)

const router = new Router({
    routes: [
        {
            path: '/',
            redirect: '/homepage',
            meta:{
                title:'Homepage'
            }
        },
        {
            path: '/homepage',
            name: 'homepage',
            component: homepage,
            meta:{
                title:'Homepage'
            }
        },
        {
            path: '/register',
            name: 'register',
            component: register,
            meta:{
                title:'Register'
            }
        },
        {
            path: '/login',
            name: 'login',
            component: login,
            meta:{
                title:'Login'
            }
        },
		{
			path: '/person',
			name: 'person',
			component: person,
			meta:{
				title:'My Profile'
			}
		},
        {
            path: '/one_book',
            name: 'one_book',
            component: one_book,
            meta:{
                title:'Book Detail'
            }
        },
        {
            path: '/search_result',
            name: 'search_result',
            component: search_result,
            meta:{
                title:'Search Result'
            }
        },
        {
            path: '/my_bookspage',
            name: 'my_bookspage',
            component: my_bookspage,
            meta:{
                title:'My Books'
            }
        },
        {
            path: '/recommendation',
            name: 'recommendation',
            component: recommendation,
            meta:{
                title:'Recommendation'
            }
        },

    ],

})


// Route navigation guard
router.beforeEach((to, from, next) => {
    document.title=to.matched[0].meta.title
    // to The path to be accessed
    // from That means jump from that path
    // next It's a function that means release
    // next() release， next('/login') Forced to jump
    const tokenStr = window.localStorage.getItem('token')
    if (to.path === '/homepage' | to.path === '/login' |
        to.path === '/register'| to.path==='/one_book' | to.path==='/search_result' |
        to.path==='/my_bookspage' | to.path === '/recommendation') { return next() }
    else if (tokenStr == null) {
        return next('/homepage')
    }
    else next()
})

export default router