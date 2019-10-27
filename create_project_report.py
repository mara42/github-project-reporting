#!/usr/bin/env python3
"""
parse graphql made by get-project-status.sh script
"""
import requests


def query_github(request, token):
    headers = {"Authorization": f"bearer {auth}"}
    return requests.post(
        "https://api.github.com/graphql", headers=headers, json={"query": graphql}
    )


class Board:
    def __init__(self, dictionary):
        self.name = dictionary["name"]
        self._len = len(dictionary["cards"]["edges"])
        self.cards = Board._parse_cards(dictionary["cards"]["edges"])

    @property
    def title(self):
        return f"## {b.name}: Tickets {len(self)}\n\n"

    def __str__(self):
        return f"{self.name} with {len(self)} cards"

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return self._len

    @staticmethod
    def _parse_cards(raw_cards):
        cards = []
        for raw_card in raw_cards:
            rc = raw_card.get("node", {}).get("content", 0)
            if not rc:
                print("error")
                continue
            cards.append(Card(rc))
        return cards


class Card:
    def __init__(self, raw_card):
        self.title = raw_card["title"]
        self.labels = [c["node"]["name"] for c in raw_card["labels"]["edges"]]
        self.assignees = [a["node"]["login"] for a in raw_card["assignees"]["edges"]]
        self.body = raw_card["bodyText"]

    @property
    def content(self):
        content = []
        content.append(f"### {self.title}")
        content.append(f"**labels**: {', '.join(self.labels)}")
        content.append(f"**assignees**: {', '.join(self.assignees)}")
        content.append(self.body)
        return "\n\n".join(content)

    def __str__(self):
        return f"{self.title}, {self.labels}, {self.assignees}, {self.body[:10]}"

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    import datetime
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-u','--user', help='which github user\' repo', required=True)
    parser.add_argument('-r','--repo', help='repo name', required=True)
    args = vars(parser.parse_args())

    with open("github-project-cards.graphql", "r") as f:
        graphql = f.read()

    graphql = graphql.replace("{{repo}}", args['repo'])
    graphql = graphql.replace("{{user}}", args['user'])

    with open("github-oauth", "r") as f:
        auth = f.read().strip()

    r = query_github(graphql, auth)
    if r.status_code != 200 or "error" in r.text:
        print(r, r.text)
        sys.exit(1)
    raw_dict = r.json()

    # I'm embarrased to say that I don't know hot to use GraphQL
    project = raw_dict["data"]["repository"]["projects"]["edges"][0]["node"]
    raw_boards = project["columns"]["edges"]

    today = datetime.datetime.now().date()

    with open(f"{today} report.md", "w") as f:
        text = []
        text.append(f"# Report for {today}\n\n")
        for board in raw_boards:
            b = Board(board["node"])
            text.append(f"\n\n{b.title}")
            text.append("\n\n".join(c.content for c in b.cards))
        f.write("".join(text))
