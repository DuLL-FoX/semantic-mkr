from rdflib import Graph
import json

g = Graph()

ttl_file_path = 'countrues_info.ttl'

try:
    g.parse(ttl_file_path, format='turtle')
    error_message = None
except Exception as e:
    error_message = str(e)

query_populous_countries = """
SELECT ?continent ?country ?population
WHERE {
    ?country <http://example.com/demo/part_of_continent> ?continent .
    ?country <http://example.com/demo/population> ?population .
}
ORDER BY ?continent DESC(?population)
"""

try:
    query_results = g.query(query_populous_countries)

    continent_countries = {}
    for row in query_results:
        continent = str(row.continent)
        country = str(row.country)
        population = int(row.population)

        if continent not in continent_countries:
            continent_countries[continent] = []

        continent_countries[continent].append((country, population))

    for continent in continent_countries:
        continent_countries[continent].sort(key=lambda x: x[1], reverse=True)
        continent_countries[continent] = continent_countries[continent][:5]

    readable_output = {}
    for continent, countries in continent_countries.items():
        readable_output[continent] = [{"Country": country, "Population": pop} for country, pop in countries]

    result = readable_output
    error_message = None

    print(json.dumps(result, indent=4))
except Exception as e:
    error_message = str(e)

