from enum import Enum

class TweetClass(Enum):
    SOURCE = 'source'
    DIRECT_REPLY = 'direct reply'
    RETWEET = 'retweet'
    DEEP_REPLY = 'deep reply'
    UNKNOWN = 'unknown'

TweetTypeColorMap = {
    TweetClass.SOURCE: 'blue',
    TweetClass.DIRECT_REPLY: 'yellow',
    TweetClass.RETWEET: 'lightblue',
    TweetClass.DEEP_REPLY: 'green',
    TweetClass.UNKNOWN: 'black'
}

class EdgeRelationship(Enum):
    FOLLOW = 'follows'
    RETWEET = 'retweets'
    REPLY = 'replies_to'

RelationColorMap = {
    EdgeRelationship.FOLLOW: 'pink',
    EdgeRelationship.RETWEET: 'lightblue',
    EdgeRelationship.REPLY: 'yellow'
}