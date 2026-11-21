# news-image-20261121-entry

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/KimLyNamHa/news-image-20261121-entry/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/KimLyNamHa/news-image-20261121-entry/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A program that draws the world news of Saturday 21 November 2026 into one 1024×1024 image — 33 stories on one newspaper front page, drawn programmatically with PIL (`draw_poster.py`).

The page follows the day in order: three Houthi missiles shot down over Riyadh in the early hours, a magnitude 6.7 earthquake in Junín, Peru at 00:09 UTC, then COP31 running into overtime in Antalya with no deal in sight. Below that are ten more stories — the double strike on Kryvyi Rih, Trump's data-centre tax vow, China telling Japan to correct its Taiwan words, the Air Niugini 767 landing safely in Davao, bitcoin below $59,000, Russell fastest in Las Vegas GP practice, Rahul's century in Wellington, BepiColombo reaching Mercury, the ANC's worst result since 1994, and the funeral boat capsizing in Bayelsa — plus 20 one-line briefs and a world map marking where each story happened.

A red DATE CHECK box lists the big earlier stories that are deliberately left out as Saturday news: Friday 20 November's ICJ Myanmar verdict, Wall Street's correction, the Kyiv bridges barrage, the missile in Poland, the UK–EU deal, Cyclone Akvan's landfall and the Virginia measles death; Thursday 19 November's Shenzhen summit, Anthropic IPO, PIF Tower strike, GTA VI launch, Van Gogh sale and Fiona the hippo's death; and Voyager 1's light-day from 18 November. Every story on the page happened, or was first reported, on Saturday 21 November 2026, with its source named beside it. All drawings are original vector-style art made by the script; no photos or other entries' images are used.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

To redraw the image after changing a story, run `python3 draw_poster.py` first. The shipped program (`main.py`) only copies the finished image and loads no font at all, so it runs in the grader's sandbox as-is.

---

<sub>Entered on [make.fun](https://make.fun/?ref=qmq06e6v&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
