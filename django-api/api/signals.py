# from api.models import User, Track
from django.dispatch import receiver
from django.db.models.signals import post_save
import redis
import sys

Redis = redis.Redis(host='localhost', port=6379, db=0)


@receiver(post_save)
def send_redis(sender, **kwargs):
    print >>sys.stderr, 'SIGNAL:', sender, kwargs

    instance = kwargs['instance']
    name = sender._meta.model_name
    if name == 'collaborator':
        user_id = instance.track.user_id
        content = instance.track.description
        title = 'New collaborator, %s added to track %s' % (instance.user.name, instance.track.name)
    elif name == 'track':
        user_id = instance.user_id
        content = instance.description
        title = instance.user.name + 'added a track'
    elif name == 'comment':
        user_id = instance.track.user_id
        content = instance.content
        title = instance.user.name + 'commented on'
    else:
        return None

    key = '%s:%s:%s:%s' % ('entry', name, str(instance.id), str(user_id))
    msg = {'type': name, 'user_id': user_id, 'id': instance.id, 'content': content, 'title': title}
    Redis.hmset(key, msg)
    Redis.publish('new-entry', key)
