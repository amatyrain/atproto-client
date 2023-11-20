import datetime
import requests
import json
from libs.atproto.models.embed.external.view import View
from libs.atproto.models.feed.feed_view_post import FeedViewPost
from libs.atproto.models.feed.post_view import PostView
from libs.atproto.models.feed.recored import Record
from libs.atproto.models.feed.reply_ref import ReplyRef
from libs.atproto.models.richtext.facet.byte_slice import ByteSlice
from libs.atproto.models.richtext.facet.facet import Facet
from libs.atproto.models.richtext.facet.link import Link


class AtprotoClient:
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
        print(f"url: {url}")
        print(f"method: {method}")
        print(f"params: {params}")

        response = requests.request(
            method=method, url=url, params=params, data=data, headers=headers
        )

        if response.status_code >= 400:
            print("【AtprotoClient】投稿に失敗しました。")
            print(f"status_code: {response.status_code}")
            raise Exception(f"atproto_api: {response.text}\n{data}")

        return response

    def create_session(self) -> list[str, str]:
        endpoint = "com.atproto.server.createSession"
        method = "POST"

        data = {"identifier": self.identifier, "password": self.password}

        headers = {"Content-Type": "application/json; charset=UTF-8"}

        response = self._request(
            endpoint=endpoint, method=method, data=json.dumps(data), headers=headers
        )

        print(response.text)

        access_jwt = response.json()["accessJwt"]
        did = response.json()["did"]

        return [access_jwt, did]

    def get_author_feed(self) -> list[FeedViewPost]:
        endpoint = "app.bsky.feed.getAuthorFeed"
        method = "GET"

        params = {"actor": self.identifier}
        headers = {"Authorization": f"Bearer {self.access_jwt}"}

        response = self._request(
            endpoint=endpoint, method=method, params=params, headers=headers
        )

        response_json = response.json()
        print(response_json)

        feed_list = []
        for feed in response_json["feed"]:
            text = feed["post"]["record"]["text"]
            created_at = feed["post"]["record"]["createdAt"]
            cid = feed["post"]["cid"]
            parent_cid = (
                feed["post"]["record"]["reply"]["parent"]["cid"]
                if "reply" in feed["post"]["record"]
                else ""
            )

            """
            feedを構築
            """
            # facetsを構築
            facets = []
            facet_dict_list = (
                feed["post"]["record"]["facets"]
                if "facets" in feed["post"]["record"]
                else []
            )
            for facet_dict in facet_dict_list:
                # indexを構築
                index = ByteSlice(
                    byteStart=facet_dict["index"]["byteStart"],
                    byteEnd=facet_dict["index"]["byteEnd"],
                )

                # featuresを構築
                features = []
                for feature_dict in facet_dict["features"]:
                    feature = None
                    print(f'type: {feature_dict["$type"]}')
                    if feature_dict["$type"] == "app.bsky.richtext.facet#link":
                        feature = Link(
                            uri=feature_dict["uri"],
                        )

                    if feature is not None:
                        features.append(feature)

                facet = Facet(index=index, features=features)

                facets.append(facet)

            # recordを構築
            record = Record(text=text, created_at=created_at, facets=facets)

            # embedを構築
            embed = None
            post_embed_type = (
                feed["post"]["embed"]["$type"] if "embed" in feed["post"] else None
            )
            if post_embed_type is not None:
                embed_dict = feed["post"]["embed"]["external"]
                if post_embed_type == "app.bsky.embed.external#view":
                    embed = View(
                        uri=embed_dict["uri"],
                        title=embed_dict["title"],
                        description=embed_dict["description"],
                        thumb=embed_dict["thumb"],
                    )

            # postを構築
            post = PostView(cid=cid, record=record, embed=embed)

            feed_list.append(
                FeedViewPost(
                    post=post,
                    reply=ReplyRef(
                        parent=PostView(
                            cid=parent_cid,
                        ),
                    ),
                )
            )
            # if "embed" in feed["post"]:
            #     print(feed["post"]["embed"]["images"][0]["fullsize"])

        return feed_list

    def generate_post_from_text(self, text: str) -> dict:
        # URLを元の状態に戻す
        origin_text = text

        # origin_textからURLを抽出
        url_list = []
        for word in origin_text.split("\n"):
            if word.startswith("http"):
                url_list.append(word)

        # textをbyte文字列に変換
        byte_text = origin_text.encode("utf-8")

        # facetsを構築
        facets = []
        for url in url_list:
            # indexを構築
            index = {
                "byteStart": byte_text.find(url.encode("utf-8")),
                "byteEnd": byte_text.find(url.encode("utf-8")) + len(url),
            }

            # featuresを構築
            features = []
            feature = {
                "$type": "app.bsky.richtext.facet#link",
                "uri": url,
            }
            features.append(feature)

            facet = {
                "index": index,
                "features": features,
            }

            facets.append(facet)

        return {
            "$type": "app.bsky.feed.post",
            "text": text,
            "createdAt": datetime.datetime.now().isoformat(),
            "facets": facets,
        }

    def create_record(self, text: str):
        endpoint = "com.atproto.repo.createRecord"
        method = "POST"

        post = self.generate_post_from_text(text=text)

        data = {
            "repo": self.did,
            "collection": "app.bsky.feed.post",
            "record": post,
        }

        headers = {
            "Authorization": f"Bearer {self.access_jwt}",
            "Content-Type": "application/json; charset=UTF-8",
        }

        response = self._request(
            endpoint=endpoint, method=method, data=json.dumps(data), headers=headers
        )

        print(response.text)

        return response.json()
