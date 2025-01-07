import urllib.parse

from interfaces.IQuery import IQuery

class Query(IQuery):
    def __init__(self, base_url: str, test_name: str = None, probe_cc: str = None, since: str = None, until: str = None, ooni_run_link_id: int = None, probe_asn: int = None, domain: str = None, input: str = None, category_code: str = None):
        self.base_url = base_url
        self.test_name = test_name
        self.probe_cc = probe_cc
        self.since = since
        self.until = until
        self.ooni_run_link_id = ooni_run_link_id
        self.probe_asn = probe_asn
        self.domain = domain
        self.input = input
        self.category_code = category_code

    def deleteNoneParams(self, parametros: dict) -> dict:
        return {k: v for k, v in parametros.items() if v is not None}

    def buildQuery(self, base_url, parametros: dict) -> str:
        parametros = self.deleteNoneParams(parametros)
        return base_url + "?" + urllib.parse.urlencode(parametros, doseq=True)

