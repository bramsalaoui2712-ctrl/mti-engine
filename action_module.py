# action_module.py
from datetime import datetime
import requests

class ActionModule:
    """
    Module d’exécution des actions du moteur MTI.
    Version simple, claire, et compatible Render / API.
    """

    def __init__(self):
        self.actions = {
            "text": self._text_response,
            "api_call": self._api_call,
            "store_log": self._store_log
        }
        self.history = []

    def execute(self, action_type: str, params: dict):
        """
        Exécute une action en fonction de son type.
        """
        if action_type not in self.actions:
            return {"success": False, "error": f"Action inconnue: {action_type}"}

        result = self.actions[action_type](params)

        # Enregistrer la trace
        self.history.append({
            "time": datetime.now(),
            "action": action_type,
            "params": params,
            "result": result
        })

        return result

    # -------------------------
    #  ACTIONS DISPONIBLES
    # -------------------------

    def _text_response(self, params: dict):
        text = params.get("text", "")
        return {
            "success": True,
            "response": text,
            "length": len(text)
        }

    def _api_call(self, params: dict):
        url = params.get("url")
        method = params.get("method", "GET")
        payload = params.get("payload", {})

        if not url:
            return {"success": False, "error": "URL manquante"}

        try:
            if method == "GET":
                r = requests.get(url, timeout=8)
            else:
                r = requests.post(url, json=payload, timeout=8)

            return {
                "success": True,
                "status": r.status_code,
                "data_preview": r.text[:250]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _store_log(self, params: dict):
        """
        Stockage simplifié (utile pour debug).
        """
        return {
            "success": True,
            "stored": params.get("content", "")[:100]
        }
