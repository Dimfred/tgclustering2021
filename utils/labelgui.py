from config import config
import utils

import PySimpleGUIQt as psg
import math


class GUI:
    def __init__(self):
        self.title = psg.Text("")
        self.description = psg.Text("")
        self.text = psg.Text("")
        self.input = psg.Input(enable_events=True, key="input")

        legend_text = "\n".join(
            f"{sc}: {label}" for sc, label in utils.mapped_topics.items()
        )
        self.legend = psg.Text(legend_text)

        self.topics = utils.mapped_topics
        self.assigned_topics = []
        self.assigned_topics_text = psg.Text("")

        self.dsnum = 0

        self.output_path = utils.make_topic_path(self.dsnum)

    @property
    def layout(self):
        self.base = [
            # ["POSTS"],
            [self.text, psg.VerticalSeparator(), self.legend],
            [psg.HorizontalSeparator()],
            [self.input],
            [self.assigned_topics_text],
            [psg.Button("submit", visible=False, bind_return_key=True)],
            # [self.legend],
        ]
        # if len(self.base)
        return self.base

    def datagen(self, start_idx=0):
        raw = utils.load_raw(self.dsnum)
        data = utils.load_data(self.dsnum)

        start_idx = 0
        counter = -1
        for r, d in zip(raw[start_idx:], data[start_idx:]):
            counter += 1
            if len(r) < 3:
                continue

            print(counter)
            # has_high_prob = False
            # for label_or_confidence in r[1:]:
            #     try:
            #         label_or_confidence = float(label_or_confidence)
            #         if label_or_confidence > 0.8:
            #             has_high_prob = True
            #             break
            #     except:
            #         pass

            # if not has_high_prob:
            #     continue


            idx = r[0]

            print(r[1:])
            text = "TITLE: {}\n\nDESC: {}\n\n".format(d["title"], d["description"])
            text += self.clean_posts(d["recent_posts"])

            yield idx, text

    def clean_posts(self, posts):
        posts = " ".join(posts)
        posts = posts.replace("\n", "")

        # break after 300 chars
        broken = []
        break_at = 200

        for i in range(math.ceil(len(posts) / break_at)):
            substring = posts[i * break_at : (i + 1) * break_at]
            broken.append(substring)

        posts = "\n".join(broken)

        return posts

    def next(self, gen):
        self.assigned_topics = []
        self.assigned_topics_text.update("")

        idx, text = next(gen)
        self.idx = idx
        self.text.update(text)

    @property
    def last_idx(self):
        with open(self.output_path, "r") as f:
            lines = f.readlines()

        try:
            idx = lines[-1].split(",")[0]
            return int(idx) + 1
        except:
            return 0

    def run(self):
        window = psg.Window("Label", self.layout, no_titlebar=True)

        gen = self.datagen(self.last_idx)

        while True:
            event, values = window.read()
            if event == psg.WIN_CLOSED or event == "Exit":
                break

            if event == "submit":
                shortcut = values["input"]
                self.input.Update("")

                # skip
                if shortcut == "nx":
                    self.next(gen)

                elif shortcut == "del":
                    if self.assigned_topics:
                        self.assigned_topics.pop()
                        self.assigned_topics_text.update(",".join(self.assigned_topics))

                elif shortcut == "ok":
                    with open(self.output_path, "a") as f:
                        label = [self.idx]
                        label.extend(self.assigned_topics)
                        label = ",".join(label)

                        print(label, file=f)

                    self.next(gen)

                elif shortcut in self.topics:
                    topic = self.topics[shortcut]
                    self.assigned_topics.append(topic)

                    self.assigned_topics_text.update(",".join(self.assigned_topics))

                else:
                    print("Doesnt exist")

        window.close()


if __name__ == "__main__":
    gui = GUI()
    gui.run()
