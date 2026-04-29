> **Part of:** [[ClioApproachForDocumentSegmentation|CLIO Guide: Document Segmentation]] | **Paper:** [[ClioPrivacyPreservingInsightsIntoRealWorldAiUse|CLIO Paper Summary]]

## Hierarchy Building

### Goal
Organize hundreds/thousands of flat clusters into a navigable multi-level taxonomy.

### CLIO's exact algorithm

The hierarchy is built iteratively. At each level `l`:

1. **Embed clusters** -- Embed each cluster's name + description using `all-mpnet-base-v2`
2. **Generate neighborhoods** -- Group cluster embeddings into neighborhoods using k-means, where k is chosen so avg neighborhood size is ~40 clusters
3. **Propose parent categories** -- For each neighborhood, ask the LLM to propose higher-level category names. Include nearest clusters outside the neighborhood for boundary handling. Target number at level `l` follows: `n_l / n_{l-1} = (n_top / n_base)^{1/(L-1)}`
4. **Deduplicate** -- Use LLM to merge near-duplicate proposed categories across all neighborhoods
5. **Assign children** -- Use LLM to assign each lower-level cluster to its best parent (shuffle order to avoid position bias)
6. **Rename parents** -- Regenerate parent name/description based on actual assigned children

Repeat until you reach the desired number of top-level clusters.

### CLIO's hierarchy dimensions (from their 100K run)
- **3 levels total:** ~10 top-level --> ~100 mid-level --> ~1000 base clusters
- **Model:** Claude 3.5 Sonnet, temperature 1.0

### Implementation

```python
from sentence_transformers import SentenceTransformer

embed_model = SentenceTransformer("all-mpnet-base-v2")


def build_hierarchy(
    base_clusters: dict,
    n_top: int = 10,
    n_levels: int = 3,
) -> dict:
    """Build a multi-level cluster hierarchy following CLIO's approach."""

    hierarchy = {"level_0": base_clusters}  # base level
    current_level = base_clusters
    n_base = len(base_clusters)

    for level in range(1, n_levels):
        # Calculate target number of clusters at this level
        # n_l / n_{l-1} = (n_top / n_base)^{1/(L-1)}
        ratio = (n_top / n_base) ** (1.0 / (n_levels - 1))
        n_target = max(n_top, int(len(current_level) * ratio))
        print(f"\nLevel {level}: {len(current_level)} clusters -> target {n_target}")

        # Step 1: Embed current cluster names + descriptions
        cluster_texts = [
            f"{c['name']}: {c['description']}" for c in current_level.values()
        ]
        cluster_ids = list(current_level.keys())
        cluster_embeddings = embed_model.encode(cluster_texts, normalize_embeddings=True)

        # Step 2: Generate neighborhoods (avg ~40 per neighborhood)
        n_neighborhoods = max(1, len(current_level) // 40)
        if n_neighborhoods > 1:
            from sklearn.cluster import KMeans
            nbhd_kmeans = KMeans(n_clusters=n_neighborhoods, random_state=42, n_init=5)
            nbhd_labels = nbhd_kmeans.fit_predict(cluster_embeddings)
        else:
            nbhd_labels = np.zeros(len(cluster_ids), dtype=int)

        # Step 3: Propose parent categories per neighborhood
        all_proposed = []
        for nbhd_id in range(n_neighborhoods):
            nbhd_cluster_ids = [
                cluster_ids[i] for i in range(len(cluster_ids))
                if nbhd_labels[i] == nbhd_id
            ]
            nbhd_clusters = [current_level[cid] for cid in nbhd_cluster_ids]

            # Desired names for this neighborhood
            desired = max(3, int(n_target * len(nbhd_cluster_ids) / len(cluster_ids)))

            proposed = propose_parent_categories(nbhd_clusters, desired)
            all_proposed.extend(proposed)

        # Step 4: Deduplicate across neighborhoods
        deduplicated = deduplicate_categories(all_proposed, n_target)
        print(f"  After dedup: {len(deduplicated)} parent categories")

        # Step 5: Assign each child cluster to best parent
        assignments = {}
        for cid in cluster_ids:
            child = current_level[cid]
            parent_name = assign_to_parent(child, deduplicated)
            if parent_name not in assignments:
                assignments[parent_name] = []
            assignments[parent_name].append(cid)

        # Step 6: Rename parents based on actual children
        next_level = {}
        for parent_name, child_ids in assignments.items():
            children = [current_level[cid] for cid in child_ids]
            renamed = rename_parent(parent_name, children)
            parent_id = f"L{level}_{len(next_level)}"
            next_level[parent_id] = {
                "name": renamed["name"],
                "description": renamed["description"],
                "children": child_ids,
                "size": sum(current_level[cid]["size"] for cid in child_ids),
            }

        hierarchy[f"level_{level}"] = next_level
        current_level = next_level

    return hierarchy
```

### LLM helper functions for hierarchy

