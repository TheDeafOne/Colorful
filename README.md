# Colorful

Colorful is an exploration of how social media could represent what people are feeling through color and location. Users share short updates, and the application uses emotion words in those updates to assign a color.

The same posts can be read in a feed, viewed together as a grid, or explored geographically on a map.

![Concept illustration of Colorful's text, color, and location views](docs/images/sentiment-views.svg)

*Illustration using synthetic posts and locations, not an application screenshot. The palette comes from the project's emotion-to-color mapping.*

## Motivation

Most social media applications organize posts around a feed. We wanted to explore other ways of viewing the same information.

What changes when you see a collection of feelings as colors rather than a list of messages? Can a map help connect people in different places? What becomes easier to notice, and what gets lost when individual experiences are summarized this way?

Colorful was built to experiment with those questions. The goal was to explore different types of social media applications and different ways of connecting people and viewing global sentiment. Text, color, and geography each provide a different way into the same collection of posts.

## Different ways to view a post

- **The feed** preserves the message and its context.
- **The grid** brings the colors together so patterns can be seen across users. Hovering over a square reveals the message; clicking opens the user's profile.
- **The map** places posts geographically, adding another way to explore what people are sharing.
- **Profiles and following** provide a way to return to particular people. The feed, grid, and map can be filtered to all users or followed users.

These views are based on users' latest updates. They are an experiment in representation, not a representative survey of how a city or country feels.

## How it works

The application uses Python and Flask, with SQLAlchemy and SQLite for user accounts, posts, and follow relationships. The interface uses JavaScript, Tailwind CSS, and Alpine.js. The geographic view uses Google Maps.

When someone posts an update, [LeXmo](https://github.com/dinbav/LeXmo) compares its words with the NRC Emotion Lexicon. Colorful selects the highest-scoring emotion from eight categories: anger, anticipation, disgust, fear, joy, sadness, surprise, and trust. The corresponding color is stored with the post and used across the different views.

This is a simple lexicon-based interpretation. It can miss sarcasm, context, and feelings that are difficult to express in a short message. Mixed or unrecognized emotions can also produce an unhelpful label. The color gives another way to explore a post; the original text provides the context.

The main parts of the project are:

- [Application setup](colorful/__init__.py) and [database models](colorful/db.py)
- [Emotion and color mapping](colorful/color_map.py)
- [Status and social API](colorful/api/routes.py)
- [Page templates](colorful/templates/app) and [browser interactions](colorful/static/scripts)

## Quick start

The commands below are for macOS or Linux and were checked with Python 3.12. Internet access is needed for the language resources, external interface libraries, and map services.

### 1. Install

```sh
git clone https://github.com/TheDeafOne/Colorful.git
cd Colorful
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m nltk.downloader -d .venv/nltk_data punkt punkt_tab
export NLTK_DATA="$PWD/.venv/nltk_data"
```

On Windows, create the environment with `py -3.12 -m venv .venv`, activate it with `.venv\Scripts\Activate.ps1`, and set `$env:NLTK_DATA = "$PWD\.venv\nltk_data"` in PowerShell. The remaining Python commands are the same.

### 2. Configure

Copy `.env.template` to `.env`. Generate a password-encryption key:

```sh
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode().rstrip('='))"
```

Paste the result into `PEPPER_KEY` in `.env`. The application adds the final padding character itself, which is why the command removes it. Keep this key when reusing an existing database.

```dotenv
PEPPER_KEY='paste-the-generated-value-here'
RELOAD_DB='False'
MAPS_API_KEY=''
```

For the map view, put your own Google Maps JavaScript API key in `MAPS_API_KEY` and allow your local address in its referrer settings. The feed and grid do not require this key.

The current prototype sets Flask's session secret in `create_app()`; the `SECRET_KEY` entry in the original template is not read there.

### 3. Run

```sh
python application.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000), register an account, and sign in. The SQLite database is created automatically at `colorful/users.sqlite3`. Posting requests a location from the browser; allow it to exercise that path.

Keep `RELOAD_DB` set to `False` for normal use. Setting it to `True` rebuilds the database on startup and loads the original randomized test data. That seed data uses random colors and words, so it should not be treated as a demonstration of emotion classification.

LeXmo fetches its lexicon when processing text. If posting fails because language resources cannot be reached, check network access and that `NLTK_DATA` is set in the shell used to start the application.
