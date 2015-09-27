var server = require('http').createServer()
var io = require('socket.io')(server)
var redis_source = require('redis')
var redis = redis_source.createClient()
var listener = redis_source.createClient()


function add_follower(followed_id, follower_id) {
    redis.rpush('followers:'+followed_id, follower_id, function(err, reply){
        console.log(reply)
    })
}
function add_feed(user_id, entry_id) { redis.lpush('feed:'+user_id, entry_id) }
function add_like(user_id, track_id) { redis.rpush('likes:'+user_id, track_id) }

function get_feed(user_id, cb) {
    redis.lrange('feed:'+user_id, 0, -1, function(err, feed) {
        if (feed) {
            console.log('feed', feed)
            cmds = []
            feed.forEach(function(entry_id){ cmds.push(['hgetall', entry_id]) })
            console.log('cmds', cmds)
            redis.multi(cmds).exec(function(err, entries){
                console.log('feed', entries)
                cb( entries )
            })
        }
    });
}

redis.on('connect', function(){
    console.log('redis connected')
})

listener.subscribe('new-entry')
listener.on('message', function(channel, message){
    if (channel == 'new-entry') {
        console.log('got new entry')
        var sender = message.split(':')[3]
        var entry_id = message
        redis.lrange('followers:'+sender, 0, -1, function(err, list){
            if (err) { throw err }
            if (list) {
                list.forEach(function(user_id){
                    add_feed(user_id, entry_id)
                });
            }
            add_feed(sender, entry_id)
        })
    }
})

io.on('connection', function(socket){
    console.log('connected')
    socket.emit('connect', 'hello')
    socket.on('add_follower', function(data){ add_follower(data.selected, data.follower) })
    socket.on('add_like', function(user_id, track_id){ add_like(user_id, track_id) })
    socket.on('get_feed', function(user_id){
        get_feed(user_id, function(entries){ socket.emit('send_feed', entries) })
    })
});

server.listen(4000, function(){
    console.log('listening on 4000')
});