```python
def propose_parent_categories(clusters: list[dict], desired: int) -> list[str]:
    """Ask LLM to propose higher-level category names for a neighborhood."""
    cluster_list = "\n".join(
        f"<cluster>{c['name']}: {c['description']}</cluster>" for c in clusters
    )
    prompt = f"""You are tasked with creating higher-level cluster names based on a
given list of clusters and their descriptions. Your goal is to come up with
broader categories that could encompass one or more of the provided clusters.

First, review the list of clusters and their descriptions:
<cluster_list>
{cluster_list}
</cluster_list>

Your task is to create roughly {desired} higher-level cluster names that could
potentially include one or more of the provided clusters. These higher-level
clusters should represent broader categories or themes that emerge from the
given clusters, while remaining as specific as possible.

You should output at least {int(0.5 * desired)} and at most {int(1.5 * desired)}
names, with {desired} as a target.

Guidelines:
1. Analyze themes, topics, or characteristics common to multiple clusters.
2. Create names specific enough to be meaningful, but broad enough to encompass
   multiple clusters.
3. Ensure names are distinct from one another.
4. Use clear, concise, descriptive language.

<scratchpad>
[Analyze clusters and brainstorm potential groupings -- keep to 1-2 paragraphs]
</scratchpad>

<answer>
1. [First higher-level cluster name]
2. [Second higher-level cluster name]
...
</answer>"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        temperature=1.0,
        messages=[{"role": "user", "content": prompt}],
    )

    # Parse numbered list from <answer> tags
    raw = response.content[0].text
    match = re.search(r"<answer>(.*?)</answer>", raw, re.DOTALL)
    if match:
        lines = match.group(1).strip().split("\n")
        return [re.sub(r"^\d+\.\s*", "", line).strip() for line in lines if line.strip()]
    return []


def deduplicate_categories(categories: list[str], desired: int) -> list[str]:
    """Deduplicate proposed categories across neighborhoods."""
    cat_list = "\n".join(f"<cluster> {c} </cluster>" for c in categories)

    prompt = f"""You are tasked with deduplicating a list of cluster names into a smaller
set of distinct cluster names. Your goal is to create approximately {desired}
relatively distinct clusters that best represent the original list.

<cluster_names>
{cat_list}
</cluster_names>

Number of distinct clusters to create: approximately {desired}

Steps:
1. Analyze the given list to identify similarities and themes.
2. Group similar names together based on semantic meaning.
3. For each group, select the most specific representative name.
4. Merge the most similar groups until you reach the desired number.
5. Output at least {int(desired * 0.5)} and at most {int(desired * 1.5)} names.

<answer>
1. [First cluster name]
2. [Second cluster name]
...
</answer>"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        temperature=1.0,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.content[0].text
    match = re.search(r"<answer>(.*?)</answer>", raw, re.DOTALL)
    if match:
        lines = match.group(1).strip().split("\n")
        return [re.sub(r"^\d+\.\s*", "", line).strip() for line in lines if line.strip()]
    return categories[:desired]


def assign_to_parent(child: dict, parent_names: list[str]) -> str:
    """Assign a child cluster to its best-fit parent category."""
    # Shuffle to avoid position bias (as CLIO does)
    shuffled = random.sample(parent_names, len(parent_names))
    parent_list = "\n".join(f"<cluster> {p} </cluster>" for p in shuffled)

    prompt = f"""You are tasked with categorizing a specific cluster into one of the
provided higher-level clusters. Determine which higher-level cluster best fits
the given specific cluster based on its name and description.

Higher-level clusters:
<higher_level_clusters>
{parent_list}
</higher_level_clusters>

Specific cluster to categorize:
<specific_cluster>
Name: {child['name']}
Description: {child['description']}
</specific_cluster>

You MUST assign to the best higher-level cluster, even if multiple could work.

<scratchpad>
[Brief reasoning -- 1-2 sentences]
</scratchpad>

<answer>
[Full name of the chosen cluster, exactly as listed above]
</answer>"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        temperature=1.0,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.content[0].text
    match = re.search(r"<answer>(.*?)</answer>", raw, re.DOTALL)
    if match:
        assigned = match.group(1).strip()
        # Fuzzy match to actual parent names
        from difflib import get_close_matches
        matches = get_close_matches(assigned, parent_names, n=1, cutoff=0.3)
        return matches[0] if matches else parent_names[0]
    return parent_names[0]


def rename_parent(parent_name: str, children: list[dict]) -> dict:
    """Rename a parent cluster based on its actual assigned children."""
    child_list = "\n".join(f"<cluster> {c['name']} </cluster>" for c in children)

    prompt = f"""You are tasked with summarizing a group of related cluster names into
a short, precise, and accurate overall description and name.

Summarize all the cluster names into a clear, precise, two-sentence description.
Generate a short name (at most ten words). Be as descriptive as possible while
still accurately describing all contents.

<answers>
{child_list}
</answers>

<summary> [Two-sentence summary] </summary>
<name> [Short name, no trailing punctuation] </name>"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        temperature=1.0,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.content[0].text
    name_match = re.search(r"<name>(.*?)</name>", raw, re.DOTALL)
    summary_match = re.search(r"<summary>(.*?)</summary>", raw, re.DOTALL)

    return {
        "name": name_match.group(1).strip() if name_match else parent_name,
        "description": summary_match.group(1).strip() if summary_match else "",
    }
```

### Running it

```python
hierarchy = build_hierarchy(
    base_clusters=cluster_descriptions,
    n_top=10,       # desired top-level categories
    n_levels=3,     # 3 levels: ~10 top -> ~100 mid -> ~1000 base
)

with open("step6_hierarchy.json", "w") as f:
    json.dump(hierarchy, f, indent=2)
```

---
