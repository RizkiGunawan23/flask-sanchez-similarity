import math

from app.services.ontology_operations import get_base_ontology_graph, skill_name_to_uri


def sanchez_similarity(set_a, set_b):
    """Calculate Sánchez similarity between two sets"""
    if set_a == set_b:
        return 1.0

    a_minus_b = len(set_a - set_b)
    b_minus_a = len(set_b - set_a)
    intersection = len(set_a.intersection(set_b))

    if intersection == 0:
        return 0.0

    numerator = a_minus_b + b_minus_a
    denominator = a_minus_b + b_minus_a + intersection

    similarity = 1 - math.log2(1 + numerator / denominator)
    return similarity


def get_limited_ancestors(graph, skill_uri, max_levels=3):
    """Get skill and its ancestors until reaching Skills class"""
    ancestors = set()
    ancestors.add(str(skill_uri))

    current_level = [skill_uri]
    skills_class_uri = "http://www.semanticweb.org/kota203/ontologies/2025/3/talent-matching-ontology/Skills"

    while current_level:
        next_level = []
        for node in current_level:
            query = f"""
            SELECT ?parent
            WHERE {{
                <{node}> rdfs:subClassOf ?parent .
                FILTER(?parent != <{node}>)
            }}
            """

            for row in graph.query(query):
                parent = row[0]
                parent_str = str(parent)

                # Tambahkan parent ke ancestors
                if parent_str not in ancestors:
                    ancestors.add(parent_str)

                    # Jika belum sampai Skills class, lanjutkan ke level berikutnya
                    if parent_str != skills_class_uri:
                        next_level.append(parent)
                    # Jika sudah sampai Skills class, stop di sini (tidak tambah ke next_level)

        current_level = next_level

    return ancestors


def calculate_sanchez_similarity(skills_list_1, skills_list_2):
    """
    Calculate similarity between two lists of skills using ontology ancestors
    """
    graph = get_base_ontology_graph()
    skill_similarities = []

    # For each skill in skills_list_1
    for skill_1 in skills_list_1:
        # Convert skill name to URI
        skill_1_uri = skill_name_to_uri(skill_1)

        # Get skill_1 + its ancestors (features)
        skill_1_features = get_limited_ancestors(graph, skill_1_uri)
        max_skill_similarity = 0

        # Compare with each skill in skills_list_2
        for skill_2 in skills_list_2:
            # Convert skill name to URI
            skill_2_uri = skill_name_to_uri(skill_2)

            # Get skill_2 + its ancestors (features)
            skill_2_features = get_limited_ancestors(graph, skill_2_uri)

            # Calculate Sanchez similarity
            skill_similarity = sanchez_similarity(skill_1_features, skill_2_features)

            # Keep track of maximum similarity for this skill_1
            if skill_similarity > max_skill_similarity:
                max_skill_similarity = skill_similarity

        # Store maximum similarity for this skill from list 1
        skill_similarities.append(max_skill_similarity)

    # Calculate overall similarity as average
    if skill_similarities:
        overall_similarity = sum(skill_similarities) / len(skill_similarities)
    else:
        overall_similarity = 0.0

    return overall_similarity
