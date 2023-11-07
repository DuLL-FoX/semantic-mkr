from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"
query = """SELECT DISTINCT ?item ?itemLabel ?numberOfEmployees WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }
  {
    SELECT DISTINCT ?item (MAX(?emp) as ?numberOfEmployees) WHERE {
      ?item p:P31 ?statement0.
      ?statement0 (ps:P31/(wdt:P279*)) wd:Q4830453.
      {
        ?item p:P452 ?statement1.
        ?statement1 (ps:P452/(wdt:P279*)) wd:Q11661.
      }
      UNION
      {
        ?item p:P452 ?statement2.
        ?statement2 (ps:P452/(wdt:P279*)) wd:Q80993.
      }
      UNION
      {
        ?item p:P452 ?statement3.
        ?statement3 (ps:P452/(wdt:P279*)) wd:Q638608.
      }
      ?item p:P17 ?statement4.
      ?statement4 (ps:P17/(wdt:P279*)) wd:Q212.
      OPTIONAL { ?item wdt:P1128 ?emp }
    }
    GROUP BY ?item
    LIMIT 100
  }
}
ORDER BY DESC(?numberOfEmployees)"""


def get_results(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


results = get_results(endpoint_url, query)

companies = []
for result in results["results"]["bindings"]:
    company = {
        'name': result["itemLabel"]["value"],
        'employees': int(result["numberOfEmployees"]["value"]) if 'numberOfEmployees' in result else None
    }
    companies.append(company)

sorted_companies = sorted(companies, key=lambda x: (x['employees'] is not None, x['employees']), reverse=True)

for company in sorted_companies:
    print(f"{company['name']}: {company['employees']}")
