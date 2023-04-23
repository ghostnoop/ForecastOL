import typing

from vkbottle_types.codegen.responses.wall import GetExtendedResponseModel, GetResponseModel, GetExtendedResponse, \
    GetResponse, GetCommentsExtendedResponse, GetCommentsResponse, GetCommentsResponseModel, \
    GetCommentsExtendedResponseModel


async def get(
        self,
        owner_id: typing.Optional[int] = None,
        domain: typing.Optional[str] = None,
        offset: typing.Optional[int] = None,
        count: typing.Optional[int] = None,
        filter: typing.Optional[str] = None,
        extended: int = 1,
        fields: typing.Optional[typing.List[str]] = None,
        **kwargs
) -> GetExtendedResponseModel:
    """Returns a list of posts on a user wall or community wall.

    :param owner_id: ID of the user or community that owns the wall. By default, current user ID. Use a negative value to designate a community ID.
    :param domain: User or community short address.
    :param offset: Offset needed to return a specific subset of posts.
    :param count: Number of posts to return (maximum 100).
    :param filter:
    :param extended: '1' — to return 'wall', 'profiles', and 'groups' fields, '0' — to return no additional fields (default)
    :param fields:
    """

    correct_types = (
        'photo', 'audio', 'video', 'doc', 'link', 'note', 'page', 'market_market_album', 'market', 'sticker'
    )

    params = self.get_set_params(locals())
    response = await self.api.request("wall.get", params)
    model = self.get_model(
        ((("extended",), GetExtendedResponse),),
        default=GetResponse,
        params=params,
    )
    items = response['response']['items']
    new_items = []
    for item in items:
        flag = False
        if 'attachments' in item:
            for attachment in item['attachments']:
                if not attachment['type'] in correct_types:
                    flag = True
                    break
        if not flag:
            new_items.append(item)

    response['response']['items'] = new_items

    return model(**response).response


async def get_comments(
        self,
        owner_id=None,
        post_id=None,
        need_likes=None,
        start_comment_id=None,
        offset=None,
        count=None,
        sort=None,
        preview_length=None,
        extended=None,
        fields=None,
        comment_id=None,
        thread_items_count=None,
        **kwargs
) -> typing.Union[GetCommentsResponseModel, GetCommentsExtendedResponseModel]:
    params = self.get_set_params(locals())
    response = await self.api.request("wall.getComments", params)
    model = self.get_model(
        ((("extended",), GetCommentsExtendedResponse),),
        default=GetCommentsResponse,
        params=params,
    )
    return model(**response).response
