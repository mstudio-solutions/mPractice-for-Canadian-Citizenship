# mPractice for Canadian Citizenship

**Canadian citizenship test practice – by mStudio**

mPractice for Canadian Citizenship helps you get ready for the Canadian citizenship test. Practise as many times as you like with questions based on the official study guide *Discover Canada: The Rights and Responsibilities of Citizenship*.

🌐 **Try it:** https://mstudio-solutions.github.io/mPractice-for-Canadian-Citizenship/

## Features

- 501 practice questions across 10 study guide topics, each with an explanation
- **Full Mock test** – 20 questions, pass = 75% (15 correct), same as the real test
- Multiple choice and True/False questions, like the real test
- Practice by topic, Key questions or Random
- Timer per question (30s / 45s / 60s / 90s / 135s) or untimed
- Fixed answer layout, with optional shuffle
- Review mistakes with explanations
- Where older copies of the guide are now out of date (the Sovereign, the oath, number of electoral districts, population, NAFTA, G8), the explanation gives today's fact and what the guide says
- No sign-up, no ads, no cookies – one HTML file, no backend

## About the test (checked October 2026)

- 20 questions, 45 minutes, pass mark 75% (15 correct). Multiple choice or True/False, in English or French.
- Most people take the test online, with a webcam. You have 3 chances to pass.
- Applicants aged 18 to 54 must take the test.
- *Discover Canada* is still the only official study guide. Always check [canada.ca](https://www.canada.ca/en/immigration-refugees-citizenship/services/canadian-citizenship/become-canadian-citizen/citizenship-test.html) before your test.

## Privacy

mPractice does not collect any personal information. Answers and scores stay in your browser while the page is open. Full policy: open the app → **About** → **Privacy Policy**.

## Project structure

- `index.html` – the full app: practice, results, About and Privacy Policy pages (question bank is embedded)
- `questions.json` – the question bank as plain JSON (generated)
- `data/ch01.json` … `data/ch10.json` – question source, one file per study guide topic
- `scripts/build.py` – checks the questions and rebuilds `questions.json` and `index.html`

## Edit or add questions

1. Edit a file in `data/`. Put the correct answer in `a` and wrong answers in `w` (for True/False, `a` is `true` or `false`). Answer order is shuffled automatically.
2. Run `python3 scripts/build.py`
3. Commit `data/`, `questions.json` and `index.html`.

`python3 scripts/build.py --check` fails if the generated files are out of date.

Every push to `main` is published by GitHub Pages (Settings → Pages → Deploy from branch `main`, folder `/ (root)`).

## Disclaimer

mPractice is an **unofficial** practice tool. It is not made by, linked to or approved by the Government of Canada or Immigration, Refugees and Citizenship Canada (IRCC). Questions are based on *Discover Canada: The Rights and Responsibilities of Citizenship* and are not the real test questions. No text from the guide is copied. Always check the [official source](https://www.canada.ca/en/immigration-refugees-citizenship/services/canadian-citizenship/become-canadian-citizen/citizenship-test.html).

## Contact

- **Company:** mStudio
- **Developer:** Martin Yeung
- **Email:** mstudiosolutions@gmail.com
- **Location:** Australia

## Licence

© 2026 Martin Yeung (mStudio). All rights reserved. See [LICENSE](LICENSE).
