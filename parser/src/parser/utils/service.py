from parser import BaseParser, CommentsParser, FollowersParser, FollowingParser, GroupMembersParser, GroupParser, \
    DetailUserParser, UsersParser, WallParser
from parser.utils.consts import TypeTask


def choose_parser(bp: BaseParser, type_of_model: str):
    if type_of_model == TypeTask.Comments:
        return CommentsParser(bp)
    if type_of_model == TypeTask.Followers:
        return FollowersParser(bp)
    if type_of_model == TypeTask.Following:
        return FollowingParser(bp)
    if type_of_model == TypeTask.GroupMembers:
        return GroupMembersParser(bp)
    if type_of_model == TypeTask.Group:
        return GroupParser(bp)
    if type_of_model == TypeTask.User:
        return DetailUserParser(bp)
    if type_of_model == TypeTask.Users:
        return UsersParser(bp)
    if type_of_model == TypeTask.Wall:
        return WallParser(bp)
