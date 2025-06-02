from rdflib import Graph, Namespace

TALENT_NAMESPACE = Namespace(
    "http://www.semanticweb.org/kota203/ontologies/2025/3/talent-matching-ontology/"
)


def get_base_ontology_graph():
    graph = Graph()
    graph.parse("./app/static_data/ontology_ver3.ttl", format="turtle")
    graph.bind("talent", TALENT_NAMESPACE)

    return graph


def skill_name_to_uri(skill_name):
    """Convert skill name to URI"""
    # Replace spaces with underscores and create URI
    skill_formatted = skill_name.replace(" ", "_")
    return f"http://www.semanticweb.org/kota203/ontologies/2025/3/talent-matching-ontology/{skill_formatted}"


def get_all_skills():
    """
    Ambil semua skill dari ontologi, return list nama skill (string)
    """
    graph = get_base_ontology_graph()
    all_skills_query = """
    SELECT ?skill
    WHERE {
        ?skill rdfs:subClassOf+ <http://www.semanticweb.org/kota203/ontologies/2025/3/talent-matching-ontology/Skills> .
    }
    """

    skills = []
    for row in graph.query(all_skills_query):
        skill_uri = row[0]
        skill_name = str(skill_uri).split("/")[-1].replace("_", " ")
        skills.append(skill_name)

    return sorted(list(set(skills)))


def skill_hierarchy(skill_name):
    """Get hierarchy path for a skill from itself to Skills class"""
    graph = get_base_ontology_graph()
    skill_uri = skill_name_to_uri(skill_name)

    hierarchy = []
    current_uri = skill_uri
    skills_class_uri = "http://www.semanticweb.org/kota203/ontologies/2025/3/talent-matching-ontology/Skills"

    # Add the skill itself
    hierarchy.append(skill_name)

    while str(current_uri) != skills_class_uri:
        query = f"""
        SELECT ?parent
        WHERE {{
            <{current_uri}> rdfs:subClassOf ?parent .
            FILTER(?parent != <{current_uri}>)
        }}
        LIMIT 1
        """

        results = list(graph.query(query))
        if not results:
            break

        parent_uri = results[0][0]
        parent_name = str(parent_uri).split("/")[-1].replace("_", " ")
        hierarchy.append(parent_name)
        current_uri = parent_uri

        # Safety check to prevent infinite loop
        if len(hierarchy) > 10:
            break

    return hierarchy
