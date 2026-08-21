**Figure 7 — "Prompt for passage NER during indexing"**

**What it shows.** This is not a data plot; it is a screenshot of a structured LLM prompt template (color‑coded sections) used at *indexing* time to extract named entities from a passage. It has no axes, no series, and no trends to read off. Its structure, top to bottom, is:

- **Title:** "Passage NER (Indexing)."
- **Instruction (blue block):** "Your task is to extract named entities from the given paragraph. Respond with a JSON list of entities." — i.e., it forces a constrained, machine‑parsable output format.
- **One‑Shot Demonstration (peach block):** a single input→output pair. Input is a short paragraph about "Radio City," India's first private FM radio station (founded ~2001, plays Hindi/English/regional music, with a PlanetRadiocity.com portal launched ~2008). Output is the expected JSON, e.g. `{"named_entities": ["Radio City", "India", "3 July 2001", "Hindi", "English", "May 2008", "PlanetRadiocity.com"]}` — showing that the model should capture proper nouns, dates, languages, and domain names.
- **Input (green block):** a placeholder field `PASSAGE TO INDEX`, where the live passage to be processed is substituted at runtime.

**Takeaway.** Figure 7 documents the *interface contract* between the system and the LLM: a one‑shot, JSON‑only named‑entity extraction prompt applied to each passage during corpus indexing. The demonstration example defines the expected entity granularity (entities, locations, dates, languages, URLs) and the strict JSON response schema that the downstream indexing pipeline relies on. (The numeric values appearing are only part of the worked example, not measured data.)