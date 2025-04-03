from rdflib import Graph, Dataset
from pyshacl import validate
from pathlib import Path
import subprocess
import enum

BASE_GRAPH_DIR = "./base-graphs"

VALID_GRAPHS_DIR = "./valid-graphs"
INVALID_GRAPHS_DIR = "./invalid-graphs"

CORE_SHACL_RULES_PATH = "~/repos/dcat-ap-no/shacl/DCAT-AP-NO-shacl_shapes_3.ttl"

RANGES_SHACL_RULES_PATH = "~/repos/dcat-ap-no/shacl/ranges.shapes.ttl"
CONTROLLED_VOC_SHACL_SHAPES_PATH = "~/repos/dcat-ap-no/shacl/vocabularies.shapes.ttl"

ONTOLOGY_PATH = "~/repos/dcat-ap-no/shacl/ontologies.ttl"


TESTS_TO_RUN = [  # must match directory name
    "valid-graphs",
    "invalid-graphs"
]

CLASS_KEYS = [  # must match file name (excluding suffixes)
    'catalog',
    # 'dataset',
    # 'data-service',
    # 'distribution',
]

class PRINT(enum.Enum):
    ALL = enum.auto()
    ONLY_NON_CONFORMANT = enum.auto()
    ONLY_FAILED_TESTS = enum.auto() # Only the reports which fail their test
    NONE = False

#PRINT_REPORTS=PRINT.ALL
#PRINT_REPORTS=PRINT.ONLY_NON_CONFORMANT
#PRINT_REPORTS=PRINT.NONE
PRINT_REPORTS=PRINT.ONLY_FAILED_TESTS

DEBUG=False
#DEBUG=True

class Colorcodes(object):
    "From: https://gist.github.com/martin-ueding/4007035"
    def __init__(self):
        try:
            self.bold = subprocess.check_output("tput bold".split()).decode()
            self.reset = subprocess.check_output("tput sgr0".split()).decode()
            self.green = subprocess.check_output("tput setaf 2".split()).decode()
            self.red = subprocess.check_output("tput setaf 1".split()).decode()
            self.magenta = subprocess.check_output("tput setaf 5".split()).decode()
            self.cyan = subprocess.check_output("tput setaf 6".split()).decode()
        except subprocess.CalledProcessError as e:
            self.bold = ""
            self.reset = ""
            self.green = ""
            self.red = ""
            self.cyan = ""
            self.magenta = ""

_color = Colorcodes()
BASE_INDENT = 6

def read_and_parse_base_graphs(folderpath, type_keys):
    base_graphs = dict()
    for key in type_keys:
        path = Path(f"{folderpath}/{key}.base.ttl").expanduser()
        base_graphs[key] = Graph().parse(path)
    return base_graphs


def read_and_parse_base_graph(filepath):
    base_graph = Graph(Path(filepath).expanduser())
    base_graph.parse()
    base_graph = read_and_parse_base_graphs()
    return base_graph


def run_shacl_validation(filepath, shacl_rules, ontology_graph, base_graph):
    reports = dict()
    rdf_dataset = Dataset()
    rdf_dataset.parse(filepath, format="trig")
    for g in rdf_dataset.graphs():
        if g.identifier.toPython() == "urn:x-rdflib:default": # skip default graph (to avoid false positives)
            continue
        data_graph = g + base_graph
        reports[g.identifier] = validate(
            data_graph,
            shacl_graph=shacl_rules,
            ont_graph=ontology_graph,
            inference=None, # options: 'rdfs', 'owlrl', 'both, 'none'
            allow_infos=True,
            allow_warnings=False,
            debug=DEBUG
            )
    return reports


def run_validation(filepath, shacl_rules, ontology_graph, base_graph, expect_valid):
    test_file_path = Path(f"{filepath}").expanduser()
    reports = run_shacl_validation(test_file_path, shacl_rules, ontology_graph, base_graph)
    if expect_valid:
        success = all([conforms for conforms, _, _ in reports.values()])
    else:
        success = not any([conforms for conforms, _, _ in reports.values()])
    return success, reports


def parse_graph(*args):
    graph = Graph()
    for path in args:
        graph.parse(Path(path).expanduser())
    return graph


def _print_result(class_type, success):
    color = _color.green if success else _color.red
    checkmark = "✓" if success else "✗"
    success_text = "Passed" if success else "Failed"
    formatted_success_text = f"{color}{checkmark} {success_text}{_color.reset}"
    formatted_class_type = f"{_color.bold}{_color.cyan}{class_type}{_color.reset}"
    print(f"{'':<{BASE_INDENT * 2}}{formatted_class_type:.<50} {formatted_success_text}")


