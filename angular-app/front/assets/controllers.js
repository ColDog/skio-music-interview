var controllers = angular.module('controllers', []);

controllers.controller('ApplicationController', ['$scope', '$resource', '$rootScope', '$location',
    function ($scope, $resource, $rootScope, $location) {
        $rootScope.current_user = function(){ return { displayName: sessionStorage.displayName, username: sessionStorage.username, user_id: sessionStorage.user_id } };
        $rootScope.logged_in = function() { return !!sessionStorage.getItem('token') };
        if (!$rootScope.logged_in()) { $location.path('/login') }
        $rootScope.$on('$locationChangeStart', function(){ if (!$rootScope.logged_in()) { $location.path('/login') } } );
    }]);

controllers.controller('FeedController', ['$scope', '$resource', '$rootScope', '$location',
    function ($scope, $resource, $rootScope, $location) {
        socket.on('connect', function(){
            socket.emit('get_feed', $rootScope.current_user().user_id)
        });
        socket.on('send_feed', function(feed){
            $scope.feed = feed
            $scope.$apply();
            console.log('got feed', feed)
        })
    }]);

controllers.controller('PeopleController', ['$scope', '$resource', '$rootScope', '$location',
    function ($scope, $resource, $rootScope, $location) {
        var User = $resource(H.api+'/users/:id', {id: '@id'})
        $scope.users = User.query()
        $scope.follow = function(id) {
            socket.emit('add_follower', { follower: $rootScope.current_user().user_id, selected: id })
        }
    }]);

controllers.controller('ProfileController', ['$scope', '$resource', '$routeParams', '$rootScope', '$location', '$http',
    function ($scope, $resource, $routeParams, $rootScope, $location, $http) {
        $rootScope.$on('$locationChangeStart', function(){
            if (!$rootScope.current_user().user_id == $routeParams.user_id ) {
                $location.path('/login') }
            }
        )
        var User = $resource(H.api+'/users/:id', {id: $routeParams.user_id})
        $scope.profile = User.get()
        $scope.tabs = [];
        $scope.newTrack = {};
        $scope.editUser = function() { User.save($scope.profile) }
        $scope.submitNewTrack = function() {
            $http.post(H.api+'/users/' + $rootScope.current_user().user_id + '/tracks', $scope.newTrack)
        }
    }]);

controllers.controller('LoginController', ['$scope', '$http', '$location', '$rootScope', '$location',
    function ($scope, $http, $location, $rootScope, $location) {
        $scope.newForm = {}
        $scope.loginForm = {}
        $scope.login = function() {
            $http.post(H.api+'/login', $scope.loginForm)
                .then(
                function(data){ login(data.data) ; $location.path('/profile'+data.data.user.id) },
                function(error){ console.log('login error', error) }
            )
        };

        $scope.newUser = function() {
            $http.post(H.api+'/users', $scope.newForm)
                .then(
                function(data){ console.log('login success', data) ; login(data.data) ; $location.path('/profile'+data.data.user.id) },
                function(error){ console.log('login error', error) }
            )
        }

        }
    ])
