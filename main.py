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

class PRINT(enum.Enum):
    ALL = enum.auto()
    ONLY_NON_CONFIRMANT = enum.auto()
    ONLY_FAILED_TESTS = enum.auto() # Only the reports which fail their test
    NONE = False

#PRINT_REPORTS=PRINT.ALL
#PRINT_REPORTS=PRINT.ONLY_NON_CONFIRMANT
PRINT_REPORTS=PRINT.ONLY_FAILED_TESTS
#PRINT_REPORTS=PRINT.NONE
SKIP_INVALID=False
SKIP_VALID=False

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
        except subprocess.CalledProcessError as e:
            self.bold = ""
            self.reset = ""

            self.green = ""
            self.red = ""

_color = Colorcodes()

def get_trig_filepaths(folderpath):
    return list(Path(folderpath).glob("*.trig"))


def read_and_parse_base_graphs(folderpath):
    p = Path(folderpath)
    filepaths = list(p.glob("*.ttl")) + list(p.glob("*.jsonld"))
    base_graph = Graph()
    for path in filepaths:
        base_graph.parse(path)
    return base_graph


def run_shacl_validation(folderpath, shacl_rules, ontology_graph, base_graph):
    reports = dict()
    for filepath in get_trig_filepaths(folderpath):
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
                allow_infos=False,
                allow_warnings=False,
                debug=DEBUG
            )
    return reports


def run_valid_trig_graphs(folderpath, shacl_rules, ontology_graph, base_graph):
    print(f" ===== Checking valid: {folderpath} ======")
    reports = run_shacl_validation(folderpath, shacl_rules, ontology_graph, base_graph)
    success = all([conforms for conforms, _, _ in reports.values()])
    color = _color.green if success else _color.red
    checkmark = "✓" if success else "✗"
    print("Passed tests: "+color+f"{checkmark} {success}"+_color.reset)
    _print_reports(reports, is_conformant = False)
    print()


def run_invalid_trig_graphs(folderpath, shacl_rules, ontology_graph, base_graph, print_reports = PRINT.NONE):
    print(f" ===== Checking invalid: {folderpath} ======")
    reports = run_shacl_validation(folderpath, shacl_rules, ontology_graph, base_graph)
    success = not any([conforms for conforms, _, _ in reports.values()])
    color = _color.green if success else _color.red
    checkmark = "✓" if success else "✗"
    print("Passed tests: "+color+f"{checkmark} {success}"+_color.reset)
    if print_reports is PRINT.ALL:
        _print_reports(reports, is_conformant=True)
        _print_reports(reports, is_conformant=False)
    if print_reports is PRINT.ONLY_FAILED_TESTS:
        _print_reports(reports, is_conformant=True)
    if print_reports is PRINT.ONLY_NON_CONFIRMANT:
        _print_reports(reports, is_conformant=False)
    print()


def _print_reports(reports, is_conformant):
    reports = {path: report for path, report in reports.items() if report[0] is is_conformant}
    for path, (_, _, text) in reports.items():
        print(f" === {path} ===")
        print(text)


def parse_graph(*args):
    graph = Graph()
    for path in args:
        graph.parse(Path(path).expanduser())
    return graph


def main():
    # Import SHACL rules and ontology
    dcatapno_shacl_rules = parse_graph(CORE_SHACL_RULES_PATH, RANGES_SHACL_RULES_PATH)
    #dcatap_shacl_path = parse_graph(DCATAP_SHACL_RULES_PATH)
    core_shacl_rules = dcatapno_shacl_rules # + dcatap_shacl_rules
    con_voc_shacl_rules = parse_graph(CORE_SHACL_RULES_PATH, RANGES_SHACL_RULES_PATH, CONTROLLED_VOC_SHACL_SHAPES_PATH)
    ontology_graph = parse_graph(ONTOLOGY_PATH)

    # Import base graphs
    base_graphs_path = Path(BASE_GRAPH_DIR).expanduser()
    base_graph = read_and_parse_base_graphs(base_graphs_path)

    if not SKIP_VALID:      # Check valid TriG graphs
        run_valid_trig_graphs(
            f"{VALID_GRAPHS_DIR}/core",
            core_shacl_rules,
            ontology_graph,
            base_graph
        )
        run_valid_trig_graphs(
            f"{VALID_GRAPHS_DIR}/controlled-vocs",
            con_voc_shacl_rules,
            ontology_graph,
            base_graph
        )

    if not SKIP_INVALID:    # Check invalid TriG graphs
        run_invalid_trig_graphs(
            f"{INVALID_GRAPHS_DIR}/core",
            core_shacl_rules,
            ontology_graph,
            base_graph,
            print_reports=PRINT_REPORTS
        )
        run_invalid_trig_graphs(
            f"{INVALID_GRAPHS_DIR}/controlled-vocs",
            con_voc_shacl_rules,
            ontology_graph,
            base_graph,
            print_reports=PRINT_REPORTS
        )


if __name__ == '__main__':
    main()
