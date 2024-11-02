from enum import Enum

class TweetClass(Enum):
    SOURCE = 'source'
    DIRECT_REPLY = 'direct reply'
    RETWEET = 'retweet'
    DEEP_REPLY = 'deep reply'
    UNKNOWN = 'unknown'

ColorMap = {
    TweetClass.SOURCE: 'blue',
    TweetClass.DIRECT_REPLY: 'yellow',
    TweetClass.RETWEET: 'lightblue',
    TweetClass.DEEP_REPLY: 'green',
    TweetClass.UNKNOWN: 'red'
}