def _print_reports_per_conformance(reports, graph_is_conformant):
    reports = {path: report for path, report in reports.items() if report[0] is graph_is_conformant}
    for path, (_, _, text) in reports.items():
        print("URI: " + _color.magenta + f"{path}" + _color.reset)
        print(text)


def _print_reports(collected_reports):
    if PRINT_REPORTS == PRINT.ALL:
        print(f"\n======================= REPORTS ========================\n")
        for _, reports in collected_reports.items():
            _print_reports_per_conformance(reports, graph_is_conformant=True)
            _print_reports_per_conformance(reports, graph_is_conformant=False)
        print()
    
    if PRINT_REPORTS == PRINT.ONLY_NON_CONFORMANT:
        print(f"\n======================= REPORTS ========================\n")
        for _, reports in collected_reports.items():
            _print_reports_per_conformance(reports, graph_is_conformant=False)
        print()

    if PRINT_REPORTS == PRINT.ONLY_FAILED_TESTS:
        print(f"\n======================= REPORTS ========================\n")
        _print_reports_per_conformance(collected_reports["valid-graphs"], graph_is_conformant=False)
        _print_reports_per_conformance(collected_reports["invalid-graphs"], graph_is_conformant=True)
        print()


def _print_results(results):
    print(f"\n======================= RESULTS ========================")

    if "valid-graphs" in TESTS_TO_RUN:
        print(f"\nValid Graphs")
        for validation_extension_key, check_type_results in results["valid-graphs"].items():
            print(f"{' ':<{BASE_INDENT}}{str(validation_extension_key).capitalize()}:")
            for class_key, result in check_type_results.items():
                _print_result(str(class_key).capitalize(), result)
    if "invalid-graphs" in TESTS_TO_RUN:
        print(f"\nInvalid Graphs")
        for validation_extension_key, check_type_results in results["invalid-graphs"].items():
            print(f"{' ':<{BASE_INDENT}}{str(validation_extension_key).capitalize()}:")
            for class_key, result in check_type_results.items():
                _print_result(str(class_key).capitalize(), result)
    print()


def main():
    # Import SHACL rules and ontology
    dcatapno_shacl_rules = parse_graph(CORE_SHACL_RULES_PATH, RANGES_SHACL_RULES_PATH)
    #dcatap_shacl_path = parse_graph(DCATAP_SHACL_RULES_PATH)
    core_shacl_rules = dcatapno_shacl_rules # + dcatap_shacl_rules
    controlled_vocs_shacl_rules = parse_graph(CORE_SHACL_RULES_PATH, RANGES_SHACL_RULES_PATH, CONTROLLED_VOC_SHACL_SHAPES_PATH)
    ontology_graph = parse_graph(ONTOLOGY_PATH)

    # Import base graphs
    base_graphs_path = Path(BASE_GRAPH_DIR).expanduser()
    base_graphs = read_and_parse_base_graphs(base_graphs_path, CLASS_KEYS)

    results = {
        "valid-graphs": {
            "core": dict(), # contains class key and success (i.e. 'dataset': True)
            "controlled-vocs": dict()
        },
        "invalid-graphs": {
            "core": dict(),
            "controlled-vocs": dict()
        }
    }

    collected_reports = {
        "valid-graphs": dict(), # contains identifier of RDF Dataset (i.e. Test) and SHACL Report
        "invalid-graphs": dict()
    }

    for valid_or_invalid in TESTS_TO_RUN:
        for validation_extensions in ["core", "controlled-vocs"]:
            for class_key in CLASS_KEYS:
                filepath = f"{valid_or_invalid}/{validation_extensions}/{class_key}.trig"
                base_graph = base_graphs[class_key]
                expect_valid = valid_or_invalid == "valid-graphs"
                if validation_extensions == "core":
                    shacl_rules = core_shacl_rules
                elif validation_extensions == "controlled-vocs":
                    shacl_rules = controlled_vocs_shacl_rules
                else:
                    raise RuntimeError("Could not decide SHACL rules, value not one of 'core' or 'controlled-vocs'")
                success, reports = run_validation(
                    filepath,
                    shacl_rules,
                    ontology_graph,
                    base_graph,
                    expect_valid
                )
                results[valid_or_invalid][validation_extensions][class_key] = success
                collected_reports[valid_or_invalid].update(**reports)

    _print_reports(collected_reports)
    _print_results(results)


if __name__ == '__main__':
    main()
