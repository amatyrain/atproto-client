import datetime
import requests
import json
from .models.embed.external.view import View
from .models.feed.feed_view_post import FeedViewPost
from .models.feed.post_view import PostView
from .models.feed.recored import Record
from .models.feed.reply_ref import ReplyRef
from .models.richtext.facet.byte_slice import ByteSlice
from .models.richtext.facet.facet import Facet
from .models.richtext.facet.link import Link


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
                post_embed_type_key = post_embed_type.split(".")[-1].split("#")[0]
                embed_dict = feed["post"]["embed"][post_embed_type_key]
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

    def generate_post_from_text(self, text: str, self_labels: list[str] = None) -> dict:
        """_summary_

        Args:
            text (str): _description_
            self_labels (ex. "porn")

        Returns:
            dict: _description_
        """
        post = {
            "$type": "app.bsky.feed.post",
            "text": text,
        }

        # labelsを構築
        if self_labels is not None:
            label_values = []
            for label in self_labels:
                label_values.append({"val": label})
            labels = {
                "$type": "com.atproto.label.defs#selfLabels",
                "values": label_values,
            }
            post["labels"] = labels

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
        post["facets"] = facets

        created_at = datetime.datetime.now(
            tz=datetime.timezone.utc).replace(tzinfo=None).isoformat(timespec="milliseconds") + "Z"
        post["createdAt"] = created_at

        return post

    def upload_image(self, image_url: str) -> dict:
        IMAGE_MIMETYPE = "image/png"
        # url to media binary data
        response = requests.get(image_url)
        img_bytes = response.content

        # this size limit is specified in the app.bsky.embed.images lexicon
        if len(img_bytes) > 1000000:
            raise Exception(
                f"image file size too large. 1000000 bytes maximum, got: {len(img_bytes)}"
            )

        resp = requests.post(
            "https://bsky.social/xrpc/com.atproto.repo.uploadBlob",
            headers={
                "Content-Type": IMAGE_MIMETYPE,
                "Authorization": "Bearer " + self.access_jwt,
            },
            data=img_bytes,
        )
        resp.raise_for_status()
        blob = resp.json()["blob"]

        return blob

    def create_record(self, text: str, image_url: str = None, self_labels: list[str] = None):
        endpoint = "com.atproto.repo.createRecord"
        method = "POST"

        post = self.generate_post_from_text(
            text=text, self_labels=self_labels
        )

        if image_url is not None:
            blob = self.upload_image(image_url=image_url)
            post["embed"] = {
                "$type": "app.bsky.embed.images",
                "images": [{
                    "alt": "image",
                    "image": blob,
                }],
            }

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
