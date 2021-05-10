import os
from distutils.dir_util import copy_tree
from pathlib import Path
from datetime import datetime
from io import StringIO

import markdown

class Renderer:

    PAGE_CHARACTER_THRESHOLD = 10000

    def __init__(self):
        with open("templates/landing.html") as f:
            self.landing_template = f.read()
        with open("templates/page.html") as f:
            self.page_template = f.read()
        with open("templates/post.html") as f:
            self.post_template = f.read()
        with open("templates/permafooter.html") as f:
            self.permafooter_template = f.read()
        with open("templates/feedfooter.html") as f:
            self.feedfooter_template = f.read()
        self.permapages = []
        self.feed_pages = []

    def _load_assets(self):
        copy_tree("assets", "output/assets")

    def _write_files(self):
        Path("output").mkdir(parents=True, exist_ok=True)
        with open('output/index.html', 'w+') as f:
            f.write(self.landing_template)
        
        for ts, permapage in self.permapages:
            Path(f"output/post/{ts}").mkdir(parents=True, exist_ok=True)
            with open(f"output/post/{ts}/index.html", 'w+') as f:
                f.write(permapage)

        for i, feed_page in enumerate(self.feed_pages):
            Path(f"output/feed/{i+1}").mkdir(parents=True, exist_ok=True)
            with open(f"output/feed/{i+1}/index.html", 'w+') as f:
                f.write(feed_page)

    def _fill_templates(self):
        html_contents = []
        char_cnt = 0
        num_feed_pages = 1
        md_file_names = os.listdir("thoughts")
        md_file_names.reverse()
        for i, file in enumerate(md_file_names):
            if file.endswith(".md"):
                with open("thoughts/" + file, "r", encoding="utf-8") as f:
                    text = f.read()
                char_cnt += len(text)
                content_html = markdown.markdown(text, extensions=['nl2br', 'tables'])
                content_html = content_html.replace("<code>", "<pre><code>").replace("</code>", "</code></pre>")
                raw_timestamp = file.split(".")[0]
                html_contents.append((raw_timestamp, content_html, num_feed_pages))

                if char_cnt > Renderer.PAGE_CHARACTER_THRESHOLD:
                    char_cnt = 0
                    if i < len(md_file_names)-1:
                        num_feed_pages += 1

        html_contents.sort(reverse=True)

        cur_page = 1
        main_feed_builder = StringIO()

        for i in range(len(html_contents)):
            ts, content_html, page_num = html_contents[i]

            # Main feed generation
            date = datetime.strptime(ts, "%Y%m%d%H%M")
            date_str = date.strftime("%a, %b %d, %Y %I:%M %p")
            post_block = self.post_template.format(
                content=content_html,
                timestamp=date_str,
                permalink_rel_path=f"../../post/{ts}"
            )
            main_feed_builder.write(post_block)

            if (i < len(html_contents)-1 and cur_page != html_contents[i+1][2]) or i == len(html_contents)-1:
                feed_footer = self.feedfooter_template.format(
                    newer=f"../{page_num-1}" if cur_page > 1 else "",
                    newer_text='<i class="fas fa-arrow-left"></i> Newer' if cur_page > 1 else "",
                    older=f"../{page_num+1}" if cur_page < num_feed_pages else "",
                    older_text='Older <i class="fas fa-arrow-right"></i>' if i < len(html_contents)-1 else "",
                    latest=f"../1",
                    latest_text="Latest" if num_feed_pages > 1 else "",
                    earliest=f"../{num_feed_pages}",
                    earliest_text="Earliest" if num_feed_pages > 1 else "",
                    separator="|"  if num_feed_pages > 1 else "",
                )
                feed_page = self.page_template.format(
                    posts=main_feed_builder.getvalue(),
                    url_depth="../../",
                    footer=feed_footer
                )
                self.feed_pages.append(feed_page)
                main_feed_builder = StringIO()
                cur_page += 1

            if i == len(html_contents)-1:
                pass

            # Permapages generation
            post_perma_block = self.post_template.format(
                content=content_html,
                timestamp=date_str,
                permalink_rel_path=""
            )
            perma_footer = self.permafooter_template.format(
                newer="../" + html_contents[i-1][0] if i > 0 else "",
                newer_text='<i class="fas fa-arrow-left"></i> Newer' if i > 0 else "",
                older="../" + html_contents[i+1][0] if i < len(html_contents)-1 else "",
                older_text='Older <i class="fas fa-arrow-right"></i>' if i < len(html_contents)-1 else "",
            )
            post_permagpage = self.page_template.format(
                posts=post_perma_block,
                url_depth="../../",
                footer=perma_footer,
            )
            self.permapages.append((ts, post_permagpage))

    def render(self):
        self._load_assets()
        self._fill_templates()
        self._write_files()

if __name__ == '__main__':
    Renderer().render()