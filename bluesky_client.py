import requests
import json
from libs.bluesky.models.feed.FeedViewPost import FeedViewPost


class BlueskyClient:
    def __init__(self, identifier, password):
        self.identifier = identifier
        self.password = password
        self.base_url = "https://bsky.social/xrpc"
        self.access_jwt, self.did = self.create_session()

    def _request(
        self,
        endpoint,
        method,
        headers,
        params=None,
        data=None,
    ) -> requests.Response:
        url = f"{self.base_url}/{endpoint}"
        response = requests.request(
            method=method,
            url=url,
            params=params,
            data=data,
            headers=headers
        )
        return response

    def create_session(self) -> list[str, str]:
        endpoint = "com.atproto.server.createSession"
        method = "POST"

        data = {
            "identifier": self.identifier,
            "password": self.password
        }

        headers = {
            "Content-Type": "application/json; charset=UTF-8"
        }

        response = self._request(
            endpoint=endpoint,
            method=method,
            data=json.dumps(data),
            headers=headers
        )

        print(response)

        access_jwt = response.json()["accessJwt"]
        did = response.json()["did"]

        return [access_jwt, did]

    def get_author_feed(self, access_jwt) -> list[FeedViewPost]:
        endpoint = "app.bsky.feed.getAuthorFeed"
        method = "GET"

        params = {"actor": self.identifier}
        headers = {"Authorization": f"Bearer {access_jwt}"}

        response = self._request(
            endpoint=endpoint,
            method=method,
            params=params,
            headers=headers
        )

        response_json = response.json()
        print(response_json)

        feed_list = []
        for feed in response_json["feed"]:
            text = feed["post"]["record"]["text"]
            created_at = feed["post"]["record"]["createdAt"]
            cid = feed["post"]["cid"]
            parent_cid = feed["post"]["record"]["reply"]["parent"]["cid"] \
                if "reply" in feed["post"]["record"] else ''

            feed_list.append(FeedViewPost(
                text=text,
                created_at=created_at,
                cid=cid,
                parent_cid=parent_cid
            ))
            # if "embed" in feed["post"]:
            #     print(feed["post"]["embed"]["images"][0]["fullsize"])

        return feed_list
