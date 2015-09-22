var express = require('express');
var path = require('path');
var app = express();

function sf(res, file) { res.sendFile(path.join(__dirname + '/front/' + file)) }

app.get('/',                    function (req, res) { sf(res,'index.html') });
app.get('/partials/feed',       function (req, res) { sf(res,'/partials/feed.html') });
app.get('/partials/login',      function (req, res) { sf(res,'/partials/login.html') });
app.get('/partials/profile',    function (req, res) { sf(res,'/partials/profile.html') });
app.get('/partials/people',     function (req, res) { sf(res,'/partials/people.html') });
app.get('/partials/articles',   function (req, res) { sf(res,'/partials/articles.html') });



app.use('/assets', express.static('./front/assets'));
app.use('/vendor', express.static('./bower_components'));

var server = app.listen(3000, function () {
    console.log('Listening on 3000');
});