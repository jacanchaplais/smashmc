# smashmc

A Dash based web gui for visualisation and on-the-fly analysis of
Monte-Carlo collider simulations.

## Installation

Clone this repository
```bash
git clone git@github.com:jacanchaplais/smashmc.git
```

then from within the root of the project, run:
```bash
pip install -r requirements.txt
```

## Usage

```bash
python app/main.py
```

### Notes

This is in very early stages of development.

Current features:

- Display visjs graph for given input hepmc files
- Search for specific interaction vertices within these graphs
  - Highlight the descendants of these interaction vertices

Planned features:

- [ ] Allow dynamic descendant highlighting for cursor selected vertices
- [ ] Provide synchronous summary and aggregation data via histograms,
      tables, _etc._
- [ ] Support for other file formats (specifically root)

