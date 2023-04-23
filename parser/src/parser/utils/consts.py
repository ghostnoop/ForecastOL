class ParserEnum:
    Wall = 'Wall'
    Comment = 'Comment'
    User = 'User'
    Like = 'Like'
    Follower = 'Follower'
    Following = 'Following'
    City = 'City'
    Country = 'Country'


class TypeTask:
    Comments = 'Comments'
    Followers = 'Followers'
    Following = 'Following'
    GroupMembers = 'GroupMembers'
    Group = 'Group'
    User = 'User'
    Users = 'Users'
    Wall = 'Wall'


USER_FIELDS = ['bdate', 'can_see_audio', 'can_see_all_posts', 'city', 'country', 'education', 'followers_count',
               'photo_400_orig', 'sex', 'schools', 'screen_name', 'military', 'nickname', 'photo_max_orig', 'relation',
               'relatives', 'universities', 'counters']

WALL_FIELDS = ['owner_id', 'from_id', 'created_by', 'date', 'text', 'reply_owner_id', 'reply_post_id', 'comments',
               'copyright', 'likes', 'reposts', 'views', 'post_type', 'post_source', 'attachments', 'geo', 'signer_id',
               'copy_history', 'marked_as_ads', 'topic_id']

GROUP_FIELDS = ['activity', 'city', 'contacts', 'counters', 'country', 'cover', 'description', 'finish_date', 'links',
                'members_count', 'place', 'site', 'status', 'verified']
