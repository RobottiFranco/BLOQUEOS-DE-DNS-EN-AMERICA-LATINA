import time
import requests

from interfaces.IExecute import IExecute

class GetData(IExecute):
    def backoff(self, attempt) -> int:
        return 2 ** attempt

    def execute(self, url: str):
        response = None
        for attempt in range(3):
            try:
                response = requests.get(url)
                response.raise_for_status()
                response = response.json()
            except requests.RequestException as e:
                wait_time = self.backoff(attempt)
                print(f"Error al consultar {url}: {e}. Reintentando en {wait_time} segundos...")
                time.sleep(wait_time)
            except Exception as e:
                print(f"Error inesperado: {e}. Deteniendo los intentos.")
                response = None
        return response