import dataclasses


# ref: https://github.com/bluesky-social/atproto/blob/main/lexicons/app/bsky/embed/external.json
@dataclasses.dataclass
class View():
    # "uri": "https://www.oculus.com/appreferrals/amatyrain/6376559029122173/?utm_source=oculus&utm_location=2&utm_parent=frl&utm_medium=app_referral",
    uri: str | None = None
    # "title": "Get 25% off IRONSTRIKE | Meta Quest",
    title: str | None = None
    # "description": "",
    description: str | None = None
    # "thumb": "https://cdn.bsky.app/img/feed_thumbnail/plain/did:plc:uzbkphrap36a6hfbajkotmw6/bafkreihl6lahzpp7cxmsl7snpk2uk7r6nqjhjpkhozu6igiftxbfkibcx4@jpeg"
    thumb: str | None = None
