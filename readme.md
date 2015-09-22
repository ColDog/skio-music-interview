This app serves an Angular front end from a Django back end. Stuck in the middle is a Node.js application that serves the front end through Socket.io. Django notifies Node through the Redis pub/sub. The idea is to offload some of the more taxing operations that don't need atomicity or reliability to the Node.js application which will only interact with Redis.

### Django
The Django application uses a custom built API controller. I did this instead of using Django Rest basically to learn Python and Django. I do like the overall design, however, and I find it easier to use than the Serializers in the Rest framework.

One of the key features of my implementation is that it hacks into the normal Django models and adds features to transform the models to dictionaries that can be called directly from the instance. I don't think I would go without this developing any custom api! It's one of the many features that I found myself wanting from Rails.

I also installed a custom authentication framework in Django that is mounted as a middleware. It essentially checks a url to see if it matches a protected route regex and then uses the json web token standard to authenticate a user.

### Node.js
The Node application is very barebones. In the architecture the Node application handles all of the 'social' aspects of the app. When someone follows a user Node is notified through the socket connection and it pushes their user id into the array of followers for the target user.

I had an interesting idea to build the users 'feed,' basically a list of things that their followers have done lately. When a person does anything of interest, the key parts of the action are pushed into a dictionary in Django and saved in Redis as an 'entry.' The node application picks up on this through the Redis pub/sub and adds the id of the entry into each 'feed' array (stored in Redis) for every follower of the user that has done something interesting. The idea is, when a user logs in to view their feed, there is no hit to the backend database. Instead, Node queries Redis for the necessary entries based on the users feed array. I've implemented the backend version of this which is working well. I think it is a unique and simple solution to providing a social feed that takes load off the database.

### Angular
The Angular application has been shown some neglect so far, as I was more interested in learning Python and to build middleware and controllers in Django. I have learned quite a lot about Angular, and love the way it works so far. Stay tuned.
