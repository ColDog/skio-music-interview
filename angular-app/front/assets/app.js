H = {};

H.api = 'http://127.0.0.1:8000'
H.path = function(path) {
    var args = Array.prototype.slice.call(arguments, 1);
    return H.host + args.join('/')
}

function access_token() { sessionStorage.getItem('token') }
function login(data) {
    sessionStorage.token = data.token
    sessionStorage.username = data.user.username
    sessionStorage.displayName = data.user.displayName
    sessionStorage.email = data.user.email
    sessionStorage.user_id = data.user.id

}
function flash(msg) { console.log(msg) }


var skio = angular.module('skio',
    [ 'ngRoute', 'controllers', 'ngResource', 'mm.foundation' ]
).config(
    ['$routeProvider',
    function($routeProvider) {
        $routeProvider
            .when('/', {
                templateUrl: 'partials/feed',
                controller: 'FeedController'
            })
            .when('/people', {
                templateUrl: '/partials/people',
                controller: 'PeopleController'
            })
            .when('/profile/:user_id', {
                templateUrl: '/partials/profile',
                controller: 'ProfileController'
            })
            .when('/login', {
                templateUrl: '/partials/login',
                controller: 'LoginController'
            })
            .otherwise({
                redirectTo: '/'
            });
    }],
    ['$resourceProvider', function ($resourceProvider) {
        $resourceProvider.defaults.headers['x-access-token'] = sessionStorage.token
        $resourceProvider.defaults.headers['Content-Type'] = 'application/json; charset=utf-8'
    }]
)