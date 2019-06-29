var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
import Vue from 'vue';
import Router from 'vue-router';
var routerOptions = [
    { path: '/', component: 'Home' },
    { path: '/about', component: 'About' },
    { path: '*', component: 'NotFound' }
];
var routes = routerOptions.map(function (route) {
    return __assign({}, route, { component: function () { return import("@/components/" + route.component + ".vue"); } });
});
Vue.use(Router);
export default new Router({
    routes: routes,
    mode: 'history'
});
//# sourceMappingURL=index.js.map